# -*- coding:UTF-8 -*-
import platform
import socket
import time
import codecs
import os


def is_win():
    return 'Windows' in platform.system()


def is_linux():
    return 'Linux' in platform.system()


# 获取linux ip
def get_linux_ip():
    import fcntl  # Linux 下的Python自带模块，win不带
    import struct

    ifname = 'bond0'  # 网口
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(s.fileno(), 0x8915, struct.pack('256s', ifname[:15]))[20:24])


# 获取本机内网IP
def get_private_ip():
    ip_list = socket.gethostbyname_ex(socket.gethostname())
    # 本机所有内网IP
    ips = ip_list[2]
    return ips[0]


# 获取本机IP
def get_ip():
    if is_win():
        return get_private_ip()
    else:
        return get_linux_ip()


# 轻量级记录日志
def log(msg):
    log_path = os.path.abspath(os.path.dirname(os.path.dirname(__file__))) + "/log"
    if not os.path.exists(log_path):
        os.makedirs(log_path)
    log_file = log_path + "/info.log"

    # 以追加模式打开一个文件，如果文件不存在则创建文件
    log_file = open(log_file, 'a')
    log_file.write(msg + "\n")
    log_file.close()


# 创建 单个目录
def mak_dir(path):
    if not os.path.exists(path):
        os.mkdir(path)


# 递归创建目录
def mak_dirs(path, mode=0777):
    if not os.path.exists(path):
        os.makedirs(path)


def read_1(name):
    result = ""

    # 读取资源
    # 'r'表示读取
    # 'w'表示写入
    # 'a'表示添加
    # '+'表示读写
    # 'b'表示2进制访问
    f = open(name, 'rb')

    # 表示读取全部内容
    text = f.read()

    result = ''.join(text)

    f.close()

    return result


def read_2(name):
    s1 = time.clock()

    result = ""
    file = open(name, 'rb')

    while 1:
        data = file.readline(10 * 1024)
        if not data:
            break
        result += ''.join(data)

    e1 = time.clock()
    print "cost time " + str(e1 - s1)
    return result


def write_1(file_path, file_list):
    # 'r'：只读（缺省。如果文件不存在，则抛出错误）
    # 'w'：只写（如果文件不存在，则自动创建文件）
    # 'a'：附加到文件末尾
    # 'r+'：读写
    src_file = open(file_path, "w")

    src_file.write(file_list)

    src_file.close()


def write_2(file_path, file_list):
    # 'r'：只读（缺省。如果文件不存在，则抛出错误）
    # 'w'：只写（如果文件不存在，则自动创建文件）
    # 'a'：附加到文件末尾
    # 'r+'：读写
    src_file = codecs.open(file_path, "w", "utf-8")

    txt = ""
    for i in file_list:
        txt += i + "\n"

    src_file.write(txt)

    src_file.close()


# 递归删除目录和文件
def remove_dir_file(dir_path):
    if not os.path.isdir(dir_path):
        return
    files = os.listdir(dir_path)
    try:
        for f in files:
            file_path = os.path.join(dir_path, f)
            if os.path.isfile(file_path):
                os.remove(file_path)
            elif os.path.isdir(file_path):
                remove_dir_file(file_path)
        os.rmdir(dir_path)
    except Exception, e:
        print e


# 获取文件列表 能控制文件，不能控制目录
def get_file_list(path, ignore_file=None):
    file_list = []
    for dir, sub_dirs, files in os.walk(path):
        # 遍历 根目录 下的files
        for f in files:
            # 文件后缀
            suffix = os.path.splitext(f)[1]
            # 文件后缀不在黑名单
            if suffix.lower() not in ignore_file:
                file_list.append(dir + os.path.sep + f.decode('gbk'))
    return file_list


# 获取文件列表 能控制文件，能控制目录
def get_file_list2(path, file_list, ignore_dir=None, ignore_suffix=None):
    if os.path.isfile(path):  # 文件
        # 替换掉 绝对路径的前缀
        # path = path.replace(os.path.dirname(path), "")

        # 文件后缀
        suffix = os.path.splitext(path)[1]

        # 不在黑名单 -- 读取
        if suffix.lower() not in ignore_suffix:
            file_list.append(path.decode('gbk'))
    elif os.path.isdir(path):  # 目录
        for item in os.listdir(path):
            # 不在黑名单 -- 放行
            if item not in ignore_dir:
                new_dir = os.path.join(path, item)
                get_file_list2(new_dir, file_list, ignore_dir, ignore_suffix)
    else:
        print "Error ", path

    return file_list
