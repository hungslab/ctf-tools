import cv2
import numpy as np


def read_img(imgPath, flags, *agrs, **kwargs) -> np.ndarray:
    """相当于cv2.imread()

    Parameters
    ----------
    imgPath : str
        图像的路径

    *args : flags
        cv2.imdecode 中的 flags 参数，用于指定读取的色彩空间。

    *args : tuple
        cv2.imdecode 中的参数，用于解码图像数据。

    **kwargs : dict
        cv2.imdecode 中的关键字参数，用于解码图像数据。

    Returns
    -------
    numpy.ndarray
        读取的图像数据，如果读取失败则返回 None。
    """
    with open(imgPath, "rb") as f:
        encoded_image = np.frombuffer(f.read(), dtype=np.uint8)
    return cv2.imdecode(encoded_image, flags=flags, *agrs, **kwargs)

def save_img(saveImgPath, img, ext, *args, **kwargs) -> bool:
    """相当于cv2.imwrite()

    Parameters
    ----------
    saveImgPath : str
        要保存的图像路径。

    img : numpy.ndarray
        要保存的图像数据。

    ext : str
        要保存的图像格式后缀。

    *args : tuple
        cv2.imencode 中的参数，用于编码图像数据。

    **kwargs : dict
        cv2.imencode 中的关键字参数，用于编码图像数据。

    Returns
    -------
    bool
        返回 True 表示保存成功，返回 False 表示保存失败。
    """
    success, encoded_image = cv2.imencode(img=img, ext=ext, *args, **kwargs)
    if success:
        with open(saveImgPath, "wb") as f:
            f.write(encoded_image)
    return success