import tkinter as tk
from tkinter import filedialog
import customtkinter as ctk
from pytube import YouTube
import os
import time

def open_path():
    root = tk.Tk()
    root.withdraw()
    filepath = filedialog.askdirectory()
    root.destroy()
    return filepath

def start_download():
    try:
        ytlink = link.get()
        res_choice = res.get()
        audio_only = Audio_checkbox.get()

        ytobject = YouTube(ytlink, on_progress_callback=on_progress)

        if audio_only:
            stream = ytobject.streams.get_audio_only()
            extension = "mp3"
        else:
            stream = ytobject.streams.get_highest_resolution()
            extension = "mp4"

        destination = open_path()
        if destination:
            filename = f"{ytobject.title}.{extension}"
            filepath = os.path.join(destination, filename)

            # Retry logic
            retries = 3
            for i in range(retries):
                try:
                    stream.download(output_path=destination, filename=filename)
                    finishlabel.configure(text=f"{ytobject.title} has been successfully downloaded to {destination}.")
                    break
                except Exception as e:
                    print(f"Download failed. Retrying attempt {i + 1}/{retries}")
                    time.sleep(3)  # Wait for 3 seconds before retrying
            else:
                raise Exception("Download failed after multiple retries. Please check your network connection.")
        else:
            finishlabel.configure(text="Download canceled.")
    except Exception as e:
        finishlabel.configure(text=f"Error: {str(e)}", text_color="red")

def on_progress(stream, chunk, bytes_remaining):
    total_size = stream.filesize
    bytes_downloaded = total_size - bytes_remaining
    percentage_of_completion = bytes_downloaded / total_size * 100
    per = str(int(percentage_of_completion))
    Percentage.configure(text=per + '%')
    Percentage.update()

    progressbar.set(float(percentage_of_completion) / 100)

# System settings 
ctk.set_appearance_mode("dark")  # Modes: system (default), light, dark
ctk.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green

# App frame
app = ctk.CTk()  # create CTk window like you do with the Tk window
app.geometry("820x400")
app.title("Youtube Downloader")

# Adding UI Elements
title = ctk.CTkLabel(app, text="Insert a YouTube link")
title.pack(padx=10, pady=10) 

# Link input 
link = ctk.CTkEntry(app, width=350, height=40)
link.pack(pady=12)

# Adding UI Elements
finishlabel = ctk.CTkLabel(app, text="")
finishlabel.pack(padx=10, pady=25)

# Resolution selection combobox
res = ctk.CTkComboBox(app, values=["Max Resolution", "1080p", "720p", "480p", "360p", "240p", "144p"])
res.place(relx=0.252, rely=0.6)

# Download Button
button = ctk.CTkButton(app, text="Download", command=start_download)
button.place(relx=0.5, rely=0.31, anchor='center')

# Audio only switch 
Audio_checkbox = ctk.CTkCheckBox(app, text="Audio only")
Audio_checkbox.place(relx=0.45, rely=0.6)

# Progress Bar 
Percentage = ctk.CTkLabel(app, text='0%')
Percentage.place(relx=0.78, rely=0.5, anchor='center')

progressbar = ctk.CTkProgressBar(app, width=400, progress_color='green')
progressbar.set(0)
progressbar.place(relx=0.74, rely=0.5, anchor='e')

# Run app
app.mainloop()
