import tkinter as tk
from tkinter import *
import qrcode
import os
from tkinter import ttk, filedialog, messagebox
import pyzbar.pyzbar as pyzbar
import webbrowser
from PIL import Image
import clipboard


class QRCodeGenerator:
    def __init__(self, master):

        self.master = master
        self.master.title("QR Code Generator")
        self.master.geometry("450x230+700+200")
        self.master.iconbitmap("qrcode.ico")
        self.master.resizable(False, False)

        self.f = tk.Frame(self.master, width=450, height=230, bg="#00e6ac")
        self.f.place(x=0, y=0)

        self.iconback = PhotoImage(
            file="iconBack.png")
        self.back_icon = self.iconback.subsample(5, 5)
        self.back_button = tk.Button(self.master, image=self.back_icon, activebackground="#00e6ac", activeforeground="White",
                                    compound=CENTER, fg="White", bg="#00e6ac", relief="flat", command=self.go_back)
        self.back_button.place(x=2, y=2)

        self.link_label = tk.Label(self.master, text="link or \n content", font=(
            "Arial", 15), fg="White", bg="#00e6ac")
        self.link_label.place(x=2, y=56)

        self.link_entry = tk.Entry(self.master, width=35, font=(
            "Arial", 12), fg="White", bg="#5D7283", relief="flat", insertbackground="white")
        self.link_entry.place(x=85, y=70)

        self.iconpaste = PhotoImage(
            file="iconPaste.png")
        self.paste_icon = self.iconpaste.subsample(15, 15)
        self.paste_button = tk.Button(self.master, image=self.paste_icon, activebackground="#e6ac00", activeforeground="White",
                                    compound=CENTER, fg="White", bg="#00e6ac", relief="flat", command=self.paste)
        self.paste_button.place(x=407, y=58)

        self.color_label = tk.Label(self.master, text="Color", font=(
            "Arial", 15), fg="White", bg="#00e6ac")
        self.color_label.place(x=7, y=110)

        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.configure('TCombobox', background='#4D677A', foreground='White', font=(
            'Arial', 15), fieldbackground='#5D7283')

        self.colors = ["black", "red", "blue", "green", "purple"]
        self.color_combo = ttk.Combobox(
            self.master, values=self.colors, height=10)
        self.color_combo.current(0)
        self.color_combo.place(x=85, y=115)

        self.generate_button = tk.Button(self.master, text="Generate", font=(
            "Arial", 15, "bold"), fg="White", bg="#5D7283", relief="flat", command=self.generate_qr_code)
        self.generate_button.place(x=172, y=163)

        self.options = {
            'initialdir': '~/Pictures',
            'initialfile': 'untitled.png',
            'defaultextension': '.png',
            'filetypes': [('PNG files', '*.png'), ('JPEG files', '*.jpg')],
            'title': 'Save As'
        }

    def go_back(self):
        self.master.destroy()  
        root = tk.Tk()  
        MainWindow(root)
        root.mainloop()

    def paste(self):
        self.link_entry.insert(0, clipboard.paste()) 

    def generate_qr_code(self):
        self.master.withdraw() 
        link = self.link_entry.get()

        if link:
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            qr.add_data(link)
            qr.make(fit=True)

            color = self.color_combo.get()
            img = qr.make_image(fill_color=color, back_color="white")
            save_file_path = filedialog.asksaveasfilename(**self.options)

            if save_file_path:
                img.save(save_file_path)
                self.link_entry.delete(0, tk.END)
                self.color_combo.current(0)
                tk.messagebox.showinfo(
                    "Success", "QR Code generated and saved successfully!")
        else:
            tk.messagebox.showwarning(
                "Error", "Please enter both link or content!")

        self.master.deiconify() 


class QRCodeReader:
    def __init__(self, master):

        self.master = master
        self.master.title("QR Code Reader")
        self.master.geometry("450x230+700+200")
        self.master.iconbitmap("qrcode.ico")
        self.master.resizable(False, False)

        self.f3 = tk.Frame(self.master, width=450, height=230, bg="#00e6ac")
        self.f3.place(x=0, y=0)

        self.iconback = PhotoImage(
            file="iconBack.png")
        self.back_icon = self.iconback.subsample(5, 5)
        self.back_button = tk.Button(self.master, image=self.back_icon, activebackground="#4D677A", activeforeground="White",
                                    compound=CENTER, fg="White", bg="#00e6ac", relief="flat", command=self.go_back)
        self.back_button.place(x=2, y=2)

        self.iconbrowse = PhotoImage(file = "iconBrowse.png")
        self.browse_icon = self.iconbrowse.subsample(3, 3)
        self.browse_button = Button(self.f3, text = ' Browse', image = self.browse_icon, compound = LEFT, bg="#00e6ac", relief="flat", fg="White", activebackground="#4D677A", activeforeground="White", command=self.browse_file)
        self.browse_button.place(x=190, y=20)

        self.qr_data_label = tk.Label(self.master, text="QR Data:", font=(
            "Arial", 15), fg="White", bg="#00e6ac")
        self.qr_data_label.place(x=2, y=90)

        self.qr_data_entry = tk.Entry(self.master, width=35, font=(
            "Arial", 12), fg="Black", bg="#5D7283", relief="flat")
        self.qr_data_entry.place(x=95, y=95)

        self.iconcopy = PhotoImage(
            file="iconCopy.png")
        self.copy_icon = self.iconcopy.subsample(12, 12)
        self.copy_button = tk.Button(self.master, image=self.copy_icon, activebackground="#4D677A", activeforeground="White",
                                    compound=CENTER, fg="White", bg="#00e6ac", relief="flat", command=self.copy)
        self.copy_button.place(x=405, y=77)

        self.open_url_button = tk.Button(
            self.master, font=("Arial", 13), fg="White", bg="#00e6ac", relief="flat", command=self.open_url, state='disabled')
        self.open_url_button.place(x=190, y=145)

    def go_back(self):
        self.master.destroy()  
        root = tk.Tk()  
        MainWindow(root)
        root.mainloop()

    def copy(self):
        clipboard.copy(self.qr_data_entry.get())  

    def browse_file(self):
        self.master.withdraw()  

        self.file_path = filedialog.askopenfilename(initialdir=os.getcwd(), filetypes=[
                                                ("PNG", "*.png"), ("JPEG", "*.jpg")])
        try:
            with Image.open(self.file_path) as img:
                img = img.convert('RGB')
                decoded_objects = pyzbar.decode(img)
                if decoded_objects:
                    link = decoded_objects[0].data.decode('utf-8')
                    for obj in decoded_objects:
                        data = obj.data.decode('utf-8')
                        self.qr_data_entry.config(state="normal")
                        self.qr_data_entry.delete(0, tk.END)
                        self.qr_data_entry.insert(0, data)
                        self.qr_data_entry.config(state="readonly")
                        print("QR Code Data:", data)

                    if link.startswith('http://') or link.startswith('https://'):
                        self.open_url_button.config(state='normal')
                        self.open_url_button.config(bg="#5D7283")
                        self.open_url_button.config(text="Open URL")
                    else:
                        self.open_url_button.config(state='disabled')

                else:
                    self.qr_data_entry.config(state="normal")
                    self.qr_data_entry.delete(0, tk.END)
                    self.qr_data_entry.insert(0, "No QR Code found in image.")
                    self.qr_data_entry.config(state="readonly")
                    print("No QR Code found in image.")
        except Exception as e:
            messagebox.showerror(
                    "Error", "Error while reading QR Code: {}".format(str(e)))
            print("Error while reading QR Code:", str(e))
        self.master.deiconify()

    def open_url(self):
        link = self.qr_data_entry.get()
        webbrowser.open_new_tab(link)


class MainWindow:
    def __init__(self, master):
        self.master = master
        self.master.title("QR Code Tool")
        self.master.geometry("360x150+700+200")
        self.master.iconbitmap("qrcode.ico")
        self.master.resizable(False, False)

        self.f1 = tk.Frame(self.master, width=360, height=150, bg="#00e6ac")
        self.f1.place(x=0, y=0)

        self.generator_button = tk.Button(self.f1, text="QR Code Reader", font=(
            "Arial", 13, "bold"), fg="White", bg="#5D7283", relief="flat", command=self.open_reader)
        self.generator_button.place(x=10, y=50)

        self.reader_button = tk.Button(self.f1, text="QR Code Generator", font=(
            "Arial", 13, "bold"), fg="White", bg="#5D7283", relief="flat", command=self.open_generator)
        self.reader_button.place(x=180, y=50)

    def open_generator(self):
        self.master.destroy() 
        generator_window = tk.Tk() 
        QRCodeGenerator(generator_window)
        generator_window.mainloop()

    def open_reader(self):
        self.master.destroy()
        reader_window = tk.Tk()
        QRCodeReader(reader_window)
        reader_window.mainloop()


if __name__ == '__main__':
    root = tk.Tk()
    MainWindow(root)
    root.mainloop()
