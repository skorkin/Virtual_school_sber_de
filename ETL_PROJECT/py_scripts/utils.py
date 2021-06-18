import sqlite3

def use_sql_script(conn, filePath):
	with open(filePath, 'r') as f:
		conn.executescript(f.read())
	conn.commit()

	conn.commit()