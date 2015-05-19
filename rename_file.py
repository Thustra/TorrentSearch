__author__ = 'Peter'
import re
#
# This script will eventually rename media files to the right
# format for the Plex Media Server.
# eg. Castle SxxEyy.mkv
#

pattern1 = re.compile('[Ss]\\d+[Ee]\\d+')
pattern2 = re.compile('[\.\-]\d{3,4}')
pattern3 = re.compile('\d{1,2}[Xx]\d{1,2}')

def match_season_episode(filename):
    return pattern1.search(filename).group()

def split_episode_number(episode_number):
    episode = episode_number[-2:]
    season = episode_number[1:3]
    return (season,episode)

def match_default_pattern(string):
    pattern = re.compile('[Ss]\\d+[Ee]\\d+')
    return pattern.search(string)

def plexify_name(string):
    #If the file matches the pattern we want, don't change it
    if pattern1.search(string):
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
