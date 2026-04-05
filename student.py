import tkinter as tk
from tkinter import messagebox, ttk, filedialog
import csv

students = []
selected_item = None

# ------------------ LOGIC ------------------
def calculate_grade(percentage):
    if percentage >= 90:
        return "A+"
    elif percentage >= 80:
        return "A"
    elif percentage >= 70:
        return "B"
    elif percentage >= 60:
        return "C"
    elif percentage >= 50:
        return "D"
    else:
        return "F"


def get_marks():
    return [
        int(math_entry.get()),
        int(science_entry.get()),
        int(english_entry.get()),
        int(computer_entry.get()),
        int(hindi_entry.get())
    ]


def add_student():
    name = name_entry.get().strip()
    roll = roll_entry.get().strip()

    if not name or not roll:
        messagebox.showerror("Error", "Name and Roll No are required")
        return

    try:
        marks = get_marks()

        for m in marks:
            if m < 0 or m > 100:
                messagebox.showerror("Error", "Marks should be 0-100")
                return

        total = sum(marks)
        percentage = total / len(marks)
        grade = calculate_grade(percentage)

        student = (roll, name, total, round(percentage, 2), grade)
        students.append(student)

        table.insert("", "end", values=student)
        clear_fields()

    except ValueError:
        messagebox.showerror("Error", "Enter valid numbers")


def select_student(event):
    global selected_item
    selected = table.selection()
    if selected:
        selected_item = selected[0]
        values = table.item(selected_item, "values")

        roll_entry.delete(0, tk.END)
        name_entry.delete(0, tk.END)

        roll_entry.insert(0, values[0])
        name_entry.insert(0, values[1])


def update_student():
    global selected_item

    if not selected_item:
        messagebox.showwarning("Warning", "Select a student to update")
        return

    try:
        marks = get_marks()

        total = sum(marks)
        percentage = total / len(marks)
        grade = calculate_grade(percentage)

        updated = (roll_entry.get(), name_entry.get(), total, round(percentage, 2), grade)

        table.item(selected_item, values=updated)

        clear_fields()
        selected_item = None

    except ValueError:
        messagebox.showerror("Error", "Enter valid numbers")


def delete_student():
    selected = table.selection()
    if not selected:
        messagebox.showwarning("Warning", "Select a student to delete")
        return

    for item in selected:
        table.delete(item)


def search_student():
    search = search_entry.get().strip().lower()

    for row in table.get_children():
        table.delete(row)

    for student in students:
        if search in student[0].lower() or search in student[1].lower():
            table.insert("", "end", values=student)


def show_all():
    for row in table.get_children():
        table.delete(row)

    for student in students:
        table.insert("", "end", values=student)


def save_to_csv():
    file = filedialog.asksaveasfilename(defaultextension=".csv",
                                        filetypes=[("CSV files", "*.csv")])
    if not file:
        return

    with open(file, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Roll No", "Name", "Total", "Percentage", "Grade"])
        writer.writerows(students)

    messagebox.showinfo("Success", "Data saved successfully")


def clear_fields():
    for entry in entries:
        entry.delete(0, tk.END)


# ------------------ UI ------------------
root = tk.Tk()
root.title("Student Result Management System")
root.geometry("950x650")

# Title
tk.Label(root, text="Student Result Management System", font=("Arial", 18, "bold")).pack(pady=10)

# Form Frame
frame = tk.Frame(root)
frame.pack(pady=10)

labels = ["Roll No", "Name", "Math", "Science", "English", "Computer", "Hindi"]
entries = []

for i, text in enumerate(labels):
    tk.Label(frame, text=text).grid(row=i, column=0, padx=10, pady=5, sticky="w")
    entry = tk.Entry(frame)
    entry.grid(row=i, column=1, padx=10, pady=5)
    entries.append(entry)

roll_entry, name_entry, math_entry, science_entry, english_entry, computer_entry, hindi_entry = entries

# Buttons
tk.Button(frame, text="Add", command=add_student, bg="green", fg="white").grid(row=7, column=0, pady=10)
tk.Button(frame, text="Update", command=update_student, bg="blue", fg="white").grid(row=7, column=1, pady=10)
tk.Button(frame, text="Delete", command=delete_student, bg="red", fg="white").grid(row=8, column=0, columnspan=2, pady=5)

# Search
search_frame = tk.Frame(root)
search_frame.pack()

tk.Label(search_frame, text="Search:").pack(side=tk.LEFT, padx=5)
search_entry = tk.Entry(search_frame)
search_entry.pack(side=tk.LEFT, padx=5)

tk.Button(search_frame, text="Search", command=search_student).pack(side=tk.LEFT, padx=5)
tk.Button(search_frame, text="Show All", command=show_all).pack(side=tk.LEFT, padx=5)
tk.Button(search_frame, text="Save CSV", command=save_to_csv).pack(side=tk.LEFT, padx=5)

# Table
columns = ("Roll No", "Name", "Total", "Percentage", "Grade")
table = ttk.Treeview(root, columns=columns, show="headings")

for col in columns:
    table.heading(col, text=col)
    table.column(col, width=150, anchor="center")

# Bind select
table.bind("<<TreeviewSelect>>", select_student)

table.pack(pady=20, fill="both", expand=True)

root.mainloop()