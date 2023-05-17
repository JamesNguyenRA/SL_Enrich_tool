import tkinter as tk
from tkinter import ttk
import numpy as np
from get_post import *
from tkinter import filedialog
import dateparser
import os


class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.create_widgets()

    def get_user_info(self):
        self.email = self.label2_entry.get()
        self.password = self.label3_entry.get()
        self.code_2fa = self.label4_entry.get()
        self.cookie = self.label5_entry.get()

    def browseFiles(self,browse_text):
        self.objects = []
        file = filedialog.askopenfilename(initialdir = "/",
                                          title = "Select a File",
                                          filetypes = (("Text files",
                                                        "*.txt*"),
                                                       ("all files",
                                                        "*.*")))
      
        source = open(file,"r")
        source_elements = source.readlines()
        for link in source_elements:
            self.objects.append(link.replace('\n', ''))
        # # Change label contents
        browse_text.configure(text=f"File {os.path.basename(file)} selected!") 

    def get_daterange(self,start_d_entry,end_d_entry):
        self.start_day = dateparser.parse(start_d_entry.get())
        self.end_day = dateparser.parse(end_d_entry.get())

    def login(self):
        self.get_user_info()
        self.driver = initDriverProfile()
        isLogin = checkLiveClone(self.driver)  # Check live
        twoFa= self.code_2fa.replace(" ","")
        if (isLogin == False):
            loginBy2FA(self.driver, self.email, self.password, twoFa)
        sleep(3)
        search_url = f'https://www.facebook.com/'
        self.driver.get(search_url)
        sleep(random.randint(2,4))
        # scroll_to_bottom(self.driver)

    def get_group_post(self):
        self.get_daterange(self.label10_entry,self.label11_entry)
        self.search_kw = self.label9_entry.get()
        convert_cookie(self.cookie)
        getPostsGroup(self.driver,self.objects,self.search_kw,self.start_day,self.end_day)
        search_url = f'https://www.facebook.com/'
        self.driver.get(search_url)
        sleep(random.randint(2,4))

    def get_post_share(self):
        self.get_daterange(self.label13_entry,self.label14_entry)
        get_post_share(self.driver,self.objects,self.start_day,self.end_day)
        sleep(1)

    def create_widgets(self):
        ### Login block
        self.label1 = tk.Label(text="User Login",fg='red').grid(row=0,column=0,sticky="w")
        self.label2 = tk.Label(text="Email").grid(row=1,column=0)
        self.label2_entry = tk.Entry()
        self.label2_entry.grid(row=1,column=1)
        self.label3 = tk.Label(text="Password").grid(row=2,column=0)
        self.label3_entry = tk.Entry()
        self.label3_entry.grid(row=2,column=1)
        self.label4 = tk.Label(text="2FA").grid(row=3,column=0)
        self.label4_entry = tk.Entry()
        self.label4_entry.grid(row=3,column=1)
        self.label5 = tk.Label(text="Cookie").grid(row=4,column=0)
        self.label5_entry = tk.Entry()
        self.label5_entry.grid(row=4,column=1)
        tk.Label(text="   ").grid(column=2)
        ### Private group 
        self.label7 = tk.Label(text="Private Group",fg='red').grid(row=0,column=3,sticky="w")
        self.label_browse = tk.Label(text=" ")
        self.label_browse.grid(row=1,column=4)
        self.browse_group = tk.Button(text="Choose file",command=lambda: self.browseFiles(self.label_browse)).grid(row=1,column=3,sticky ="w")
        self.label9 = tk.Label(text="Keyword").grid(row=2,column=3,sticky="w")
        self.label9_entry = tk.Entry()
        self.label9_entry.grid(row=2,column=4)
        self.label10 = tk.Label(text="Start_day(mm/dd/yy)").grid(row=3,column=3)
        self.label10_entry = tk.Entry()
        self.label10_entry.grid(row=3,column=4)
        self.label11 = tk.Label(text="End_day(mm/dd/yy)").grid(row=4,column=3)
        self.label11_entry = tk.Entry()
        self.label11_entry.grid(row=4,column=4)
        tk.Label(text="   ").grid(column=5)

        ### Share post
        self.label12 = tk.Label(text="Share Post",fg='red').grid(row=0,column=6,sticky="w")
        self._browse = tk.Label(text=" ")
        self._browse.grid(row=1,column=7)
        self.browse_share = tk.Button(text="Choose file",command=lambda: self.browseFiles(self._browse)).grid(row=1,column=6,sticky ="w")
        self.label13 = tk.Label(text="Start_day(mm/dd/yy)").grid(row=3,column=6)
        self.label13_entry = tk.Entry()
        self.label13_entry.grid(row=3,column=7)
        self.label14 = tk.Label(text="End_day(mm/dd/yy)").grid(row=4,column=6)
        self.label14_entry = tk.Entry()
        self.label14_entry.grid(row=4,column=7)

        

        self.login_btn = tk.Button(text="Login", bg = "green",command=self.login).grid(row=5,column=1,sticky ="e")
        self.scrape_btn = tk.Button(text="Scrape", bg = "Orange",command=self.get_group_post).grid(row=5,column=4,sticky ="e")
        self.get_share_btn = tk.Button(text="Scrape", bg = "Orange",command=self.get_post_share).grid(row=5,column=7,sticky ="e")


root = tk.Tk()
app = Application(master=root)
app.master.title("Facebook Group Scraper")
app.master.minsize(200, 150)
app.mainloop()