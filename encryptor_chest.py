#!/usr/bin/env python
import os
import sys
import threading
import ctypes
import win32con, win32api

import pyperclip
import pyAesCrypt
from tkinter import *
import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext


FILE_ATTRIBUTE_HIDDEN = 0x02
FILE_ATTRIBUTE_DIRECTORY = 0x10


class MainWindow(tk.Frame):
    def __init__(self, root):
        super().__init__(root)
        self.init_main()

    def init_main(self):
        self.img_cache = []
        self.thread_count = 0
        self.path_error = False
        lb_dir = Label(text=u"Директория шифрования", font="Alef 10", fg="#9dff00", bg="#1a1a1a")
        lb_dir.pack()
        self.ent_value_dir = Entry(width=40, font="Alef 10", fg="#9dff00", bg="#1a1a1a")
        self.ent_value_dir.place(x=50, y=20)
        self.ent_value_dir.pack()
        lb_pass = Label(text=u"Пароль", font="Alef 10", fg="#9dff00", bg="#1a1a1a")
        lb_pass.pack()
        ent_value_pass = Entry(width=40, font="Alef 10", fg="#9dff00", bg="#1a1a1a", show="*")
        ent_value_pass.pack()
        crypt_img = PhotoImage(file='1.png')
        self.img_cache.append(crypt_img)
        btn_crypt = tk.Button(text='  CRYPT', fg="#9dff00", bg="#1a1a1a", width=80, image=self.img_cache[0], compound='left', command=lambda: self.crypting(self.ent_value_dir.get(), ent_value_pass.get()))
        btn_crypt.place(x=10, y=24)
        decrypt_img = PhotoImage(file='2.png')
        self.img_cache.append(decrypt_img)
        btn_decrypt = tk.Button(text='  DECRT', fg="#9dff00", bg="#1a1a1a", width=80, image=self.img_cache[1], compound='left', command=lambda: self.decrypting(self.ent_value_dir.get(), ent_value_pass.get()))
        btn_decrypt.place(x=10, y=60)
        paste_img = PhotoImage(file='3.png')
        self.img_cache.append(paste_img)
        btn_stop = tk.Button(text='  PASTE', fg="#9dff00", bg="#1a1a1a", width=80, image=self.img_cache[2], compound='left', command=lambda: self.paste_dir_to_entry())
        btn_stop.place(x=462, y=23)
        stop_img = PhotoImage(file='4.png')
        self.img_cache.append(stop_img)
        btn_stop = tk.Button(text='  STOP', fg="#9dff00", bg="#1a1a1a", width=80, image=self.img_cache[3], compound='left', command=lambda: self.close_crypter())
        btn_stop.place(x=462, y=60)
        self.console = scrolledtext.ScrolledText(fg="#9dff00", bg="#1a1a1a", bd=3, state='disable', font="Alef 9")
        self.console.pack(pady=20)

    def close_crypter(self):
        sys.exit()

    def insert_to_console(self, text):
        self.console.configure(state='normal')  # enable insert
        self.console.insert(END, text)
        self.console.yview(END)  # autoscroll
        self.console.configure(state='disabled')

    def paste_dir_to_entry(self):
        self.ent_value_dir.insert(tk.END, pyperclip.paste())

    def crypt_file(self, file, password):
        bufferSize = 512 * 1024
        try:
            pyAesCrypt.encryptFile(str(file), str(file) + ".Dead__Man'$__Che$t",
                                   password, bufferSize)
            self.insert_to_console('file was encrypt $ ' + str(file) + ".Dead__Man'$__Che$t" + '\n')
            os.remove(file)
            hidden_f = win32api.SetFileAttributes(str(file) + ".Dead__Man'$__Che$t", win32con.FILE_ATTRIBUTE_HIDDEN)
        except Exception as e:
            pass

    def crypt_disks_win(self, dir, password):
        try:
            for file in os.listdir(dir):
                if os.path.isdir(dir + '\\' + file):
                    self.crypt_disk(dir + '\\' + file, password)
                if os.path.isfile(dir + '\\' + file):
                    try:
                        self.crypt_file(dir + '\\' + file, password)
                    except Exception as ex:
                        self.insert_to_console(ex)
                        pass
        except OSError:
            self.path_error = True
            return
         
    def crypt_disk(self, dir, password):
        hidden_dir = ctypes.windll.kernel32.SetFileAttributesW(dir, FILE_ATTRIBUTE_HIDDEN)
        try:
            for file in os.listdir(dir):
                if os.path.isdir(dir + '/' + file):
                    self.crypt_disk(dir + '/' + file, password)
                if os.path.isfile(dir + '/' + file):
                    try:
                        if file[-19::] == ".Dead__Man'$__Che$t":
                            pass
                        else:
                            self.crypt_file(dir + '/' + file, password)
                    except Exception as ex: 
                        self.insert_to_console(ex)
                        pass
            self.thread_count = 0
        except OSError:
            self.path_error = True
            return

    def decrypt_file(self, file, password):
        #normal_f = win32api.SetFileAttributes(file, win32con.FILE_ATTRIBUTE_NORMAL)
        bufferSize = 512 * 1024
        try:
            pyAesCrypt.decryptFile(str(file), str(os.path.splitext(file)[0]),
                                   password, bufferSize)
            self.insert_to_console('file was decrypt $ ' + str(os.path.splitext(file)[0]) + '\n')
            os.remove(file)
        except Exception as e:
            self.insert_to_console(e)
            pass

    def decrypt_disk_win(self, dir, password):
        try:
            for file in os.listdir(dir):
                if os.path.isdir(dir + '\\' + file):
                    self.decrypt_disk(dir + '\\' + file, password)
                if os.path.isfile(dir + '\\' + file):
                    try:
                        self.decrypt_file(dir + '\\' + file, password)
                    except Exception as ex:
                        self.insert_to_console(ex)
                        pass
        except OSError:
            self.path_error = True
            pass
      
    def decrypt_disk(self, dir, password):
        normal_dir = ctypes.windll.kernel32.SetFileAttributesW(dir, FILE_ATTRIBUTE_DIRECTORY)
        try:
            for file in os.listdir(dir):
                if os.path.isdir(dir + '/' + file):
                    self.decrypt_disk(dir + '/' + file, password)
                if os.path.isfile(dir + '/' + file):
                    try:
                        self.decrypt_file(dir + '/' + file, password)
                    except Exception as ex: 
                        self.insert_to_console(ex)
                        pass
            self.thread_count = 0
        except OSError:
            self.path_error = True
            return
 
    def crypting(self, dir, password):
        if self.path_error or password == '':
            self.path_error = False
            self.thread_count = 0
            self.insert_to_console('Ошибка : Неправильный путь или ты не Deavy Jones !\n')
            return
        else:
            self.thread_count += 1
            if self.thread_count > 1:
                # print(threading.enumerate())
                self.insert_to_console('Ограничение потока, запущено : 1\n')
                return
        pycrypt = threading.Thread(name="aesEncryptor", target=self.crypt_disk, args=(dir, password))
        pycrypt.start()

    def decrypting(self, dir, password):
        if self.path_error or password == '':
            self.path_error = False
            self.thread_count = 0
            self.insert_to_console('Ошибка : Неправильный путь или ты не Deavy Jones !\n')
            return
        else:
            self.thread_count += 1
            if self.thread_count > 1:
                self.insert_to_console('Ограничение потока, запущено : 1\n')
                return
        pycrypt = threading.Thread(name="aesDecryptor", target=self.decrypt_disk, args=(dir, password))
        pycrypt.start()

    def run_app():
        root = tk.Tk()
        root.resizable(width=False, height=False)
        MainWindow(root)
        root.title("Encryptor che$t")
        root.iconbitmap("main.ico")
        root.geometry("562x250")
        root.configure(bg="#1a1a1a")
        root.mainloop()


if __name__ == '__main__':
    zv = MainWindow
    zv.run_app()
