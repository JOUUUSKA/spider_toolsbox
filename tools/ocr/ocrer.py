import cv2
import ddddocr
from typing import Union, List, Tuple, Optional

import numpy as np
from loguru import logger


def get_image_bytes(image_source: Union[str, bytes]) -> bytes:
    """统一处理图片输入源，返回图片字节数据"""
    if isinstance(image_source, str):
        with open(image_source, 'rb') as f:
            return f.read()
    elif isinstance(image_source, bytes):
        return image_source
    else:
        raise ValueError("image_source 必须是文件路径(str)或字节数据(bytes)")


def recognize_text_captcha(image_source: Union[str, bytes]) -> str:
    """
    识别简单字母+数字验证码

    Args:
        image_source: 图片路径或字节数据

    Returns:
        str: 识别出的验证码文本
    """
    try:
        ocr = ddddocr.DdddOcr(show_ad=False)
        img_bytes = get_image_bytes(image_source)
        result = ocr.classification(img_bytes)
        logger.info(f'识别结果: {result}')
        return result
    except Exception as e:
        logger.error(f"验证码识别失败: {str(e)}")
        raise


def recognize_slide_captcha_with_hole(
        background_source: Union[str, bytes],
        fullpage_source: Union[str, bytes]
) -> int:
    """
    识别带坑位的滑块验证码

    Args:
        background_source: 带坑位的背景图(路径或字节)
        fullpage_source: 完整背景图(路径或字节)

    Returns:
        int: 缺口左上角x坐标
    """
    try:
        slide = ddddocr.DdddOcr(det=False, ocr=False, show_ad=False)
        bg_bytes = get_image_bytes(background_source)
        full_bytes = get_image_bytes(fullpage_source)

        result = slide.slide_comparison(bg_bytes, full_bytes)
        logger.info(f"滑块缺口位置: x={result}")
        return result
    except Exception as e:
        logger.error(f"滑块验证码识别失败: {str(e)}")
        raise


def recognize_slide_captcha_with_transparent(
        slider_source: Union[str, bytes],
        background_source: Union[str, bytes]
) -> Tuple[int, int]:
    """
    识别透明背景的小滑块验证码

    Args:
        slider_source: 透明背景的小滑块图(路径或字节)
        background_source: 完整背景图(路径或字节)

    Returns:
        tuple: (x, y) 滑块在背景图中的位置坐标
    """
    try:
        det = ddddocr.DdddOcr(det=False, ocr=False, show_ad=False)
        slider_bytes = get_image_bytes(slider_source)
        bg_bytes = get_image_bytes(background_source)

        result = det.slide_match(slider_bytes, bg_bytes)
        target_x, target_y = result['target']
        logger.info(f"滑块位置坐标: ({target_x}, {target_y})")
        return (target_x, target_y)
    except Exception as e:
        logger.error(f"透明滑块验证码识别失败: {str(e)}")
        raise


def recognize_click_captcha(
        image_source: Union[str, bytes],
        output_path: Optional[str] = None
) -> List[Tuple[int, int, int, int]]:
    """
    识别点选验证码中的目标位置

    Args:
        image_source: 验证码图片(路径或字节)
        output_path: 可选，标注结果的保存路径

    Returns:
        list: 识别出的目标框列表 [(x1, y1, x2, y2), ...]
    """
    try:
        det = ddddocr.DdddOcr(det=True, show_ad=False)
        img_bytes = get_image_bytes(image_source)
        boxes = det.detection(img_bytes)

        logger.info(f"识别到 {len(boxes)} 个目标区域")

        # 如果需要生成标注图
        if output_path:
            img = cv2.imread(image_source) if isinstance(image_source, str) else cv2.imdecode(
                np.frombuffer(image_source, np.uint8), cv2.IMREAD_COLOR
            )
            for box in boxes:
                x1, y1, x2, y2 = box
                cv2.rectangle(img, (x1, y1), (x2, y2), (0, 0, 255), 2)
            cv2.imwrite(output_path, img)
            logger.info(f"标注结果已保存至: {output_path}")

        return boxes
    except Exception as e:
        logger.error(f"点选验证码识别失败: {str(e)}")
        raise