import urllib.request
import urllib.parse
import re
from bs4 import BeautifulSoup
from os import makedirs

import scan, rename_file


base_url = 'http://www.extratorrent.cc/'

user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
headers = {'User-Agent': user_agent}
library_root = 'Z:\Series\\'
watched_dir = 'E:\Watched\\'

series_to_watch = ['Castle','2 Broke Girls', '12 Monkeys', 'Bones', 'Criminal Minds',
                   'Gotham', 'Marvels Agent Carter', 'Marvels Agents of SHIELD', 'Scorpion', 'The Big Bang theory',
                   'Game of Thrones', 'The Walking Dead', 'Glee', 'Penny Dreadful','Mr Robot']

#series_to_watch = ['Mr. Robot']
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
# Returns a tuple (link, seeders, leechers)
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

#
# Creates 3 lists respectively for 1080p, 720p and 'other'
#

def split_link_list(linklist):
    linklist1080p = []
    linklist720p = []
    linklistOther = []
    for item in linklist:
        if '1080p' in item[0]:
            linklist1080p.append(item)
        elif '720p' in item[0]:
            linklist720p.append(item)
        else:
            linklistOther.append(item)

    return (linklist1080p,linklist720p,linklistOther)

def download_next_episode(show,current_episode):

    episode_number_int = int(current_episode[1])+1
    episode_number = "%02d" % episode_number_int

    season_number_int = int(current_episode[0])
    season_number = "%02d" % season_number_int

    result_page = search_show(show+' S'+ season_number +'E'+ episode_number)

    linklist = extract_links(result_page)
    #print(linklist)


    linklist.sort(key=lambda t: t[1],reverse=True)
    #Search for next episode in this season
    if not find_text(result_page,'total 0 torrents found on your search query') and not linklist == []:
        quality_lists = split_link_list(linklist)

        if not quality_lists[1] == []:
            quality_lists[1].sort(key=lambda t: t[1],reverse=True)
            link = quality_lists[1][0][0]
        else:
            quality_lists[1].sort(key=lambda t: t[1],reverse=True)
            link = quality_lists[2][0][0]
        download_torrent(link,show+' S'+current_episode[0]+'E'+str(int(current_episode[1])+1))
        next_episode = (current_episode[0],str(int(current_episode[1])+1))
        download_next_episode(show,next_episode)
    else:
        print('done!')


def main():

    # Get a list of the episodes we have for this show
    for x in series_to_watch:
        try:
            list_of_episodes = scan.list_current_episodes(x,library_root)
            last_episode = list_of_episodes.pop()
            print('last episode found:' + last_episode)
            episode_number = rename_file.match_season_episode(last_episode)
            episode_number_tuple = rename_file.split_episode_number(episode_number)
            download_next_episode(x,episode_number_tuple)

        except FileNotFoundError:
            # File doesn't exist so we create the directory
            makedirs(library_root+x)
            # Download starting from season one, episode one.
            download_next_episode(x,("1","0"))

        #Try next season
        download_next_episode(x,(str(int(episode_number_tuple[0])+1),"0"))


if __name__ == "__main__":
    main()