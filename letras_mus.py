#!/usr/bin/env python
#-*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup


def get_track_list(artist_url):
    r = requests.get("https://www.letras.mus.br/%s" % artist_url)
    soup = BeautifulSoup(r.text, 'html.parser')
    li_tracks = soup.find("div", {"id": "cnt-artist-songlist"}).findAll("li")
    return [{"name": track.text,
             "url": track.find("a").attrs["href"]} for track in li_tracks]


def get_lyrics(mus_url):
    r = requests.get("https://www.letras.mus.br%s" % mus_url)
    soup = BeautifulSoup(r.text, 'html.parser')
    lyrics = soup.find("div", {"class": "cnt-letra"})
    map(lambda br: br.replaceWith("\n"), lyrics.findAll("br"))

    return u"\n\n".join([p.text for p in lyrics.findAll("p")])


def get_lyrics_list(url_list, pool_size=8):
    from multiprocessing import Pool

    pool = Pool(pool_size)
    return pool.map(get_lyrics, url_list)


def pretty_print(mus_name, lyrics):
    print "\33[1m" + mus_name.strip().upper()
    print "\33[0m"
    print lyric
    print
    print


if __name__ == "__main__":
    import sys

    if len(sys.argv) != 2:
        sys.stderr.write("usage:\n\t%s <artist-url>\n" % sys.argv[0])
        sys.stderr.write("example:\n\t%s mc-anitta\n" % sys.argv[0])
        sys.exit(1)

    reload(sys)
    sys.setdefaultencoding('utf-8')
    track_list = get_track_list(sys.argv[1])
    lyrics = get_lyrics_list([track["url"] for track in track_list])
    for i, lyric in enumerate(lyrics):
        pretty_print(track_list[i]["name"], lyric)
