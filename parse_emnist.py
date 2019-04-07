#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
from PIL import Image
import numpy as np
import struct
from typing import Generator
import os

def read_4bytes(f) -> int:
    '''
    ファイルから4バイト読み込む
    '''
    return int.from_bytes(f.read(4), 'big')

def read_1bytes(f) -> int:
    '''
    ファイルから1バイト読み込む
    '''
    return int.from_bytes(f.read(1), 'big')

def load_image(f, width, height) ->np.ndarray:
    '''
    画像ファイルから1画像分の情報を読み込む
    '''
    data = f.read(width * height)
    data = np.frombuffer(data, dtype=np.uint8)
    data = data.reshape(width, height)

    # -90度回転
    data = np.rot90(data, k=1)
    # 上下反転
    data = np.flip(data, axis=0)

    return data

def open_label(filename: str) -> Generator[int, None, None]:
    '''
    ラベルファイルを読み込み、ラベル情報を返す
    '''
    with open(filename, 'rb') as f:
        # ファイルチェック
        if read_4bytes(f) != 2049:
            raise Exception('file is not mnist label')

        # ファイル数
        file_count = read_4bytes(f)
        print(f'number of file: {file_count}')

        # ラベルの読み込み
        for _ in range(0, file_count):
            yield read_1bytes(f)

def open_image(filename: str) -> Generator[np.ndarray, None, None]:
    '''
    画像ファイルを読み込み、画像情報を返す
    '''
    with open(filename, 'rb') as f:
        # ファイルチェック
        if int.from_bytes(f.read(4), 'big') != 2051:
            raise Exception('file is not mnist label')

        # ファイル数
        file_count = read_4bytes(f)
        print(f'number of file: {file_count}')

        # 画像の高さ
        width = read_4bytes(f)
        # 画像の幅
        height = read_4bytes(f)

        print(f'image width: {width}')
        print(f'image height: {height}')
        
        for _ in range(0, file_count):
            yield load_image(f, width, height)

def save_file(dir: str, imagedata: np.ndarray, label: int, index: int):
    '''
    画像ファイルを保存する
    '''
    savedir = os.path.join(dir, str(label))
    if not os.path.exists(savedir):
        os.makedirs(savedir)

    image = Image.fromarray(imagedata)
    image.save(os.path.join(savedir, f'{index:05}.png'), 'PNG')

def parse_args():
    '''
    コマンドライン引数から画像データのファイルとラベルデータのファイルを返す
    '''
    parser = argparse.ArgumentParser()
    parser.add_argument('--image', help='images.idx3-ubyte file path', type=str, default='emnist-mnist-train-images-idx3-ubyte')
    parser.add_argument('--label', help='labels.idx3-ubyte file path', type=str, default='emnist-mnist-train-labels-idx1-ubyte')
    parser.add_argument('--dir', help='save dir', type=str, default='images')

    args = parser.parse_args()
    return args

def main():
    args = parse_args()
    print(args.image)
    print(args.label)
    print(args.dir)

    index = 0
    for image, label in zip(open_image(args.image), open_label(args.label)):
        save_file(args.dir, image, label, index)
        index += 1

main()
