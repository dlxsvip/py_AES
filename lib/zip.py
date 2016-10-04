# -*- coding:UTF-8 -*-

import zipfile
import time
import os

try:
    import zlib

    compression = zipfile.ZIP_DEFLATED
except:
    compression = zipfile.ZIP_STORED


# file_path 待压缩的目录
def zip(src_dir):
    start = src_dir.rfind(os.sep) + 1
    # 压缩后的文件名
    name = str(src_dir).split(os.path.sep)[-1]
    if name:
        file_name = name + ".zip"
    else:
        file_name = 'tmp.zip'

    z = zipfile.ZipFile(file_name, mode="w", compression=compression)

    try:
        for root, s_dirs, files in os.walk(src_dir):
            for f in files:
                if f == file_name or f == "zip.py":
                    continue
                # 打印压缩的文件
                # print f
                z_path = os.path.join(root, f)
                z.write(z_path, z_path[start:])
        z.close()
    except Exception as e:
        if z:
            z.close()
        print e


# src_file待解压的文件,解压后放入org_dir目录
def unzip(src_file, org_dir=None):
    if not org_dir:
        # src_file 文件的目录
        org_dir = os.path.dirname(src_file)

    if not os.path.exists(org_dir):
        os.makedirs(org_dir)

    if zipfile.is_zipfile(src_file):
        start_time = time.time()
        fz = zipfile.ZipFile(src_file, 'r')
        for file in fz.namelist():
            # 打印zip归档中文件
            # print(file)
            fz.extract(file, org_dir)
        end_time = time.time()
        times = end_time - start_time
        print times
