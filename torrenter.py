__author__ = 'Peter'


import subprocess, search, cleardownloads
import logging


logging.getLogger('torrenter')
logging.basicConfig(filename='example.log',level=logging.DEBUG, format='%(asctime)s %(message)s')


def main():
    logging.info("Starting search.py")
    search.main()

    logging.info("Starting torrent client")
    subprocess.call("C:\Program Files (x86)\qBittorrent\qbittorrent.exe")

    logging.info("Starting cleardownloads.py")
    cleardownloads.main()

    logging.info("DONE!")

if __name__ == "__main__":
    main()