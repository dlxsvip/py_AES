# -*- coding:UTF-8 -*-
import os
import base64
from mm import *
import util
import zip

# 当前脚本所在的目录
__cur_path__ = os.path.abspath(os.path.dirname(__file__))

# 当前脚本所在目录的父级目录
__par_path__ = os.path.dirname(__cur_path__)


def print_file_list(file_list):
    for item in file_list:
        print item

    print "total", len(file_list)


def get_files(path):
    # 忽略目录
    ignore_dir = [".idea", ".mvn", "target"]

    # 忽略文件: "" 代表没有后缀名的文件
    ignore_suffix = [".rar", ".zip", ".7z", "log", ".iml"]

    # file_list = util.get_file_list(__cur_path__ + os.path.sep + "src", ignore_suffix)
    file_list = util.get_file_list2(path, [], ignore_dir, ignore_suffix)

    # print_file_list(file_list)

    return file_list


def name_m(f_name, pc, t):
    if t:
        mm_txt = pc.encrypt(f_name)
    else:
        mm_txt = pc.decrypt(f_name)
    return mm_txt


def str_rev(s):
    return s[::-1]


def dirs_rev(ps):
    rp = ""
    ps_list = ps.split(os.path.sep)
    for d in ps_list:
        rp += d[::-1] + os.path.sep

    if rp.endswith(os.path.sep):
        rp = rp[:-1]

    return rp


# 统一放在一个目录
def jia_m(file_list, key=None):
    pc = Mm(key)
    for item in file_list:
        txt = util.read_1(item)
        mm_txt = pc.encrypt(txt)

        # 文件名
        name = str(item).split(os.path.sep)[-1]

        # 文件名加密
        name = name_m(name, pc, 1)

        p_o = __par_path__ + "/m+/" + name
        util.mak_dir(os.path.dirname(p_o))
        util.write_1(p_o, mm_txt)


# 统一放在一个目录
def jie_m(file_list, key=None):
    pc = Mm(key)
    for item in file_list:
        txt = util.read_1(item)
        mm_txt = pc.decrypt(txt)

        # 文件名
        name = str(item).split(os.path.sep)[-1]

        # 文件名解密
        name = name_m(name, pc, 0)

        p_o = __par_path__ + "/m-/" + name
        util.mak_dir(os.path.dirname(p_o))
        util.write_1(p_o, mm_txt)


# 目录结构一样
def jia_m_d(file_list, key=None):
    pc = Mm(key)
    for item in file_list:
        txt = util.read_1(item)
        mm_txt = pc.encrypt(txt)

        # 把split(path)分为目录和文件两个部分
        f_path = os.path.split(item)[0]
        f_name = os.path.split(item)[1]

        # 文件名
        f_name = str_rev(f_name)

        # 替换文件绝对路径里的 src 为 m+
        # n_p = f_path.replace(__par_path__ + os.path.sep + "src", __par_path__ + os.path.sep + "m+")

        ps = f_path.replace(__par_path__ + os.path.sep + "src" + os.path.sep, "")
        # 目录加密
        ps = dirs_rev(ps)
        # 文件路径(不包含文件名)
        n_p = __par_path__ + os.path.sep + "m+" + os.path.sep + ps

        # 目录路径不存在，则递归创建
        util.mak_dirs(n_p)

        # 密文mm_txt 写入到新的文件里
        util.write_1(n_p + os.path.sep + f_name, mm_txt)


# 目录结构一样
def jie_m_d(file_list, key=None):
    pc = Mm(key)
    for item in file_list:
        txt = util.read_1(item)
        mm_txt = pc.decrypt(txt)

        # 把split(path)分为目录和文件两个部分
        f_path = os.path.split(item)[0]
        f_name = os.path.split(item)[1]

        # 文件名解密
        f_name = str_rev(f_name)

        # 替换路径里的 m+ 为 m-
        # n_p = f_path.replace(__par_path__ + os.path.sep + "m+", __par_path__ + os.path.sep + "m-")

        ps = f_path.replace(__par_path__ + os.path.sep + "m+" + os.path.sep, "")
        # 目录解密
        ps = dirs_rev(ps)
        n_p = __par_path__ + os.path.sep + "m-" + os.path.sep + ps

        # 目录路径不存在，则递归创建
        util.mak_dirs(n_p)
        # 密文mm_txt 写入到新的文件里
        util.write_1(n_p + os.path.sep + f_name, mm_txt)


def main(m_type, key=None):
    if m_type == "encrypt":
        src_file_list = get_files(__par_path__ + os.path.sep + "src")
        # 加密
        jia_m_d(src_file_list, key)
        # 压缩
        zip.zip(__par_path__ + os.sep + "m+")
        # 压缩后删除源文件
        # util.remove_dir_file(__par_path__ + os.sep + "m+")
    elif m_type == "decrypt":
        # 解压
        zip.unzip(__par_path__ + os.path.sep + "m+.zip")

        mm_file_list = get_files(__par_path__ + os.path.sep + "m+")

        # 解密
        jie_m_d(mm_file_list, key)

        # 删除解压后加密文件
        # util.remove_dir_file(__par_path__ + os.sep + "m+")

    else:
        print "encrypt or decrypt ?"


if __name__ == '__main__':
    if len(sys.argv) >= 3:
        main(sys.argv[1], sys.argv[2])
    elif len(sys.argv) == 2:
        main(sys.argv[1])
    else:
        # main("encrypt")
        print "parm encrypt or decrypt ?"
