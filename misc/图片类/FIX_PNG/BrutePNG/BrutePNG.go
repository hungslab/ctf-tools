package main

import (
	"bytes"
	"encoding/binary"
	"errors"
	"fmt"
	"hash/crc32"
	"io"
	"os"
	"path/filepath"
	"time"
)

const (
	MAX_SIZE = 0x1FFF
)

var (
	start             time.Time
	dirPath, fileName string
)

func check_file(args []string) (string, error) {
	if len(args) < 2 {
		fmt.Println("[-] 请输入图片路径")
		return "", errors.New("[-] 请输入图片路径")
	}

	filePath, err := filepath.Abs(args[1])
	if err != nil {
		fmt.Printf("[-] 获取文件绝对路径失败：%v\n", err)
		fmt.Println(err) // 打印错误信息
		return "", err
	}
	fileName = filepath.Base(filePath)
	dirPath = filepath.Dir(filePath)

	if filepath.Ext(fileName) != ".png" {
		fmt.Println("[-] 您的文件后缀名不为PNG!")
		return "", errors.New("[-] 您的文件后缀名不为PNG")
	}
	return filePath, nil
}

func read_file(filePath string) ([]byte, error) {
	file, err := os.Open(filePath)
	if err != nil {
		fmt.Println("[-] 读取文件失败")
		fmt.Println(err) // 打印错误信息
		return nil, err
	}
	defer file.Close()

	data, err := io.ReadAll(file)
	if err != nil {
		fmt.Println("[-] 读取文件失败")
		fmt.Println(err) // 打印错误信息
		return nil, err
	}
	return data, nil
}

func calculation_crc32(data []byte, width int, height int) uint32 {
	crc32 := crc32.NewIEEE()
	crc32.Write(data[12:16])
	binary.Write(crc32, binary.BigEndian, uint32(width))
	binary.Write(crc32, binary.BigEndian, uint32(height))
	crc32.Write(data[24:29])
	return crc32.Sum32()
}

func displayDuration(width, height int, crc32 uint32) {
	end := time.Now()
	duration := end.Sub(start)
	hours := int(duration.Hours())
	minutes := int(duration.Minutes()) % 60
	seconds := int(duration.Seconds()) % 60
	milliseconds := int(duration.Milliseconds()) % 1000
	fmt.Printf("[-] 宽度: %d, hex: 0x%X\n", width, width)
	fmt.Printf("[-] 高度: %d, hex: 0x%X\n", height, height)
	fmt.Printf("[-] 运行时间为：%d小时 %d分钟 %d秒 %d毫秒\n", hours, minutes, seconds, milliseconds)
	fmt.Printf("[-] CRC32: 0x%X, 已经为您保存到运行目录中!", crc32)
}

func wirte_png(data []byte, width int, height int, crc32 uint32) {
	var buf bytes.Buffer
	buf.Write(data[:16])
	binary.Write(&buf, binary.BigEndian, int32(width))
	binary.Write(&buf, binary.BigEndian, int32(height))
	buf.Write(data[24:])
	err := os.WriteFile(filepath.Join(dirPath, fmt.Sprintf("fix_%s", fileName)), buf.Bytes(), 0644)
	if err != nil {
		fmt.Println("[-] 保存文件失败")
		fmt.Println(err) // 打印错误信息
		return
	}

	displayDuration(width, height, crc32)
	os.Exit(0)
}

func crack_image(data []byte, width int, height int, targetCRC uint32) {
	crc32 := calculation_crc32(data, width, height)
	if crc32 == targetCRC {
		wirte_png(data, width, height, crc32)
	}
}

func crack_height(data []byte, width int, targetCRC uint32) {
	for i := 0; i < MAX_SIZE; i++ {
		go crack_image(data, width, i, targetCRC)
	}
}

func crack_width(data []byte, height int, targetCRC uint32) {
	for i := 0; i < MAX_SIZE; i++ {
		go crack_image(data, i, height, targetCRC)
	}
}

func crack_width_height(data []byte, targetCRC uint32) {
	for width := 0; width < 0x1FFF; width++ {
		go func(width int) {
			for height := 0; height < 0x1FFF; height++ {
				crc32 := calculation_crc32(data, width, height)
				if crc32 == targetCRC {
					wirte_png(data, width, height, crc32)
				}
			}
		}(width)
	}
}

func main() {
	args := os.Args
	filePath, err := check_file(args)
	if err != nil {
		return
	}

	data, err := read_file(filePath)
	if err != nil {
		return
	}

	var (
		width     = int(binary.BigEndian.Uint32(data[0x10:0x14]))
		height    = int(binary.BigEndian.Uint32(data[0x14:0x18]))
		targetCRC = binary.BigEndian.Uint32(data[29:33])
	)

	start = time.Now()
	// 并行化爆破高度
	fmt.Println("[-] 爆破高度中...")
	crack_height(data, width, targetCRC)
	time.Sleep(time.Second * 10)
	
	// 并行化爆破宽度
	fmt.Println("[-] 爆破宽度中...")
	crack_width(data, height, targetCRC)
	time.Sleep(time.Second * 10)

	// 并行化爆破高度和宽度
	fmt.Println("[-] 爆破宽度和高度中...")
	crack_width_height(data, targetCRC)
	time.Sleep(time.Second * 10)

	fmt.Println("[-] 已经帮您爆破完了0x1FFF的宽高了!")
}

/*
	每一个爆破的goroutine添加一个time.Sleep(time.Second * 10)，这样能够让爆破出来了就退出了，而不是爆破出来后
	由于没有Sleep所以导致该goroutine没有运行保存图像的位置就去到下一个代码执行goroutine，所以没有正常保存图像并且退出

    在程序的最后，有一行代码time.Sleep(time.Second * 10)，它的作用是让程序暂停10秒钟，
  	以确保所有的goroutine都有足够的时间来完成它们的执行。如果程序立即退出，一些goroutine可
  	能没有足够的时间来完成它们的执行，输出可能不完整。

    因为有延迟函数，所以使用retun返回，而不是使用os.Exit(-1)，os.Exit(0)没问题，只要是非0的都会导致延迟函数不执行
*/
