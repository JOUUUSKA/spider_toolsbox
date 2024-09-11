import os


def create_infile(name=None):
    """
    :param name: 需要创建的文件夹的名字
    :return: None


    此函数用于创建一个在 当前文件夹 下的新文件夹，
    名字默认为New_file。可以自行指定
    """
    if name is None:
        name = "New_file"
    if not os.path.exists(f"./{name}"):
        os.mkdir(f"./{name}")


def create_outfile(name=None):
    """
    :param name: 需要创建的文件夹的名字
    :return: None


    此函数用于创建一个在 上一级文件夹 的新文件夹，
    名字默认为New_file。可以自行指定
    """
    if name is None:
        name = "New_file"
    if not os.path.exists(f"../{name}"):
        os.mkdir(f"../{name}")
