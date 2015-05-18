__author__ = 'Peter'

from shutil import copy,rmtree

import scan


ROOT_DIR = 'E:\Downloads - finished\\'

def flatten_directory(path):
    root_path=path
    dirlist = scan.scan_all(path)
    for dir in dirlist:
        flatten_directory(root_path+dir+'\\')
        rmtree(root_path+dir)
    filelist = scan.scan_all_files(path)
    for file in filelist:
        if not path+file == root_path+file:
            print('Copying file from ' + path+file + ' to ' + root_path+file)
            copy(path+file,ROOT_DIR+file)

def main():
    flatten_directory(ROOT_DIR)

if __name__ == "__main__":
    main()



