from tools.file import image_name, txt_name, video_name


def test_generate_name():
    i = 0
    name = image_name()
    while (i := i + 1) < 3:
        assert name() == f"image_{i}"

    i = 0
    name = txt_name()
    while (i := i + 1) < 3:
        assert name() == f"txt_{i}"

    i = 0
    name = video_name()
    while (i := i + 1) < 3:
        assert name() == f"video_{i}"
