from youtubesearchpython import VideosSearch
import yt_dlp
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from threading import Thread
import os

def read_songs_from_file(destination_folder): # file path dos sons)
    with open(os.path.join(destination_folder, 'track_info.txt'), 'r') as file:
        lines = file.read()
    # Separates songs in a list based on the word "Track Name:"
    songs_list = lines.split("Track Name: ")[1:]
    
    # Extract song name and artist from each entry    formatted_songs = []
    for song in songs_list:
        song_lines = song.strip().split("\n")
        name = song_lines[0]
        artist_line = [line for line in song_lines if "Artists: " in line][0]
        artist = artist_line.replace("Artists: ", "")
        formatted_songs.append(f"{name} - {artist}")
    return formatted_songs

def search_youtube_links(songs_list):
    links_dict = {}
    for song in songs_list:
        search_query = f'{song} official audio'  # Adding 'official audio' to improve search accuracy
        search = VideosSearch(search_query, limit=1)
        results = search.result()
        if 'result' in results and len(results['result']) > 0:
            link = results['result'][0]['link']
            links_dict[song] = link
        else:
            print(f"Link not found for: {song}")
    return links_dict

def download_youtube_links(links_dict, destination, progress_callback, total_songs):
    progress = 0
    num_songs = len(links_dict)

    for song, link in links_dict.items():
        try:
            ydl_opts = {
                'outtmpl': f'{destination}/{song}.%(ext)s',
                'format': 'bestaudio/best',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '320',
                }],
            }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([link])

            progress += 1
            progress_percent = (progress / num_songs) * 100
            progress_text = f"Progresso: {progress}/{num_songs} músicas ({progress_percent:.2f}%)"
            progress_callback(progress_text)
        except Exception as e:
            print(f"An error occurred while downloading {song}: {e}")

def browse_folder():
    destination_folder = filedialog.askdirectory()
    entry_destination_folder.delete(0, tk.END)
    entry_destination_folder.insert(0, destination_folder)

def start_download():
    file_path = entry_file_path.get()
    destination_folder2 = entry_destination_folder.get()

    if not file_path or not destination_folder:
        messagebox.showerror("Error", "Please select text file and destination folder.")
        return

    songs_list = read_songs_from_file(file_path)
    links_dict = search_youtube_links(songs_list)

    #progress_label.config(text="Progresso: 0/0 músicas (0.00%)")

    #download_thread = Thread(target=download_youtube_links, args=(links_dict, destination_folder2, progress_label))
    #download_thread.start()
