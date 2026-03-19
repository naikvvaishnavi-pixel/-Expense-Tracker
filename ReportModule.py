from Database import conn, cursor
import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from datetime import datetime


def open_report_window(username):
    rep_win = tk.Toplevel()
    rep_win.geometry("800x500")
    rep_win.title("Expense Report")
    rep_win.configure(bg="#D2B48C")

    bg = tk.PhotoImage(file="D:/Python_code/Project/image.png")
    bg_label = tk.Label(rep_win, image=bg)
    bg_label.image = bg  # prevent image disappearing
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)


    # ---------- DATE FRAME ----------
    date_frame = tk.Frame(rep_win, bg="#D2B48C")
    date_frame.pack(pady=5)

    # From Date
    from_label = tk.Label(
        date_frame,
        text="From Date (DD-MM-YYYY):",
        font=("Times", 12, "bold"),
        bg="#D2B48C"
    )
    from_label.grid(row=0, column=0, padx=10)

    from_date_entry = tk.Entry(date_frame, font=("Arial", 12), width=15)
    from_date_entry.grid(row=0, column=1, padx=10)

    # To Date
    to_label = tk.Label(
        date_frame,
        text="To Date (DD-MM-YYYY):",
        font=("Times", 12, "bold"),
        bg="#D2B48C"
    )
    to_label.grid(row=0, column=2, padx=10)

    to_date_entry = tk.Entry(date_frame, font=("Times", 12), width=15)
    to_date_entry.grid(row=0, column=3, padx=10)

    # ---------- TABLE FRAME ----------
    table_frame = tk.Frame(rep_win)
    table_frame.pack(pady=15)

    columns = ("Date", "Category", "Amount", "Description")

    tree = ttk.Treeview(
        table_frame,
        columns=columns,
        show="headings",
        height=12
    )

    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=150, anchor="center")

    tree.pack(side="left")

    scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)
    scrollbar.pack(side="right", fill="y")

    # ---------- TOTAL LABEL ----------
    total_label = tk.Label(
        rep_win,
        text="Total Expense: ₹ 0.00",
        font=("Times", 14, "bold"),
        bg="#D2B48C"
    )
    total_label.pack(pady=5)

    # ---------- FUNCTION: CONVERT DATE ----------
    def convert_to_sql_date(date_str):
        # Converts DD-MM-YYYY → YYYY-MM-DD (for SQLite comparison)
        date_obj = datetime.strptime(date_str, "%d-%m-%Y")
        return date_obj.strftime("%Y-%m-%d")

    # ---------- SEARCH FUNCTION ----------
    def search_expenses():
        from_date = from_date_entry.get()
        to_date = to_date_entry.get()

        if from_date == "" or to_date == "":
            messagebox.showwarning("Warning", "Enter both dates")
            return

        try:
            # Validate and convert dates
            from_sql = convert_to_sql_date(from_date)
            to_sql = convert_to_sql_date(to_date)
        except:
            messagebox.showerror("Error", "Date format must be DD-MM-YYYY")
            return

        # Clear table
        for row in tree.get_children():
            tree.delete(row)

        # CORRECT QUERY (with converted dates)
        cursor.execute("""
            SELECT date, category, amount, description
            FROM expenses
            WHERE username = ?
            AND date BETWEEN ? AND ?
            ORDER BY date
        """, (username, from_sql, to_sql))

        rows = cursor.fetchall()

        total = 0
        for row in rows:
            tree.insert("", tk.END, values=row)
            total += float(row[2])

        total_label.config(text=f"Total Expense: ₹ {total:.2f}")

        if not rows:
            messagebox.showinfo("Info", "No expenses found for selected dates")

    # ---------- PIE CHART FUNCTION ----------
    def show_pie_chart():
        from_date = from_date_entry.get()
        to_date = to_date_entry.get()

        if from_date == "" or to_date == "":
            messagebox.showwarning("Warning", "Enter both dates")
            return

        try:
            from_sql = convert_to_sql_date(from_date)
            to_sql = convert_to_sql_date(to_date)
        except:
            messagebox.showerror("Error", "Date format must be DD-MM-YYYY")
            return

        cursor.execute("""
            SELECT category, SUM(amount)
            FROM expenses
            WHERE username = ?
            AND date BETWEEN ? AND ?
            GROUP BY category
        """, (username, from_sql, to_sql))

        data = cursor.fetchall()

        if not data:
            messagebox.showinfo("No Data", "No data available for chart")
            return

        categories = [row[0] for row in data]
        amounts = [row[1] for row in data]

        plt.figure(figsize=(6, 6))
        plt.pie(amounts, labels=categories, autopct="%1.1f%%", startangle=90)
        plt.title(f"Category-wise Expense\n({from_date} to {to_date})")
        plt.axis("equal")
        plt.show()

    # ---------- BUTTON FRAME ----------
    btn_frame = tk.Frame(rep_win, bg="#D2B48C")
    btn_frame.pack(pady=15)

    search_btn = tk.Button(
        btn_frame,
        text="Search",
        font=("Times", 12, "bold"),
        bg="#4CAF50",
        fg="white",
        width=12,
        command=search_expenses
    )
    search_btn.grid(row=0, column=0, padx=10)

    chart_btn = tk.Button(
        btn_frame,
        text="Show Pie Chart",
        font=("Times", 12, "bold"),
        bg="#FF9800",
        fg="white",
        width=15,
        command=show_pie_chart
    )
    chart_btn.grid(row=0, column=1, padx=10)

    back_btn = tk.Button(
        btn_frame,
        text="Back",
        font=("Times", 12, "bold"),
        bg="red",
        fg="white",
        width=10,
        command=rep_win.destroy
    )
    back_btn.grid(row=0, column=2, padx=10)
