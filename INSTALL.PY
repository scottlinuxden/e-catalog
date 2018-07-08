#!/usr/bin/env python
# $Id: install.py,v 1.1 2000/07/16 00:10:04 davis Exp davis $
# Copyright (C) 1999 LinuXden, All Rights Reserved
# Copright Statement at http://www.linuxden.com/copyrighted_apps.html
# 
import stat
import glob
import string
import compileall
import os_utils
import shutil
import os, string, sys
import types
import commands
import file_io
import gadfly_utils

class install:

	def __init__(self,
		application_name,
		db_name=None,
		db_location=None):

		self.application_name = application_name
		self.db_name = db_name
		self.db_location = db_location

	def create_declarations(self):

		status, declaration_template_lines = file_io.readFromFile(self.application_name + '.template')

		line_index = 0

		for line in declaration_template_lines:

			field = string.split(line)

			if len(field) < 3:
				line_index = line_index + 1
				continue

			if field[0][:len('tec_info')] == "tec_info":

				if field[1] == '=':

					if field[2] == "'{{{TEC_DB_NAME}}}'":
						declaration_template_lines[line_index] = field[0] + ' ' + field[1] + " '" + self.db_name + "'"

			line_index = line_index + 1

		status, output = file_io.writeToFile('declarations.py', declaration_template_lines)

		if status != 'success':
			print output
			sys.exit(1)

	def create_db(self):

		import declarations

		table_data = declarations.define_tables()

		result = gadfly_utils.create_db(
			database_name = self.db_name,
			database_location = self.db_location,
			overwrite_existing_db = 1)

		if result['status'] != "success":
			print result['message']
			sys.exit(1)

		db = result['result']

		result = gadfly_utils.create_tables(
			db = db,
			table_data = table_data,
			echo_statement = 1,
			commit_after = 1,
			leave_cursor_open = 1)

		if result["status"] != 'success':
			print result['message']
			sys.exit(1)

		result = gadfly_utils.create_sequence(db=db,
			sequence_name='customer_id_seq',
			start_value=101,
			increment_by=1,
			commit_after=1,
			leave_cursor_open=1)

		if result['status'] != 'success':
			print result['message']
			return result

		result = gadfly_utils.create_sequence(db=db,
			sequence_name='orders_id_seq',
			start_value=101,
			increment_by=1,
			commit_after=1,
			leave_cursor_open=1)

		if result['status'] != 'success':
			print result['message']
			return result

		result = gadfly_utils.create_sequence(db=db,
			sequence_name='products_id_seq',
			start_value=101,
			increment_by=1,
			commit_after=1,
			leave_cursor_open=1)

		if result['status'] != 'success':
			print result['message']
			return result

		result = gadfly_utils.insert_from_file(db=db,
			table_data=table_data,
			table_name='products',
			filename='tec_products.dat',
			delimiter=',',
			echo_statement=1,
			commit_after=1,
			leave_cursor_open=1)

		if result['status'] != 'success':
			print result['message']
			return result

		result = gadfly_utils.insert_from_file(db=db,
			table_data=table_data,
			table_name='sales_tax_by_state',
			filename='tec_sales_tax_by_state.dat',
			delimiter=',',
			echo_statement=1,
			commit_after=1,
			leave_cursor_open=1)

		if result['status'] != 'success':
			print result['message']
			return result

		result = gadfly_utils.insert_from_file(db=db,
			table_data=table_data,
			table_name='payment_methods',
			filename='tec_payment_methods.dat',
			delimiter=',',
			echo_statement=1,
			commit_after=1,
			leave_cursor_open=1)

		if result['status'] != 'success':
			print result['message']
			return result

		result = gadfly_utils.insert_from_file(db=db,
			table_data=table_data,
			table_name='shipping_methods',
			filename='tec_shipping_methods.dat',
			delimiter=',',
			echo_statement=1,
			commit_after=1,
			leave_cursor_open=1)

		if result['status'] != 'success':
			print result['message']
			return result

		result = gadfly_utils.insert_from_file(db=db,
			table_data=table_data,
			table_name='order_status_values',
			filename='tec_order_status_values.dat',
			delimiter=',',
			echo_statement=1,
			commit_after=1,
			leave_cursor_open=1)

		if result['status'] != 'success':
			print result['message']
			return result

		result = gadfly_utils.insert_from_file(db=db,
			table_data=table_data,
			table_name='product_categories',
			filename='tec_product_categories.dat',
			delimiter=',',
			echo_statement=1,
			commit_after=1,
			leave_cursor_open=1)

		if result['status'] != 'success':
			print result['message']
			return result

		result = gadfly_utils.insert_from_file(db=db,
			table_data=table_data,
			table_name='store_info',
			filename='tec_store_info.dat',
			delimiter='|',
			echo_statement=1,
			commit_after=1,
			leave_cursor_open=1)

		if result['status'] != 'success':
			print result['message']
			return result

	def install_to_destination(self):

		status, dist_list = file_io.readFromFile(os.path.expandvars(os.path.join('${PWD}',self.application_name + '.files')))

		if not os.path.exists(os.path.join(os.sep, 'home', self.application_name)):
			os.mkdir(os.path.join(os.sep, 'home', self.application_name))

		if not os.path.exists(os.path.join(os.sep, 'home', self.application_name, 'db')):
			os.mkdir(os.path.join(os.sep, 'home', self.application_name, 'db'))

		if not os.path.exists(os.path.join(os.sep, 'home', self.application_name, 'bin')):
			os.mkdir(os.path.join(os.sep, 'home', self.application_name, 'bin'))
		if not os.path.exists(os.path.join(os.sep, 'home', self.application_name, 'images')):
			os.mkdir(os.path.join(os.sep, 'home', self.application_name, 'images'))
		if not os.path.exists(os.path.join(os.sep, 'home', self.application_name, 'icons')):
			os.mkdir(os.path.join(os.sep, 'home', self.application_name, 'icons'))

		if os.path.exists(os.path.join('.', 'staging')):
			os_utils.super_remove(os.path.join('.', 'staging'))

		os.mkdir(os.path.join('.', 'staging'))

		for curfile in dist_list:
			shutil.copy(curfile,os.path.join('.','staging'))

		os.chdir(os.path.join('.','staging'))

		compileall.compile_dir('.',0,None,0)

		os.chdir(os.path.join('..'))

		for curfile in glob.glob(os.path.join('.','staging','*.pyc')):
			shutil.copy(curfile,os.path.join(os.sep, 'home',self.application_name,'bin'))

		for curfile in glob.glob(os.path.join('.','images','*')):
			shutil.copy(curfile,os.path.join(os.sep, 'home',self.application_name,'images'))

		for curfile in glob.glob(os.path.join('.','icons','*')):
			shutil.copy(curfile,os.path.join(os.sep, 'home',self.application_name,'icons'))

		os_utils.set_file_mode(filename = os.path.join(os.sep, 'home',self.application_name),
			user = ['r','w','x'])

		os_utils.set_file_mode(filename = os.path.join(os.sep, 'home',self.application_name,'db'),
			user = ['r','w','x'])

		for curfile in glob.glob(os.path.join(os.sep, 'home',self.application_name,'db','*')):
			os_utils.set_file_mode(filename = curfile,
				user = ['r','w','x'])

		os_utils.set_file_mode(filename = os.path.join(os.sep, 'home',self.application_name,'bin'),
			user = ['r','w','x'])

		for curfile in glob.glob(os.path.join(os.sep, 'home',self.application_name,'bin','*')):
			os_utils.set_file_mode(filename = curfile,
				user = ['r','w','x'])

		os_utils.set_file_mode(filename = os.path.join(os.sep, 'home',self.application_name,'images'),
			user = ['r','w','x'])

		for curfile in glob.glob(os.path.join(os.sep, 'home',self.application_name,'images','*')):
			os_utils.set_file_mode(filename = curfile,
				user = ['r','w'])

		os_utils.set_file_mode(filename = os.path.join(os.sep, 'home',self.application_name,'icons'),
			user = ['r','w','x'])

		for curfile in glob.glob(os.path.join(os.sep, 'home',self.application_name,'icons','*')):
			os_utils.set_file_mode(filename = curfile,
				user = ['r','w'])

		status, output = os_utils.super_chown(
			directory_name=os.path.join(os.sep,'home',self.application_name),
			username='davis',
			groupname='davis')

		if status != 'success':
			print 'Ownership settings of tec %s failed.' % (os.path.join(os.sep,'home',self.application_name))

if __name__ == "__main__":

	install_engine = install('tec',
		'tec',
		os.path.join(os.sep,'home','tec','db'))

	install_engine.create_declarations()
	install_engine.create_db()
	install_engine.install_to_destination()
