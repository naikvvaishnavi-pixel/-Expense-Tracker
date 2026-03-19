
import Register
import HomePage
import tkinter as tk
from Database import conn, cursor
from tkinter import messagebox

def open_login():
    root = tk.Tk()
    root.geometry("800x500")
    root.title("LOGIN")

    bg = tk.PhotoImage(file="D:/Python_code/Project/image.png")  
    bg_label = tk.Label(root, image=bg)
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)


    loginlabel = tk.Label(root, text="LOGIN", font=("Times", 30, "bold"), bg="#D2B48C")
    loginlabel.place(relx=0.5, rely=0.1, anchor="center")


    userlabel = tk.Label(root, text="Username", font=("Times", 14), bg="#D2B48C")
    userlabel.place(relx=0.5, rely=0.25, anchor="center")

    usertextbox = tk.Entry(root, font=("Times", 16), width=20)
    usertextbox.place(relx=0.5, rely=0.32, anchor="center")


    passlabel = tk.Label(root, text="Password", font=("Times", 14), bg="#D2B48C")
    passlabel.place(relx=0.5, rely=0.42, anchor="center")

    passtextbox = tk.Entry(root, font=("Times", 16), width=20, show="*")
    passtextbox.place(relx=0.5, rely=0.49, anchor="center")


    def submit():
        username = usertextbox.get()
        password = passtextbox.get()

        if username == "" or password == "":
            messagebox.showwarning("Warning", "Enter all the data")
            return

        cursor.execute(
            "SELECT * FROM users WHERE Username=? AND Password=?",
            (username, password)
        )

        user = cursor.fetchone()

        if user:
            messagebox.showinfo("Success", "Login successful")
            HomePage.open_HomePage(username)
            root.withdraw()
        else:
            messagebox.showerror("Error", "Invalid username or password")


    submitbutton = tk.Button(root,text="Submit",command=submit,font=("Times", 14, "bold"),width=15,height=2,bg="#8B4513",fg="white")
    submitbutton.place(relx=0.5, rely=0.62, anchor="center")


    def openregister():
        Register.open_register_window()

    newuser = tk.Label(root, text="New User?", font=("Times", 12), bg="#D2B48C")
    newuser.place(relx=0.4, rely=0.75, anchor="center")

    register_btn = tk.Button(root,text="Register",command=openregister,font=("Times", 12, "bold"),width=10,height=1,bg="#A0522D",fg="white")
    register_btn.place(relx=0.6, rely=0.75, anchor="center")

    root.mainloop()
