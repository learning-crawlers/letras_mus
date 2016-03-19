#!/usr/bin/env python
#-*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup


def get_track_list(artist_url):
    r = requests.get("https://www.letras.mus.br/%s" % artist_url)
    soup = BeautifulSoup(r.text, 'html.parser')
    if soup.find("div", {"id": "cnt-artist-songlist"}):
        li_tracks = soup.find("div", {"id": "cnt-artist-songlist"}).findAll("li")
    else:
        li_tracks = li_tracks = soup.findAll("li", {"itemprop": "tracks"})
    
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


def string_compare(a, b):
    a, b = a.lower(), b.lower()
    return a in b or b in a


if __name__ == "__main__":
    import sys
    reload(sys)
    sys.setdefaultencoding('utf-8')

    if len(sys.argv) not in [2, 3]:
        sys.stderr.write("usage:\n\t%s <artist-url> [music name]\n\n" % sys.argv[0])
        sys.stderr.write("examples:\n\t%s mc-anitta\n" % sys.argv[0])
        sys.stderr.write("\t%s jimi-hendrix 'spanish castle magic'\n" % sys.argv[0])
        sys.stderr.write("\t%s jimi-hendrix purple\n" % sys.argv[0])
        sys.exit(1)

    if len(sys.argv) == 2:
        track_list = get_track_list(sys.argv[1])

    if len(sys.argv) == 3:
        track_list = get_track_list(sys.argv[1])
        track_list = filter(lambda track: string_compare(sys.argv[2], track["name"]), track_list)

    lyrics = get_lyrics_list([track["url"] for track in track_list])
    for i, lyric in enumerate(lyrics):
        pretty_print(track_list[i]["name"], lyric)

    
