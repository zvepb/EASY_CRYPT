#zv#
import os
import threading

import pyperclip
import pyAesCrypt
from tkinter import *
import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext


class MainWindow(tk.Frame):
    def __init__(self, root):
        super().__init__(root)
        self.init_main()

    def init_main(self):
        self.img_cache = []
        self.thread_count = 0
        self.path_error = False
        lb_dir = Label(text=u"Директория шифрования : ")
        lb_dir.pack()
        self.ent_value_dir = Entry(width=40)
        self.ent_value_dir.pack()
        lb_pass = Label(text=u"Пароль : ")
        lb_pass.pack()
        ent_value_pass = Entry(width=40)
        ent_value_pass.pack()
        crypt_img = PhotoImage(file='1.png')
        self.img_cache.append(crypt_img)
        btn_crypt = ttk.Button(text='  CRYPT', image=self.img_cache[0], compound='left', command=lambda: self.crypting(self.ent_value_dir.get(), ent_value_pass.get()))
        btn_crypt.place(x=5, y=20)
        decrypt_img = PhotoImage(file='2.png')
        self.img_cache.append(decrypt_img)
        btn_decrypt = ttk.Button(text='  DECRYPT', image=self.img_cache[1], compound='left', command=lambda: self.decrypting(self.ent_value_dir.get(), ent_value_pass.get()))
        btn_decrypt.place(x=5, y=60)
        paste_img = PhotoImage(file='3.png')
        self.img_cache.append(paste_img)
        btn_stop = ttk.Button(text='  PASTE', image=self.img_cache[2], compound='left', command=lambda: self.paste_dir_to_entry())
        btn_stop.place(x=390, y=20)
        stop_img = PhotoImage(file='4.png')
        self.img_cache.append(stop_img)
        btn_stop = ttk.Button(text='  STOP', image=self.img_cache[3], compound='left', command=lambda: self.close_crypter())
        btn_stop.place(x=390, y=60)
        self.console = scrolledtext.ScrolledText(fg="red", bg="black", state='disable')
        self.console.pack(pady=20)

    def close_crypter(self):
        quit()

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
            pyAesCrypt.encryptFile(str(file), str(file) + ".zvp",
                                   password, bufferSize)
            self.insert_to_console('ENCRYPTED >>> ' + str(file) + ".zvp" + '\n')
            os.remove(file)
        except Exception as e:
            self.insert_to_console('Ошибка шифрования')
            pass

    def crypt_disk(self, dir, password):
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

    def decrypt_file(self, file, password):
        bufferSize = 512 * 1024
        try:
            pyAesCrypt.decryptFile(str(file), str(os.path.splitext(file)[0]),
                                   password, bufferSize)
            self.insert_to_console('DECRYPTED >>> ' + str(os.path.splitext(file)[0]) + '\n')
            os.remove(file)
        except Exception as e:
            print('Ошибка расшифровки, файлы не зашифрованы,'
                  'неверный пароль или файл поврежден')
            self.insert_to_console(e)
            pass

    def decrypt_disk(self, dir, password):
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

    def crypting(self, dir, password):
        if self.path_error or password == '':
            self.path_error = False
            self.thread_count = 0
            self.insert_to_console('Ошибка : Неправильный путь или нет пароля !\n')
            return
        else:
            self.thread_count += 1
            if self.thread_count > 1:
                # print(threading.enumerate())
                self.insert_to_console('Ограничение потока, запущено : 1\n')
                return
        pycrypt = threading.Thread(target=self.crypt_disk, args=(dir, password))
        pycrypt.start()

    def decrypting(self, dir, password):
        if self.path_error or password == '':
            self.path_error = False
            self.thread_count = 0
            self.insert_to_console('Ошибка : Неправильный путь или нет пароля !\n')
            return
        else:
            self.thread_count += 1
            if self.thread_count > 1:
                self.insert_to_console('Ограничение потока, запущено : 1\n')
                return
        pycrypt = threading.Thread(target=self.decrypt_disk, args=(dir, password))
        pycrypt.start()

    def run_app():
        root = tk.Tk()
        root.resizable(width=False, height=False)
        MainWindow(root)
        root.title("zvepb_crypter")
        root.geometry("500x500")
        root.mainloop()


if __name__ == '__main__':
    zv = MainWindow
    zv.run_app()
