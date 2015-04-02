import urllib.request
import urllib.parse
import re
import sys
from bs4 import BeautifulSoup

import scan, menu,rename


base_url = 'http://www.extratorrent.cc/'

user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
headers = {'User-Agent': user_agent}
library_root = 'Z:\Series\\'
watched_dir = 'E:\Watched\\'

series_to_watch = ['Castle','2 Broke Girls', '12 Monkeys', 'Bones', 'Criminal Minds',
                   'Gotham', 'Marvels Agent Carter', 'Marvels Agents of SHIELD',
                   'Once Upon A time', 'Scorpion', 'The Big Bang theory',
                   'The Flash (2014)', 'The Walking Dead', 'Glee']


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

#
# Search for this show and return the html page
#

def search_show(show):
    print(show)
    show = urllib.parse.quote_plus(show)
    url = base_url + '/search/?new=1&search='+show+'&s_cat=8'
    req = urllib.request.Request(url,headers=headers)
    response = urllib.request.urlopen(req)
    htmlpage = response.read()
    return htmlpage

#
# Extract the .torrent links we are interested in from the given
# html page
#

def extract_links(page):
    soup = BeautifulSoup(page)
    torrentrows = soup.find_all(class_=re.compile('tl[rz]'))
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
            print('Oops, no seeders or leechers found!')

    return links

def find_text(page,text_to_match):
    soup = BeautifulSoup(page)
    return text_to_match in soup.get_text()


def download_torrent(link,show):
    print(link)
    req = urllib.request.Request(link,headers=headers)
    response = urllib.request.urlopen(req)
    f = open(watched_dir+show+'.torrent', 'wb')
    torrent_file = response.read(1024)
    while torrent_file:
        f.write(torrent_file)
        torrent_file = response.read(1024)


def download_next_episode(show,current_episode):
    result_page = search_show(show+' S'+current_episode[0]+'E'+str(int(current_episode[1])+1))
    linklist = extract_links(result_page)
    print(linklist)
    linklist.sort(key=lambda t: t[1],reverse=True)
    print(find_text(result_page,'total 0 torrents found on your search query'))
    if not find_text(result_page,'total 0 torrents found on your search query'):
        link = linklist[0][0]
        download_torrent(link,show+' S'+current_episode[0]+'E'+str(int(current_episode[1])+1))
        next_episode = (current_episode[0],str(int(current_episode[1])+1))
        download_next_episode(show,next_episode)
    else:
        print('done!')


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

    # Get a list of the episodes we have for this show
    for x in series_to_watch:
        list_of_episodes = scan.list_current_episodes(x,library_root)
        last_episode = list_of_episodes.pop()

        episode_number = rename.match_season_episode(last_episode)
        print(episode_number)
        episode_number_tuple = rename.split_episode_number(episode_number)
        download_next_episode(x,episode_number_tuple)


if __name__ == "__main__":
    main()