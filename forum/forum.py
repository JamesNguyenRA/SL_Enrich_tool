import tkinter as tk
import numpy as np
from f247_crawler import _run_247
from f319_crawler import _run_319
from viettrader import _run_viettrader
from datetime import datetime

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        # self.pack()
        self.var1 = tk.IntVar()
        self.var2 = tk.IntVar()
        self.var3 = tk.IntVar()
        self.create_widgets()
        


    def platform_select(self):
        check_list = [cb for cb in [self.var1.get(),self.var2.get(),self.var3.get()]]
        options = np.where(np.array(check_list)>0)[0]
        return options
    
    def get_scraper_infos(self):
        self.search_kw = str(self.kw_entry.get())
        self.num_page = self.nb_entry.get()
        self.platform = self.platform_select()
        self.start_day = datetime.strptime(self.start_day_entry.get(), '%d/%m/%y').date()
        self.end_day = datetime.strptime(self.end_day_entry.get(), '%d/%m/%y').date()

    def run_and_export(self):
        self.get_scraper_infos()
        for i in self.platform:
            if i == 0:
                _run_319(self.search_kw,self.num_page,self.start_day,self.end_day)
            elif i == 1:
                _run_247(self.search_kw,self.start_day,self.end_day)
            elif i == 2:
                _run_viettrader(self.search_kw,self.num_page,self.start_day,self.end_day)

    def create_widgets(self):
        self.label1 = tk.Label(text="Keyword").grid(row=0, column=0)
        self.kw_entry = tk.Entry()
        self.kw_entry.grid(row=0, column=1)
        self.label2 = tk.Label(text="Platform").grid(row=1, column=0)
        self.forum1_cb = tk.Checkbutton(text="F319.com", variable=self.var1, onvalue=1, offvalue=0,command=self.platform_select)
        self.forum1_cb.grid(row=2,column=0)
        self.forum2_cb = tk.Checkbutton(text="F247.com", variable=self.var2, onvalue=1, offvalue=0,command=self.platform_select)
        self.forum2_cb.grid(row=2,column=1)
        self.forum3_cb = tk.Checkbutton(text="viettrader.net", variable=self.var3, onvalue=1, offvalue=0,command=self.platform_select)
        self.forum3_cb.grid(row=2,column=2)
        self.label3 = tk.Label(text="Number of pages").grid(row=4, column=0)
        self.nb_entry = tk.Entry()
        self.nb_entry.grid(row=4,column=1)
        self.label4 = tk.Label(text="From (dd/mm/yy)").grid(row=5, column=0)
        self.start_day_entry = tk.Entry()
        self.start_day_entry.grid(row=5,column=1)
        self.label5 = tk.Label(text="To").grid(row=5, column=2)
        self.end_day_entry = tk.Entry()
        self.end_day_entry.grid(row=5,column=3)
        # self.nb_entry = tk.Entry()
        # self.nb_entry.grid(row=3, column=1)
        self.label6 = tk.Label(text="(Remember to close xlsx file before run!)",bg='orange').grid(row=6, column=1,sticky="e")
        self.run_btn = tk.Button(text="Run and Export", bg = "green",command=self.run_and_export).grid(row=6,column=3,sticky ="w")
        self.quit = tk.Button(text="Quit", bg= "red",command=root.destroy).grid(row=6,column=3,sticky ="e")
        
        # self.quit.pack()



root = tk.Tk()
app = Application(master=root)
app.master.title("Forum Scraper")
app.master.minsize(450, 150)
app.mainloop()

# root= tk.Tk()

# canvas1 = tk.Canvas(root, width=400, height=300)
# canvas1.pack()

# label1 = tk.Label(master=canvas1, text="Keyword", bg="gray")
# label1.place(x=10, y=50)
# entry1 = tk.Entry(canvas1)
# entry1.place(x=100,y=50) 

# # canvas1.create_window(100, 50, window=entry1)

# def run():  
#     print("keyword: ",entry1.get())
    

    
# button1 = tk.Button(text='Run', command=run)
# canvas1.create_window(200, 180, window=button1)

# root.mainloop()