##################################
# Coin Gecko Watch by Ryan Holden

# Import required modules
import tkinter as tk
from tkinter import ttk
from tkinter import *
from tkinter.ttk import Treeview, Scrollbar
import os
import sys
import responses
import json
import time
import threading
import tkinter.tix as tix
from datetime import datetime
from pycoingecko import CoinGeckoAPI
from requests.exceptions import HTTPError
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.figure import Figure

# set the status and image directory
status = ""
image_dir = os.path.dirname(sys.argv[0])
logo_icon = os.path.join(image_dir, "images\logo_icon.ico")

# Gets the current time and splits the value to remove decimal place (Hours, Mins, Seconds)
def get_time():
    now = str(datetime.now().time())
    now = now.split(".")[0]
    return now

# Function to read the coins_list.txt file for a list of coins and compile the coin list 
def get_coin_list():
    global list_dir
    list_dir = os.path.dirname(sys.argv[0])
    list_dir = os.path.join(list_dir, "coins_list.txt")
    with open(list_dir, "r") as coin_list_file:
        coin_list = coin_list_file.read().splitlines()
    #coin_list_file.close()
    return coin_list

# Main function to pull coin statistics through including current price, changes etc.
def get_coins_markets(coin_list):
    coin_market_refresh = {}
    count = 0
    global status
    coin_market_refresh = CoinGeckoAPI().get_coins_markets('usd', ids=coin_list, sparkline='false', price_change_percentage='1h,24h,7d,14d,30d,200d,1y')
    return coin_market_refresh


# Loading window creation & update
def loading_window(argument):
    
    logo_loading = os.path.join(image_dir, "images\coingecko.gif")
    
      
    if argument == 'create':
        rootloading = tk.Tk()
        rootloading.title('Coin Gecko Prices')
        rootloading.overrideredirect(1)
        rootloading.tk.eval('tk::PlaceWindow . center')
        text1 = tk.Text(rootloading, height=19, width=31)
        photo = tk.PhotoImage(file=logo_loading,master=rootloading)
        text1.image_create(tk.END, image=photo)
        text1.pack()
        rootloading.update()
        coin_market_refresh_dict = []
        coin_market_refresh_dict = get_coins_markets(get_coin_list())
        rootloading.destroy()
        return coin_market_refresh_dict
    elif argument == 'update':
        rootloading = tk.Tk()
        rootloading.title('Coin Gecko Prices')
        rootloading.overrideredirect(1)
        rootloading.tk.eval('tk::PlaceWindow . center')
        text1 = tk.Text(rootloading, height=19, width=31)
        photo = tk.PhotoImage(file=logo_loading,master=rootloading)
        text1.image_create(tk.END, image=photo)
        text1.pack()
        rootloading.update()
        coin_market_refresh_dict = []
        coin_market_refresh_dict = get_coins_markets(get_coin_list())
        rootloading.destroy()
        return coin_market_refresh_dict

coin_market_refresh_dict = loading_window('create')
    
# Delete Treeview values function as part of the refresh function
def delete_treeview_values(tree_var):
    x = tree_var.get_children()
    for item in x:
        tree_var.delete(item)
        
# Refresh function - Retreives updated coin stats, deletes and re-creates treeview entries.
def refresh():
    print ("Updating")
    coin_market_refresh_dict = loading_window('update')
    delete_treeview_values(tree)
    
    populate_treeview(coin_market_refresh_dict)
    btn_text.set("Last Updated: " + get_time())
    print ("Done")

# Runs the refresh command in a separate thread.
def refreshing():    
    t = threading.Thread(target=refresh,name=refresh,args=())
    t.daemon = True
    t.start()

def calculate_height():
    if len(coin_market_refresh_dict) >= 15 and len(coin_market_refresh_dict) <= 30:
        return len(coin_market_refresh_dict)
    elif len(coin_market_refresh_dict) > 30:
        return 30
    else:
        return 15

treeview_height = calculate_height()
prices_length = len(coin_market_refresh_dict)


# Runs the about function in a separate thread.
def about_thread():
    t = threading.Thread(target=about,name=about,args=())
    t.daemon = True
    t.start()

# Creates the about window.
def about():
    
    about_window = Toplevel()
    about_window.iconbitmap(logo_icon)
    about_window.title("About Coin Gecko Watch")
    
    # specify size of window. 
    about_window.geometry("850x340")
    
    # Create text widget and specify size. 
    T = Text(about_window, height = 19, width = 140) 
  
    about = """Written in Python 3 by Ryan Holden
Leveraging PYcoingecko Powered by CoinGecko API.
    
    
Sources:
Coin Gecko Watch: 
Pycoingecko: https://github.com/man-c/pycoingecko
Coin Gecko API: https://www.coingecko.com/en/api

Instructions:
1 - Click the coin list button
2 - Enter the coin name or symbol in the search box at the bottom left and hit search
3 - Select and add the required coin in the left hand list to the current coin watch list on the right
        *Note - to remove a coin from the watch list, select the coin and click remove from watch list*
4 - Hit save and close
5 - Enjoy the coin stats and don't forget to periodically hit the refresh button!"""
  
  
    # Create close button. 
    b1 = Button(about_window, text = "Close", 
                command=lambda: about_window.destroy())  
  
    T.pack() 
    b1.pack() 
    
  
    # Insert Text. 
    T.insert(tk.END, about) 

# Function to run the coin selection window in a new thread 
def coin_selection_window_thread():
    t = threading.Thread(target=coin_selection_window,name=coin_selection_window,args=())
    t.daemon = True
    t.start()

# Coin selection window function
def coin_selection_window():
    coin_selection_tkinter = Toplevel()
    coin_selection_tkinter.iconbitmap(logo_icon)
    coin_selection_tkinter.title('CoinGecko Search')
   
    tree_cs=ttk.Treeview(coin_selection_tkinter, height=treeview_height)
    style = ttk.Style()

    def fixed_map(option):
        # Returns the style map for 'option' with any styles starting with
        # ("!disabled", "!selected", ...) filtered out

        # style.map() returns an empty list for missing options, so this should
        # be future-safe
        return [elm for elm in style.map("Treeview", query_opt=option)
                if elm[:2] != ("!disabled", "!selected")]

   

    tree_cs.tag_configure("oddrow", background='khaki1')
    tree_cs.tag_configure('evenrow', background='DarkOliveGreen1')

    tree_cs["columns"]=("1", "2")
    tree_cs.column("#0", width=210, minwidth=150, stretch=tk.YES)
    tree_cs.column("1", width=100, minwidth=100, stretch=tk.YES)
    tree_cs.column("2", width=180, minwidth=150, stretch=tk.YES)    

    tree_cs.heading("#0",text="Coin Name",anchor=tk.W)
    tree_cs.heading("1", text="Symbol",anchor=tk.W)
    tree_cs.heading("2", text="ID",anchor=tk.W)
    
    tree_watchlist=ttk.Treeview(coin_selection_tkinter, height=treeview_height)
    style = ttk.Style()

    tree_watchlist.tag_configure("oddrow", background='khaki1')
    tree_watchlist.tag_configure('evenrow', background='DarkOliveGreen1')

    tree_watchlist["columns"]=("1", "2")
    tree_watchlist.column("#0", width=210, minwidth=150, stretch=tk.YES)
    tree_watchlist.column("1", width=100, minwidth=100, stretch=tk.YES)
    tree_watchlist.column("2", width=180, minwidth=150, stretch=tk.YES)    

    tree_watchlist.heading("#0",text="Coin Name",anchor=tk.W)
    tree_watchlist.heading("1", text="Symbol",anchor=tk.W)
    tree_watchlist.heading("2", text="ID",anchor=tk.W)

  
    if coin_selection_window.runcount < 1:
        coin_selection_window.coin_selection = CoinGeckoAPI().get_coins_list()
        coin_list = get_coin_list()
        for item in coin_selection_window.coin_selection:
            item["disp"] = 'yes'
            item["Watchlist"] = 'no'
            for coin in coin_list:
                if item["id"] == coin:
                    item["Watchlist"] = 'yes'
        coin_selection_window.runcount += 1
        print (coin_selection_window.runcount)
    else:
        coin_list = get_coin_list()
        for item in coin_selection_window.coin_selection:
            for coin in coin_list:
                    if item["id"] == coin:
                        item["Watchlist"] = 'yes'
        coin_selection_window.runcount += 1
        print (coin_selection_window.runcount)
    
    def selectItem(a):
        curItem = tree_cs.focus()
        if curItem != "":
            selected_coin_values = (tree_cs.item(curItem))
            selected_coin_val_list = selected_coin_values['values']
            selectItem.selected_coin_id = selected_coin_val_list[1]

    def selectItemCW(a):
        curItem = tree_watchlist.focus()
        if curItem != "":
            selected_coin_values = (tree_watchlist.item(curItem))
            selected_coin_val_list = selected_coin_values['values']
            selectItemCW.selected_coin_id = selected_coin_val_list[1]

    
    def populate(populate_string):
        len = 0
        print ("Populating")
        for item in populate_string:
            len = len + 1
            lenmod = len % 2
            if item.get("Watchlist") == 'yes':
                for k, v in item.items():
                    if k == 'name':
                        name = v
                    elif k == 'symbol':
                        symbol = v
                    elif k == 'id':
                        id = v
                    elif k == 'disp':
                        disp = v
                if lenmod > 0:
                    tag = "evenrow"
                else:
                    tag = "oddrow"
                tree_watchlist.insert("", len, text=name, values=(symbol,id), tags=(tag,))
                tree_watchlist.bind('<ButtonRelease-1>', selectItemCW)
            if item.get("disp") == 'yes' and item.get("Watchlist") == 'no':
                for k, v in item.items():
                    if k == 'name':
                        name = v
                    elif k == 'symbol':
                        symbol = v
                    elif k == 'id':
                        id = v
                    elif k == 'disp':
                        disp = v
                    elif k == 'Watchlist':
                        Watchlist = v
                if lenmod > 0:
                    tag = "evenrow"
                else:
                    tag = "oddrow"
                tree_cs.insert("", len, text=name, values=(symbol,id), tags=(tag,))
                tree_cs.bind('<ButtonRelease-1>', selectItem)
    
    def populate_search(populate_string):
        len = 0
        print ("Populating")
        for item in populate_string:
            len = len + 1
            lenmod = len % 2
            if item.get("disp") == 'yes' and item.get("Watchlist") == 'no':
                for k, v in item.items():
                    if k == 'name':
                        name = v
                    elif k == 'symbol':
                        symbol = v
                    elif k == 'id':
                        id = v
                    elif k == 'disp':
                        disp = v
                    elif k == 'Watchlist':
                        Watchlist = v
                if lenmod > 0:
                    tag = "evenrow"
                else:
                    tag = "oddrow"
                tree_cs.insert("", len, text=name, values=(symbol,id,Watchlist), tags=(tag,))
                tree_cs.bind('<ButtonRelease-1>', selectItem)
    
    def add_to_watchlist(coin):
        for item in coin_selection_window.coin_selection:
            if item.get("id") == coin:
                item["Watchlist"] = 'yes'
        delete_treeview_values(tree_cs)
        delete_treeview_values(tree_watchlist)
        populate(coin_selection_window.coin_selection)

    def remove_from_watchlist(coin):
        for item in coin_selection_window.coin_selection:
            if item.get("id") == coin:
                item["Watchlist"] = 'no'
        delete_treeview_values(tree_cs)
        delete_treeview_values(tree_watchlist)
        populate(coin_selection_window.coin_selection)

    def search(searchstring):
        print (searchstring)
        for item in coin_selection_window.coin_selection:
            if searchstring.casefold() in item.get("symbol").casefold() or searchstring.casefold() in item.get("name").casefold():
                item["disp"] = 'yes'
            else:
                item["disp"] = 'no'
            
        delete_treeview_values(tree_cs)
        print ("Deleted")
        populate_search(coin_selection_window.coin_selection)

    def save_and_close():
        coin_selection_window.coin_selection_write = []
        x = tree_watchlist.get_children()
        for item in x:
            #print (item)
            selected_coin_val_list = (tree_watchlist.item(item))
            #print (selected_coin_val_list)
            selected_coin_val = selected_coin_val_list['values']
            #print (selected_coin_val)
            selected_coin_id = selected_coin_val[1]
            #print (selected_coin_id)
            coin_selection_window.coin_selection_write.append(selected_coin_id)
            #print (coin_selection)
        with open(list_dir, "w") as coin_list_file:
            coin_list_file.seek(0)
            coin_list_file.truncate()
            for coin in coin_selection_window.coin_selection_write:
                coin_list_file.write(coin)
                coin_list_file.write("\n")
        coin_selection_tkinter.destroy()
        refreshing()

    populate(coin_selection_window.coin_selection)

    tree_cs.grid(column = 1, row = 1, sticky='nsew', columnspan=2)
    tree_watchlist.grid(column = 4, row = 1, sticky='nsew', columnspan=2)

    vsb = ttk.Scrollbar(coin_selection_tkinter, orient="vertical", command=tree_cs.yview)
    vsb2 = ttk.Scrollbar(coin_selection_tkinter, orient="vertical", command=tree_watchlist.yview)
    vsb.grid(column = 3, row = 1, stick='ns')
    vsb2.grid(column = 6, row = 1, stick='ns')

    tree_cs.configure(yscrollcommand=vsb.set)
    tree_watchlist.configure(yscrollcommand=vsb2.set)
    

    # Use this as a flag to indicate if the box was clicked.
    global clicked   
    clicked = False

    # Delete the contents of the Entry widget. Use the flag
    # so that this only happens the first time.
    def callback(event):
        global clicked
        if (clicked == False):
            dirname[0].delete(0, END)         #  
            dirname[0].config(fg = "black")   # Change the colour of the text here.
            clicked = True

    
    dirname = []                              # Declare a list for the Entry widgets.
    directory=StringVar(None)
    dirname.append(Entry(coin_selection_tkinter,textvariable=directory,width=25, fg = "gray"))        # Create an Entry box with gray text.
    dirname[0].bind("<Button-1>", callback)   # Bind a mouse-click to the callback function.
    dirname[0].insert(0, "Enter coin name or symbol")           # Set default text at cursor position 0.
    dirname[0].grid(column = 1, row = 2)
    

    b1 = Button(coin_selection_tkinter, text = "Save & Close", 
                command=lambda: save_and_close()).grid(column = 5, row = 2, sticky=E)
    b2 = Button(coin_selection_tkinter, text = "Search", 
                command=lambda: search(dirname[0].get())).grid(column = 1, row = 2, sticky=W)
    b3 = Button(coin_selection_tkinter, text = "Add to Watchlist =>", 
                command=lambda: add_to_watchlist(selectItem.selected_coin_id)).grid(column = 2, row = 2)
    b4 = Button(coin_selection_tkinter, text = "<= Remove from Watchlist", 
                command=lambda: remove_from_watchlist(selectItemCW.selected_coin_id)).grid(column = 4, row = 2)

# Call the get coin list function
coin_list = get_coin_list()

# Coin Selection Window dictionary and runcount
coin_selection_window.coin_selection = {}
coin_selection_window.runcount = 0 

# Main Tkinter window
root = tk.Tk()
tree_frame = Frame(root)
button_frame = Frame(root)
root.title('CoinGecko Watch')
tree=ttk.Treeview(tree_frame, height=treeview_height)
logo_icon = os.path.join(image_dir, "images\logo_icon.ico")

style = ttk.Style()

def fixed_map(option):
    # Returns the style map for 'option' with any styles starting with
    # ("!disabled", "!selected", ...) filtered out

    # style.map() returns an empty list for missing options, so this should
    # be future-safe
    return [elm for elm in style.map("Treeview", query_opt=option)
            if elm[:2] != ("!disabled", "!selected")]

style.map("Treeview",
          foreground=fixed_map("foreground"),
          background=fixed_map("background"))

tree.tag_configure("oddrow", background='khaki1')
tree.tag_configure('evenrow', background='DarkOliveGreen1')

tree["columns"]=("1", "2", "3", "4", "5", "6", "7", "8", "9", "10")
tree.column("#0", width=1, minwidth=1, stretch=tk.NO)
tree.column("1", width=130, minwidth=130, stretch=tk.NO)
tree.column("2", width=130, minwidth=130, stretch=tk.NO)    
tree.column("3", width=130, minwidth=130, stretch=tk.NO)
tree.column("4", width=130, minwidth=130, stretch=tk.NO)
tree.column("5", width=130, minwidth=130, stretch=tk.NO)
tree.column("6", width=130, minwidth=130, stretch=tk.NO)
tree.column("7", width=130, minwidth=130, stretch=tk.NO)
tree.column("8", width=130, minwidth=130, stretch=tk.NO)
tree.column("9", width=130, minwidth=130, stretch=tk.NO)
tree.column("10", width=130, minwidth=130, stretch=tk.NO)

tree.heading("1", text="Coin Name",anchor=tk.W)
tree.heading("2", text="Current $ USD Value",anchor=tk.W)
tree.heading("3", text="1 Hour % Change",anchor=tk.W)
tree.heading("4", text="24 Hour % Change",anchor=tk.W)
tree.heading("5", text="7 Day % Change",anchor=tk.W)
tree.heading("6", text="14 Day % Change",anchor=tk.W)
tree.heading("7", text="30 Day % Change",anchor=tk.W)
tree.heading("8", text="200 Day % Change",anchor=tk.W)
tree.heading("9", text="1 Year % Change",anchor=tk.W)
tree.heading("10", text="Market Cap",anchor=tk.W)
   


# Populate Treeview function
def populate_treeview(arg):
    len = 0
    #for k, v in arg.items():
    for i in arg:
        len = len + 1
        lenmod = len % 2
        #for k1, v1 in v.items():
        for k1, v1 in i.items():
            if k1 == 'name':
                coin = v1
            elif k1 == 'current_price':
                if v1 is not None:
                    value = float(v1)
                elif v1 is None:
                    value = 0
            elif k1 == 'price_change_percentage_1h_in_currency':
                if v1 is not None:
                    price_change_1h = float(v1)
                elif v1 is None:
                    price_change_1h = 0
            elif k1 == 'price_change_percentage_24h_in_currency':
                if v1 is not None:
                    price_change_24h = float(v1)
                elif v1 is None:
                    price_change_24h = 0
            elif k1 == 'price_change_percentage_7d_in_currency':
                if v1 is not None:
                    price_change_7d = float(v1)
                elif v1 is None:
                    price_change_7d = 0
            elif k1 == 'price_change_percentage_14d_in_currency':
                if v1 is not None:
                    price_change_14d = float(v1)
                elif v1 is None:
                    price_change_14d = 0
            elif k1 == 'price_change_percentage_30d_in_currency':
                if v1 is not None:
                    price_change_30d = float(v1)
                elif v1 is None:
                    price_change_30d = 0
            elif k1 == 'price_change_percentage_200d_in_currency':
                if v1 is not None:
                    price_change_200d = float(v1)
                elif v1 is None:
                    price_change_200d = 0
            elif k1 == 'price_change_percentage_1y_in_currency':
                if v1 is not None:
                    price_change_1y = float(v1)
                elif v1 is None:
                    price_change_1y = 0
            elif k1 == 'market_cap':
                if v1 is not None:
                    market_cap_value = float(v1)
                elif v1 is None:
                    market_cap_value = 0
        if lenmod > 0:
            tag = "evenrow"
        else:
            tag = "oddrow"
        tree.insert("", len, text="", values=(coin,value,price_change_1h,price_change_24h,price_change_7d,price_change_14d,price_change_30d,price_change_200d,price_change_1y,market_cap_value), tags=(tag,))
    
  
    tree.grid(column = 1, row = 1, sticky='nsew', columnspan=1)




# Call the populate treeview function    
populate_treeview(coin_market_refresh_dict)

  
   
# Final pack of main treeview and buttons

btn_text = tk.StringVar()
vsb = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)

tree.configure(yscrollcommand=vsb.set)
vsb.grid(column = 2, row = 1, stick='ns')

btn_text.set("Last Updated: " + get_time())
ttk.Button(button_frame, text='Update', command=refreshing).pack(side=LEFT) 
ttk.Button(button_frame, textvariable=btn_text).pack(side=LEFT)
ttk.Button(button_frame, text='Coin List', command=coin_selection_window_thread).pack(side=LEFT) 
ttk.Button(button_frame, text='Exit', command=lambda: os._exit(0)).pack(side=RIGHT, padx=(0, 16))
ttk.Button(button_frame, text='About', command=about_thread).pack(side=RIGHT)

# Sort columns function
def treeview_sort_column(tree, col, reverse):
    
    
    try:
        l = [(float(tree.set(k, col)), k) for k in tree.get_children('')]
    except Exception:
        l = [(tree.set(k, col), k) for k in tree.get_children('')]
        
    try:
        l.sort(key=lambda t: priority_item, reverse=reverse)
    except Exception:
        l.sort(reverse=reverse)

    # rearrange items in sorted positions
    for index, (val, k) in enumerate(l):
        tree.move(k, '', index)

    # reverse sort next time
    tree.heading(col, command=lambda _col=col: treeview_sort_column(tree, _col, not reverse))

for col in tree["columns"]:
    tree.heading(col, command=lambda _col=col: treeview_sort_column(tree, _col, False))

tree_frame.pack()
button_frame.pack(fill=tk.X)
tree.mainloop()


    
   



