__author__ = 'Peter'


import subprocess, search, cleardownloads
import logging, urllib,sys


logging.getLogger('torrenter')
logging.basicConfig(filename='example.log',level=logging.DEBUG, format='%(asctime)s %(message)s')


def main():
    logging.info("Starting search.py")
    try:
        search.main()
    except urllib.error.HTTPError:
        sys.exit("Failure to connect")

    ## If torrents are present start the client
    if search.files_downloaded:
        logging.info("Starting torrent client")
        subprocess.call("C:\Program Files (x86)\qBittorrent\qbittorrent.exe")

        logging.info("Starting cleardownloads.py")
        cleardownloads.main()

    logging.info("DONE!")

if __name__ == "__main__":
    main()