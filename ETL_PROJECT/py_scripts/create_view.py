import sqlite3

#Создание view для таблицы TERMINALS
def create_view_terminals(conn):
	cursor = conn.cursor()

	cursor.execute('''
	CREATE VIEW IF NOT EXISTS	V_TERMINALS
	AS select
		terminal_id
		,terminal_type	
		,terminal_city	
		,terminal_address
	from DWH_TERMINALS
	where
		deleted_flg = 0
		and current_timestamp between effective_from and effective_to
	''')

	conn.commit()

#Создание view для таблицы TRANSACTIONS
def create_view_transaction(conn):
	cursor = conn.cursor()

	cursor.execute('''
	CREATE VIEW IF NOT EXISTS	V_TRANSACTIONS
	AS select
		transaction_id as trans_id
		,transaction_date as trans_date
		,card_num
		,oper_type
		,amount as amt
		,oper_result
		,terminal
	from DWH_TRANSACTIONS
	where
		deleted_flg = 0
		and current_timestamp between effective_from and effective_to
	''')

	conn.commit()

#Создание view для таблицы PASSPORT_BLACKLIST
def create_view_passport_blacklist(conn):
	cursor = conn.cursor()

	cursor.execute('''
	CREATE VIEW IF NOT EXISTS	V_PASSPORT_BLACKLIST 
	AS select
		passport as passport_num
		,date as entry_dt
	from DWH_PASSPORT_BLACKLIST
	where
		deleted_flg = 0
		and current_timestamp between effective_from and effective_to
	''')

	conn.commit()

#Создание всех view
def create_all_view(conn):
	create_view_terminals(conn)
	create_view_transaction(conn)
	create_view_passport_blacklist(conn)