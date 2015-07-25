__author__ = 'Peter'

from shutil import copy,rmtree
from os.path import getsize
from os import remove,rename,chmod
import stat

import scan,rename_file


ROOT_SRC_DIR = 'E:\Downloads - finished\\'
ROOT_TRG_DIR = 'Z:\Series\\'

def remove_readonly(func, path, excinfo):
    chmod(path, stat.S_IWRITE)
    func(path)

def flatten_directory(dir):
    root_path=dir
    print("root path is " + root_path)
    dirlist = scan.scan_all(dir)
    print("Dirlist")
    print(dirlist)
    for dir in dirlist:
        flatten_directory(root_path+dir+'\\')
        print("Removing: " + root_path+dir)
        rmtree(root_path+dir, onerror=remove_readonly)
    if dirlist == []:
        filelist = scan.scan_all_files(dir)
        print("Filelist")
        print(filelist)
        for file in filelist:
            print('Copying file from ' + dir+file + ' to ' + ROOT_SRC_DIR+file)
            if not (dir+file == ROOT_SRC_DIR+file):
                copy(dir+file,ROOT_SRC_DIR+file)

# Keep all files over 100MB in size

def filter_episodes(dir):
    filelist = scan.scan_all_files(dir)
    for file in filelist:
        absolute_file_path = dir+file
        if getsize(absolute_file_path) < 102400000:
            chmod(absolute_file_path, stat.S_IWRITE)
            remove(absolute_file_path)

def rename_episodes(dir):
    filelist = scan.scan_all_files(dir)
    for file in filelist:
        new_name = rename_file.plexify_name(file)
        rename(dir+file,dir+new_name)

def move_files_to_NAS():
    available_dirs = scan.scan_all(ROOT_TRG_DIR)

    files_to_move = scan.scan_all_files(ROOT_SRC_DIR)
    dotted_dirs = [rename_file.add_dots_remove_years(dir) for dir in available_dirs]
    for episode in files_to_move:
        match = [dir for dir in dotted_dirs if (episode.lower()).startswith(dir.lower())]
        target_series_directory = rename_file.undot_file(max(match))
        season = rename_file.split_episode_number(rename_file.match_season_episode(episode))[0]
        season = str(season).lstrip('0')
        source =  ROOT_SRC_DIR+episode
        target = ROOT_TRG_DIR + target_series_directory + '\\' + 'Season ' + season + '\\' + episode
        print('copy ' + source + ' to ' + target)
        copy(source, target)

def main():
    flatten_directory(ROOT_SRC_DIR)
    filter_episodes(ROOT_SRC_DIR)
    rename_episodes(ROOT_SRC_DIR)
    move_files_to_NAS()



if __name__ == "__main__":
    main()



