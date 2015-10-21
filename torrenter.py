__author__ = 'Peter'


import subprocess

def main():
    output = subprocess.call("python search.py")
    print("output= " + str(output))
    subprocess.call("C:\Program Files (x86)\qBittorrent\qbittorrent.exe")
    subprocess.call("python cleardownloads.py")

if __name__ == "__main__":
    main()