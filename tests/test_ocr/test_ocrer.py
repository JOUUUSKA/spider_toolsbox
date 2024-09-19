from tools.ocr import ocr_img, ocr_click_choose, ocr_slide_with_hole, ocr_slide_with_clean

result = ocr_img("./captcha_img/test_ocr_img.png")
assert result == "iepv"

result = ocr_click_choose("./captcha_img/test_click_ocr.jpg", "./result_captcha_img/result_click_ocr_img.png")
# assert result == "iepv"

result = ocr_slide_with_hole("./captcha_img/test_slide_with_hole_ocr_bg.jpg", "./captcha_img/test_slide_with_hole_ocr_target.jpg")
# assert result == "iepv"

result = ocr_slide_with_clean("./captcha_img/test_slide_with_clean_ocr_bg.png", "./captcha_img/test_slide_with_clean_ocr_target.png")
# assert result == "iepv"
