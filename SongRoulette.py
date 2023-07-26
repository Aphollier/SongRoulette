import pathlib
import tkinter as tk
from functools import partial
from PIL import ImageTk, Image
import random
from time import perf_counter_ns

songs = {}
selectedSongs = {}
width = 1280

path = str(pathlib.Path(__file__).parent.resolve()) + "\\Assets\\"
window = tk.Tk()
window.geometry("1280x720")
window.config(bg = '#00ff00')
window.wm_attributes('-transparentcolor','#00ff00')
frame = tk.Frame(window, bg='#00ff00')
frame.pack(side="top", expand=True, fill="both")

def main():
    with open("Assets\\SongList.txt", "r", encoding="utf-8") as f:
        line = f.readline()
        while line:
            fixedLine = str(line)
            splitLine = fixedLine.strip().split("|")
            img = Image.open(path + splitLine[1])
            songs[splitLine[0]] = [ImageTk.PhotoImage(img.resize((100,100), Image.LANCZOS)), ImageTk.PhotoImage(img.resize((300,300), Image.LANCZOS))]
            line = f.readline()

    selectionScreen()

def songSelect(button, song):
    if selectedSongs[song]:
        selectedSongs[song] = False
        button.config(bg="red")
    else:
        selectedSongs[song] = True
        button.config(bg="#1f1c31")

def clear_frame():
    for widgets in frame.winfo_children():
        widgets.destroy()

def wait(delay):
    target = perf_counter_ns() + delay
    while perf_counter_ns() < target:
        pass

def selectionScreen():
    clear_frame()
    for count, (song, img) in enumerate(songs.items()):
        selectedSongs[song] = True
        albumButton = tk.Button(frame, image=img[0], bg="#1f1c31", activebackground="#1f1c31", relief=tk.FLAT)
        albumButton.config(command=partial(songSelect, albumButton, song))
        albumButton.image = img[0]
        songName = tk.Label(frame, text=song, justify=tk.CENTER, wraplength=100, bg="#1f1c31", width=16)
        songName.config(font=("Impact", 10), fg="#ffffff")
        albumButton.place(x=50 + (count % 10 * 120), y=50 + (int(count/10) * 200))
        songName.place(x=50 + (count % 10 * 120), y=155 + (int(count/10) * 200))  

        spinButton = tk.Button(frame, text="SPIN!", font=("Impact", 30), fg="#ffffff", 
                               activeforeground="#ffffff", bg="#3a345c", activebackground="#6c62a6", 
                               relief=tk.FLAT, width=10, height=1, command=spinScreen)
        spinButton.place(relx=0.5, rely=0.9, anchor=tk.CENTER)

def spinScreen():
    clear_frame()
    randomizedSongs = []
    albums = {}
    canvas = tk.Canvas(frame, bg="#00ff00")
    canvas.pack(fill="both", expand=True)
    img = Image.open(path + "pointer.png")
    img = img.rotate(-90)
    pointer = ImageTk.PhotoImage(img)
    window.pointer = pointer
    canvas.create_image(int(width/2), 100, image=pointer)

    for (song, enabled) in selectedSongs.items():
        if enabled:
            randomizedSongs.append(song)

    if len(randomizedSongs) == 0:
        selectionScreen()
        return

    random.shuffle(randomizedSongs)
    while len(randomizedSongs) < 6:
        added = []
        for song in randomizedSongs:
            added.append(song)
        randomizedSongs.extend(added)

    for count, song in enumerate(randomizedSongs):
        albums[canvas.create_image((count * 300), 300, image=songs[song][1])] = song

    songName = tk.Label(frame, text=albums[canvas.find_closest(int(width/2), 300)[0]], justify=tk.CENTER, bg="#1f1c31", width=80)
    songName.config(font=("Impact", 25), fg="#ffffff")
    songName.place(x=0, y=450)
    window.update()

    speed = -15000
    while speed < 0:
        for (album, song) in albums.items():
            canvas.move(album, speed/1000, 0)
            if canvas.coords(album)[0] < -150:
                canvas.move(album, len(albums) * 300, 0)

        songName.config(text=albums[canvas.find_closest(int(width/2), 300)[0]])
        window.update()
        if speed < -5000:
            speed += -speed / 1000 + 1
        elif speed < -1000:
            speed += -speed / 5000 + 0.7
        else:
            speed += -speed / 10000 + 0.1
        wait(1)

    songName.config(relief=tk.RIDGE)
    selectButton = tk.Button(frame, text="SELECT AGAIN!", font=("Impact", 30), fg="#ffffff", 
                               activeforeground="#ffffff", bg="#3a345c", activebackground="#6c62a6", 
                               relief=tk.FLAT, width=15, height=1, command=selectionScreen)
    selectButton.place(relx=0.5, rely=0.9, anchor=tk.CENTER)

if __name__ == "__main__":
    main()

window.mainloop()