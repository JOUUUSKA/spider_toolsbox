import cv2
import ddddocr


def ocr_img(img_path):
    '''
    :param imgpath: 需要识别的图片路径
    :return: 图片中显示的验证码


    此函数用于识别简单字母＋图片验证码，
    返回给图片中显示的验证码
    '''
    ocr = ddddocr.DdddOcr(show_ad=False)
    with open(img_path, 'rb') as f:
        img_bytes = f.read()
    res = ocr.classification(img_bytes)
    print('识别出的验证码为：' + res)
    return res


def ocr_slide_with_hole(bgimg_path, fullpage_path):
    '''
    :param imgpath: 需要识别的背景图片路径
    :param fullpage_path: 需要识别的全图片路径
    :return: 图片中显示的验证码缺口坐标


    此函数用于识别 一张图为带坑位的滑块图，
    返回图片中显示的滑块图缺口坐标
    '''
    slide = ddddocr.DdddOcr(det=False, ocr=False, show_ad=False)
    with open(bgimg_path, 'rb') as f:
        target_bytes = f.read()
    with open(fullpage_path, 'rb') as f:
        background_bytes = f.read()
    img = cv2.imread(bgimg_path)
    res = slide.slide_comparison(target_bytes, background_bytes)
    print(res)
    return res

def ocr_slide_with_clean(bgimg_path, fullpage_path):
    '''小滑块为单独的png图片，背景是透明图'''
    '''
    :param imgpath: 需要识别的背景图片路径
    :param fullpage_path: 需要识别的全图片路径
    :return: 图片中显示的验证码缺口坐标
    
    
    此函数用于识别 小滑块为单独的png图片，背景是透明图的滑块图，
    返回图片中显示的滑块图缺口坐标
    '''
    det = ddddocr.DdddOcr(det=False, ocr=False, show_ad=False)
    with open(bgimg_path, 'rb') as f:
        target_bytes = f.read()
    with open(fullpage_path, 'rb') as f:
        background_bytes = f.read()
    res = det.slide_match(target_bytes, background_bytes)
    print(res, res.get('target')[0])
    return res

def ocr_click_choose(test_img_path, result_img_path):
    '''
    :param test_img_path: 需要识别的背景图片路径
    :param result_img_path: 识别后，生成的 新的 带红框的 全图片 的路径
    :return: 点选图片中的图案坐标


    此函数用于识别 简单点选验证码 图片，
    返回图片中显示的 点选验证码 所在坐标
    '''
    det = ddddocr.DdddOcr(det=True, show_ad=False)
    with open(test_img_path, 'rb') as f:
        image = f.read()
    poses = det.detection(image)
    print(poses)
    print(poses[0][0], poses[1][0], poses[2][0])
    im = cv2.imread(test_img_path)
    for box in poses:
        x1, y1, x2, y2 = box
        im = cv2.rectangle(im, (x1, y1), (x2, y2), color=(0, 0, 255), thickness=2)
    cv2.imwrite(result_img_path, im)
    return poses
