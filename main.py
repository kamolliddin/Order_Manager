import tkinter as tk
from tkinter import messagebox
from db import Database

# Database object
db = Database('store.db')

# Main Application class
class Application(tk.Frame):
	# Constructor to create tk object and application window
	def __init__(self, master):
		super().__init__(master)
		self.master = master
		master.title('Order Manager')
		master.geometry("700x400")
		self.create_widgets()
		self.selected_item = 0
		self.populate_list()

	# Create required widgets in main window. Label, text_area, text_list, scrollbar
	def create_widgets(self):
		# Item
		self.item_text = tk.StringVar()
		self.item_label = tk.Label(self.master, text='Item Name', font=('bold', 14), pady=20)
		self.item_label.grid(row=0, column=0, sticky=tk.W)
		self.item_entry = tk.Entry(self.master, textvariable=self.item_text)
		self.item_entry.grid(row=0, column=1)

		# Customer
		self.customer_text = tk.StringVar()
		self.customer_label = tk.Label(self.master, text='Customer', font=('bold', 14))
		self.customer_label.grid(row=0, column=2, sticky=tk.W)
		self.customer_entry = tk.Entry(self.master, textvariable=self.customer_text)
		self.customer_entry.grid(row=0, column=3)

		# Retailer
		self.retailer_text = tk.StringVar()
		self.retailer_label = tk.Label(self.master, text='Retailer', font=('bold', 14))
		self.retailer_label.grid(row=1, column=0, sticky=tk.W)
		self.retailer_entry = tk.Entry(self.master, textvariable=self.retailer_text)
		self.retailer_entry.grid(row=1, column=1)

		# Price
		self.price_text = tk.StringVar()
		self.price_label = tk.Label(self.master, text='Price', font=('bold', 14))
		self.price_label.grid(row=1, column=2, sticky=tk.W)
		self.price_entry = tk.Entry(self.master, textvariable=self.price_text)
		self.price_entry.grid(row=1, column=3)

		# Parts list (listbox)
		self.orders_list = tk.Listbox(self.master, height=8, width=50, border=0)
		self.orders_list.grid(row=3, column=0, columnspan=3, rowspan=6, pady=20, padx=20)

		# Create scrollbar
		self.scrollbar = tk.Scrollbar(self.master)
		self.scrollbar.grid(row=3, column=3)
		# Set scrollbar to parts
		self.orders_list.configure(yscrollcommand=self.scrollbar.set)
		self.scrollbar.configure(command=self.orders_list.yview)

		# Bind select
		self.orders_list.bind('<<ListboxSelect>>', self.select_order)

		# Buttons
		self.add_btn = tk.Button(self.master, text="Add Order", width=12, command=self.add_order)
		self.add_btn.grid(row=2, column=0, pady=20)

		self.remove_btn = tk.Button(self.master, text="Remove Order", width=12, command=self.remove_order)
		self.remove_btn.grid(row=2, column=1)

		self.update_btn = tk.Button(self.master, text="Update Order", width=12, command=self.update_order)
		self.update_btn.grid(row=2, column=2)

		self.exit_btn = tk.Button(self.master, text="Clear Input", width=12, command=self.clear_text)
		self.exit_btn.grid(row=2, column=3)

	# Method that takes records from sqlite database and inserts them in record_list widget
	def populate_list(self):
		# Delete items before update to prevent dublicate values
		self.orders_list.delete(0, tk.END)
		for row in db.fetch():
			self.orders_list.insert(tk.END, row)

	# Add new item
	def add_order(self):
		if self.item_text.get() == '' or self.customer_text.get() == '' or self.retailer_text.get() == '' or self.price_text.get() == '':
			messagebox.showerror("Required Fields", "Please include all fields")
			return

		print(self.item_text.get())
		db.insert(self.item_text.get(), self.customer_text.get(), self.retailer_text.get(), self.price_text.get())
		# Refresh values in list widget after adding new record
		self.orders_list.delete(0, tk.END)
		self.orders_list.insert(tk.END, (self.item_text.get(), self.customer_text.get(), self.retailer_text.get(), self.item_text.get()))
		self.clear_text()
		self.populate_list()

	# Runs when record from list is selected (click, arrow keys)
	def select_order(self, event):
		try:
			# Get index
			index = self.orders_list.curselection()[0]
			# Get selected item
			self.selected_item = self.orders_list.get(index)

			# Place values of selected record into corresponding text area widgets
			self.item_entry.delete(0, tk.END)
			self.item_entry.insert(tk.END, self.selected_item[1])
			self.customer_entry.delete(0, tk.END)
			self.customer_entry.insert(tk.END, self.selected_item[2])
			self.retailer_entry.delete(0, tk.END)
			self.retailer_entry.insert(tk.END, self.selected_item[3])
			self.price_entry.delete(0, tk.END)
			self.price_entry.insert(tk.END, self.selected_item[4])
		except IndexError:
			pass

	# Remove record
	def remove_order(self):
		db.remove(self.selected_item[0])
		self.clear_text()
		self.populate_list()

	# Update record
	def update_order(self):
		db.update(self.selected_item[0], self.item_text.get(), self.customer_text.get(), self.retailer_text.get(), self.price_text.get())
		self.populate_list()

	# Clear all text fields
	def clear_text(self):
		self.item_entry.delete(0, tk.END)
		self.customer_entry.delete(0, tk.END)
		self.retailer_entry.delete(0, tk.END)
		self.price_entry.delete(0, tk.END)


root = tk.Tk()
app = Application(master=root)
app.mainloop()