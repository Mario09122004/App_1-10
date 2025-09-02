from tkinter import *
from backend import Database

db = Database()

def view_all_books():
    list1.delete(0, END)
    for row in db.view_all():
        list1.insert(END, f"{row[0]} | {row[1]} | {row[2]} | {row[3]} | {row[4]}")

def search_books(event=None):
    query = search_var.get().lower()
    list1.delete(0, END)
    for row in db.view_all():
        book_str = f"{row[0]} | {row[1]} | {row[2]} | {row[3]} | {row[4]}"
        if query in book_str.lower():
            list1.insert(END, book_str)

def add_entry():
    db.insert(title_var.get(), author_var.get(), year_var.get(), isbn_var.get())
    view_all_books()

def get_selected_row(event):
    global selected_tuple
    try:
        index = list1.curselection()[0]
        selected_id = int(list1.get(index).split('|')[0].strip())
        for row in db.view_all():
            if row[0] == selected_id:
                selected_tuple = row
                break
        e1.delete(0, END)
        e1.insert(END, selected_tuple[1])
        e2.delete(0, END)
        e2.insert(END, selected_tuple[2])
        e3.delete(0, END)
        e3.insert(END, selected_tuple[3])
        e4.delete(0, END)
        e4.insert(END, selected_tuple[4])
    except IndexError:
        pass

def update_selected():
    try:
        db.update(selected_tuple[0], title_var.get(), author_var.get(), year_var.get(), isbn_var.get())
        view_all_books()
    except NameError:
        pass

def delete_selected():
    try:
        db.delete(selected_tuple[0])
        view_all_books()
    except NameError:
        pass

#View
window = Tk()
window.title("Book Store")

Label(window, text="Title").grid(row=1, column=0)
Label(window, text="Author").grid(row=1, column=2)
Label(window, text="Year").grid(row=2, column=0)
Label(window, text="ISBN").grid(row=2, column=2)
Label(window, text="Search:").grid(row=0, column=0, sticky=W)

title_var = StringVar()
author_var = StringVar()
year_var = StringVar()
isbn_var = StringVar()
search_var = StringVar()

e1 = Entry(window, textvariable=title_var)
e1.grid(row=1, column=1)
e2 = Entry(window, textvariable=author_var)
e2.grid(row=1, column=3)
e3 = Entry(window, textvariable=year_var)
e3.grid(row=2, column=1)
e4 = Entry(window, textvariable=isbn_var)
e4.grid(row=2, column=3)
e_search = Entry(window, textvariable=search_var, width=60)
e_search.grid(row=0, column=1, columnspan=3, sticky=W)

list1 = Listbox(window, height=12, width=80)
list1.grid(row=3, column=0, columnspan=4)
sb1 = Scrollbar(window)
sb1.grid(row=3, column=4, rowspan=6)
list1.config(yscrollcommand=sb1.set)
sb1.config(command=list1.yview)

list1.bind('<<ListboxSelect>>', get_selected_row)
search_var.trace("w", lambda *args: search_books())

Button(window, text="Add entry", width=12, command=add_entry).grid(row=4, column=5)
Button(window, text="Update selected", width=12, command=update_selected).grid(row=5, column=5)
Button(window, text="Delete selected", width=12, command=delete_selected).grid(row=6, column=5)
Button(window, text="Close", width=12, command=window.destroy).grid(row=7, column=5)

view_all_books()

window.mainloop()
