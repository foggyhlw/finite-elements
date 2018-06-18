#! py3k
# -*- coding: utf-8 -*-

# 将文件行倒序
import os

def main():
    filepath = input('please drag a file here:')
    if os.path.exists(filepath):
        print(filepath)
        input('waiting for you')
        revert_file_lines(filepath)
        print('done')

def revert_file_lines(filepath):
    print('reading')
    with open(filepath, mode='r') as fin:
        lines = fin.readlines()
        print(lines)
        with open(filepath+'.r', mode='w') as fout:
            print('converting and saving')
            fout.writelines(lines[::-1])

if __name__ == "__main__":
    main()
    input()

