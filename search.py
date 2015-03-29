import urllib.request
import urllib.parse
import re
import sys
from bs4 import BeautifulSoup

import scan, menu


base_url = 'http://www.extratorrent.cc/'

user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
headers = {'User-Agent': user_agent}
library_root = 'Z:\Series\\'


def update_series(show):
    print('Searching for ' + show)
    result = search_show(show)
    linklist = extract_links(result)
    linklist.sort(key=lambda t: t[1],reverse=True)
    download_torrent(linklist[0][0],show)
    print("Thingy downloaded")
    main_menu.set_previous(None)
    return main_menu

def update_all():
    None

def update_last_season():
    None

def generate_series_list():
        dirlist = scan.scan_all(library_root)
        dirlist.sort()
        series = []
        for dir in dirlist:
            series.append((dir, update_series, dir))

        library_menu = menu.Menu('Library',series)
        return library_menu



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
            seeders = int(row.find('td', {'class': 'sy'} ).string)
            leechers = int(row.find('td', {'class': 'ly'} ).string)

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
    while torrent_file:
        f.write(torrent_file)
        torrent_file = response.read(1024)


test_menu = menu.Menu('Test',
                      [
                          ('option 1', generate_series_list),
                          ('option 2', generate_series_list),
                      ])

main_menu = menu.Menu('Main',
                      [
                          ('Download an episode', test_menu),
                          ('Update one or more series', generate_series_list)
                      ])

update_menu = menu.Menu('What do you want to update?',
                        [
                            ('Last Season', update_last_season),
                            ('All', update_all)
                        ]
                        )




def main():
    #current_menu = main_menu
    #while True:
     #   current_menu.show()
     #   choice = input('>>')
     #   current_menu = current_menu.evaluate(choice)

  #  print_menu(main_menu)
    print(scan.list_current_episodes('Castle',library_root))


if __name__ == "__main__":
    main()