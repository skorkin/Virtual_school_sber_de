import sqlite3
import pandas as pd
import sys
from py_scripts import utils

sys.path.append("py_scripts/") 

COLUMNS = '''
	terminal_id
	,terminal_type
	,terminal_city
	,terminal_address
'''

# Таблица новых полей
def create_table_new_rows(conn):
	cursor = conn.cursor()
	cursor.execute('''
	create table STG_AUTO_01 as
		select
			t1.* 
		from
			STG_TERMINALS t1
		left join V_TERMINALS t2 on t1.terminal_id = t2.terminal_id
		where 
			t2.terminal_id is NULL
	''')

	conn.commit()

# Таблица удаленных полей
def create_table_delete_rows(conn):
	cursor = conn.cursor()
	cursor.execute('''
	create table STG_AUTO_02 as
		select
			t1.terminal_id
		from V_TERMINALS t1
		left join STG_TERMINALS t2 on t1.terminal_id = t2.terminal_id
		where
			t2.terminal_id is NULL
	''')

	conn.commit()

# измененные поля
def create_changed_rows(conn):
	cursor = conn.cursor()
	cursor.execute('''
	create table STG_AUTO_03 as
		select
			t1.*
		from STG_TERMINALS t1
		inner join DWH_TERMINALS t2 on t1.terminal_id = t2.terminal_id
		where
			current_timestamp between t2.effective_from and t2.effective_to
			and
			(
			t1.terminal_type <> t2.terminal_type 
			or t1.terminal_city <> t2.terminal_city
			or t1.terminal_address <> t2.terminal_address
			)
			and t2.deleted_flg = 0
	''')

	conn.commit()

# восстановленные поля
def create_res_rows(conn):
	cursor = conn.cursor()
	cursor.execute('''
	create table STG_AUTO_04 as
		select
			t1.*
		from DWH_TERMINALS t1
		left join STG_TERMINALS t2 on t1.terminal_id = t2.terminal_id
		where
			t1.deleted_flg = 1
			and current_timestamp between t1.effective_from and t1.effective_to
	''')

	conn.commit()

# примененние изменений
def update_auto_hist(conn):
	cursor = conn.cursor()
	# удаленные записи
	cursor.execute('''
		UPDATE DWH_TERMINALS
		SET deleted_flg = 1
		WHERE
			terminal_id in (select terminal_id from STG_AUTO_02)
			and current_timestamp between effective_from and effective_to
	''')

	# восстановленные записи
	cursor.execute('''
		UPDATE DWH_TERMINALS
		SET deleted_flg = 0
		WHERE
			terminal_id in (select terminal_id from STG_AUTO_04)
			and current_timestamp between effective_from and effective_to
	''')

	# новые записи
	cursor.execute(f'''
		INSERT INTO DWH_TERMINALS(
			{COLUMNS}
		)select
			{COLUMNS}
		from STG_AUTO_01
	''')

	# измененные записи
	# Изменяем время не актуальных записей
	cursor.execute('''
		UPDATE DWH_TERMINALS
		SET effective_to = datetime('now', '-1 second')
		WHERE
			terminal_id in (select terminal_id from STG_AUTO_03)
			and current_timestamp between effective_from and effective_to
	''')

	# Добавляем актуальные записи
	cursor.execute(f'''
		INSERT INTO DWH_TERMINALS(
			{COLUMNS}
		)select
			{COLUMNS}
		from STG_AUTO_03
	''')

	conn.commit()

# Заполнение таблицы TERMINALS
def incr(conn, filePath):
	cursor = conn.cursor()

	utils.use_sql_script(conn, 'sql_scripts/drop_auto_stg_table.sql')

	df = pd.read_excel(filePath)
	df.to_sql('STG_TERMINALS', con=conn, if_exists='replace')

	create_table_new_rows(conn)
	create_table_delete_rows(conn)
	create_res_rows(conn)
	create_changed_rows(conn)
	update_auto_hist(conn)

	utils.use_sql_script(conn, 'sql_scripts/drop_auto_stg_table.sql')

	conn.commit()