import threading
import time
import tkinter
import enums
import Betterfy
import customtkinter as ctk
from technical import check_resource, create_resource, song, update_token


# general settings
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("green")

# app frame
app = ctk.CTk()
app.geometry("720x480")
app.title("Betterfy")
app.iconbitmap('spotify_black_logo_icon_147079.ico')


def run():
    button.destroy()
    token = Betterfy.authenticate()
    title.configure(text=f"Welcome: \n{Betterfy.get_profile(token)["display_name"]}")
    current.pack(padx=20, pady=50)
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
progressbar = ctk.CTkProgressBar(app, orientation="horizontal", progress_color="green")
current = ctk.CTkLabel(app, textvariable=name)
device_label = ctk.CTkLabel(app, textvariable=device)



def main():
    if not check_resource():
        app.mainloop()
    else:
        enums.token = Betterfy.authenticate()
        scope_box.destroy()
        entry_ID.destroy()
        button.destroy()
        title.configure(text=f"Welcome: \n{Betterfy.get_profile(enums.token)["display_name"]}", pady=100)
        current.pack(padx=20, pady=5)
        progressbar.pack()
        device_label.pack(pady=50)
        next.pack()
        t1 = threading.Thread(target=track)
        t2 = threading.Thread(target=update_token)
        t1.start()
        t2.start()
        for thread in threading.enumerate():
            print(thread.name)
        app.mainloop()



def track():
    while True:
        token = enums.token
        progressbar.set(Betterfy.get_progress(token))
        track = Betterfy.current_track(token)
        name.set(f"Currently playing: \n{track["item"]["name"]} | {track["item"]["artists"][0]["name"]}")
        device.set(f"On device: \n{track["device"]["name"]}")
        time.sleep(0.1)



if __name__ == '__main__':
    main()
