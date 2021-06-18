import sqlite3
import pandas as pd
import sys
from py_scripts import utils

sys.path.append("py_scripts/") 
COLUMNS = '''
	date
	,passport
'''

# Таблица новых полей
def create_table_new_rows(conn):
	cursor = conn.cursor()
	cursor.execute('''
	create table if not exists STG_AUTO_01 as
		select
			t1.* 
		from STG_PASSPORT_BLACKLIST t1
		left join DWH_PASSPORT_BLACKLIST t2 on t1.passport = t2.passport
		where t2.passport is NULL
	''')

	conn.commit()

# примененние изменений
def update_auto_hist(conn):
	cursor = conn.cursor()

	# новые записи
	cursor.execute(f'''
		INSERT INTO DWH_PASSPORT_BLACKLIST(
			{COLUMNS}
		)select
			{COLUMNS}
		from STG_AUTO_01
	''')

	conn.commit()

# Проверка на то, не наступило ли начало месяца
# Если да, то таблица чистится
def month_clear(conn, filePath):
	cursor = conn.cursor()
	if filePath.find('_01'):
		cursor.execute('DELETE FROM DWH_PASSPORT_BLACKLIST')

	conn.commit()

# Заполнение таблицы PASSPORT_BLACKLIST
def incr(conn, filePath):
	cursor = conn.cursor()

	df = pd.read_excel(filePath)
	df.to_sql('STG_PASSPORT_BLACKLIST', con=conn, if_exists='replace')
	
	month_clear(conn, filePath)

	create_table_new_rows(conn)
	update_auto_hist(conn)

	utils.use_sql_script(conn, 'sql_scripts/drop_auto_stg_table.sql')

	conn.commit()