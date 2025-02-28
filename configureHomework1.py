import tkinter as tk
from tkinter import scrolledtext
from zipfile import ZipFile
import configparser

config = configparser.ConfigParser()
config.read('emu.ini')

username = config.get('Settings', 'username')
vfs_path = config.get('Settings', 'vfs_path')


current = "\n" + username +":~> "

def ls():
    with ZipFile('files.zip', 'a') as myzip:
        if current == "\n" +username +":~> ":
            for name in myzip.namelist():
                scroll_text.config(state=tk.NORMAL)  
                scroll_text.insert(tk.END,"\n"+ name ) 
                scroll_text.config(state=tk.DISABLED)
                
        else:
            for name in myzip.namelist():
                if name.find(current[len(username)+3:-2]):
                    scroll_text.config(state=tk.NORMAL)
                    if(name.rfind(current[len(username)+3:-2])!=-1):
                        scroll_text.insert(tk.END, "\n"+name[name.rfind(current[len(username)+3:-2]):]) 
                    scroll_text.config(state=tk.DISABLED)
    scroll_text.config(state=tk.NORMAL)  
    scroll_text.insert(tk.END, current) 
    scroll_text.config(state=tk.DISABLED)
def Exit():
    window.destroy();
    exit();
def cat(text):
    path = text.split()[1]
    with ZipFile('files.zip', 'a') as myzip:
        try:
            if current != "\n" + username +":~> ":
                path = current[len(username+ ":~"):-2]+"/"+path
            content = myzip.read("files/"+path).decode()
        except KeyError:
            content = f"Файл 'files/{path}' не найден"
    scroll_text.config(state=tk.NORMAL)  
    scroll_text.insert(tk.END, "\n"+content+current) 
    scroll_text.config(state=tk.DISABLED)
def echo(text):
    text = text[5:]
    scroll_text.config(state=tk.NORMAL)  
    scroll_text.insert(tk.END, "\n"+text+current) 
    scroll_text.config(state=tk.DISABLED)
def clear():
    scroll_text.config(state=tk.NORMAL)  
    scroll_text.delete(1.0,tk.END)
    scroll_text.insert(tk.END, current[1:]) 
    scroll_text.config(state=tk.DISABLED)
def pwd():
    scroll_text.config(state=tk.NORMAL)
    scroll_text.insert(tk.END, "C:\\Users" + path)
    scroll_text.config(state=tk.DISABLED)
def cd(text):
    path = text.split()
    global current
    if(len(path)>1):
        path = path[1]
        current = "\n"+username+ ":~" + path +"> "
        scroll_text.config(state=tk.NORMAL)  
        scroll_text.insert(tk.END, current) 
        scroll_text.config(state=tk.DISABLED)
    else:
        current = "\n"+username +":~> "
        scroll_text.config(state=tk.NORMAL)  
        scroll_text.insert(tk.END, current) 
        scroll_text.config(state=tk.DISABLED)
def add_text(event=None):
    text = entry.get()
    if text:
        scroll_text.config(state=tk.NORMAL)  
        scroll_text.insert(tk.END, text) 
        scroll_text.config(state=tk.DISABLED)
        entry.delete(0, tk.END)
    if text == 'ls':
        ls()
    elif text == 'exit':
        Exit()
    elif text.startswith('cat '):
        cat(text)
    elif text.startswith('echo'):
        echo(text)
    elif text == "pwd":
        pwd()
    elif text == "clear":
        clear()

    elif text.startswith('cd'):
        cd(text)
    else:
        scroll_text.config(state=tk.NORMAL)  
        scroll_text.insert(tk.END, "\n"+current) 
        scroll_text.config(state=tk.DISABLED)
        


window = tk.Tk('750x350')
window.title("Эмулятор")


scroll_text = scrolledtext.ScrolledText(window, wrap=tk.WORD, width=80, height=30, state=tk.DISABLED)
scroll_text.pack(pady=10)
scroll_text.config(state=tk.NORMAL)  
scroll_text.insert(tk.END, "Путь к файловой системе: " + vfs_path+"\n"+ username +":~> ") 
scroll_text.config(state=tk.DISABLED)
            
entry = tk.Entry(window, width=80)
entry.pack(pady=5)

entry.bind('<Return>', add_text)

window.mainloop()




