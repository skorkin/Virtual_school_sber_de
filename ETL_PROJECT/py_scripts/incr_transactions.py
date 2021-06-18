import sqlite3
import pandas as pd
import sys
from py_scripts import utils

sys.path.append("py_scripts/") 


COLUMNS = '''
	transaction_id
	,transaction_date
	,amount
	,card_num
	,oper_type
	,oper_result
	,terminal
'''

# Таблица новых полей
def create_table_new_rows(conn):
	cursor = conn.cursor()
	cursor.execute('''
	create table if not exists STG_AUTO_01 as
		select
			* 
		from
			STG_TRANSACTIONS t1
	''')

	conn.commit()


# примененние изменений
def update_auto_hist(conn):
	cursor = conn.cursor()

	# новые записи
	cursor.execute(f'''
		INSERT INTO DWH_TRANSACTIONS(
			{COLUMNS}
		)select
			{COLUMNS}
		from STG_AUTO_01
	''')

	conn.commit()

# Заполнение таблицы TRANSACTIONS
def incr(conn, filePath):
	cursor = conn.cursor()

	utils.use_sql_script(conn, 'sql_scripts/drop_auto_stg_table.sql')

	df = pd.read_csv(filePath, sep=';')
	df.to_sql('STG_TRANSACTIONS', con=conn, if_exists='replace')

	create_table_new_rows(conn)
	update_auto_hist(conn)

	utils.use_sql_script(conn, 'sql_scripts/drop_auto_stg_table.sql')

	conn.commit()