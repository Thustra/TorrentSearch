__author__ = 'Peter'

from os import listdir
from os.path import isdir
from os.path import isfile

#
# Scans a directory
#


def scan_directory(dir):
    None


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
    print(seasons)
    #last_season = season.pop()

    all_season_episodes = []

    for season in seasons:
        season_episodes = scan_all_files(root+show+'\\'+season+'\\')
        if season_episodes.__contains__('Thumbs.db'):
            season_episodes.remove('Thumbs.db')
        season_episodes.sort()
        all_season_episodes.extend(season_episodes)
    #last_episode= season_episodes.pop()

    return all_season_episodes