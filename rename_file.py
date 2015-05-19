__author__ = 'Peter'
import re
#
# This module provides functions for manipulating
# filenames and changing them to plex default
# eg. Castle SxxEyy
#

default_pattern = re.compile('[Ss]\\d+[Ee]\\d+')
pattern2 = re.compile('[\.\-]\d{3,4}')
pattern3 = re.compile('\d{1,2}[Xx]\d{1,2}')

def match_season_episode(filename):
    return default_pattern.search(filename).group()

def split_episode_number(episode_number):
    episode = episode_number[-2:]
    season = episode_number[1:3]
    return (season,episode)


def match_default_pattern(string):
    return default_pattern.search(string)

def add_dots_remove_years(string):
    return re.sub(r'.[(]\d{4}[)]','',string.replace(' ','.'))

def undot_file(string):
    return string.replace('.',' ')

def plexify_name(string):
    #If the file matches the pattern we want, don't change it
    if default_pattern.search(string):
        return string
    elif pattern2.search(string):
        piece_to_change = list(pattern2.finditer(string))[-1]
        endpos = piece_to_change.end()
        startpos = piece_to_change.start()
        #Cut out the piece to change
        cut = string[startpos+1:endpos]
        if len(cut) == 4:
            cut = 'S'+cut[0:2] + 'E' + cut[2:4]
        if len(cut) == 3:
            cut = 'S0'+cut[0:1] + 'E' + cut[1:3]
        return string[0:startpos+1] + cut + string[endpos-1:]
