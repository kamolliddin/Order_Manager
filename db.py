import sqlite3

class Database:
	def __init__(self, db):
		self.conn = sqlite3.connect(db)
		self.cursor = self.conn.cursor()
		self.cursor.execute("CREATE TABLE IF NOT EXISTS orders (id INTEGER PRIMARY KEY, item text, customer text, retailer text, price text )")
		self.conn.commit()

	def fetch(self):
		self.cursor.execute("SELECT * FROM orders")
		rows = self.cursor.fetchall()
		return rows

	def insert(self, item, customer, retailer, price):
		self.cursor.execute("INSERT INTO orders VALUES (NUll, ?,?,?,?)", (item, customer, retailer, price))
		self.conn.commit()

	def remove(self, id):
		self.cursor.execute("DELETE FROM orders WHERE id=?",(id,))
		self.conn.commit()

	def update(self, id, item, customer, retailer, price):
		self.cursor.execute("UPDATE orders  SET item = ?, customer=?, retailer=?, price=? WHERE id = ?",(item, customer, retailer, price,id))
		self.conn.commit()

	def __del__(self):
		self.conn.close()
