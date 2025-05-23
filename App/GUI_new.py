r"""Creates Betterfy's UI"""
#  Copyright (c) 2025.

import threading
import time
import tkinter
import enums
import customtkinter as ctk
from BetterfyFunc import BetterfyFunc as Betterfy
from technical import check_resource, create_resource, song, update_token, volume, random_shuffle_queue
from BetterfyFunc.urlimage import CTkUrlLabel, url_to_color

# general settings
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("green")

# app frame
app = ctk.CTk()
app.geometry("720x480")
app.title("Betterfy")
#app.iconbitmap('spotify_black_logo_icon_147079.ico')


def run():
    button.destroy()
    token = Betterfy.authenticate()
    title.configure(text=f"Welcome: \n{Betterfy.get_profile(token)["display_name"]}")
    current.pack(padx=20, pady=50)
    slider.pack(pady=20)
    t1 = threading.Thread(target=track)
    t2 = threading.Thread(target=update_token)
    t1.start()
    t2.start()


def create():
    create_resource(entry_ID.get(), scope_box.get(0, 10))
    title.configure(text="Resource file created successfully.")
    scope_box.destroy()
    entry_ID.destroy()
    button.configure(text="Run Application", command=run)


def song_button(value):
    song(value)
    next.set(value="None")


def shuffle():
    random_shuffle_queue()


# adding UI
title = ctk.CTkLabel(app, text="Resource file not found! \n Please give your credentials")
title.pack(padx=10, pady=10)
entry_ID = ctk.CTkEntry(textvariable=enums.id_gui, width=200, master=app, placeholder_text="App ID")
entry_Scope = ctk.CTkEntry(textvariable=enums.scope_gui, width=200, master=app, placeholder_text="Scope")
entry_ID.pack(padx=10, pady=10)
scope_box = tkinter.Listbox(app, setgrid=True, foreground="white", background="#222222", selectbackground="green", width=100, selectmode = "multiple", activestyle="none", relief="sunken", justify="center")
scope_box.pack(padx=10, pady=10, expand = False, fill = "both")
x = ["ugc-image-upload", "user-read-private", "user-read-email", "user-read-playback-state", "user-modify-playback-state",
     "user-library-modify", "user-library-read", "user-top-read", "playlist-modify-public", "playlist-modify-private",
     "user-follow-modify"]

for each_item in range(len(x)):
    scope_box.insert("end", x[each_item])
    scope_box.itemconfig(each_item)

button = ctk.CTkButton(app, text="Submit", command=create)
button.pack(padx=10, pady=50)
next = ctk.CTkSegmentedButton(app, values=["<", "||", "|>", ">"], command=song_button)
name = ctk.StringVar(value=None)
device = ctk.StringVar(value=None)
shuffle = ctk.CTkButton(app, text="sf", command=shuffle)
progressbar = ctk.CTkProgressBar(app, orientation="horizontal", progress_color="green")
current = ctk.CTkLabel(app, textvariable=name)
device_label = ctk.CTkLabel(app, textvariable=device)
slider = ctk.CTkSlider(app, from_=0, to=100, command=volume)
slider.set(output_value=100)
image_label = CTkUrlLabel(app, compound="center", text="", url="", url_image_size=(200, 200))



def main():
    if not check_resource():
        app.mainloop()
    else:
        enums.token = Betterfy.authenticate()
        scope_box.destroy()
        entry_ID.destroy()
        button.destroy()
        title.configure(text=f"Welcome: \n{Betterfy.get_profile(enums.token)["display_name"]}", pady=100)
        image_label.pack()
        current.pack(padx=20, pady=5)
        progressbar.pack()
        device_label.pack(pady=50)
        next.pack()
        shuffle.pack()
        slider.pack(pady=20)
        t1 = threading.Thread(target=track)
        t2 = threading.Thread(target=update_token)
        t1.start()
        t2.start()
        app.mainloop()


def track():
    img_old = ""
    track_old = None
    while True:
        token = enums.token
        progressbar.set(Betterfy.get_progress(token))
        track = Betterfy.current_track(token)
        img = track["item"]["album"]["images"][0]["url"]
        if track != track_old:
            name.set(f"{track["item"]["name"]} | {track["item"]["artists"][0]["name"]}")
            device.set(f"On device: \n{track["device"]["name"]}")
        if img != img_old:
            color = url_to_color(img)
            image_label.configure(url=img)
            app.configure(fg_color=color, require_redraw=True)
            img_old = img
        time.sleep(0.1)



if __name__ == '__main__':
    main()
