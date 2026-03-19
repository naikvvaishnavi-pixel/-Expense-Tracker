from Database import conn,cursor
import tkinter
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
cursor=conn.cursor()
def open_view_window(username):
    view_win = tk.Toplevel()
    view_win .geometry("800x500")
    view_win.title("View Expense")
    view_win.configure(bg="#D2B48C")

    bg = tk.PhotoImage(file="D:/Python_code/Project/image.png")
    bg_label = tk.Label(view_win, image=bg)
    bg_label.image = bg  # prevent image disappearing
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)

    # -------- TABLE FRAME --------
    table_frame = tk.Frame(view_win, bg="#D2B48C")
    table_frame.pack(pady=10)

    # -------- TREEVIEW (TABLE) --------
    columns = ("Date", "Category", "Amount", "Description")

    tree = ttk.Treeview(
        table_frame,
        columns=columns,
        show="headings",
        height=10
    )

    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=150, anchor="center")

    tree.pack()

    # -------- SCROLLBAR --------
    scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=tree.yview)
    tree.configure(yscroll=scrollbar.set)
    scrollbar.pack(side="right", fill="y")

    # -------- FUNCTIONS --------
    def load_expenses():
        # Clear existing data
        for row in tree.get_children():
            tree.delete(row)

        cursor.execute(
            "SELECT id, date, category, amount, description FROM expenses WHERE username=?",
            (username,)
        )
        rows = cursor.fetchall()

        total = 0

        for row in rows:
            expense_id, date, category, amount, description = row
            total += amount
            tree.insert("", "end", values=(date, category, amount, description), iid=expense_id)

        total_label.config(text=f"Total Expense: ₹ {total:.2f}")

    def delete_expense():
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Select an expense to delete")
            return

        expense_id = selected[0]

        confirm = messagebox.askyesno("Confirm", "Delete selected expense?")
        if confirm:
            cursor.execute("DELETE FROM expenses WHERE id=?", (expense_id,))
            conn.commit()
            load_expenses()
            messagebox.showinfo("Success", "Expense Deleted Successfully")

    def go_back():
        view_win.destroy()

    # -------- BUTTON FRAME --------
    btn_frame = tk.Frame(view_win, bg="#D2B48C")
    btn_frame.pack(pady=15)

    delete_btn = tk.Button(
        btn_frame,
        text="Delete Selected",
        font=("Times", 12, "bold"),
        width=18,
        bg="red",
        fg="white",
        command=delete_expense
    )
    delete_btn.pack(side="left", padx=10)

    back_btn = tk.Button(
        btn_frame,
        text="← Back",
        font=("Times", 12, "bold"),
        width=12,
        bg="#8B4513",
        fg="white",
        command=go_back
    )
    back_btn.pack(side="left", padx=10)

    # -------- TOTAL LABEL --------
    total_label = tk.Label(
        view_win,
        text="Total Expense: ₹ 0.00",
        font=("Times", 16, "bold"),
        bg="#D2B48C"
    )
    total_label.pack(pady=10)

    # Load data when window opens
    load_expenses()
