import tkinter as tk
import LoginPage  # IMPORTANT: your login file name

def open_start_page():
    start_win = tk.Tk()
    start_win.geometry("800x500")
    start_win.title("Welcome")

    # -------- BACKGROUND IMAGE --------
    bg = tk.PhotoImage(file="D:/Python_code/Project/image5.png")
    bg_label = tk.Label(start_win, image=bg)
    bg_label.image = bg  # Prevent image from disappearing
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)

    # -------- FUNCTION TO OPEN LOGIN --------
    def go_to_login():
        start_win.destroy()   # Close start page
        LoginPage.open_login()    # Open login window

    # -------- START BUTTON --------
    start_btn = tk.Button(
        start_win,
        text="GO",
        font=("Times", 20, "bold"),
        width=10,
        height=1,
        bg="#8B4513",
        fg="white",
        command=go_to_login
    )
    start_btn.place(relx=0.90, rely=0.90, anchor="se")

    start_win.mainloop()