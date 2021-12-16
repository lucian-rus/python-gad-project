from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from database import *
from scraper import *
from exporter import *

window = Tk()
window.title('covidscraper')
window.geometry('800x500')
window.resizable(False, False)

country_list = []
scraped_data = []

variable = StringVar()
variable.set('select country')
enable_debug_var = IntVar();

def test_database():
    connection = database_connect()
    if connection:
         messagebox.showinfo(title="info", message="database connected")
    else:
        messagebox.showerror(title="error", message="could not connect to database!")

def get_scraped_data():
    data = init_scraper('#main_table_countries_yesterday tr')

    iid_counter = 0
    for obj in data:
        table.insert(parent='', index='end', iid=iid_counter, text='', values=(obj.id,obj.country_name,obj.new_cases,obj.new_deaths,obj.population))
        iid_counter += 1
        country_list.append(obj.country_name)
        scraped_data.append(obj)

    country_list.sort();
    messagebox.showinfo(title="info", message="data retrieved")

def save_to_db():
    if scraped_data:
        table_title = database_get_table();
        database_insert_to_table(table_title, scraped_data);
        messagebox.showinfo(title="info", message="saved to the database as:" + table_title)
    else:
        messagebox.showerror(title="error", message="empty list!")

def export_to_csv():
    if scraped_data:
        exporter_to_csv(scraped_data, 'export.csv')
        messagebox.showinfo(title="info", message="exported to .csv file: output/export.csv")
    else:
        messagebox.showerror(title="error", message="empty list!")

def clear_table():
    if scraped_data:
        country_list.clear()
        scraped_data.clear()
        table.delete(*table.get_children())
    else:
        messagebox.showerror(title="error", message="empty table!")

table_frame = Frame(window)
table = ttk.Treeview(table_frame)

table['columns'] = ('country_id', 'country_name', 'new_cases', 'new_deaths', 'population')

table.column('#0', width=0,  stretch=NO)
table.column('country_id',anchor=CENTER, width=120)
table.column('country_name',anchor=CENTER,width=120)
table.column('new_cases',anchor=CENTER,width=120)
table.column('new_deaths',anchor=CENTER,width=120)
table.column('population',anchor=CENTER,width=120)

table.heading('#0',text='',anchor=CENTER)
table.heading('country_id',text='id',anchor=CENTER)
table.heading('country_name',text='country',anchor=CENTER)
table.heading('new_cases',text='new cases',anchor=CENTER)
table.heading('new_deaths',text='new deaths',anchor=CENTER)
table.heading('population',text='population',anchor=CENTER)

db_new_table_btn = Button(window, text ='test database', command = test_database, highlightthickness=0)
db_new_table_btn.place(x=30, y=100, width=120, height=25)

scrape_btn = Button(window, text ='scrape', command = get_scraped_data, highlightthickness=0)
scrape_btn.place(x=30, y=140, width=120, height=25)

clear_btn = Button(window, text ='clear', command = clear_table, highlightthickness=0)
clear_btn.place(x=30, y=180, width=120, height=25)

save_to_db_btn = Button(window, text ='save to database', command = save_to_db, highlightthickness=0)
save_to_db_btn.place(x=30, y=220, width=120, height=25)

export_csv_btn = Button(window, text ='export to csv', command = export_to_csv, highlightthickness=0)
export_csv_btn.place(x=30, y=260, width=120, height=25)

table_frame.place(x=180, y=100, width=610, height=300)
table.pack()

window.mainloop()
