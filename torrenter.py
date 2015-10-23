__author__ = 'Peter'


import subprocess
import logging

logging.basicConfig(filename='example.log',level=logging.DEBUG, format='%(asctime)s %(message)s')

def main():
    logging.info("Starting search.py")
    output = subprocess.call("python search.py")

    logging.info("Starting torrent client")
    subprocess.call("C:\Program Files (x86)\qBittorrent\qbittorrent.exe")

    logging.info("Starting cleardownloads.by")
    subprocess.call("python cleardownloads.py")

if __name__ == "__main__":
    main()