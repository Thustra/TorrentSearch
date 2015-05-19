__author__ = 'Peter'

from shutil import copy,rmtree
from os.path import getsize
from os import remove,rename

import scan,rename_file


ROOT_SRC_DIR = 'E:\Downloads - finished\\'
ROOT_TRG_DIR = 'Z:\Series\\'

def flatten_directory(dir):
    root_path=dir
    dirlist = scan.scan_all(dir)
    for dir in dirlist:
        flatten_directory(root_path+dir+'\\')
        rmtree(root_path+dir)
    filelist = scan.scan_all_files(dir)
    for file in filelist:
        print('Copying file from ' + dir+file + ' to ' + root_path+file)
        if not (dir+file == ROOT_SRC_DIR+file):
            copy(dir+file,ROOT_SRC_DIR+file)

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
    available_dirs = scan.scan_all(ROOT_TRG_DIR)

    files_to_move = scan.scan_all_files(ROOT_SRC_DIR)
    dotted_dirs = [rename_file.add_dots_remove_years(dir) for dir in available_dirs]
    for episode in files_to_move:
        match = [dir for dir in dotted_dirs if (episode.lower()).startswith(dir.lower())]
        target_series_directory = rename_file.undot_file(max(match))
        season = rename_file.split_episode_number(rename_file.match_season_episode(episode))[0]
        season = str(season).lstrip('0')
        print('copy ' + ROOT_SRC_DIR+episode + ' to '
              + ROOT_TRG_DIR + target_series_directory + '\\' + 'Season ' + season + '\\' + episode)
        #copy(ROOT_SRC_DIR+episode, ROOT_TRG_DIR + target_series_directory + '\\' + 'Season ' + season + '\\' + episode)

def main():
    #flatten_directory(ROOT_DIR)
    #filter_episodes(ROOT_DIR)
    #rename_episodes(ROOT_SRC_DIR)
    move_files_to_NAS()



if __name__ == "__main__":
    main()



