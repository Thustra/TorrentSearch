__author__ = 'Peter'
import re
#
# This script will rename media files to the right format
# for the Plex Media Server.
# eg. Castle SxxEyy.mkv
#

def match_season_episode(filename):

    # List of patterns observed in filenames

    pattern1 = re.compile('[Ss]\\d+[Ee]\\d+')
    pattern2 = re.compile('[\.\-]\d{3,4}[\.\-]')
    pattern3 = re.compile('\d{1,2}[Xx]\d{1,2}')
    return pattern1.search(filename).group()

def split_episode_number(episode_number):
    episode = episode_number[-2:]
    season = episode_number[1:3]
    return (season,episode)

def match_default_pattern(string):
    pattern = re.compile('[Ss]\\d+[Ee]\\d+')
    return pattern.search(string)