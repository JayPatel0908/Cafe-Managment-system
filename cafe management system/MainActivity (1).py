import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

# Enhanced Menu items with sub-options
menu = {
    "Coffee": {
        "Espresso": 70,
        "Cappuccino": 100,
        "Latte": 120
    },
    "Tea": {
        "Masala Tea": 40,
        "Lemon Tea": 50,
        "Green Tea": 60
    },
    "Sandwich": {
        "Veg Sandwich": 120,
        "Cheese Sandwich": 150,
        "Grilled Sandwich": 180
    },
    "Cake": {
        "Chocolate Cake": 100,
        "Vanilla Cake": 90,
        "Red Velvet Cake": 150
    },
    "Juice": {
        "Orange Juice": 80,
        "Mango Juice": 100,
        "Mixed Fruit Juice": 120
    }
}

# Order dictionary grouped by table numbers
order = {}  # Format: {table_number: {item: quantity}}

# Helper function to get the price of an item
def get_item_price(item):
    for category in menu:
        if isinstance(menu[category], dict):  # Check if it's a category with sub-options
            if item in menu[category]:  # If the item is found in sub-options
                return menu[category][item]
        elif item == category:  # If the item is a top-level option
            return menu[category]
    return 0  # Default to 0 if the item is not found

# Add items to order for a specific table
def add_to_order(item):
    table = table_var.get()
    if table == "Select Table":
        messagebox.showwarning("Table Selection", "Please select a table number before adding items!")
        return
    if table not in order:
        order[table] = {}
    if item in order[table]:
        order[table][item] += 1
    else:
        order[table][item] = 1
    update_order_list()

# Update the order list to display orders grouped by table numbers
def update_order_list():
    order_list.delete(0, tk.END)
    for table, items in order.items():
        order_list.insert(tk.END, f"--- {table} ---")
        for item, quantity in items.items():
            price = get_item_price(item)
            order_list.insert(tk.END, f"{item} x {quantity} = Rs. {quantity * price}")
        order_list.insert(tk.END, "")  # Add a blank line bet

# Remove an item from the order for the selected table
def remove_from_order():
    selected = order_list.curselection()
    if selected:
        selected_text = order_list.get(selected[0])
        if "---" in selected_text:  # Ignore table headers
            return
        item = selected_text.split(" x ")[0]
        table = table_var.get()
        if table in order and item in order[table]:
            order[table][item] -= 1
            if order[table][item] == 0:
                del order[table][item]
            if not order[table]:  # If the table has no items left
                del order[table]
            update_order_list()

# Generate a receipt for the selected table
def generate_receipt():
    table = table_var.get()
    if table == "Select Table":
        messagebox.showwarning("Table Selection", "Please select a table number to generate a receipt!")
        return
    if table not in order or not order[table]:
        messagebox.showinfo("Receipt", f"No items in order for {table}!")
        return
    receipt_text = f"\n--- Café Delight Receipt for {table} ---\n"
    total = 0
    for item, quantity in order[table].items():
        price = get_item_price(item)
        total += price * quantity
        receipt_text += f"{item} x {quantity} = Rs. {price * quantity}\n"
    receipt_text += f"\nTotal Amount: Rs. {total}\n"
    receipt_text += "Please kindly pay the bill amount at the cash counter or in the bill presenter on your table. Thank you!"
    messagebox.showinfo("Receipt", receipt_text)

# Reset the order for the selected table
def reset_table_order():
    table = table_var.get()
    if table == "Select Table":
        messagebox.showwarning("Table Selection", "Please select a table number to reset!")
        return
    if table in order:
        del order[table]
        update_order_list()
    else:
        messagebox.showinfo("Reset Order", f"No orders found for {table}.")

# Exit the application
def exit_app():
    root.destroy()

# Function to display the main menu (restore main menu)
def show_main_menu():
    for widget in menu_frame.winfo_children():  # Clear existing buttons
        widget.destroy()
    for category in menu:  # Display main menu buttons
        btn = tk.Button(menu_frame, text=f"{category}", font=("Arial", 10, "italic"), bg="#6c5b7b", fg="white", height=1, command=lambda c=category: show_sub_menu(c))
        btn.pack(fill=tk.X, padx=20, pady=2)

# Function to display sub-options for categories
def show_sub_menu(category):
    for widget in menu_frame.winfo_children():  # Clear existing buttons
        widget.destroy()
    if category in menu and isinstance(menu[category], dict):  # Check if category has sub-options
        for sub_item, price in menu[category].items():
            btn = tk.Button(menu_frame, text=f"{sub_item} - Rs. {price}", font=("Arial", 10, "italic"), bg="#ff847c", fg="white", height=1, command=lambda i=sub_item: add_to_order(i))
            btn.pack(fill=tk.X, padx=20, pady=2)
        # Add "Back to Main Menu" button
        btn_back = tk.Button(menu_frame, text="Back to Main Menu", font=("Arial", 10, "italic"), bg="#e53935", fg="white", height=1, command=show_main_menu)
        btn_back.pack(fill=tk.X, padx=20, pady=2)
    else:
        add_to_order(category)  # If it's not a category with sub-options, directly add to order

# GUI setup
root = tk.Tk()
root.title("Café Management System")
root.geometry("700x600")
root.attributes("-fullscreen", True)  # Enable full screen mode

# Load and set background image
bg_image = Image.open("background.png")
bg_image = bg_image.resize((root.winfo_screenwidth(), root.winfo_screenheight()), Image.Resampling.LANCZOS)
bg_photo = ImageTk.PhotoImage(bg_image)
bg_label = tk.Label(root, image=bg_photo)
bg_label.place(x=0, y=0, relwidth=1, relheight=1)

# Header
header = tk.Label(root, text="Welcome to Café Delight", font=("Arial", 20, "italic"), bg="#2a363b", fg="#f67280")
header.pack(pady=20)

# Table number selection
table_var = tk.StringVar(value="Select Table")
table_label = tk.Label(root, text="Table Number:", font=("Arial", 14, "italic"), bg="#2a363b", fg="#99b898")
table_label.pack(pady=5)

table_dropdown = tk.OptionMenu(root, table_var, *[f"Table {i}" for i in range(1, 11)])  # Example: 10 tables
table_dropdown.config(font=("Arial", 12), bg="#6c5b7b", fg="white")
table_dropdown.pack(pady=5)

# Menu frame
menu_frame = tk.Frame(root, bg="#2a363b")
menu_frame.pack(pady=10)

menu_label = tk.Label(menu_frame, text="Menu", font=("Arial", 16, "italic"), bg="#2a363b", fg="#99b898")
menu_label.pack()

# Display main menu
show_main_menu()

# Order list
order_frame = tk.Frame(root, bg="#2a363b")
order_frame.pack(pady=10)

order_label = tk.Label(order_frame, text="Your Order", font=("Arial", 16, "italic" ), bg="#2a363b", fg="#99b898")
order_label.pack()

order_list = tk.Listbox(order_frame, height=10, width=40, font=("Arial", 12, "italic"), bg="#355c7d", fg="white")
order_list.pack(pady=5)

# Control buttons
btn_receipt = tk.Button(root, text="Generate Receipt", font=("Arial", 12, "italic"), bg="#6c5b7b", fg="white", command=generate_receipt)
btn_receipt.pack(pady=2, padx=20, ipadx=10)

btn_remove = tk.Button(root, text="Remove Item", font=("Arial", 12, "italic"), bg="#ff847c", fg="white", command=remove_from_order)
btn_remove.pack(pady=2, padx=20, ipadx=10)

btn_reset_table = tk.Button(root, text="Reset Table Order", font=("Arial", 12, "italic"), bg="#e84a5f", fg="white", command=reset_table_order)
btn_reset_table.pack(pady=1, padx=20, ipadx=10)

btn_exit = tk.Button(root, text="Exit", font=("Arial", 12, "italic"), bg="#e53935", fg="white", command=exit_app)
btn_exit.pack(pady=2, padx=20, ipadx=10)

footer = tk.Label(root, text="Thank you for visiting!", font=("Arial", 14, "italic"), bg="#2a363b", fg="#f67280")
footer.pack(pady=2)

root.mainloop()                                                