__author__ = 'Peter'

from os import listdir
from os.path import isdir

#
# Scans a directory
#


def scan_directory(dir):
    None


def scan_all(path):
    result = listdir(path)
    return [x for x in result if isdir(path+x)]