import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import spotifyscraper
import spotifydownloader
import threading

#Opens a search window to determine where to save the txt
def browse_destination_folder():
    destination_folder = filedialog.askdirectory()
    entry_destination.delete(0, tk.END)
    entry_destination.insert(0, destination_folder)

#Opens a search window to determine where to save the songs
def browse_destination_folder2():
    destination_folder2 = filedialog.askdirectory()
    entry_destination2.delete(0, tk.END)
    entry_destination2.insert(0, destination_folder2)

#Start spotifyscraper.py functions
def start_scraper():
    playlist_id = entry_playlist.get()
    destination_folder = entry_destination.get()

    if not playlist_id or not destination_folder:
        messagebox.showerror("Error", "Please enter playlist link and choose destination folder.")
        return
    #The functions themselves; 1-URI retriver, 2- Song and artist;
    spotifyscraper.get_playlist_track_uris(playlist_id, client_id, client_secret,destination_folder)
    spotifyscraper.convert_uri_to_track_info(client_id, client_secret,destination_folder)
    messagebox.showinfo("Done", "Playlist download finished!")

#Start spotifydownloader.py functions
def start_download():
    destination_folder = entry_destination.get() #Use this var. to fetch the txt file with the music data;
    destination_folder2 = entry_destination2.get() #Use this var. to define where to save the songs;
  
    if not destination_folder or not destination_folder2:
        messagebox.showerror("Error", "Please enter the location from the list and choose the destination folder.")
        return

    try:
        #The functions themselves; 1-Songs and artists, 2-YouTube links;
        songs_list = spotifydownloader.read_songs_from_file(destination_folder)
        links_dict = spotifydownloader.search_youtube_links(songs_list)
        print(songs_list)
        total_songs = len(links_dict)
        progress_label.config(text="Progress: 0/0 Songs (0.00%)")
        
        download_thread = threading.Thread(target=spotifydownloader.download_youtube_links,args=(links_dict, destination_folder2, update_progress_label, total_songs))
        download_thread.start()
        
    except Exception as e:
        messagebox.showerror("Erro", str(e))
        
    messagebox.showinfo("Download Done", "The playlist has been successfully downloaded.")
    
def update_progress_label(progress_text):
    progress_label.config(text=progress_text)
    
def on_entry_right_click(event):
    entry_playlist.event_generate("<<Paste>>")

def select_all(event):
    entry_playlist.select_range(0, tk.END)
    
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Spotify Playlist Downloader")

    # Replace these with your actual Spotify credentials
    client_id = "INSERT HERE YOUR CLIENT ID"
    client_secret = "INSERT HERE YOUR CLIENT SECRET"
    
    # Playlist Label and Entry
    label_playlist = tk.Label(root, text="Spotify Playlist link:")
    label_playlist.grid(row=1, column=0, padx=5, pady=5)

    entry_playlist = tk.Entry(root, width=50)
    entry_playlist.grid(row=1, column=1, padx=5, pady=5)
    
    # Bind right-click event to entry_playlist
    entry_playlist.bind("<Button-3>", on_entry_right_click)
    
    # Destination Label and Entry with Browse Button
    label_destination = tk.Label(root, text="Playlist file destination:")
    label_destination.grid(row=0, column=0, padx=5, pady=5)

    entry_destination = tk.Entry(root, width=50)
    entry_destination.grid(row=0, column=1, padx=5, pady=5)

    button_browse = tk.Button(root, text="Browse", command=browse_destination_folder)
    button_browse.grid(row=0, column=2, padx=5, pady=5)
    
    # Start Scraping
    button_start = tk.Button(root, text="Start Scraping", command=start_scraper)
    button_start.grid(row=1, column=2, padx=5, pady=5, rowspan=1)

    # Start Button
    button_start = tk.Button(root, text="Start Download", command=start_download)
    button_start.grid(row=4, column=2, padx=5, pady=5, rowspan=1)

    # Destination and Entry with Browse Button for music download
    label_destination = tk.Label(root, text="Download destination:")
    label_destination.grid(row=3, column=0, padx=5, pady=5)

    entry_destination2 = tk.Entry(root, width=50)
    entry_destination2.grid(row=3, column=1, padx=5, pady=5)

    button_browse = tk.Button(root, text="Browse", command=browse_destination_folder2)
    button_browse.grid(row=3, column=2, padx=5, pady=5)
    
    # Progress Label
    progress_label = tk.Label(root, text="Progress: 0/0 Songs (0.00%)")
    progress_label.grid(row=5, column=0, columnspan=3, padx=5, pady=5)
    
    root.mainloop()
