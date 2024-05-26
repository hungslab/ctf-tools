import os
import shutil
from typing import Tuple


def get_baseDir():
    """获取当前工作目录。

    Returns
    -------
    str
        当前工作目录的路径。
    """
    return os.getcwd()

def get_save_info(filePath) -> Tuple[str, str, str]:
    """从文件路径中提取文件名、文件夹路径和保存文件夹路径。

    Parameters
    ----------
    filePath : str
        要处理的文件路径。

    Returns
    -------
    Tuple[str, str, str]
        一个包含三个元素的元组，分别是文件名前缀、文件名和保存文件夹路径。
    """

    fileDir = os.path.dirname(filePath)
    fileName = filePath.split('\\')[-1]
    filePrefix, fileSuffix = os.path.splitext(fileName)

    if fileSuffix == "":
        saveDir = os.path.join(fileDir, f"{filePrefix}_BYXS20")
    else:
        saveDir = os.path.join(fileDir, filePrefix)
    return filePrefix, fileName, saveDir

def clear_and_create_dir(saveDir):
    """删除指定的文件夹，并重新创建一个同名的空文件夹。如果指定的文件夹不存在，则不进行任何操作。

    Parameters
    ----------
    saveDir : str
        要操作的文件夹路径。
    """
    if os.path.exists(saveDir):
        shutil.rmtree(saveDir, ignore_errors=True)
    os.makedirs(saveDir)
