import sqlite3

class Database:

	# idea taken from https://gist.github.com/goldsborough/c973d934f620e16678bf

	def __init__(self, name=None):

	    self.conn = None
	    self.cursor = None

	    if name:
	        self.open(name)

	def open(self,name):

	    try:
	        self.conn = sqlite3.connect(name);
	        self.cursor = self.conn.cursor()

	    except sqlite3.Error as e:
	        print("Error connecting to database!")
	        raise e

	def close(self):

	    if self.conn:
	        self.conn.commit()
	        self.cursor.close()
	        self.conn.close()

	def __enter__(self):

	    return self

	def __exit__(self,exc_type,exc_value,traceback):

	    self.close()
