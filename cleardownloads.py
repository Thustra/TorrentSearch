__author__ = 'Peter'

from shutil import copy,rmtree
from os.path import getsize,exists
from os import remove,rename,chmod,makedirs
import stat
import logging

import scan,rename_file


ROOT_SRC_DIR = 'E:\Downloads - finished\\'
ROOT_TRG_DIR = 'Z:\Series\\'

def remove_readonly(func, path, excinfo):
    chmod(path, stat.S_IWRITE)
    func(path)

def flatten_directory(dir):
    root_path=dir
    dirlist = scan.scan_all(dir)
    while dirlist:
        flatten_directory(root_path+dirlist.pop(0)+'\\')
    #for dir in dirlist:
    #    flatten_directory(root_path+dir+'\\')
    if dirlist == []:
        filelist = scan.scan_all_files(dir)
        for file in filelist:
            if not (dir+file == ROOT_SRC_DIR+file):
                logging.info('Copying file from ' + dir+file + ' to ' + ROOT_SRC_DIR+file)
                copy(dir+file,ROOT_SRC_DIR+file)
        if ( root_path != ROOT_SRC_DIR):
            logging.info("Removing: " + root_path)
            rmtree(root_path, onerror=remove_readonly)


# Keep all files over 100MB in size

def filter_episodes(dir):
    filelist = scan.scan_all_files(dir)
    for file in filelist:
        absolute_file_path = dir+file
        if getsize(absolute_file_path) < 102400000:
            chmod(absolute_file_path, stat.S_IWRITE)
            remove(absolute_file_path)

def create_dir_dict():
    #Get all directories on the NAS root folder
    series_dirs = scan.scan_all(ROOT_TRG_DIR)

    #Add dots and remove spaces
    # Game of Thrones ==> Game.of.Thrones
    # Agents of S.H.I.E.L.D ==> Agents.of.S.H.I.E.L.D
    # Mr. Robot ==> Mr.Robot
    dotted_dirs = [rename_file.add_dots_remove_years(dir) for dir in series_dirs]
    series_dict = dict(zip(dotted_dirs,series_dirs))

    return series_dict





def rename_episodes(dir):
    filelist = scan.scan_all_files(dir)
    for file in filelist:
        new_name = rename_file.plexify_name(file)
        rename(dir+file,dir+new_name)

def verify_target_dir(dir):
    if not exists(dir):
        makedirs(dir)

def export_blacklist(blacklist):
    blacklistfile = open("blacklist.txt",'a')
    for item in blacklist:
        blacklistfile.write(item)
    blacklistfile.close()


def move_files_to_NAS():

    logging.info("Moving files to NAS")
    series = create_dir_dict()

    files_to_move = scan.scan_all_files(ROOT_SRC_DIR)

    blacklist = []

    for episode in files_to_move:
        source =  ROOT_SRC_DIR+episode
        match = [dir for dir in series if (episode.lower()).startswith(dir.lower())]
        if match:
            target_series_directory = series[match[0]]
            season = rename_file.split_episode_number(rename_file.match_season_episode(episode))[0]
            season = str(season).lstrip('0')
            target = ROOT_TRG_DIR + target_series_directory + '\\' + 'Season ' + season + '\\' + episode
            verify_target_dir(ROOT_TRG_DIR + target_series_directory + '\\' + 'Season ' + season + '\\')
            logging.info('Copying ' + source + ' to ' + target)
            copy(source, target)
        else:
            logging.warning(episode + " should not have been downloaded. Added to blacklist.")
            blacklist.append(episode)
        remove(source)

    export_blacklist(blacklist)

def main():
    logging.info("Starting to clear downloads.")
    flatten_directory(ROOT_SRC_DIR)
    filter_episodes(ROOT_SRC_DIR)
    rename_episodes(ROOT_SRC_DIR)
    move_files_to_NAS()


if __name__ == "__main__":
    main()



