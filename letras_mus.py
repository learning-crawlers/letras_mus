#!/usr/bin/env python
#-*- coding: utf-8 -*-

import requests
from sys import argv
from bs4 import BeautifulSoup
import sys


def get_mus_list(artist_url):
    r = requests.get("https://www.letras.mus.br/%s" % artist_url)
    
    soup = BeautifulSoup(r.text, 'html.parser')

    return [(track.text, 
             track.find("a").attrs["href"])  
                for track in soup.findAll("li", {"itemprop":"tracks"})]

def get_lyrics(mus_url):
    r = requests.get("https://www.letras.mus.br%s" % mus_url)
    soup = BeautifulSoup(r.text, 'html.parser')    
    lyrics = soup.find("div", {"class": "cnt-letra"})
    
    return u"\n".join([p.text for p in lyrics.findAll("p")])
    
    
if __name__ == "__main__":
    reload(sys)
    sys.setdefaultencoding('utf-8')
    for mus in get_mus_list(argv[1]):
        print mus[0].upper()
        print get_lyrics(mus[1])
        print "==============================================================================================="
        print
