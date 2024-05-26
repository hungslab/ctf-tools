package main

import (
	"bytes"
	"crypto/aes"
	"crypto/cipher"
	"encoding/base64"
	"fmt"
)

func encrypt(plaintext []byte, key []byte, iv []byte) ([]byte, error) {
	block, err := aes.NewCipher(key)
	if err != nil {
		return nil, err
	}

	ciphertext := make([]byte, len(plaintext))
	mode := cipher.NewCBCEncrypter(block, iv)
	mode.CryptBlocks(ciphertext, plaintext)

	return ciphertext, nil
}

func decrypt(ciphertext []byte, key []byte, iv []byte) ([]byte, error) {
	block, err := aes.NewCipher(key)
	if err != nil {
		return nil, err
	}

	plaintext := make([]byte, len(ciphertext))
	mode := cipher.NewCBCDecrypter(block, iv)
	mode.CryptBlocks(plaintext, ciphertext)

	return plaintext, nil
}

func pad(plaintext []byte) []byte {
	if len(plaintext)%aes.BlockSize == 0 {
		return plaintext
	}
	padding := aes.BlockSize - (len(plaintext) % aes.BlockSize)
	padtext := bytes.Repeat([]byte{byte(padding)}, padding)
	return append(plaintext, padtext...)
}

func unpad(padded []byte) []byte {
	if len(padded)%aes.BlockSize == 0 {
		return padded
	}
	padding := int(padded[len(padded)-1])
	return padded[:len(padded)-padding]
}

func main() {
	key := []byte("this_iskeykeykey")
	iv := []byte{0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00}

	plaintext := []byte("hello world")
	plaintext = pad(plaintext)

	// 加密
	ciphertext, err := encrypt(plaintext, key, iv)
	if err != nil {
		panic(err)
	}
	fmt.Printf("加密结果：%s\n", base64.StdEncoding.EncodeToString(ciphertext))

	// 解密
	decrypted, err := decrypt(ciphertext, key, iv)
	if err != nil {
		panic(err)
	}
	fmt.Printf("解密结果：%s\n", unpad(decrypted))
}
