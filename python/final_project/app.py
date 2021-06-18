import pandas as pd
import sqlite3

con = sqlite3.connect('sber.db')
cursor = con.cursor()

COLUMS = '''
model,
transmission,
body_type,
drive_type,
color,
production_year,
auto_key,
engine_capacity,
horsepower,
engine_type,
price,
milage
'''

link = 'store/data.csv'

def csv2sql(filePath, tableName):
	df = pd.read_csv(filePath)
	df.to_sql(tableName, con=con, if_exists='replace')

def showData(objName):
	print('-_'*20+'\n'+objName+'-_'*20+'\n')
	cursor.execute(f'select * from {objName}')
	for row in cursor.fetchall():
		print(row)
	
def init():
	cursor.execute('''
		CREATE TABLE if not exists auto_hits(
			
		)
	''')