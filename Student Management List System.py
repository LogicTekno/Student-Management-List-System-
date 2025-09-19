import tkinter as tk
from tkinter import ttk, messagebox
import os

# Function to add an expense
def add():
    try:
        vals = (
            float(e[0].get()),  # Amount
            e[1].get(),         # Category
            e[2].get(),         # Description
            e[3].get()          # Date
        )
        if not vals[1] or not vals[3]:
            raise ValueError
        tree.insert('', 'end', values=vals)
        with open("exp.txt", "a") as f:
            f.write(','.join(map(str, vals)) + '\n')
        total()
        clear()
    except:
        messagebox.showerror("Error", "Fill all fields correctly")

# Function to delete selected expense(s)
def delete():
    for i in tree.selection():
        tree.delete(i)
    save()
    total()

# Function to overwrite selected expense with new values
def rewrite():
    try:
        vals = (
            float(e[0].get()),
            e[1].get(),
            e[2].get(),
            e[3].get()
        )
        tree.item(tree.selection()[0], values=vals)
        save()
        clear()
        total()
    except:
        messagebox.showerror("Error", "Select and enter valid data")

# Save all data currently in the table to file
def save():
    with open("exp.txt", "w") as f:
        for i in tree.get_children():
            f.write(','.join(map(str, tree.item(i)['values'])) + '\n')

# Load data from file into the table when the app starts
def load():
    if os.path.exists("exp.txt"):
        with open("exp.txt") as f:
            for line in f:
                tree.insert('', 'end', values=line.strip().split(','))
    total()

# Calculate and display total expenses
def total():
    t = sum(float(tree.item(i)['values'][0]) for i in tree.get_children())
    lbl.config(text=f"Total: ${t:.2f}")

# Clear all input entry fields
def clear():
    for x in e:
        x.delete(0, tk.END)

# When user selects a row, fill fields with its values for editing
def select(ev):
    s = tree.selection()
    if s:
        v = tree.item(s[0])['values']
        for i in range(4):
            e[i].delete(0, tk.END)
            e[i].insert(0, v[i])

# --- GUI Layout ---
root = tk.Tk()
root.title("Expense Tracker")
root.geometry("700x460")

# Input area
f = tk.Frame(root)
f.pack(pady=10)

labels = ["Amount", "Category", "Description", "Date"]
e = [tk.Entry(f, width=18) for _ in labels]

for i, l in enumerate(labels):
    tk.Label(f, text=l).grid(row=i//2, column=i%2*2)
    e[i].grid(row=i//2, column=i%2*2+1)

# Buttons
b = tk.Frame(root)
b.pack()

for i, (t, cmd) in enumerate([("Add", add), ("Delete", delete), ("Rewrite", rewrite)]):
    tk.Button(b, text=t, width=12, command=cmd).grid(row=0, column=i, padx=5)

# Expense table
cols = ["Amount", "Category", "Description", "Date"]
tree = ttk.Treeview(root, columns=cols, show="headings")

for c in cols:
    tree.heading(c, text=c)
    tree.column(c, anchor="center", width=150)

tree.pack(fill="both", expand=True, padx=10, pady=5)
tree.bind("<<TreeviewSelect>>", select)

# Total display
lbl = tk.Label(root, text="Total: $0.00", font=("Arial", 12))
lbl.pack(pady=5)

# Load data and run app
load()
root.mainloop()
