__author__ = 'Peter'

from os import listdir
from os.path import isdir
from os.path import isfile


# Returns all directories under this path
def scan_all(path):
    result = listdir(path)
    return [x for x in result if isdir(path+x)]


# Returns all files under this path
def scan_all_files(path):
    result = listdir(path)
    return [x for x in result if isfile(path+x)]


# Returns an ordered list of all episodes we currently have
def list_current_episodes(show, root):
    # Get all seasons we currently have folders for
    seasons = scan_all(root+show+'\\')
    seasons.sort(key=lambda x: int(x[7:]))
    # print(seasons)

    all_season_episodes = []

    for season in seasons:
        season_episodes = scan_all_files(root+show+'\\'+season+'\\')
        if season_episodes.__contains__('Thumbs.db'):
            season_episodes.remove('Thumbs.db')
        sorted_season_episodes = sorted(season_episodes, key=lambda s: s.lower())
        all_season_episodes.extend(sorted_season_episodes)

    return all_season_episodes