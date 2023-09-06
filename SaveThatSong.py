#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import yt_dlp
from youtube_search import YoutubeSearch
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy
import json


urls = []
songs = []

ydl_opts = {
    'format': 'mp3/bestaudio/best',
    'postprocessors': [{  
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
    }]
}

class Downloader:
    
    def spotifyPlaylistInfoDownload(Playlist):
        sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())
        
        PID = Playlist.rsplit('/', 1)[1]
        playlist_id = 'spotify:user:spotifycharts:playlist:' + PID
        results = sp.playlist(playlist_id)
        
        totalTracks = results['tracks']['total']
        
        for i in range(totalTracks):
            artistName = results['tracks']['items'][i]['track']['artists'][0]['name']
            trackName = results['tracks']['items'][i]['track']['name']

            searchQuery = trackName + ' ' + artistName + ' lyrics'
            songs.append(searchQuery)
        
        for song in songs:
            Downloader.urlFinder(song)


    def urlFinder(song):
        print('Looking for song: ', song, 'on YouTube')
        try:
            results = YoutubeSearch(song, max_results=1).to_json()
            data = json.loads(results)
            for v in data['videos']:
                videoID = v['id']
                baseUrl = 'https://www.youtube.com/watch?v='
                videoURL = baseUrl + videoID
                urls.append(videoURL)
        except:
            print('Could not find the song: ', song)
            
            
    def downloadSong(link):
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            try:
                ydl.download(link)
            except:
                print('Could not download: ', link)
                
                
    def downloadFromLinks(urls):
        for url in urls:
            print("Downloading song " + str(urls.index(url) + 1) + "/" + str(len(urls)) + "...")
            Downloader.downloadSong(url)




print('''
        #######################################################################################
        ##################  SPOTIFY/Youtube DOWNLOADER  ####################################
       ---------------------------------------------------------------------------------------
          This script lets you download songs from Spotify or Youtube for free using yt-dlp
       ---------------------------------------------------------------------------------------
        ##################  SPOTIFY/Youtube DOWNLOADER  ######################################
        #######################################################################################
Menu:
1. Download songs from a Spotify playlist.
2. Download songs from a YouTube playlist.
3. Download songs from a list of songs.
4. Download a single song (search).
5. Download a single song (link).
6. Help
      ''')

choice = input("Enter your choice: ")

match choice:
    case "1":
        playlist = input('Enter playlist: ')
        Downloader.spotifyPlaylistInfoDownload(playlist)
        Downloader.downloadFromLinks(urls)
        
    case "2":
        playlist = input('Enter playlist: ')
        Downloader.downloadSong(playlist)
        
    case "3":
        userlist = input('Enter the name of the file (with the extension): ')
        with open(userlist, 'r') as file:
            listOfSongs = file.readlines()
            for song in listOfSongs:
                Downloader.urlFinder(song)
            Downloader.downloadFromLinks(urls)
        
    case "4":
        song = input('Enter song: ')
        Downloader.urlFinder(song)
        Downloader.downloadFromLinks(urls)
        
    case "5":
        link = input('Enter Link: ')
        Downloader.downloadSong(link)
        
    case _:
        print("Invalid input. Try again")
        
        
        
        
        
        
        
        
        
        
        
        

