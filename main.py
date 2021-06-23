from tkinter import *
from tkinter import messagebox
from PIL import ImageTk, Image
import threading
import pyqrcode
import os
import re
import webbrowser

tk = Tk()
tk.geometry("400x400")
tk.title("QR Kodu | 05.03.2021 - 20:05")
windowWidth = tk.winfo_reqwidth()
windowHeight = tk.winfo_reqheight()
positionRight = int(tk.winfo_screenwidth()/3 - windowWidth/2)
positionDown = int(tk.winfo_screenheight()/3 - windowHeight/2)
tk.geometry(f"400x400+{positionRight}+{positionDown}")
tk.resizable(width=False, height=False)

def callback(url):
    webbrowser.open_new(url)
me = Label(tk, text="Developer: yazilimfuryasi.com | @yazilimfuryasi", fg="#6E7371",cursor="hand2",font="Verdana 7 bold")
me.pack(side=BOTTOM)
me.bind("<Button-1>", lambda e: callback(webbrowser.open_new("https://www.instagram.com/yazilimfuryasi/")))

def threadPaste():
    threading.Thread(target=yapistir).start()

frame = Frame(tk)
frame.place(x=10,y=50)

label = Label(frame)
label.grid(row = 0, column = 0)

E1 = Entry(frame, width="63")
E1.grid(row=1, column=0)
btn = Button(frame, text="QR Kod Oluştur", cursor="hand2",command=threadPaste)
btn.grid(row=2, column=0)

label1 = Label(frame)
label1.grid(row = 3, column = 0)

m = Menu(tk, tearoff=0)
m.add_command(label="Yapıştır")


def do_popup(event):
    paste = tk.clipboard_get()
    E1["text"] = paste
    try:
        m.tk_popup(event.x_root, event.y_root)
        E1.insert(0 ,paste)
    finally:
        m.grab_release()
E1.bind("<Button-3>", do_popup)

def yapistir():
    desktop = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop//')
    url = pyqrcode.create(E1.get())

    qr = E1.get()
    # Dosya Adına, yazılan veri verileceği için Windows'un desteklemediği karakterleri replace ediyoruz.
    karakter = re.sub(r'[\\/\:*"<>\|\.%\$\?^&£]', '', qr)

    # Burası ezbere yapıldı. URL girilirse https gibi alanları atlaması için yapıldı.
    # Daha gelişmiş yapmak istiyorsanız https:// gibi alanlar aynı yöntemle silinebilir.
    if len(karakter) <= 10:
        yeni = karakter
    else:
        yeni = karakter[7:25]
    url.png(desktop+yeni+".png", scale=12)
    resim = desktop+yeni+".png"

    # Tk ekranına QR kodunu koyabilmek için bu alan zorunludur.
    im = Image.open(resim)
    im = im.resize((200,200), Image.ANTIALIAS)
    tkimage = ImageTk.PhotoImage(im)
    lresim = Label(frame,image=tkimage)
    lresim.image = tkimage
    lresim.grid(row=4, column=0)
    try:
        kayityolu = Label(frame, text="Masaüstüne Kayıt Edilmiştir.")
        kayityolu.grid(row=5,column=0)
    except Exception as e:
        kayityolu["text"] = "Kayıt Edilemedi."
        messagebox.showerror("Hata","Kayıt Edilemedi.")
tk.mainloop()