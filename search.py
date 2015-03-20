import urllib.request
import urllib.parse
import re
import collections
from bs4 import BeautifulSoup

import scan, menu


base_url = 'http://www.extratorrent.cc/'

user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
headers = {'User-Agent': user_agent}

main_menu = menu.Menu('Main',['Download an episode','Update one or more series','Exit'])


def print_menu(menu_options):
    for key,item in menu_options.items():
        print(key+ ': ' + item)

    choice = input('>> ')

    resolve_choice(menu_options, choice)

def resolve_choice(options,choice):
    if options is main_menu:
        print(main_menu[choice])

def options_menu():
    option = input(
        'What do you want to do? \n'
        '1 - Download a specific episode \n'
        '2 - Update one or more series \n'
    )
    print(option)
    if option == '2':
        print('Pick one of these shows: \n')
        dirlist = scan.scan_all('Z:\Series\\')
        dirlist.sort()
        i=1
        for dir in dirlist:
            print(str(i) + '. ' + dir)
            i += 1


def search_show(show):
    show = urllib.parse.quote_plus(show)
    url = base_url + '/search/?new=1&search='+show+'&s_cat=8'
    req = urllib.request.Request(url,headers=headers)
    response = urllib.request.urlopen(req)
    htmlpage = response.read()
    return htmlpage

def extract_links(page):
    soup = BeautifulSoup(page)
    torrentrows = soup.find_all(class_= re.compile('tl[rz]'))
    links = []
    for row in torrentrows:
        #
        # this creates the .torrent link
        #
        relative_link_to_torrent = row.td.a.get('href')
        link_to_torrent = base_url + relative_link_to_torrent[9:]
        #download_torrent(link_to_torrent)

        #
        # Find out how many seeders/leechers each torrent has
        #

        try:
            seeders = int(row.find('td', {'class' : 'sy'} ).string)
            leechers = int(row.find('td', {'class' : 'ly'} ).string)

            # Create a tuple with link, seeders, leechers

            t = (link_to_torrent,seeders,leechers)
            links.append(t)

        except AttributeError:
            # No seeders/leechers --> discard
            print('Oops, no seeders or leechers found! \n')

    return links

def download_torrent(link,show):
    print(link)
    req = urllib.request.Request(link,headers=headers)
    response = urllib.request.urlopen(req)
    f = open('torrents\\'+show+'.torrent', 'wb')
    torrent_file = response.read(1024)
    while(torrent_file):
        f.write(torrent_file)
        torrent_file = response.read(1024)


def main():
    print(main_menu)
  #  print_menu(main_menu)
    show = input('Which show?')
    print('Searching for ' + show)
    result = search_show(show)
    linklist = extract_links(result)
    linklist.sort(key=lambda t: t[1],reverse=True)
    download_torrent(linklist[0][0],show)


if __name__ == "__main__":
    main()