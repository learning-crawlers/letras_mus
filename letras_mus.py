#!/usr/bin/env python
#-*- coding: utf-8 -*-

import requests
from sys import argv
from bs4 import BeautifulSoup
import sys


def get_track_list(artist_url):
    r = requests.get("https://www.letras.mus.br/%s" % artist_url)
    soup = BeautifulSoup(r.text, 'html.parser')
    return [{"name": track.text, 
             "url": track.find("a").attrs["href"]}  
                for track in soup.findAll("li", {"itemprop":"tracks"})]

def get_lyrics(mus_url):
    r = requests.get("https://www.letras.mus.br%s" % mus_url)
    soup = BeautifulSoup(r.text, 'html.parser')    
    lyrics = soup.find("div", {"class": "cnt-letra"})
    
    return u"\n".join([p.text for p in lyrics.findAll("p")])
    
def get_lyrics_list(url_list, pool_size=8):
    from multiprocessing import Pool
    
    pool = Pool(pool_size)
    return pool.map(get_lyrics, url_list)

def pretty_print(mus_name, lyrics):
    import re
    print mus_name.upper()
    print re.sub(r"[A-Z]", lambda m: m.expand("\n\g<0>"), lyric)
    print "="*80
    print

if __name__ == "__main__":
    reload(sys)
    sys.setdefaultencoding('utf-8')
    track_list = get_track_list(argv[1])
    lyrics = get_lyrics_list([track["url"] for track in track_list])
    for i, lyric in enumerate(lyrics):
        pretty_print(track_list[i]["name"], lyric)

        
        
