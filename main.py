import customtkinter
import tkinter 
import json
import os
from datetime import date
from tkinter import ttk
import csv
import pandas as pd
import userpaths

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("green")  

app = customtkinter.CTk()
app.title("Stock")
app.geometry("800x600")
app.resizable(False,False)

def stock_item_window():
    global stock
    stock = customtkinter.CTkToplevel()
    stock.geometry("600x400")
    stock.resizable(False,False)
    stock.title("Stock Items")
    stock.attributes('-topmost', 'true')

    Add_stock_btn = customtkinter.CTkButton(master=stock, text="Add Stock",command=add_stock_window)
    Add_stock_btn.place(relx=0.05, rely=0.05, anchor=customtkinter.NW)

    remove_stock_btn = customtkinter.CTkButton(master=stock, text="Remove Stock",command=remove_stock_window)
    remove_stock_btn.place(relx=0.3, rely=0.05, anchor=customtkinter.NW)

    view_stock_btn = customtkinter.CTkButton(master=stock, text="View Stock",command=view_stock_window)
    view_stock_btn.place(relx=0.55, rely=0.05, anchor=customtkinter.NW)

def view_stock_window():
    stock.attributes('-topmost', 'false')
    viewstock = customtkinter.CTkToplevel()
    viewstock.geometry('800x600')
    viewstock.resizable(False,False)
    viewstock.title("View Stock")
    viewstock.attributes('-topmost','true')
    
    totalstock_data = "data/Stock_data/totalstock_data.csv"
    addedstock_data = "data/Stock_data/addedstock_data.csv"
    removedstock_data = "data/Stock_data/removedstock_data.csv"
    allstock_data = "data/Stock_data/all_data.csv"
    documents_path = userpaths.get_my_documents()

    if(os.path.isfile(totalstock_data))and os.access(totalstock_data, os.R_OK):
        os.remove(totalstock_data)
        stocklist = []
        for i,file in enumerate(os.listdir("data/")):
            if file.endswith(".json"):
                file_name = os.path.basename(file)
                stock_name = file_name.split('.json')[0]
                stocklist.append(stock_name)
                
            fields = ['Stock Name','Current Quantity']
            with open(totalstock_data, 'w+',newline='') as file: 
                writer = csv.DictWriter(file, fieldnames = fields)
                writer.writeheader()
                for stocks in stocklist:
                    with open('data/' + stocks + ".json", 'r') as file:
                        data = json.load(file)
                        file.close()
                        Stock_data = [{'Stock Name': stocks,'Current Quantity': str(data["Quantity"])}]
                        writer.writerows(Stock_data)
    else:
        stocklist = []
        for i,file in enumerate(os.listdir("data/")):
            if file.endswith(".json"):
                file_name = os.path.basename(file)
                stock_name = file_name.split('.json')[0]
                stocklist.append(stock_name)
                
            fields = ['Stock Name','Current Quantity']
            with open(totalstock_data, 'w+',newline='') as file: 
                writer = csv.DictWriter(file, fieldnames = fields)
                writer.writeheader()
                for stocks in stocklist:
                    with open('data/' + stocks + ".json", 'r') as file:
                        data = json.load(file)
                        file.close()
                        Stock_data = [{'Stock Name': stocks,'Current Quantity': str(data["Quantity"])}]
                        writer.writerows(Stock_data)

    treeframe = customtkinter.CTkFrame(viewstock)
    treeframe.pack(pady=100,padx=20, fill="both", expand=False,side="bottom")
    treestyle = ttk.Style()
    treestyle.theme_use("clam")
    treestyle.configure("Treeview",
                        background = 'silver',
                        foreground = 'black',
                        rowheight = 30,
                        fieldbackground = 'silver')
    tree_scroll = tkinter.Scrollbar(treeframe)
    tree_scroll.pack(side = "right",fill="y")
    tree = ttk.Treeview(treeframe,show="headings",yscrollcommand=tree_scroll.set)
    tree.pack(fill="both")

    tree_scroll.config(command=tree.yview)



    with open(totalstock_data, 'r', newline='') as file:
        csv_reader = csv.reader(file)
        header = next(csv_reader)
        tree.delete(*tree.get_children())

        tree["columns"] = header
        for col in header:
            tree.heading(col, text=col)
            tree.column(col, width=100,anchor="center")

        for row in csv_reader:
            tree.insert("", "end", values=row)

    def added_stock_history_to_excel():
        viewstock.attributes('-topmost','false')
        read_file = pd.read_csv (addedstock_data)
        read_file.to_excel (documents_path + "/Added_Stock_Data.xlsx", index = None, header=True)
        os.system(documents_path + "/Added_Stock_Data.xlsx")

    def removed_stock_history_to_excel():
        viewstock.attributes('-topmost','false')
        read_file = pd.read_csv (removedstock_data)
        read_file.to_excel (documents_path + "/Removed_Stock_Data.xlsx", index = None, header=True)
        os.system(documents_path + "/Removed_Stock_Data.xlsx")      

    def current_stock_history_to_excel():
        viewstock.attributes('-topmost','false')
        read_file = pd.read_csv (totalstock_data)
        read_file.to_excel (documents_path + "/Current_Stock_Data.xlsx", index = None, header=True)
        os.system(documents_path + "/Current_Stock_Data.xlsx")
        
    def total_stock_history_to_excel():
        viewstock.attributes('-topmost','false')
        read_file = pd.read_csv (allstock_data)
        read_file.to_excel (documents_path + "/Total_Stock_Data.xlsx", index = None, header=True)
        os.system(documents_path + "/Total_Stock_Data.xlsx")

    def added_stock_history():
            totalstock_label.configure(text = "Added Stock History")
            with open(addedstock_data, 'r', newline='') as file:
                csv_reader = csv.reader(file)
                header = next(csv_reader)
                tree.delete(*tree.get_children())

                tree["columns"] = header
                for col in header:
                    tree.heading(col, text=col)
                    tree.column(col, width=100,anchor="center")

                for row in csv_reader:
                    tree.insert("", "end", values=row)
    
    def remove_stock_history():
            totalstock_label.configure(text = "Removed Stock History")
            with open(removedstock_data, 'r', newline='') as file:
                csv_reader = csv.reader(file)
                header = next(csv_reader)
                tree.delete(*tree.get_children())

                tree["columns"] = header
                for col in header:
                    tree.heading(col, text=col)
                    tree.column(col, width=100,anchor="center")

                for row in csv_reader:
                    tree.insert("", "end", values=row)
    
    def reset_stock_history():
            totalstock_label.configure(text = "Current Stock")
            with open(totalstock_data, 'r', newline='') as file:
                csv_reader = csv.reader(file)
                header = next(csv_reader)
                tree.delete(*tree.get_children())

                tree["columns"] = header
                for col in header:
                    tree.heading(col, text=col)
                    tree.column(col, width=100,anchor="center")

                for row in csv_reader:
                    tree.insert("", "end", values=row)
    
    def total_stock_history():
            totalstock_label.configure(text = "Total Stock History")
            with open(allstock_data, 'r', newline='') as file:
                csv_reader = csv.reader(file)
                header = next(csv_reader)
                tree.delete(*tree.get_children())

                tree["columns"] = header
                for col in header:
                    tree.heading(col, text=col)
                    tree.column(col, width=100,anchor="center")

                for row in csv_reader:
                    tree.insert("", "end", values=row)

    totalstock_label = customtkinter.CTkLabel(master=viewstock,text="Current Stock",font=("Arial",35))
    totalstock_label.place(relx = 0.5,rely = 0.1,anchor = customtkinter.CENTER)

    viewaddhistory_btn = customtkinter.CTkButton(master=viewstock,text="View Added Stock History",command=added_stock_history)
    viewaddhistory_btn.place(relx = 0.20,rely = 0.2,anchor = customtkinter.CENTER)

    exportaddhistory_btn = customtkinter.CTkButton(master=viewstock,text="Export Added Stock History to Excel",command=added_stock_history_to_excel)
    exportaddhistory_btn.place(relx = 0.25,rely = 0.9,anchor = customtkinter.S)

    viewremovehistory_btn = customtkinter.CTkButton(master=viewstock,text="View Removed Stock History",command=remove_stock_history)
    viewremovehistory_btn.place(relx = 0.43,rely = 0.2,anchor = customtkinter.CENTER)

    exportremovehistory_btn = customtkinter.CTkButton(master=viewstock,text="Export Removed Stock History to Excel",command=removed_stock_history_to_excel)
    exportremovehistory_btn.place(relx = 0.55,rely = 0.9,anchor = customtkinter.S)

    reset_btn = customtkinter.CTkButton(master=viewstock,text="View Current Stock",command=reset_stock_history)
    reset_btn.place(relx = 0.66,rely = 0.2,anchor = customtkinter.CENTER)

    exportCurrentStock_btn = customtkinter.CTkButton(master=viewstock,text="Export Current Stock to Excel",command=current_stock_history_to_excel)
    exportCurrentStock_btn.place(relx = 0.83,rely = 0.9,anchor = customtkinter.S)

    total_stock_history_btn = customtkinter.CTkButton(master=viewstock,text="View Total Stock History",command=total_stock_history)
    total_stock_history_btn.place(relx = 0.86,rely = 0.2,anchor = customtkinter.CENTER)

    exporttotalhistory_btn = customtkinter.CTkButton(master=viewstock,text="Export Total Stock History to Excel",command=total_stock_history_to_excel)
    exporttotalhistory_btn.place(relx = 0.55,rely = 0.97,anchor = customtkinter.S)
      
def add_stock_window():
    addstock = customtkinter.CTkToplevel()
    addstock.geometry("600x400")
    addstock.resizable(False,False)
    addstock.title("Add Stock")
    addstock.attributes('-topmost', 'true')
    stock.attributes('-topmost', 'false')

    selected_stock = customtkinter.StringVar()
    selected_stock.set("Select a Stock")
    stock_quantity = customtkinter.StringVar()
    stock_unit = customtkinter.StringVar()
    stock_type = customtkinter.StringVar()
    stock_type.set("Select a Stock type")

    stockPath= "data/"
    stocklist = []
    for i,file in enumerate(os.listdir(stockPath)):
        if file.endswith(".json"):
            file_name = os.path.basename(file)
            stock_name = file_name.split('.json')[0]
            stocklist.append(stock_name)


    stocktypes = ["Order","Extra","Other"]

    def add_stock_button_function():
        if(selected_stock.get() == "Select a Stock" or stock_type.get() == "Select a Stock type"):
            tkinter.messagebox.showwarning("Stock Not Select","Select both Stock and Stock Type",parent = addstock)
        else:
            if os.path.isfile("data/Stock_data/all_data.csv") and os.access("data/Stock_data/all_data.csv", os.R_OK):
                Stock_data = [{'Stock Name': selected_stock.get(),'Added Quantity': str(stock_quantity.get()),'Stock Type':stock_type.get(),'Removed Quantity':'----','Buyer Name':'----','Date':str(date.today())}]
                fields = ['Stock Name','Added Quantity','Stock Type','Removed Quantity','Buyer Name','Date']
                with open('data/Stock_data/all_data.csv', 'a',newline='') as file: 
                    writer = csv.DictWriter(file, fieldnames = fields)
                    writer.writerows(Stock_data)
            else:
                Stock_data = [{'Stock Name': selected_stock.get(),'Added Quantity': str(stock_quantity.get()),'Stock Type':stock_type.get(),'Removed Quantity':'----','Buyer Name':'----','Date':str(date.today())}]
                fields = ['Stock Name','Added Quantity','Stock Type','Removed Quantity','Buyer Name','Date']
                with open('data/Stock_data/all_data.csv', 'a',newline='') as file: 
                    writer = csv.DictWriter(file, fieldnames = fields)
                    writer.writeheader()
                    writer.writerows(Stock_data)
            if os.path.isfile("data/Stock_data/addedstock_data.csv") and os.access("data/Stock_data/addedstock_data.csv", os.R_OK):
                Stock_data = [{'Stock Name': selected_stock.get(),'Added Quantity': str(stock_quantity.get()),'Stock Type':stock_type.get(),'Date':str(date.today())}]
                fields = ['Stock Name','Added Quantity','Stock Type','Date']
                with open('data/Stock_data/addedstock_data.csv', 'a',newline='') as file: 
                    writer = csv.DictWriter(file, fieldnames = fields)
                    writer.writerows(Stock_data)
            else:
                Stock_data = [{'Stock Name': selected_stock.get(),'Added Quantity': str(stock_quantity.get()),'Stock Type':stock_type.get(),'Date':str(date.today())}]
                fields = ['Stock Name','Added Quantity','Stock Type','Date']
                with open('data/Stock_data/addedstock_data.csv', 'a',newline='') as file: 
                    writer = csv.DictWriter(file, fieldnames = fields)
                    writer.writeheader()
                    writer.writerows(Stock_data)
            with open('data/' + selected_stock.get() + ".json", 'r') as file:
                data = json.load(file)
                data["Quantity"] += float(stock_quantity.get())
                json_object = json.dumps(data, indent=4)
                with open("data/" + selected_stock.get() + ".json", "w") as outfile:
                    outfile.write(json_object)
            
            tkinter.messagebox.showinfo("Stock Added","The selected stock has been added",parent = addstock)
        

            selected_stock.set("Select a Stock")
            stock_quantity.set(0)
            quantity_entry.delete(0,)
            stock_unit.set("")
            stock_type.set("Select a Stock type")

    add_stock_label = customtkinter.CTkLabel(master=addstock,text="Add Stocks",font=("Arial",50))
    add_stock_label.place(relx=0.05, rely=0.05, anchor=customtkinter.NW)

    selectstock_label = customtkinter.CTkLabel(master=addstock,text="Select Stock:")
    selectstock_label.place(relx=0.05, rely=0.25, anchor=customtkinter.NW)

    stockname_dropdown = customtkinter.CTkOptionMenu(master=addstock,corner_radius=10,variable=selected_stock,values=stocklist,width=200)
    stockname_dropdown.place(relx=0.05, rely=0.32, anchor=customtkinter.NW)
   
    quantity_label = customtkinter.CTkLabel(master=addstock,text="Quantity:")
    quantity_label.place(relx=0.05, rely=0.47, anchor=customtkinter.NW)

    quantity_entry = customtkinter.CTkEntry(master=addstock,textvariable=stock_quantity)
    quantity_entry.place(relx=0.05, rely=0.54, anchor=customtkinter.NW)

    stocktype_label = customtkinter.CTkLabel(master=addstock,text="Select Stock Type:")
    stocktype_label.place(relx=0.35, rely=0.47, anchor=customtkinter.NW)

    stocktype_dropdown = customtkinter.CTkOptionMenu(master=addstock,corner_radius=10,variable=stock_type,values=stocktypes)
    stocktype_dropdown.place(relx=0.35, rely=0.54, anchor=customtkinter.NW)

    add_stock_button = customtkinter.CTkButton(master=addstock,text="Add Stock",width=510,command=add_stock_button_function)
    add_stock_button.place(relx=0.05, rely=0.75, anchor=customtkinter.NW)

def remove_stock_window():
    removestock = customtkinter.CTkToplevel()
    removestock.geometry("600x400")
    removestock.resizable(False,False)
    removestock.title("Remove Stock")
    removestock.attributes('-topmost', 'true')
    stock.attributes('-topmost', 'false')

    selected_stock = customtkinter.StringVar()
    selected_stock.set("Select a Stock")
    stock_quantity = customtkinter.StringVar()
    reason_variable = customtkinter.StringVar()
    reason_variable.set("Select a Reason")

    stockPath= "data/"
    stocklist = []
    for i,file in enumerate(os.listdir(stockPath)):
        if file.endswith(".json"):
            file_name = os.path.basename(file)
            stock_name = file_name.split('.json')[0]
            stocklist.append(stock_name)
    reasons = ["Order Sold","Waste","Other"]

    def removeStockFunction():
        if(selected_stock.get() == "Select a Stock" or reason_variable.get() == "Select a Reason"):
            tkinter.messagebox.showwarning("Stock or Reason Not Select","Select Both Stock and Reason",parent = removestock)
        else:
            with open('data/' + selected_stock.get() + '.json', 'r') as file:
                data = json.load(file)
                if(data["Quantity"] >= float(stock_quantity.get())):
                    if(reason_variable.get() == "Order Sold"):
                        buyernamewindow = customtkinter.CTkToplevel()
                        buyernamewindow.geometry("400x200")
                        buyernamewindow.resizable(False,False)
                        buyernamewindow.title("Buyer Name")
                        buyernamewindow.attributes('-topmost', 'true')
                        removestock.attributes('-topmost','false')

                        buyer_name = customtkinter.StringVar()

                        def remove_stock_btn_buyerwin():
                            if(buyer_name.get() == ""):
                                tkinter.messagebox.showwarning("Buyer Name","Please Enter A Valid Name",parent = buyernamewindow)
                            else:
                                if os.path.isfile("data/Stock_data/all_data.csv") and os.access("data/Stock_data/all_data.csv", os.R_OK):
                                    Stock_data = [{'Stock Name': selected_stock.get(),'Added Quantity': '----','Stock Type':'----','Removed Quantity':str(stock_quantity.get()),'Buyer Name':str(buyer_name.get()),'Date':str(date.today())}]
                                    fields = ['Stock Name','Added Quantity','Stock Type','Removed Quantity','Buyer Name','Date']
                                    with open('data/Stock_data/all_data.csv', 'a',newline='') as file: 
                                        writer = csv.DictWriter(file, fieldnames = fields)
                                        writer.writerows(Stock_data)
                                else:
                                    Stock_data = [{'Stock Name': selected_stock.get(),'Added Quantity': '----','Stock Type':'----','Removed Quantity':str(stock_quantity.get()),'Buyer Name':str(buyer_name.get()),'Date':str(date.today())}]
                                    fields = ['Stock Name','Added Quantity','Stock Type','Removed Quantity','Buyer Name','Date']
                                    with open('data/Stock_data/all_data.csv', 'a',newline='') as file: 
                                        writer = csv.DictWriter(file, fieldnames = fields)
                                        writer.writeheader()
                                        writer.writerows(Stock_data)
                                if os.path.isfile("data/Stock_data/removedstock_data.csv") and os.access("data/Stock_data/removedstock_data.csv", os.R_OK):
                                    Stock_data = [{'Stock Name': selected_stock.get(),'Removed Quantity': str(stock_quantity.get()),'Buyer Name':buyer_name.get(),'Date':str(date.today())}]
                                    fields = ['Stock Name','Removed Quantity','Buyer Name','Date']
                                    with open('data/Stock_data/removedstock_data.csv', 'a',newline='') as file: 
                                        writer = csv.DictWriter(file, fieldnames = fields)
                                        writer.writerows(Stock_data)
                                else:
                                    Stock_data = [{'Stock Name': selected_stock.get(),'Removed Quantity': str(stock_quantity.get()),'Buyer Name':buyer_name.get(),'Date':str(date.today())}]
                                    fields = ['Stock Name','Removed Quantity','Buyer Name','Date']
                                    with open('data/Stock_data/removedstock_data.csv', 'a',newline='') as file: 
                                        writer = csv.DictWriter(file, fieldnames = fields)
                                        writer.writeheader()
                                        writer.writerows(Stock_data)
                                data["Quantity"] = data["Quantity"] - float(stock_quantity.get())
                                json_object = json.dumps(data, indent=4)
                                with open("data/" + selected_stock.get() + ".json", "w") as outfile:
                                    outfile.write(json_object)
                                tkinter.messagebox.showinfo("Stock Removed","The selected stock has been removed",parent = buyernamewindow)
                                reason_variable.set("Select a Reason")
                                selected_stock.set("Select a Stock")
                                stock_quantity.set(0)
                                quantity_entry.delete(0,)
                                buyer_name.set("")
                                buyernamewindow.destroy()


                        buyername_label = customtkinter.CTkLabel(master=buyernamewindow,text="Buyer Name:")
                        buyername_label.place(relx=0.05, rely=0.05, anchor=customtkinter.NW)

                        buyername_entry = customtkinter.CTkEntry(master=buyernamewindow,textvariable=buyer_name,width=200)
                        buyername_entry.place(relx=0.05, rely=0.25, anchor=customtkinter.NW)

                        remove_stock_button = customtkinter.CTkButton(master=buyernamewindow,text="Remove Stock",width=200,command= remove_stock_btn_buyerwin)
                        remove_stock_button.place(relx=0.05, rely=0.55, anchor=customtkinter.NW)
                    else:
                        if os.path.isfile("data/Stock_data/all_data.csv") and os.access("data/Stock_data/all_data.csv", os.R_OK):
                            Stock_data = [{'Stock Name': selected_stock.get(),'Added Quantity': '----','Stock Type':'----','Removed Quantity':str(stock_quantity.get()),'Buyer Name':"No buyer: " + reason_variable.get(),'Date':str(date.today())}]
                            fields = ['Stock Name','Added Quantity','Stock Type','Removed Quantity','Buyer Name','Date']
                            with open('data/Stock_data/all_data.csv', 'a',newline='') as file: 
                                writer = csv.DictWriter(file, fieldnames = fields)
                                writer.writerows(Stock_data)
                        else:
                            Stock_data = [{'Stock Name': selected_stock.get(),'Added Quantity': '----','Stock Type':'----','Removed Quantity':str(stock_quantity.get()),'Buyer Name':"No buyer: " + reason_variable.get(),'Date':str(date.today())}]
                            fields = ['Stock Name','Added Quantity','Stock Type','Removed Quantity','Buyer Name','Date']
                            with open('data/Stock_data/all_data.csv', 'a',newline='') as file: 
                                writer = csv.DictWriter(file, fieldnames = fields)
                                writer.writeheader()
                                writer.writerows(Stock_data)
                        if os.path.isfile("data/Stock_data/removedstock_data.csv") and os.access("data/Stock_data/removedstock_data.csv", os.R_OK):
                            Stock_data = [{'Stock Name': selected_stock.get(),'Removed Quantity': str(stock_quantity.get()),'Buyer Name':"No buyer: " + reason_variable.get(),'Date':str(date.today())}]
                            fields = ['Stock Name','Removed Quantity','Buyer Name','Date']
                            with open('data/Stock_data/removedstock_data.csv', 'a',newline='') as file: 
                                writer = csv.DictWriter(file, fieldnames = fields)
                                writer.writerows(Stock_data)
                        else:
                            Stock_data = [{'Stock Name': selected_stock.get(),'Removed Quantity': str(stock_quantity.get()),'Buyer Name':"No buyer: " + reason_variable.get(),'Date':str(date.today())}]
                            fields = ['Stock Name','Removed Quantity','Buyer Name','Date']
                            with open('data/Stock_data/removedstock_data.csv', 'a',newline='') as file: 
                                writer = csv.DictWriter(file, fieldnames = fields)
                                writer.writeheader()
                                writer.writerows(Stock_data)
                        data["Quantity"] = data["Quantity"] - float(stock_quantity.get())
                        json_object = json.dumps(data, indent=4)
                        with open("data/" + selected_stock.get() + ".json", "w") as outfile:
                            outfile.write(json_object)
                            tkinter.messagebox.showinfo("Stock Removed","Stock Removed Succesfully",parent = removestock)
                        selected_stock.set("Select a Stock")
                        reason_variable.set("Select a Reason")
                        stock_quantity.set(0)
                        quantity_entry.delete(0,)
                else:
                    tkinter.messagebox.showwarning("Quantity Error","There is not sufficient stock quantity. Current Quantity present " + str(data["Quantity"]),parent = removestock)



    add_stock_label = customtkinter.CTkLabel(master=removestock,text="Remove Stocks",font=("Arial",50))
    add_stock_label.place(relx=0.05, rely=0.05, anchor=customtkinter.NW)

    selectstock_label = customtkinter.CTkLabel(master=removestock,text="Select Stock:")
    selectstock_label.place(relx=0.05, rely=0.25, anchor=customtkinter.NW)

    stockname_dropdown = customtkinter.CTkOptionMenu(master=removestock,corner_radius=10,variable=selected_stock,values=stocklist,width= 200)
    stockname_dropdown.place(relx=0.05, rely=0.32, anchor=customtkinter.NW)
    
    quantity_label = customtkinter.CTkLabel(master=removestock,text="Quantity:")
    quantity_label.place(relx=0.05, rely=0.47, anchor=customtkinter.NW)

    quantity_entry = customtkinter.CTkEntry(master=removestock,textvariable=stock_quantity)
    quantity_entry.place(relx=0.05, rely=0.54, anchor=customtkinter.NW)

    removereason_label = customtkinter.CTkLabel(master=removestock,text="Reason:")
    removereason_label.place(relx=0.3, rely=0.47, anchor=customtkinter.NW)

    removereason_dropdown = customtkinter.CTkOptionMenu(master=removestock,corner_radius=10,variable=reason_variable,values=reasons)
    removereason_dropdown.place(relx=0.3, rely=0.54, anchor=customtkinter.NW)
    
    remove_stock_button = customtkinter.CTkButton(master=removestock,text="Remove Stock",width=510,command=removeStockFunction)
    remove_stock_button.place(relx=0.05, rely=0.75, anchor=customtkinter.NW)

def add_item_window():
    additem = customtkinter.CTkToplevel()
    additem.geometry("600x400")
    additem.resizable(False,False)
    additem.title("Add Stock")
    additem.attributes('-topmost', 'true')

    item_name = customtkinter.StringVar()
    stock_quantity = customtkinter.StringVar()
    stock_unit = customtkinter.StringVar()
    item_name.set("")
    stock_quantity.set("")
    stock_unit.set("")

    def create_item():

        if os.path.isfile("data/" + item_name.get() + ".json") and os.access("data/" + item_name.get() + ".json", os.R_OK):
            tkinter.messagebox.showwarning("Item Already Present","The Item You are trying to add is already present",parent = additem)
            item_name.set("")
            stock_quantity.set("")
            stock_unit.set("")
        else:
            if(item_name.get() == "" or stock_unit.get() == ""):
                tkinter.messagebox.showwarning("Item Name Error","Please type a valid item name and unit",parent = additem)
            else:
                try:
                    quantityvar = float(stock_quantity.get())
                    print(quantityvar)
                    if os.path.isfile("data/Stock_data/all_data.csv") and os.access("data/Stock_data/all_data.csv", os.R_OK):
                        Stock_data = [{'Stock Name': item_name.get(),'Added Quantity': str(stock_quantity.get()),'Stock Type':"Intial Stock",'Removed Quantity':'----','Buyer Name':'----','Date':str(date.today())}]
                        fields = ['Stock Name','Added Quantity','Stock Type','Removed Quantity','Buyer Name','Date']
                        with open('data/Stock_data/all_data.csv', 'a',newline='') as file: 
                            writer = csv.DictWriter(file, fieldnames = fields)
                            writer.writerows(Stock_data)
                    else:
                        Stock_data = [{'Stock Name': item_name.get(),'Added Quantity': str(stock_quantity.get()),'Stock Type':"Intial Stock",'Removed Quantity':'----','Buyer Name':'----','Date':str(date.today())}]
                        fields = ['Stock Name','Added Quantity','Stock Type','Removed Quantity','Buyer Name','Date']
                        with open('data/Stock_data/all_data.csv', 'a',newline='') as file: 
                            writer = csv.DictWriter(file, fieldnames = fields)
                            writer.writeheader()
                            writer.writerows(Stock_data)
                    if os.path.isfile("data/Stock_data/addedstock_data.csv") and os.access("data/Stock_data/addedstock_data.csv", os.R_OK):
                        Stock_data = [{'Stock Name': item_name.get(),'Added Quantity': str(stock_quantity.get()),'Stock Type':"Intial Stock",'Date':str(date.today())}]
                        fields = ['Stock Name','Added Quantity','Stock Type','Date']
                        with open('data/Stock_data/addedstock_data.csv', 'a',newline='') as file: 
                            writer = csv.DictWriter(file, fieldnames = fields)
                            writer.writerows(Stock_data)
                    else:
                        Stock_data = [{'Stock Name': item_name.get(),'Added Quantity': str(stock_quantity.get()),'Stock Type':"Initial Stock",'Date':str(date.today())}]
                        fields = ['Stock Name','Added Quantity','Stock Type','Date']
                        with open('data/Stock_data/addedstock_data.csv', 'a',newline='') as file: 
                            writer = csv.DictWriter(file, fieldnames = fields)
                            writer.writeheader()
                            writer.writerows(Stock_data)
                    stockdata = {
                        "Stock Name":item_name.get(),
                        "Quantity":float(stock_quantity.get()),
                        "unit":stock_unit.get()
                    }
                    json_object = json.dumps(stockdata, indent=4)
                    with open("data/" + item_name.get() + ".json", "w") as outfile:
                        outfile.write(json_object)
                    tkinter.messagebox.showinfo("Item Adeed","The Item has been added",parent = additem)
                    item_name.set("")
                    stock_quantity.set("")
                    stock_unit.set("")
                except:
                    tkinter.messagebox.showwarning("Item Quantity Error","Please type a valid Quantity",parent = additem)

    add_item_label = customtkinter.CTkLabel(master=additem,text="Add Items",font=("Arial",50))
    add_item_label.place(relx=0.05, rely=0.05, anchor=customtkinter.NW)

    itemname_label = customtkinter.CTkLabel(master=additem,text="Item Name:")
    itemname_label.place(relx=0.05, rely=0.25, anchor=customtkinter.NW)

    itemname_entry = customtkinter.CTkEntry(master=additem,corner_radius=10,textvariable=item_name,width=200)
    itemname_entry.place(relx=0.05, rely=0.32, anchor=customtkinter.NW)

    quantity_label = customtkinter.CTkLabel(master=additem,text="Present Quantity:")
    quantity_label.place(relx=0.05, rely=0.47, anchor=customtkinter.NW)

    quantity_entry = customtkinter.CTkEntry(master=additem,textvariable=stock_quantity)
    quantity_entry.place(relx=0.05, rely=0.54, anchor=customtkinter.NW)

    unit_label = customtkinter.CTkLabel(master=additem,text="Units:")
    unit_label.place(relx=0.35, rely=0.47, anchor=customtkinter.NW)

    unit_entry = customtkinter.CTkEntry(master=additem,textvariable=stock_unit)
    unit_entry.place(relx=0.35, rely=0.54, anchor=customtkinter.NW)

    add_item_button = customtkinter.CTkButton(master=additem,text="Add Item",width=510,command=create_item)
    add_item_button.place(relx=0.05, rely=0.75, anchor=customtkinter.NW)

def remove_item_window():
    removeitem = customtkinter.CTkToplevel()
    removeitem.geometry("600x400")
    removeitem.resizable(False,False)
    removeitem.title("Remove Items")
    removeitem.attributes('-topmost', 'true')

    selected_stock = customtkinter.StringVar()
    selected_stock.set("Select a Item")
    stockPath= "data/"
    stocklist = []
    for i,file in enumerate(os.listdir(stockPath)):
        if file.endswith(".json"):
            file_name = os.path.basename(file)
            stock_name = file_name.split('.json')[0]
            stocklist.append(stock_name)
    
    def removeitemfunction():
        if(selected_stock.get() == "Select a Item"):
            tkinter.messagebox.showwarning("Item Not Select","Select a Item",parent = removeitem)
        else:
            if os.path.isfile("data/Stock_data/all_data.csv") and os.access("data/Stock_data/all_data.csv", os.R_OK):
                Stock_data = [{'Stock Name': selected_stock.get(),'Added Quantity': '----','Stock Type':'----','Removed Quantity':'Item Removed','Buyer Name':'----','Date':str(date.today())}]
                fields = ['Stock Name','Added Quantity','Stock Type','Removed Quantity','Buyer Name','Date']
                with open('data/Stock_data/all_data.csv', 'a',newline='') as file: 
                    writer = csv.DictWriter(file, fieldnames = fields)
                    writer.writerows(Stock_data)
            else:
                Stock_data = [{'Stock Name': selected_stock.get(),'Added Quantity': '----','Stock Type':'----','Removed Quantity':'Item Removed','Buyer Name':'----','Date':str(date.today())}]
                fields = ['Stock Name','Added Quantity','Stock Type','Removed Quantity','Buyer Name','Date']
                with open('data/Stock_data/all_data.csv', 'a',newline='') as file: 
                    writer = csv.DictWriter(file, fieldnames = fields)
                    writer.writeheader()
                    writer.writerows(Stock_data)
            os.remove("data/" + selected_stock.get() + ".json")
            stocklist.pop(stocklist.index(selected_stock.get()))
            tkinter.messagebox.showinfo("Item Removed","Item has been Removed",parent = removeitem)
            selected_stock.set("Select a Item")
    
    selectstock_label = customtkinter.CTkLabel(master=removeitem,text="Select Item:")
    selectstock_label.place(relx=0.05, rely=0.25, anchor=customtkinter.NW)

    stockname_dropdown = customtkinter.CTkOptionMenu(master=removeitem,corner_radius=10,variable=selected_stock,values=stocklist,width=200)
    stockname_dropdown.place(relx=0.05, rely=0.32, anchor=customtkinter.NW)

    add_stock_button = customtkinter.CTkButton(master=removeitem,text="Remove Item",width=510,command=removeitemfunction)
    add_stock_button.place(relx=0.05, rely=0.75, anchor=customtkinter.NW)

Stock_item_btn = customtkinter.CTkButton(master=app, text="Stock Items", command=stock_item_window)
Stock_item_btn.place(relx=0.05, rely=0.05, anchor=customtkinter.NW)

new_item_btn = customtkinter.CTkButton(master=app, text="Add Items", command=add_item_window)
new_item_btn.place(relx=0.25, rely=0.05, anchor=customtkinter.NW)

new_item_btn = customtkinter.CTkButton(master=app, text="Remove Items", command=remove_item_window)
new_item_btn.place(relx=0.45, rely=0.05, anchor=customtkinter.NW)

app.mainloop()