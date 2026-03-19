from tkcalendar import DateEntry
from Database import conn, cursor
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk  # CORRECT IMPORT

cursor = conn.cursor()

def open_Add_window(username):
    add_win = tk.Toplevel()
    add_win.geometry("800x500")
    add_win.title("AddExpense")
    add_win.configure(bg="#D2B48C")

    bg = tk.PhotoImage(file="D:/Python_code/Project/image.png")  # Keep image in project folder
    bg_label = tk.Label(add_win, image=bg)
    bg_label.image = bg  # VERY IMPORTANT (prevents image disappearing)
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)

    # ---------- DATE ----------
    date_label = tk.Label(add_win, text="Date", font=("Times", 14, "bold"), bg="#D2B48C")
    date_label.pack(pady=(5))

    date_entry = DateEntry(add_win,width=20,background="darkblue",foreground="white",borderwidth=2,date_pattern="yyyy-mm-dd")
    date_entry.pack(pady=5)

    # ---------- CATEGORY ----------
    category_label = tk.Label(add_win, text="Category", font=("Times", 14, "bold"), bg="#D2B48C")
    category_label.pack(pady=(15, 5))

    category_combo = ttk.Combobox(
        add_win,
        font=("Times", 12),
        width=27,
        state="readonly",
        values=["Food", "Travel", "Shopping", "Bills", "Others"]
    )
    category_combo.set("Select Category")
    category_combo.pack(pady=5)

    # ---------- AMOUNT ----------
    amount_label = tk.Label(add_win, text="Amount", font=("Times", 14, "bold"), bg="#D2B48C")
    amount_label.pack(pady=(15, 5))

    amount_entry = tk.Entry(add_win, font=("Times", 12), width=30)
    amount_entry.pack(pady=5)

    # ---------- DESCRIPTION ----------
    desc_label = tk.Label(add_win, text="Description", font=("Times", 14, "bold"), bg="#D2B48C")
    desc_label.pack(pady=(15, 5))

    desc_text = tk.Text(add_win, font=("Times", 12), width=30, height=4)
    desc_text.pack(pady=5)

    

    # ---------- FUNCTIONS ----------
    def clear_fields():
        date_entry.set_date(date_entry._date)
        category_combo.set("Select Category")
        amount_entry.delete(0, tk.END)
        desc_text.delete("1.0", tk.END)

    def update_total():
        cursor.execute(
            "SELECT SUM(amount) FROM expenses WHERE username=?",(username,))
        total = cursor.fetchone()[0]
        if total is None:
            total = 0
        total_label.config(text=f"Total Expense: ₹ {total:.2f}")

    def add_expense():
        date = date_entry.get()
        category = category_combo.get()
        amount = amount_entry.get()
        description = desc_text.get("1.0", tk.END).strip()

        if date == "" or category == "Select Category" or amount == "":
            messagebox.showwarning("Warning", "Please fill all fields")
            return

        try:
            amount = float(amount)
        except:
            messagebox.showerror("Error", "Amount must be a number")
            return

        cursor.execute(
            "INSERT INTO expenses (username,date, category, amount, description) VALUES (?, ?, ?, ?, ?)",
            (username,date, category, amount, description)
        )
        conn.commit()

        messagebox.showinfo("Success", "Expense Added Successfully")
        clear_fields()
        update_total()

    # ---------- BUTTON FRAME ----------
    btn_frame = tk.Frame(add_win, bg="#D2B48C")
    btn_frame.pack(pady=25)

    add_btn = tk.Button(
        btn_frame,
        text="Add Expense",
        font=("Times", 12, "bold"),
        width=15,
        bg="#4CAF50",
        fg="white",
        command=add_expense
    )
    add_btn.pack(side="left", padx=15)

    clear_btn = tk.Button(
        btn_frame,
        text="Clear",
        font=("Times", 12, "bold"),
        width=15,
        bg="red",
        fg="white",
        command=clear_fields
    )
    clear_btn.pack(side="left", padx=15)

    back_btn = tk.Button(
    add_win,
    text="← Back",
    font=("Times", 12, "bold"),
    width=10,
    bg="#8B4513",
    fg="white",
    command=add_win.destroy  # THIS keeps you on HomePage
    )
    back_btn.pack(pady=10)

    # ---------- TOTAL ----------
    total_label = tk.Label(
        add_win,
        text="Total Expense: ₹ 0.00",
        font=("Times", 14, "bold"),
        bg="#D2B48C"
    )
    total_label.pack(pady=10)

    update_total()
    