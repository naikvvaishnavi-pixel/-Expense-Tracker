import Add_Expense
import Weekly_Expense
import View_Expense
import ReportModule 
from Database import conn,cursor
import tkinter
import tkinter as tk
from tkinter import messagebox
cursor=conn.cursor()

def open_HomePage(username):
    hom_win = tk.Toplevel()
    hom_win.geometry("800x500")
    hom_win.title("Home Page")
    hom_win.configure(bg="#D2B48C")

    bg = tk.PhotoImage(file="D:/Python_code/Project/image.png")  # Keep image in project folder
    bg_label = tk.Label(hom_win, image=bg)
    bg_label.image = bg  # VERY IMPORTANT (prevents image disappearing)
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)

    hellolabel=tkinter.Label(hom_win,text=f"HELLO,{username}!",bg="#D2B48C",font=("Times", 20))
    hellolabel.pack()


    def Add_expense():
        Add_Expense.open_Add_window(username)

    Add_button=tk.Button(hom_win,font=("Times",11),width=25,height=2,text="Add Expense",command=Add_expense)
    Add_button.pack(anchor=tkinter.W, padx=10,pady=20)

    def WM_Expense():
        Weekly_Expense.open_WM_window(username)

    week_button=tk.Button(hom_win,font=("Times",11),width=25,height=2,text="weekly & Monthly Expense",command=WM_Expense)
    week_button.pack(anchor=tkinter.W, padx=10,pady=25)

    def view_Expense():
        View_Expense.open_view_window(username)

    view_button=tk.Button(hom_win,font=("Times",11),width=25,height=2,text="View Expense",command=view_Expense)
    view_button.pack(anchor=tkinter.W,padx=10,pady=20)

    
    def report_Expense():
        ReportModule.open_report_window(username)

    report_button=tk.Button(hom_win,font=("Times",11),width=25,height=2,text="Report",command=report_Expense)
    report_button.pack(anchor=tkinter.W, padx=10,pady=25)
    
    
    def back():
        hom_win.destroy() 
    logout_button=tk.Button(hom_win,font=("Times",11),width=25,height=2,text="LOGOUT",command=back)
    logout_button.pack(anchor=tkinter.W, padx=10,pady=25)