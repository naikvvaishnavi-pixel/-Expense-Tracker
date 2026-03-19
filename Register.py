from Database import conn, cursor
import tkinter as tk
from tkinter import messagebox

cursor = conn.cursor()

def open_register_window():
    reg_win = tk.Toplevel()
    reg_win.geometry("800x500")
    reg_win.title("Register Page")

    # Background Image
    bg = tk.PhotoImage(file="D:/Python_code/Project/image.png")
    bg_label = tk.Label(reg_win, image=bg)
    bg_label.image = bg  # VERY IMPORTANT
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)

   
    # Title
    reg_label = tk.Label(
        reg_win,
        text="REGISTRATION",
        font=("Times", 22, "bold"),
        bg="#D2B48C",
        fg="black"
    )
    reg_label.pack(pady=10)

    # Name
    name_label = tk.Label(
        reg_win,
        text="Name",
        font=("Times", 14, "bold"),
        bg="#D2B48C"
    )
    name_label.pack(pady=(10, 2))
    nametextbox = tk.Entry(
        reg_win,
        width=30,
        font=("Times", 14),
        justify="center"
    )
    nametextbox.pack()

    # Username
    user_label = tk.Label(
        reg_win,
        text="Username",
        font=("Times", 14, "bold"),
        bg="#D2B48C"
    )
    user_label.pack(pady=(15,2))
    usertextbox = tk.Entry(
        reg_win,
        width=30,
        font=("Times", 14),
        justify="center"
    )
    usertextbox.pack()

    # Password
    pass_label = tk.Label(
        reg_win,
        text="Password",
        font=("Times", 14, "bold"),
        bg="#D2B48C"
    )
    pass_label.pack(pady=(15, 2))
    passtextbox = tk.Entry(
        reg_win,
        show="*",
        width=30,
        font=("Times", 14),
        justify="center"
    )
    passtextbox.pack()

    def register():
        name = nametextbox.get()
        username = usertextbox.get()
        password = passtextbox.get()

        if name == "" or username == "" or password == "":
            messagebox.showwarning("Warning", "All fields are required")
            return
        try:
            cursor.execute(
                "INSERT INTO users(Name, Username, Password) VALUES(?,?,?)",
                (name, username, password)
            )
            conn.commit()
            messagebox.showinfo("Success", "Registration successful")
        except:
            messagebox.showerror("Error", "Username already exists")

    # Register Button
    regbutton = tk.Button(
        reg_win,
        text="Register",
        font=("Times", 14, "bold"),
        width=20,
        bg="#8B4513",
        fg="white",
        cursor="hand2",
        command=register
    )
    regbutton.pack(pady=20)

    def back():
        reg_win.destroy()

    # Back to Login Button
    backbutton = tk.Button(
        reg_win,
        text="Back to Login",
        font=("Times", 11),
        width=20,
        bg="#D2B48C",
        cursor="hand2",
        command=back
    )
    backbutton.pack(pady=5)

    reg_win.mainloop()