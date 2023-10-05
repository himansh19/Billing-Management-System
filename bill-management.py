import tkinter as tk
import sqlite3
from tkinter import messagebox

# Connect to the SQLite database
conn = sqlite3.connect("customer_orders.db")
cursor = conn.cursor()

# Create the customer_orders table if it doesn't exist
cursor.execute('''CREATE TABLE IF NOT EXISTS customer_orders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                customer_name TEXT,
                phone_number TEXT,
                additional_details TEXT,
                order_details TEXT,
                order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                total_price REAL)''')
conn.commit()

# Create a list to store order details
order_details = []

# Function to add a product to the order details list
def add_product():
    product = product_name_entry.get()
    quantity = int(quantity_entry.get())
    price = float(price_entry.get())
    
    # Calculate the total price for this product
    total_price = quantity * price
    
    # Append product details to the order details list
    order_details.append((product, quantity, price, total_price))
    
    # Display the added product in the product_listbox
    product_listbox.insert(tk.END, f"{product:<30}{price:<15.2f}{quantity:<15}{total_price:.2f}")
    
    # Clear the entry fields
    product_name_entry.delete(0, tk.END)
    quantity_entry.delete(0, tk.END)
    price_entry.delete(0, tk.END)

# Function to calculate and display the total order details
def calculate_total():
    total_bill = sum(total_price for _, _, _, total_price in order_details)
    
    # Display the total order details in a table
    total_text.delete("1.0", tk.END)
    total_text.insert(tk.END, f"{'Product Name':<30}{'Price':<15}{'Quantity':<15}{'Total Price':<15}\n")
    total_text.insert(tk.END, "-"*80 + "\n")
    
    for product, quantity, price, total_price in order_details:
        total_text.insert(tk.END, f"{product:<30}{price:<15.2f}{quantity:<15}{total_price:.2f}\n")
    
    total_text.insert(tk.END, "="*80 + "\n")
    total_text.insert(tk.END, f"{'Total Bill:':<60}{total_bill:.2f}\n")

# Function to add the order to the database
def add_order():
    customer = customer_name_entry.get()
    phone = phone_number_entry.get()
    additional_details = additional_details_entry.get()
    
    # Format order details as a string
    order_details_str = "\n".join([f"{product:<30}{price:<15.2f}{quantity:<15}{total_price:.2f}" for product, quantity, price, total_price in order_details])
    
    # Calculate the total price of the order
    total_bill = sum(total_price for _, _, _, total_price in order_details)
    
    # Insert the order details into the database
    cursor.execute("INSERT INTO customer_orders (customer_name, phone_number, additional_details, order_details, total_price) VALUES (?, ?, ?, ?, ?)", (customer, phone, additional_details, order_details_str, total_bill))
    
    conn.commit()
    
    # Clear the order details list and the product_listbox
    order_details.clear()
    product_listbox.delete(0, tk.END)
    
    # Clear the entry fields
    customer_name_entry.delete(0, tk.END)
    phone_number_entry.delete(0, tk.END)
    additional_details_entry.delete(0, tk.END)
    
    # Clear the total_text area
    total_text.delete("1.0", tk.END)

    messagebox.showinfo("Success", "Order added successfully!")

# Function to retrieve orders for a specific customer
def retrieve_orders():
    customer = customer_name_entry.get()
    phone = phone_number_entry.get()
    
    # Query the database for orders of the specified customer
    cursor.execute("SELECT additional_details, order_details, order_date, total_price FROM customer_orders WHERE customer_name=? AND phone_number=? ORDER BY order_date DESC", (customer, phone))
    orders = cursor.fetchall()
    
    # Create a new window to display the retrieved orders
    retrieve_window = tk.Toplevel(root)
    retrieve_window.title("Customer Orders")
    
    # Create a text area to display retrieved orders
    retrieve_text = tk.Text(retrieve_window, width=110, height=25)
    retrieve_text.pack()
    
    # Display retrieved orders in the text area
    for order in orders:
        additional_details, order_details, order_date, total_price = order
        retrieve_text.insert(tk.END, f"Other Details: {additional_details}\n")
        retrieve_text.insert(tk.END, f"Order Date: {order_date}\n")
        retrieve_text.insert(tk.END, "="*70 + "\n")
        retrieve_text.insert(tk.END, order_details + "\n")
        retrieve_text.insert(tk.END, "-"*70 + "\n")
        retrieve_text.insert(tk.END, f"Total Bill: {total_price:.2f}\n\n")

# Function to delete the selected product
def delete_product():
    selected_product = product_listbox.curselection()
    if selected_product:
        index = selected_product[0]
        order_details.pop(index)
        product_listbox.delete(index)

# Function to delete previous orders for a specific customer
def delete_previous_orders():
    customer = customer_name_entry.get()
    phone = phone_number_entry.get()
    
    # Delete previous orders of the specified customer from the database
    cursor.execute("DELETE FROM customer_orders WHERE customer_name=? AND phone_number=?", (customer, phone))
    
    conn.commit()
    messagebox.showinfo("Success", "Previous orders deleted successfully!")

# Create the main window
root = tk.Tk()
root.title("Customer Orders Management")

# Customer Entry Fields
customer_name_label = tk.Label(root, text="Customer Name:")
customer_name_label.grid(row=0, column=0, padx=5, pady=5, sticky="e")
customer_name_entry = tk.Entry(root)
customer_name_entry.grid(row=0, column=1, padx=5, pady=5)

phone_number_label = tk.Label(root, text="Phone Number:")
phone_number_label.grid(row=0, column=2, padx=5, pady=5, sticky="e")
phone_number_entry = tk.Entry(root)
phone_number_entry.grid(row=0, column=3, padx=5, pady=5)

additional_details_label = tk.Label(root, text="Other Details:")
additional_details_label.grid(row=0, column=4, padx=5, pady=5, sticky="e")
additional_details_entry = tk.Entry(root)
additional_details_entry.grid(row=0, column=5, padx=5, pady=5)

# Product Entry Fields
product_name_label = tk.Label(root, text="Product Name:")
product_name_label.grid(row=1, column=0, padx=5, pady=5, sticky="e")
product_name_entry = tk.Entry(root)
product_name_entry.grid(row=1, column=1, padx=5, pady=5)

quantity_label = tk.Label(root, text="Quantity:")
quantity_label.grid(row=1, column=2, padx=5, pady=5, sticky="e")
quantity_entry = tk.Entry(root)
quantity_entry.grid(row=1, column=3, padx=5, pady=5)

price_label = tk.Label(root, text="Price:")
price_label.grid(row=1, column=4, padx=5, pady=5, sticky="e")
price_entry = tk.Entry(root)
price_entry.grid(row=1, column=5, padx=5, pady=5)

# Add Product Button
add_product_button = tk.Button(root, text="Add Product", command=add_product)
add_product_button.grid(row=1, column=6, padx=5, pady=5)

# Product Listbox
product_listbox = tk.Listbox(root, width=80, height=5)
product_listbox.grid(row=2, column=0, columnspan=7, padx=5, pady=5)

# Calculate Total Button
calculate_total_button = tk.Button(root, text="Calculate Total", command=calculate_total)
calculate_total_button.grid(row=3, column=0, padx=5, pady=5)

# Total Label
total_label = tk.Label(root, text="Order Details:")
total_label.grid(row=4, column=0, padx=5, pady=5)

# Text area for displaying order details
total_text = tk.Text(root, width=80, height=10)
total_text.grid(row=5, column=0, columnspan=7, padx=5, pady=5)

# Add Order Button
add_order_button = tk.Button(root, text="Add Order", command=add_order)
add_order_button.grid(row=6, column=0, padx=5, pady=5)

# Retrieve Orders Button
retrieve_orders_button = tk.Button(root, text="Retrieve Orders", command=retrieve_orders)
retrieve_orders_button.grid(row=6, column=1, padx=5, pady=5)

# Delete Product Button
delete_product_button = tk.Button(root, text="Delete Product", command=delete_product)
delete_product_button.grid(row=6, column=5, padx=5, pady=5)

# Delete Previous Orders Button
delete_previous_orders_button = tk.Button(root, text="Delete Previous Orders", command=delete_previous_orders)
delete_previous_orders_button.grid(row=6, column=6, padx=5, pady=5)

root.mainloop()

# Close the database connection when the application is closed
conn.close()
