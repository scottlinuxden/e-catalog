# $Id: gadfly_utils.py,v 1.3 2000/07/16 16:41:18 davis Exp davis $
# Copyright (C) 1999 LinuXden, All Rights Reserved
# Copright Statement at http://www.linuxden.com/copyrighted_apps.html
# 
import os
import sys
import string
import gadfly
import file_io

def connect_db(
	database_name,
	database_location,
	create_if_does_not_exist=0,
	create_cursor_also=1):

	db = {}
	db['instance'] = None
	db['cursor'] = None

	try:
		# create a database instance
		db['instance'] = gadfly.gadfly(database_name,
			database_location)
	except:

		if create_if_does_not_exist:

			# create the database
			result = create_db(database_name,
				database_location,
				overwrite_existing_db=1,
				create_cursor_also=0)

			if result['status'] != 'success':

				return {'status' : 'error', 'message' : "Can not connect and create a database at specified location", 'result' : None}

			else:

				db = result['result']

		else:

			return {'status' : 'error', 'message' : "Can not connect to database specified", 'result' : None}


	if create_cursor_also:
		result = create_cursor(db)
		if result['status'] != 'success':
			return {'status' : 'error', 'message' : "Could not create cursor", 'result' : db}
		else:
			db = result['result']

	return {'status' : 'success', 'message' : "Connected to database.", 'result' : db}

def create_db(
	database_name,
	database_location,
	overwrite_existing_db=0,
	create_cursor_also=1):

	db = {}
	db['instance'] = None
	db['cursor'] = None

	# if the caller does not want to overwrite database if it already exists
	if not overwrite_existing_db:

		# check to see if database already exists
		if os.path.exists(os.path.join(os.sep,database_location,database_name)):
			# database already exists return
			return {'status' : 'error', 'message' : "Database already exists at specified path and no overwrite specified", 'result' : None}

	try:
		if not os.path.exists(os.path.join(os.sep,database_location)):
			os.makedirs(os.path.join(os.sep,database_location),0700)

		# create a db instance
		db['instance'] = gadfly.gadfly()

	except:

		return {'status' : 'error', 'message' : "Database could not be created", 'result' : None}

	else:

		try:
			# startup the instance
			db['instance'].startup(database_name,
				database_location)
		except:

			return {'status' : 'error', 'message' : "Database could not be started", 'result' : None}

	if create_cursor_also:

		result = create_cursor(db)

		if result['status'] != 'success':
			return {'status' : 'error', 'message' : "Could not create cursor", 'result' : db}
		else:
			db = result['result']

	return {'status' : 'success', 'message' : "Database created.", 'result' : db}

def create_tables(db,
	table_data,
	echo_statement=0,
	commit_after=1,
	leave_cursor_open=1):

	table_name_keys = table_data.keys()

	# loop through each table name
	for table_name in table_name_keys:

		sqlStatement = "DROP TABLE " + table_name

		queryResult = execute_sql_statement(db,
			sqlStatement,
			commit_after,
			leave_cursor_open)

		sqlStatement = "CREATE TABLE "

		sqlStatement = sqlStatement + table_name + " ("

		creation_order = sort_table_columns(table_data,table_name)

		# put id key up front
		for column_name in creation_order:

			sqlStatement = sqlStatement + build_column_declaration(table_name, column_name, table_data)

			sqlStatement = sqlStatement + ", "

		sqlStatement = sqlStatement[:-2] + ")"

		if echo_statement == 1:
			print "\nSQL Statement:\n" + sqlStatement + "\nPerformed successfully"

		queryResult = execute_sql_statement(db,
			sqlStatement,
			commit_after,
			leave_cursor_open)

		if queryResult['status'] != 'success':
			return queryResult

	return {'status' : 'success', 'message' : "Database tables created successfully", 'result' : None}

def create_cursor(db,
	close_existing_cursor=1):

	if db['instance'] == None:
		return {'status' : 'error', 'message' : 'No database instance exists for cursor', 'result' : db} 

	if db['cursor'] != None:

		# close the cursor that already exists
		if close_existing_cursor:
			db['cursor'].close()
		else:
			return {'status' : 'error', 'message' : 'Cursor already open and user specified no close', 'result' : db} 

	try:
		# create a cursor
		db['cursor'] = db['instance'].cursor()
	except:
		return {'status' : 'error', 'message' : message, 'result' : db} 

	if db['cursor'] == None:
		return {'status' : 'error', 'message' : "Could not create a cursor", 'result' : db}

	return {'status' : 'success', 'message' : "Cursor created", 'result' : db}

def execute_sql_statement(db,
	sqlStatement,
	commit_after=1,
	leave_cursor_open=1,
	create_cursor_also=1):
	"""
        Execute a sql statement specified by sqlStatement for the already
        open db connection designate by db
        Returns a queryResult type, see above
        """

	if not db.has_key('instance') or db['instance'] == None:
		return {'status' : 'error', 'message' : 'No database instance exists to process statement', 'result' : None} 


	if create_cursor_also and ((not db.has_key('cursor')) or db['cursor'] == None):
		try:
			# create a cursor
			db['cursor'] = db['instance'].cursor()
		except gadfly.error, message:
			return {'status' : 'error', 'message' : message, 'result' : None} 

	if db['cursor'] == None:
		return {'status' : 'success', 'message' : "Could not create a cursor", 'result' : None}

	try:
		# execute the sql statement
		db['cursor'].execute(sqlStatement)
	except gadfly.error, message:
		return {'status' : 'error', 'message' : message, 'result' : None} 
	except NameError, message:
		return {'status' : 'error', 'message' : message, 'result' : None} 
	except ValueError, message:
		return {'status' : 'error', 'message' : message, 'result' : None} 
	except SyntaxError, message:
		return {'status' : 'error', 'message' : message, 'result' : None} 

	# test the sql statement for SELECT keyword
	test_statement = string.upper(string.strip(sqlStatement))

	if test_statement[:len('SELECT')] == 'SELECT':
		# select statement so fetch all rows
		try:
			result = db['cursor'].fetchall()
		except gadfly.error, message:
			return {'status' : 'error', 'message' : message, 'result' : None}

		if not leave_cursor_open:
			db['cursor'].close()

		if commit_after:
			db['instance'].commit()

		return {'status' : 'success', 'message' : "SQL Query processed returning rows fetched", 'result' : result}

	else:
		# non-select statement

		if not leave_cursor_open:
			db['cursor'].close()

		if commit_after:
			db['instance'].commit()

		return {'status' : 'success', 'message' : "Non select statement processed", 'result' : None}

def execute_sql_item_list(db,
	sqlList,
	echoStatement=0,
	ignoreErrors=0,
	commit_after=1,
	leave_cursor_open=1):

	for sqlItem in sqlList:

		queryResult = execute_sql_statement(db,
			sqlItem,
			commit_after,
			leave_cusor_open)

		if not ignoreErrors:
			if echoStatement == 1:
				print "\nSQL Statement: " + sqlItem + '\nPerformed with status: ' + queryResult['status']
				if queryResult['status'] != 'success':
					print 'Details: ' + queryResult['message']
			if queryResult["status"] != 'success':
				return queryResult
		else:
			if echoStatement == 1:
				print "\nSQL Statement: " + sqlItem + '\nPerformed with status: ' + queryResult['status']
				if queryResult['status'] != 'success':
					print 'Details: ' + queryResult['message']

	return {'status' : "success", 'message' : "Items in SqlItemList processed", 'result' : None}

def table_to_db(table_data,table_name):
	"""
        Converts table data items specified by table_name to data values that
        can be stored in the database.  Resultant db data created is returned.
        """

	dbData = {}

	for field_name in table_data[table_name].keys():

		if string.upper(table_data[table_name][field_name]["type"]) == 'INTEGER':
			dbData[field_name] = int(table_data[table_name][field_name]["value"])

		elif string.upper(table_data[table_name][field_name]["type"]) == 'FLOAT':
			dbData[field_name] = float(table_data[table_name][field_name]["value"])

		else:
			dbData[field_name] = string.strip(table_data[table_name][field_name]["value"])

	return dbData

def db_to_table(table_data, table_name, db):

	for field_name in db.keys():

		if table_data[table_name].has_key(field_name):

			if string.upper(table_data[table_name][field_name]["type"]) == 'INTEGER' or \
				string.upper(table_data[table_name][field_name]["type"]) == 'FLOAT':
				table_data[table_name][field_name]["value"] = `db[field_name]`

			else:
				table_data[table_name][field_name]["value"] = db[field_name]

			string.strip(table_data[table_name][field_name]["value"])

	return table_data

def init_table(table_data, table_name):

	field_name_keys = table_data[table_name].keys()

	for field_name in field_name_keys:
		if table_data[table_name][field_name]["default"] != None:
			table_data[table_name][field_name]["value"] = table_data[table_name][field_name]["default"]
		else:
			table_data[table_name][field_name]["value"] = ''

	return table_data

def build_column_declaration(table_name, column_name, table_data):
	"""
        Builds a column declaration to be used in a create table statement
        """

	return column_name + " " + table_data[table_name][column_name]["type"]

def build_select_all_table_columns_statement(table_data,table_name,id,id_field_name='id'):

	creation_order = sort_table_columns(table_data,table_name)

	sqlStatement = "SELECT "

	for columnName in creation_order:
		sqlStatement = sqlStatement + columnName + ", "

	sqlStatement = sqlStatement[:-2]

	sqlStatement = sqlStatement + " FROM " + table_name + " WHERE " + id_field_name + " = '" + id + "'"

	return sqlStatement

def execute_sql_from_file(db,
	filename,
	commit_after,
	leave_cursor_open):

	status, populate_tables = file_io.readFromFile(filename)

	for index in xrange(0,len(populate_tables)):

		populate_tables[index] = string.strip(populate_tables[index])

		if populate_tables[index] == '':
			del populate_tables[index]

	result = execute_sql_item_list(db,
		populate_tables,
		1,
		1,
		commit_after,
		leave_cursor_open)

	if result["status"] != 'success':
		return {'status' : 'error', 'message' : "Failed to execute all SQL statements in file", 'result' : None}

	return {'status' : 'success', 'message' : "All SQL statements in file executed correctly", 'result' : None}

def insert_into_table(db,
	table_data,
	table_name,
	echoStatement=0,
	commit_after=1,
	leave_cursor_open=1):

	# row does not exist so insert
	sqlStatement = "INSERT INTO " + table_name + " ("

	for i in table_data[table_name].keys():

		sqlStatement = sqlStatement + i + ", "

	sqlStatement = sqlStatement[:-2] + ") VALUES ("

	for i in table_data[table_name].keys():

		if (table_data[table_name][i]["type"] == 'VARCHAR'):

			if string.strip(table_data[table_name][i]['value']) == '':
				sqlStatement = sqlStatement + "'', "
			else:
				sqlStatement = sqlStatement + "'" + table_data[table_name][i]['value'] + "', "

		else:

			if string.strip(table_data[table_name][i]['value']) == '':
				sqlStatement = sqlStatement + "'', "
			else:
				sqlStatement = sqlStatement + table_data[table_name][i]['value'] + ", "

	# remove last comma
	sqlStatement = sqlStatement[:-2] + ")"

	if echoStatement == 1:
		print "\nSQL Statement:\n" + sqlStatement + "\nPerformed successfully"

	result = execute_sql_statement(db,
		sqlStatement,
		commit_after,
		leave_cursor_open)

	return result

def insert_from_file(
	db,
	table_data,
	table_name,
	filename,
	delimiter=',',
	echo_statement=0,
	commit_after=1,
	leave_cursor_open=1):

	status, lines = file_io.readFromFile(filename)

	sorted_columns = sort_table_columns(table_data,table_name)

	for line_index in xrange(0, len(lines)):

		line_field = string.splitfields(lines[line_index], delimiter)

		if len(line_field) != len(sorted_columns):
			return {'status' : 'error', 'message' : "Not enough fields specified on line %d" % (line_index+1), 'result' : None}

		field_index = 0

		for field_name in sorted_columns:
			table_data[table_name][field_name]['value'] = line_field[field_index]
			field_index = field_index + 1

		result = insert_into_table(db,
			table_data,
			table_name,
			echo_statement,
			commit_after,
			leave_cursor_open)

		if result['status'] != 'success':
			break

	return result

def create_sequence(db,
	sequence_name,
	start_value=0,
	increment_by=1,
	commit_after=1,
	leave_cursor_open=1):

	result = execute_sql_statement(db,
		'CREATE TABLE %s (last_value INTEGER, increment_by INTEGER)' % (sequence_name),
		commit_after,
		leave_cursor_open)

	if result['status'] != 'success':
		return result

	result = execute_sql_statement(db,
		'INSERT INTO %s (last_value, increment_by) VALUES (%d, %d)' % (sequence_name, start_value, increment_by),
		commit_after,
		leave_cursor_open)

	if result['status'] != 'success':
		return result

	return {'status' : 'success', 'message' : "Created sequence.", 'result' : None}

def get_next_sequence(db,
	sequence_name,
	commit_after=1,
	leave_cursor_open=1):

	result = execute_sql_statement(db,
		'SELECT last_value, increment_by FROM %s' % (sequence_name),
		commit_after,
		leave_cursor_open)

	if result['status'] != 'success':
		return result

	data = result['result']

	result = execute_sql_statement(db,
		'UPDATE %s SET last_value = %d' % (sequence_name, data[0] + data[1]),
		commit_after,
		leave_cursor_open)

	return {'status' : 'success', 'message' : "Retrieved sequence number", 'result' : data[0]}

def sort_table_columns(table_data,table_name):

	column_name_keys = table_data[table_name].keys()

	column_name_keys.sort()

	sorted_columns = []

	for i in xrange(0,len(column_name_keys)):
		sorted_columns.append("")

	for i in column_name_keys:
		sorted_columns[int(table_data[table_name][i]['display_order'])-1] = i

	return sorted_columns
