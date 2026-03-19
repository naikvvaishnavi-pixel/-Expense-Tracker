from Database import conn, cursor
import tkinter as tk
from tkinter import messagebox
from datetime import datetime,timedelta 
cursor=conn.cursor()
def open_WM_window(username):
    win = tk.Toplevel()
    win.title("Weekly & Monthly Expense")
    win.geometry("500x500")
    win.configure(bg="#D2B48C")

    bg = tk.PhotoImage(file="D:/Python_code/Project/image.png")
    bg_label = tk.Label(win, image=bg)
    bg_label.image = bg  # prevent image disappearing
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)

    # ---------- FROM DATE ----------
    from_label = tk.Label(win, text="From Date (YYYY-MM-DD)",
                          font=("Times", 14, "bold"), bg="#D2B48C")
    from_label.pack(pady=(10, 5))

    from_entry = tk.Entry(win, font=("Times", 14), width=25)
    from_entry.pack(pady=5)

    # ---------- TO DATE ----------
    to_label = tk.Label(win, text="To Date (YYYY-MM-DD)",
                        font=("Times", 14, "bold"), bg="#D2B48C")
    to_label.pack(pady=(10, 5))

    to_entry = tk.Entry(win, font=("Times", 14), width=25)
    to_entry.pack(pady=5)

    # ---------- RESULT LABELS ----------
    monthly_label = tk.Label(win, text="Monthly Expense: ₹ 0",
                             font=("Times", 14, "bold"), bg="#D2B48C")
    monthly_label.pack(pady=15)

    week1_label = tk.Label(win, text="Week 1: ₹ 0",
                           font=("Times", 12, "bold"), bg="#D2B48C")
    week1_label.pack(pady=5)

    week2_label = tk.Label(win, text="Week 2: ₹ 0",
                           font=("Times", 12, "bold"), bg="#D2B48C")
    week2_label.pack(pady=5)

    week3_label = tk.Label(win, text="Week 3: ₹ 0",
                           font=("Times", 12, "bold"), bg="#D2B48C")
    week3_label.pack(pady=5)

    week4_label = tk.Label(win, text="Week 4: ₹ 0",
                           font=("Times", 12, "bold"), bg="#D2B48C")
    week4_label.pack(pady=5)

    # ---------- FUNCTION ----------
    def calculate_expense():
        from_date = from_entry.get()
        to_date = to_entry.get()

        if from_date == "" or to_date == "":
            messagebox.showwarning("Warning", "Enter both dates")
            return

        try:
            start = datetime.strptime(from_date, "%Y-%m-%d")
            end = datetime.strptime(to_date, "%Y-%m-%d")
        except:
            messagebox.showerror("Error", "Use format YYYY-MM-DD")
            return

        # ----- MONTHLY TOTAL -----
        cursor.execute(
            "SELECT SUM(amount) FROM expenses WHERE username=? AND date BETWEEN ? AND ?",
            (username, from_date, to_date)
        )
        total = cursor.fetchone()[0]
        if total is None:
            total = 0

        monthly_label.config(
            text=f"Monthly Expense ({from_date} to {to_date}): ₹ {total:.2f}"
        )

        # ----- WEEK CALCULATION -----
        week_labels = [week1_label, week2_label, week3_label, week4_label]

        current_start = start
        for i in range(4):
            current_end = current_start + timedelta(days=6)

            if current_end > end:
                current_end = end

            cursor.execute(
                "SELECT SUM(amount) FROM expenses WHERE username=? AND date BETWEEN ? AND ?",
                (username,
                 current_start.strftime("%Y-%m-%d"),
                 current_end.strftime("%Y-%m-%d"))
            )

            week_total = cursor.fetchone()[0]
            if week_total is None:
                week_total = 0

            week_labels[i].config(
                text=f"Week {i+1} ({current_start.strftime('%d %b')} - {current_end.strftime('%d %b')}): ₹ {week_total:.2f}"
            )

            current_start = current_end + timedelta(days=1)
            if current_start > end:
                break

    # ---------- BUTTON ----------
    calc_btn = tk.Button(
        win,
        text="Calculate Report",
        font=("Times", 14, "bold"),
        bg="#8B4513",
        fg="white",
        width=18,
        command=calculate_expense
    )
    calc_btn.pack(pady=25)

    def back():
        win.destroy() 
    backbutton=tk.Button(win,text="Back",command=back)
    backbutton.pack()
    