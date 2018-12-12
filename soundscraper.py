from __future__ import unicode_literals
from selenium import webdriver
import requests
import bs4
import re
import os
import youtube_dl

artist_url = "http://soundcloud.com/search/people?q="
track_url = "http://soundcloud.com/search/sounds?q="

browser = webdriver.Chrome("/usr/bin/chromedriver")
browser.get("https://soundcloud.com")

print()
print(">>> Search for track or artist<<<")
print()


print(">>> Menu")
print(">>> 1 - Search for an artist")
print(">>> 0 - exit")
print()

choice = int(input(">>> Your choice: "))

if choice == 0:
    browser.quit()
    quit()
print()

# if choice == 1:
#     name = input(">>> Track name: ")
#     print()
#     "%20".join(name.split(" "))
#     browser.get(track_url + name)


if choice == 1:
    name = input(">>> Artist name:  ")
    print()
    "%20".join(name.split(" "))
    browser.get(artist_url + name)
    url = artist_url + name
    request = requests.get(url)
    soup = bs4.BeautifulSoup(request.text, "lxml")
    # print(request.text)
    artists = soup.select("a[href/]")[6:-7]
    artist_links = []
    for index, artist in enumerate(artists):
        print(str(index) + ": " + artist.text)
        artist_links.append(artist.get("href"))

    print()
    choice = input(">>> Your choice (x to go back): ")

    print()

    if choice == "x":
        quit()
    else:
        choice = int(choice)
    url = "http://soundcloud.com" + artist_links[choice]
    request = requests.get(url)
    soup = bs4.BeautifulSoup(request.text, "lxml")
    # print(request.text)
    tracks = soup.find_all("h2")[1:]
    track_links = []
    track_names = []
    for index, track in enumerate(tracks):
        track_links.append(track.find("a", href=re.compile(r'[/]([a-z]|[A-Z])\w+')).attrs['href'])
        track_names.append(track.text)
        print(str(index + 1) + ": " + track.text)
        print()

    choice = int(input(">>> Your choice (x to exit): "))
    print()

    if choice == "x":
        quit()

    print("Now playing: " + track_names[choice])
    print()
    base_url = "http://soundcloud.com"
    song_url = track_links[choice]
    browser.get("http://soundcloud.com" + track_links[choice])

    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '320',
    }]

    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([base_url + song_url])




print()
print("Goodbye")
print()

