__author__ = 'Peter'

from shutil import copy,rmtree
from os.path import getsize
from os import remove,rename

import scan,rename_file


ROOT_DIR = 'E:\Downloads - finished\\'

def flatten_directory(dir):
    root_path=dir
    dirlist = scan.scan_all(dir)
    for dir in dirlist:
        flatten_directory(root_path+dir+'\\')
        rmtree(root_path+dir)
    filelist = scan.scan_all_files(dir)
    for file in filelist:
        print('Copying file from ' + dir+file + ' to ' + root_path+file)
        if not (dir+file == ROOT_DIR+file):
            copy(dir+file,ROOT_DIR+file)

# Keep all files over 100MB in size

def filter_episodes(dir):
    filelist = scan.scan_all_files(dir)
    for file in filelist:
        absolute_file_path = dir+file
        if getsize(absolute_file_path) < 102400000:
            remove(absolute_file_path)

def rename_episodes(dir):
    filelist = scan.scan_all_files(dir)
    for file in filelist:
        new_name = rename_file.plexify_name(file)
        rename(dir+file,dir+new_name)

def move_files_to_NAS():
    None

def main():
    #flatten_directory(ROOT_DIR)
    #filter_episodes(ROOT_DIR)
    rename_episodes(ROOT_DIR)



if __name__ == "__main__":
    main()



