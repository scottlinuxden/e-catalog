# $Id$
# Copyright (C) 1999 LinuXden, All Rights Reserved
# Copright Statement at http://www.linuxden.com/copyrighted_apps.html
# 
# it is imperative that there is white space between the = in following lines
tec_info = {}
tec_info['db_name'] = 'tec'

def define_tables():
	data_tables = { \
		'store_info' : { \
		'id' : { \
		'label' : 'Store Id', \
		'type': 'VARCHAR', \
		'db_size' : '10', \
		'form_size' : '10', \
		'default' : '1', \
		'display' : 'read-only', \
		'value' : '', \
		'display_order' : 1, \
		'required' : 1, \
		'leaveFocus' : None, \
		'gainFocus' : "displayHint('Enter your store id')" \
		}, \
		'name': { \
		'label' : 'Name', \
		'type' : 'VARCHAR', \
		'db_size' : '30', \
		'form_size' : '30', \
		'default' : None, \
		'display' : 'editable', \
		'value' : '', \
		'display_order' : 2, \
		'required' : 1, \
		'validation_routine' : 'checkBlankField', \
		'validation_arguments' : ['form.name',"'Name'"], \
		'leaveFocus' : None, \
		'gainFocus' : "displayHint('Enter your Store Name')" \
		}, \
		'slogan': { \
		'label' : 'Slogan', \
		'type' : 'VARCHAR', \
		'db_size' : '50', \
		'form_size' : '50', \
		'default' : None, \
		'display' : 'editable', \
		'value' : '', \
		'display_order' : 3, \
		'required' : 1, \
		'validation_routine' : 'checkBlankField', \
		'validation_arguments' : ['form.slogan',"'Slogan'"], \
		'leaveFocus' : None, \
		'gainFocus' : "displayHint('Enter your Store Slogan')" \
		}, \
		'address_line_1': { \
		'label' : 'Address Line 1', \
		'type' : 'VARCHAR', \
		'db_size' : '40', \
		'form_size' : '40', \
		'default' : None, \
		'display' : 'editable', \
		'value' : '', \
		'display_order' : 4, \
		'required' : 1, \
		'validation_routine' : 'checkBlankField', \
		'validation_arguments' : ['form.address_line_1',"'Store Address Line 1'"], \
		'leaveFocus' : None, \
		'gainFocus' : "displayHint('Enter your Store Address Line 1')" \
		}, \
		'address_line_2': { \
		'label' : 'Address Line 2', \
		'type' : 'VARCHAR', \
		'db_size' : '40', \
		'form_size' : '40', \
		'default' : None, \
		'display' : 'editable', \
		'value' : '', \
		'display_order' : 5, \
		'leaveFocus' : None, \
		'gainFocus' : "displayHint('Enter your Store Address Line 2')" \
		}, \
		'city' : { \
		'label' : 'City (Billing)', \
		'type' : 'VARCHAR', \
		'db_size' : '60', \
		'form_size' : '60', \
		'default' : None, \
		'display' : 'editable', \
		'value' : '', \
		'display_order' : 6, \
		'required' : 1, \
		'validation_routine' : 'checkBlankField', \
		'validation_arguments' : ['form.city',"'City'"], \
		'leaveFocus' : None, \
		'gainFocus' : "displayHint('Enter the city')" \
		}, \
		'state' : { \
		'label' : 'State (Billing)', \
		'type' : 'VARCHAR', \
		'db_size' : '2', \
		'form_size' : '2', \
		'default' : 'NA', \
		'display' : 'editable', \
		'value' : '', \
		'display_order' : 7, \
		'required' : 1, \
		'leaveFocus' : None, \
		'gainFocus' : "displayHint('Enter the abbreviated state')", \
		'lov' : "SELECT state_abbreviation FROM sales_tax_by_state ORDER BY state_abbreviation" \
		}, \
		'zip' : { \
		'label' : 'Zip Code', \
		'type' : 'VARCHAR', \
		'db_size' : '5', \
		'form_size' : '5', \
		'default' : None, \
		'display' : 'editable', \
		'value' : '', \
		'display_order' : 8, \
		'required' : 1, \
		'validation_routine' : 'valid_integer', \
		'validation_arguments' : ['form.zip',"''","'Zip Code (Billing)'","true"], \
		'leaveFocus' : None, \
		'gainFocus' : "displayHint('Enter the zip code')", \
		'format' : '#####' \
		}, \
		'owner': { \
		'label' : 'Owner Name', \
		'type' : 'VARCHAR', \
		'db_size' : '40', \
		'form_size' : '40', \
		'default' : None, \
		'display' : 'editable', \
		'value' : '', \
		'display_order' : 9, \
		'required' : 1, \
		'validation_routine' : 'checkBlankField', \
		'validation_arguments' : ['form.owner',"'Owner Name'"], \
		'leaveFocus' : None, \
		'gainFocus' : "displayHint('Enter Store Owner Name')" \
		}, \
		'email' : { \
		'label' : 'E-mail Address', \
		'type' : 'VARCHAR', \
		'db_size' : '40', \
		'form_size' : '40', \
		'default' : None, \
		'display' : 'editable', \
		'value' : '', \
		'display_order' : 10, \
		'leaveFocus' : None, \
		'gainFocus' : "displayHint('Enter the store e-mail address')" \
		}, \
		'toll_free_number' : { \
		'label' : 'Toll Free Phone Number', \
		'type' : 'VARCHAR', \
		'db_size' : '12', \
		'form_size' : '12', \
		'default' : None, \
		'display' : 'editable', \
		'value' : '', \
		'display_order' : 11, \
		'validation_routine' : 'valid_format', \
		'validation_arguments' : ["form.toll_free_number","'###-###-####'","'Toll Free Phone Number'","false"], \
		'leaveFocus' : None, \
		'gainFocus' : "displayHint('Enter the toll free phone number')", \
		'format' : "###-###-####" \
		}, \
		'phone_number_voice' : { \
		'label' : 'Phone Number (Voice)', \
		'type' : 'VARCHAR', \
		'db_size' : '12', \
		'form_size' : '12', \
		'default' : None, \
		'display' : 'editable', \
		'value' : '', \
		'display_order' : 12, \
		'validation_routine' : 'valid_format', \
		'validation_arguments' : ["form.phone_number_voice","'###-###-####'","'Daytime Phone Number'","false"], \
		'leaveFocus' : None, \
		'gainFocus' : "displayHint('Enter the phone number (Voice)')", \
		'format' : "###-###-####" \
		}, \
		'phone_number_fax' : { \
		'label' : 'Phone Number (FAX)', \
		'type' : 'VARCHAR', \
		'db_size' : '12', \
		'form_size' : '12', \
		'default' : None, \
		'display' : 'editable', \
		'value' : '', \
		'display_order' : 13, \
		'validation_routine' : 'valid_format', \
		'validation_arguments' : ["form.phone_number_fax","'###-###-####'","'Daytime Phone Number'","false"], \
		'leaveFocus' : None, \
		'gainFocus' : "displayHint('Enter the phone number (FAX)')", \
		'format' : "###-###-####" \
		}, \
		'category' : { \
		'label' : 'Mall Category', \
		'type' : 'VARCHAR', \
		'db_size' : '20', \
		'form_size' : '20', \
		'default' : 'NA', \
		'display' : 'editable', \
		'value' : '', \
		'display_order' : 14, \
		'required' : 1, \
		'leaveFocus' : None, \
		'gainFocus' : "displayHint('Enter the mall category')", \
		'lov' : "SELECT store_type FROM mall_store_types ORDER BY store_type" \
		}, \
		'description' : { \
		'label' : 'Description', \
		'type' : 'VARCHAR', \
		'db_size' : '512', \
		'form_size' : '512', \
		'default' : None, \
		'display' : 'editable', \
		'value' : '', \
		'display_order' : 15, \
		'required' : 1, \
		'validation_routine' : 'checkBlankField', \
		'validation_arguments' : ['form.description',"'Description'"], \
		'leaveFocus' : None, \
		'gainFocus' : "displayHint('Enter the description of your store')" \
		}, \
		'policies' : { \
		'label' : 'Ordering Policies', \
		'type' : 'VARCHAR', \
		'db_size' : '2048', \
		'form_size' : '2048', \
		'default' : None, \
		'display' : 'editable', \
		'value' : '', \
		'display_order' : 16, \
		'required' : 1, \
		'validation_routine' : 'checkBlankField', \
		'validation_arguments' : ['form.policies',"'Ordering Policies'"], \
		'leaveFocus' : None, \
		'gainFocus' : "displayHint('Enter the ordering policies of your store')" \
		}}, \
		'customers' : { \
		'id' : { \
		'label' : 'Customer Id', \
		'type': 'VARCHAR', \
		'db_size' : '10', \
		'form_size' : '10', \
		'default' : None, \
		'display' : 'read-only', \
		'value' : '', \
		'display_order' : 1, \
		'required' : 1, \
		'leaveFocus' : None, \
		'gainFocus' : "displayHint('Enter your customer id')" \
		}, \
		'first_name' : { \
		'label' : 'First Name', \
		'type' : 'VARCHAR', \
		'db_size' : '50', \
		'form_size' : '50', \
		'default' : None, \
		'display' : 'editable', \
		'value' : '', \
		'display_order' : 2, \
		'required' : 1, \
		'validation_routine' : 'checkBlankField', \
		'validation_arguments' : ['form.first_name',"'First Name'"], \
		'leaveFocus' : None, \
		'gainFocus' : "displayHint('Enter your First Name')" \
		}, \
		'middle_initial' : { \
		'label' : 'Middle Initial', \
		'type' : 'VARCHAR', \
		'db_size' : '1', \
		'form_size' : '1', \
		'default' : None, \
		'display' : 'editable', \
		'value' : '', \
		'display_order' : 3, \
		'leaveFocus' : None, \
		'gainFocus' : "displayHint('Enter your Middle Initial')" \
		}, \
		'last_name' : { \
		'label' : 'Last Name', \
		'type' : 'VARCHAR', \
		'db_size' : '50', \
		'form_size' : '50', \
		'default' : None, \
		'display' : 'editable', \
		'value' : '', \
		'display_order' : 4, \
		'required' : 1, \
		'validation_routine' : 'checkBlankField', \
		'validation_arguments' : ['form.last_name',"'Last Name'"], \
		'leaveFocus' : None, \
		'gainFocus' : "displayHint('Enter your Last Name')" \
		}, \
		'street_1' : { \
		'label' : 'Street Line 1 (Billing)', \
		'type' : 'VARCHAR', \
		'db_size' : '40', \
		'form_size' : '40', \
		'default' : None, \
		'display' : 'editable', \
		'value' : '', \
		'display_order' : 5, \
		'required' : 1, \
		'validation_routine' : 'checkBlankField', \
		'validation_arguments' : ['form.street_1',"'Street Line 1 (Billing)'"], \
		'leaveFocus' : None, \
		'gainFocus' : "displayHint('Enter your address')" \
		}, \
		'street_2' : { \
		'label' : 'Street Line 2 (Billing)', \
		'type' : 'VARCHAR', \
		'db_size' : '40', \
		'form_size' : '40', \
		'default' : None, \
		'display' : 'editable', \
		'value' : '', \
		'display_order' : 6, \
		'leaveFocus' : None, \
		'gainFocus' : "displayHint('Enter your street address')" \
		}, \
		'city' : { \
		'label' : 'City (Billing)', \
		'type' : 'VARCHAR', \
		'db_size' : '60', \
		'form_size' : '60', \
		'default' : None, \
		'display' : 'editable', \
		'value' : '', \
		'display_order' : 7, \
		'required' : 1, \
		'validation_routine' : 'checkBlankField', \
		'validation_arguments' : ['form.city',"'City'"], \
		'leaveFocus' : None, \
		'gainFocus' : "displayHint('Enter the city')" \
		}, \
		'state' : { \
		'label' : 'State (Billing)', \
		'type' : 'VARCHAR', \
		'db_size' : '2', \
		'form_size' : '2', \
		'default' : None, \
		'display' : 'editable', \
		'value' : '', \
		'display_order' : 8, \
		'required' : 1, \
		'leaveFocus' : None, \
		'gainFocus' : "displayHint('Enter the abbreviated state')", \
		'lov' : "SELECT state_abbreviation FROM sales_tax_by_state ORDER BY state_abbreviation" \
		}, \
		'zip' : { \
		'label' : 'Zip Code (Billing)', \
		'type' : 'VARCHAR', \
		'db_size' : '5', \
		'form_size' : '5', \
		'default' : None, \
		'display' : 'editable', \
		'value' : '', \
		'display_order' : 9, \
		'required' : 1, \
		'validation_routine' : 'valid_integer', \
		'validation_arguments' : ['form.zip',"''","'Zip Code (Billing)'","true"], \
		'leaveFocus' : None, \
		'gainFocus' : "displayHint('Enter the zip code')", \
		'format' : '#####' \
		}, \
		'email' : { \
		'label' : 'E-mail Address', \
		'type' : 'VARCHAR', \
		'db_size' : '40', \
		'form_size' : '40', \
		'default' : None, \
		'display' : 'editable', \
		'value' : '', \
		'display_order' : 10, \
		'leaveFocus' : None, \
		'gainFocus' : "displayHint('Enter the e-mail address')" \
		}, \
		'daytime_phone_number' : { \
		'label' : 'Daytime Phone Number', \
		'type' : 'VARCHAR', \
		'db_size' : '12', \
		'form_size' : '12', \
		'default' : None, \
		'display' : 'editable', \
		'value' : '', \
		'display_order' : 11, \
		'required' : 1, \
		'validation_routine' : 'valid_format', \
		'validation_arguments' : ["form.daytime_phone_number","'###-###-####'","'Daytime Phone Number'","true"], \
		'leaveFocus' : None, \
		'gainFocus' : "displayHint('Enter the daytime phone number')", \
		'format' : "###-###-####" \
		}, \
		'evening_phone_number' : { \
		'label' : 'Evening Phone Number', \
		'type' : 'VARCHAR', \
		'db_size' : '12', \
		'form_size' : '12', \
		'default' : None, \
		'display' : 'editable', \
		'value' : '', \
		'display_order' : 12, \
		'required' : 1, \
		'validation_routine' : 'valid_format', \
		'validation_arguments' : ["form.evening_phone_number","'###-###-####'","'Evening Phone Number'","false"], \
		'leaveFocus' : None, \
		'gainFocus' : "displayHint('Enter the evening phone number')", \
		'format' : "###-###-####" \
		}, \
		'account_username' : { \
		'label' : 'Account Username', \
		'type' : 'VARCHAR', \
		'db_size' : '9', \
		'form_size' : '9', \
		'default' : None, \
		'display' : 'editable', \
		'value' : '', \
		'display_order' : 13, \
		'required' : 1, \
		'validation_routine' : 'checkBlankField', \
		'validation_arguments' : ['form.account_username',"'Account Username'"], \
		'leaveFocus' : None, \
		'gainFocus' : "displayHint('Enter a username to access your account data')" \
		}, \
		'account_password' : { \
		'label' : 'Account Password', \
		'type' : 'VARCHAR', \
		'db_size' : '10', \
		'form_size' : '10', \
		'default' : None, \
		'display' : 'editable', \
		'form_input_type' : 'password', \
		'value' : '', \
		'display_order' : 14, \
		'required' : 1, \
		'validation_routine' : 'checkBlankField', \
		'validation_arguments' : ['form.account_password',"'Account Password'"], \
		'leaveFocus' : None, \
		'gainFocus' : "displayHint('Enter a password to access your account data')" \
		}}, \
		'orders' : { \
		'id' : { \
		'label' : 'Order Id', \
		'type' : 'VARCHAR', \
		'db_size' : '10', \
		'form_size' : '10', \
		'default' : None, \
		'display' : 'read-only', \
		'value' : '', \
		'display_order' : 1, \
		'required' : 1, \
		'leaveFocus' : None, \
		'gainFocus' : "displayHint('Enter the order id')" \
		}, \
		'customer_id' : { \
		'label' : 'Customer Id', \
		'type' : 'VARCHAR', \
		'db_size' : '10', \
		'form_size' : '10', \
		'default' : None, \
		'display' : 'editable', \
		'value' : '', \
		'display_order' : 2, \
		'required' : 1, \
		'validation_routine' : 'valid_integer', \
		'validation_arguments' : ['form.customer_id',"''","'Customer Id'","true"], \
		'leaveFocus' : None, \
		'gainFocus' : "displayHint('Enter the customer id')" \
		}, \
		'creation_date' : { \
		'label' : 'Creation Date', \
		'type' : 'VARCHAR', \
		'db_size' : '10', \
		'form_size' : '10', \
		'default' : None, \
		'display' : 'editable', \
		'value' : '', \
		'display_order' : 3, \
		'required' : 1, \
		'validation_routine' : 'valid_date', \
		'validation_arguments' : ['form.creation_date',"'Creation Date'","true"], \
		'leaveFocus' : None, \
		'gainFocus' : "displayHint('Enter the order creation date')", \
		'format' : "MM-DD-YYYY" \
		}, \
		'shipped_date' : { \
		'label' : 'Order Ship Date', \
		'type' : 'VARCHAR', \
		'db_size' : '10', \
		'form_size' : '10', \
		'default' : None, \
		'display' : 'editable', \
		'value' : '', \
		'display_order' : 4, \
		'validation_routine' : 'valid_date', \
		'validation_arguments' : ['form.shipped_date',"'Order Ship Date'","false"], \
		'leaveFocus' : None, \
		'gainFocus' : "displayHint('Enter the shipped date')", \
		'format' : "MM-DD-YYYY" \
		}, \
		'processor' : { \
		'label' : 'Order Processor', \
		'type' : 'VARCHAR', \
		'db_size' : '20', \
		'form_size' : '20', \
		'default' : None, \
		'display' : 'editable', \
		'value' : '', \
		'display_order' : 5, \
		'leaveFocus' : None, \
		'gainFocus' : "displayHint('Enter the id of the processor')" \
		}, \
		'shipping_street1' : { \
		'label' : 'Street Line 1 (Shipping)', \
		'type' : 'VARCHAR', \
		'db_size' : '40', \
		'form_size' : '40', \
		'default' : None, \
		'display' : 'editable', \
		'value' : '', \
		'display_order' : 6, \
		'required' : 1, \
		'validation_routine' : 'checkBlankField', \
		'validation_arguments' : ['form.shipping_street1',"'Street Line 1 (Shipping)'"], \
		'leaveFocus' : None, \
		'gainFocus' : "displayHint('Enter the shipping street line 1')" \
		}, \
		'shipping_street2' : { \
		'label' : 'Street Line 2 (Shipping)', \
		'type' : 'VARCHAR', \
		'db_size' : '40', \
		'form_size' : '40', \
		'default' : None, \
		'display' : 'editable', \
		'value' : '', \
		'display_order' : 7, \
		'leaveFocus' : None, \
		'gainFocus' : "displayHint('Enter the shipping street line 2')" \
		}, \
		'city' : { \
		'label' : 'City (Shipping)', \
		'type' : 'VARCHAR', \
		'db_size' : '60', \
		'form_size' : '60', \
		'default' : None, \
		'display' : 'editable', \
		'value' : '', \
		'display_order' : 8, \
		'required' : 1, \
		'validation_routine' : 'checkBlankField', \
		'validation_arguments' : ['form.city',"'City (Shipping)'"], \
		'leaveFocus' : None, \
		'gainFocus' : "displayHint('Enter the city')" \
		}, \
		'state' : { \
		'label' : 'State (Shipping)', \
		'type' : 'VARCHAR', \
		'db_size' : '2', \
		'form_size' : '2', \
		'default' : None, \
		'display' : 'editable', \
		'value' : '', \
		'display_order' : 9, \
		'required' : 1, \
		'leaveFocus' : None, \
		'gainFocus' : "displayHint('Enter an abbreviated state')", \
		'lov' : "SELECT state_abbreviation FROM sales_tax_by_state ORDER BY state_abbreviation" \
		}, \
		'zip' : { \
		'label' : 'Zip Code (Shipping)', \
		'type' : 'VARCHAR', \
		'db_size' : '5', \
		'form_size' : '5', \
		'default' : None, \
		'display' : 'editable', \
		'value' : '', \
		'display_order' : 10, \
		'required' : 1, \
		'validation_routine' : 'valid_integer', \
		'validation_arguments' : ['form.zip',"''","'Zip Code (Shipping)'","true"], \
		'leaveFocus' : None, \
		'gainFocus' : "displayHint('Enter the zip code')", \
		'format' : '#####' \
		}, \
		'method_of_payment' : { \
		'label' : 'Payment Method', \
		'type' : 'VARCHAR', \
		'db_size' : '25', \
		'form_size' : '25', \
		'default' : None, \
		'display' : 'editable', \
		'value' : '', \
		'display_order' : 11, \
		'required' : 1, \
		'leaveFocus' : None, \
		'gainFocus' : "displayHint('Enter the payment method')", \
		'lov' : "SELECT payment_type FROM payment_methods ORDER BY payment_type" \
		}, \
		'credit_card_number' : { \
		'label' : 'Credit Card Number', \
		'type' : 'VARCHAR', \
		'db_size' : '16', \
		'form_size' : '16', \
		'default' : None, \
		'display' : 'editable', \
		'value' : '', \
		'display_order' : 12, \
		'required' : 1, \
		'validation_routine' : 'valid_integer', \
		'validation_arguments' : ['form.credit_card_number',"''","'Credit Card Number'","true"], \
		'leaveFocus' : None, \
		'gainFocus' : "displayHint('Enter the credit card number')", \
		'format' : "################" \
		}, \
		'card_expiration_date' : { \
		'label' : 'Credit Card Expiration Date', \
		'type' : 'VARCHAR', \
		'db_size' : '10', \
		'form_size' : '10', \
		'default' : None, \
		'display' : 'editable', \
		'value' : '', \
		'required' : 1, \
		'display_order' : 13, \
		'validation_routine' : 'valid_date', \
		'validation_arguments' : ['form.card_expiration_date',"'Credit Card Expiration Date'","true"], \
		'leaveFocus' : None, \
		'gainFocus' : "displayHint('Enter the credit card expiration date')", \
		'format' : "MM-DD-YYYY" \
		}, \
		'shipping_method' : { \
		'label' : 'Shipping Method', \
		'type' : 'VARCHAR', \
		'db_size' : '30', \
		'form_size' : '30', \
		'default' : None, \
		'display' : 'editable', \
		'value' : '', \
		'display_order' : 14, \
		'required' : 1, \
		'leaveFocus' : None, \
		'gainFocus' : "displayHint('Enter the shipping method')", \
		'lov' : "SELECT method FROM shipping_methods ORDER BY method" \
		}, \
		'shipping_handling' : { \
		'label' : 'Shipping Handling', \
		'type' : 'FLOAT', \
		'db_size' : '9,2', \
		'form_size' : '10', \
		'default' : '0.00', \
		'display' : 'editable', \
		'value' : '', \
		'display_order' : 15, \
		'required' : 1, \
		'validation_routine' : 'valid_money', \
		'validation_arguments' : ['form.shipping_handling',"''","'Shipping Handling'","true"], \
		'leaveFocus' : None, \
		'gainFocus' : "displayHint('Enter the shipping/handling')" \
		}, \
		'subtotal' : { \
		'label' : 'Subtotal', \
		'type' : 'FLOAT', \
		'db_size' : '9,2', \
		'form_size' : '10', \
		'default' : '0.00', \
		'display' : 'editable', \
		'value' : '', \
		'display_order' : 16, \
		'required' : 1, \
		'validation_routine' : 'valid_money', \
		'validation_arguments' : ['form.subtotal',"''","'Subtotal'","true"], \
		'leaveFocus' : None, \
		'gainFocus' : "displayHint('Enter the subtotal')", \
		'format' : "#######.##" \
		}, \
		'sales_tax' : { \
		'label' : 'Sales Tax', \
		'type' : 'FLOAT', \
		'db_size' : '9,2', \
		'form_size' : '10', \
		'default' : '0.00', \
		'display' : 'editable', \
		'value' : '', \
		'display_order' : 17, \
		'required' : 1, \
		'validation_routine' : 'valid_money', \
		'validation_arguments' : ['form.sales_tax',"''","'Sales Tax'","true"], \
		'leaveFocus' : None, \
		'gainFocus' : "displayHint('Enter the sales tax')", \
		'format' : "#######.##" \
		}, \
		'total' : { \
		'label' : 'Total', \
		'type' : 'FLOAT', \
		'db_size' : '9,2', \
		'form_size' : '10', \
		'default' : '0.00', \
		'display' : 'editable', \
		'value' : '', \
		'required' : 1, \
		'validation_routine' : 'valid_money', \
		'validation_arguments' : ['form.total',"''","'Total'","true"], \
		'display_order' : 18, \
		'leaveFocus' : None, \
		'gainFocus' : "displayHint('Enter the total')", \
		'format' : "#######.##" \
		}, \
		'order_status' : { \
		'label' : 'Order Status', \
		'type' : 'VARCHAR', \
		'db_size' : '40', \
		'form_size' : '40', \
		'default' : None, \
		'display' : 'editable', \
		'value' : '', \
		'display_order' : 19, \
		'required' : 1, \
		'leaveFocus' : None, \
		'gainFocus' : "displayHint('Enter the order status')", \
		'lov' : "SELECT status_of_order FROM order_status_values ORDER BY status_of_order" \
		}, \
		'tracking_number' : { \
		'label' : 'Tracking Number', \
		'type' : 'VARCHAR', \
		'db_size' : '20', \
		'form_size' : '20', \
		'default' : None, \
		'display' : 'editable', \
		'validation_routine' : 'valid_integer', \
		'validation_arguments' : ['form.tracking_number',"''","'Tracking Number'","false"], \
		'value' : '', \
		'display_order' : 20, \
		'leaveFocus' : None, \
		'gainFocus' : "displayHint('Enter the tracking number')", \
		'format' : "####################" \
		}},\
		'order_items' : { \
		'line_item' : { \
		'label' : 'Line Item', \
		'type' : 'VARCHAR', \
		'db_size' : '10', \
		'form_size' : '10',
		'default' : None, \
		'display' : 'editable', \
		'value' : '', \
		'display_order' : 1, \
		'leaveFocus' : None, \
		'gainFocus' : "displayHint('Enter the line item')" \
		}, \
		'order_id' : { \
		'label' : 'Order Id', \
		'type' : 'VARCHAR', \
		'db_size' : '10', \
		'form_size' : '10', \
		'default' : None, \
		'display' : 'editable', \
		'value' : '', \
		'display_order' : 2, \
		'leaveFocus' : None, \
		'gainFocus' : "displayHint('Enter the order id')" \
		}, \
		'product_id' : { \
		'label' : 'Product Id:', \
		'type' : 'VARCHAR', \
		'db_size' : '10', \
		'form_size' : '10', \
		'default' : None, \
		'display' : 'editable', \
		'value' : '', \
		'display_order' : 3, \
		'leaveFocus' : None, \
		'gainFocus' : "displayHint('Enter the product id')" \
		}, \
		'quantity' : { \
		'label' : 'Quantity', \
		'type' : 'INTEGER', \
		'db_size' : '4', \
		'form_size' : '3', \
		'default' : '0', \
		'display' : 'editable', \
		'value' : '', \
		'display_order' : 4, \
		'leaveFocus' : None, \
		'gainFocus' : "displayHint('Enter the quantity')", \
		'format' : "###" \
		}, \
		'quantity_shipped' : { \
		'label' : 'Quantity Shipped', \
		'type' : 'INTEGER', \
		'db_size' : '4', \
		'form_size' : '3', \
		'default' : '0', \
		'display' : 'editable', \
		'value' : '', \
		'display_order' : 5, \
		'leaveFocus' : None, \
		'gainFocus' : "displayHint('Enter the quantity shipped')", \
		'format' : "###" \
		}, \
		'price' : { \
		'label' : 'Price', \
		'type' : 'FLOAT', \
		'db_size' : '9,2', \
		'form_size' : '10', \
		'default' : '0.00', \
		'display' : 'editable', \
		'value' : '', \
		'display_order' : 6, \
		'leaveFocus' : None, \
		'gainFocus' : "displayHint('Enter the price of product')", \
		'format' : "#######.##" \
		}, \
		'line_subtotal' : { \
		'label' : 'Line Subtotal', \
		'type' : 'FLOAT', \
		'db_size' : '9,2', \
		'form_size' : '10', \
		'default' : '0.00', \
		'display' : 'editable', \
		'value' : '', \
		'display_order' : 7, \
		'leaveFocus' : None, \
		'gainFocus' : "displayHint('Enter the line subtotal')", \
		'format' : "#######.##" \
		}}, \
		'sales_tax_by_state' : { \
		'state_name' : { \
		'label' : 'State Full Name', \
		'type' : 'VARCHAR', \
		'db_size' : '30', \
		'form_size' : '30', \
		'default' : None, \
		'display' : 'editable', \
		'value' : '', \
		'display_order' : 1, \
		'required' : 1, \
		'validation_routine' : 'checkBlankField', \
		'validation_arguments' : ['form.state_name',"'State Name'"], \
		'leaveFocus' : None, \
		'gainFocus' : "displayHint('Enter the state full name')" \
		}, \
		'state_abbreviation' : { \
		'label' : 'State Abbreviation', \
		'type' : 'VARCHAR', \
		'db_size' : '2', \
		'form_size' : '2', \
		'default' : None, \
		'display' : 'editable', \
		'value' : '', \
		'display_order' : 2, \
		'required' : 1, \
		'validation_routine' : 'checkBlankField', \
		'validation_arguments' : ['form.state_abbreviation',"'State Abbreviation'"], \
		'leaveFocus' : None, \
		'gainFocus' : "displayHint('Enter the state abbreviation')" \
		}, \
		'tax' : { \
		'label' : 'Sales Tax', \
		'type' : 'FLOAT', \
		'db_size' : '6,5', \
		'form_size' : '7', \
		'default' : '0.00', \
		'display' : 'editable', \
		'value' : '', \
		'display_order' : 3, \
		'required' : 1, \
		'validation_routine' : 'valid_money', \
		'validation_arguments' : ['form.tax',"''","'Sales Tax'","true"], \
		'leaveFocus' : None, \
		'gainFocus' : "displayHint('Enter the sales tax charged in state')", \
		'format' : "#.####" \
		}}, \
		'payment_methods' : { \
		'payment_type' : { \
		'label' : 'Payment Method', \
		'type' : 'VARCHAR', \
		'db_size' : '30', \
		'form_size' : '30', \
		'default' : None, \
		'display' : 'editable', \
		'value' : '', \
		'display_order' : 1, \
		'required' : 1, \
		'validation_routine' : 'checkBlankField', \
		'validation_arguments' : ['form.payment_type',"'Payment Method'"], \
		'leaveFocus' : None, \
		'gainFocus' : "displayHint('Enter the payment method')" \
		}, \
		'image' : { \
		'label' : 'Image filename', \
		'type' : 'VARCHAR', \
		'db_size' : '50', \
		'form_size' : '50', \
		'default' : None, \
		'display' : 'editable', \
		'value' : '', \
		'display_order' : 2, \
		'leaveFocus' : None, \
		'gainFocus' : "displayHint('Enter the payment method image filename')" \
		}}, \
		'product_categories' : { \
		'category' : { \
		'label' : 'Category', \
		'type' : 'VARCHAR', \
		'db_size' : '20', \
		'form_size' : '20', \
		'default' : None, \
		'display' : 'editable', \
		'value' : '', \
		'display_order' : 1, \
		'required' : 1, \
		'validation_routine' : 'checkBlankField', \
		'validation_arguments' : ['form.category',"'Category'"], \
		'leaveFocus' : None, \
		'gainFocus' : "displayHint('Enter a category')", \
		}}, \
		'order_status_values' : { \
		'status_of_order' : { \
		'label' : 'Order Status', \
		'type' : 'VARCHAR', \
		'db_size' : '40', \
		'form_size' : '40', \
		'default' : None, \
		'display' : 'editable', \
		'value' : '', \
		'display_order' : 1, \
		'required' : 1, \
		'validation_routine' : 'checkBlankField', \
		'validation_arguments' : ['form.status_of_order',"'Order Status'"], \
		'leaveFocus' : None, \
		'gainFocus' : "displayHint('Enter the order status')" \
		}}, \
		'shipping_methods' : { \
		'method' : { \
		'label' : 'Shipping Method', \
		'type' : 'VARCHAR', \
		'db_size' : '30', \
		'form_size' : '30', \
		'default' : None, \
		'display' : 'editable', \
		'value' : '', \
		'display_order' : 1, \
		'leaveFocus' : None, \
		'gainFocus' : "displayHint('Enter the shipping method')" \
		}}, \
		'products' : { \
		'id' : { \
		'label' : 'Product Id', \
		'type' : 'VARCHAR', \
		'db_size' : '10', \
		'form_size' : '10', \
		'default' : None, \
		'display' : 'read-only', \
		'value' : '', \
		'display_order' : 1, \
		'required' : 1, \
		'leaveFocus' : None, \
		'gainFocus' : "displayHint('Enter the product id')" \
		}, \
		'category' : { \
		'label' : 'Category', \
		'type' : 'VARCHAR', \
		'db_size' : '20', \
		'form_size' : '20', \
		'default' : None, \
		'display' : 'editable', \
		'value' : '', \
		'display_order' : 2, \
		'required' : 1, \
		'leaveFocus' : None, \
		'gainFocus' : "displayHint('Enter a category')", \
		'lov' : "SELECT category FROM product_categories ORDER BY category" \
		}, \
		'quantity_on_hand' : { \
		'label' : 'Quantity On Hand', \
		'type' : 'INTEGER', \
		'db_size' : '4', \
		'form_size' : '4', \
		'default' : '0', \
		'display' : 'editable', \
		'value' : '', \
		'display_order' : 3, \
		'required' : 1, \
		'validation_routine' : 'valid_integer', \
		'validation_arguments' : ['form.quantity_on_hand',"''","'Quantity on Hand'","true"], \
		'leaveFocus' : None, \
		'gainFocus' : "displayHint('Enter the quantity on hand in inventory')", \
		'format' : "####" \
		}, \
		'quantity_sold' : { \
		'label' : 'Quantity Sold', \
		'type' : 'INTEGER', \
		'db_size' : '4', \
		'form_size' : '4', \
		'default' : '0', \
		'display' : 'editable', \
		'value' : '', \
		'display_order' : 4, \
		'required' : 1, \
		'validation_routine' : 'valid_integer', \
		'validation_arguments' : ['form.quantity_sold',"''","'Quantity Sold'","true"], \
		'leaveFocus' : None, \
		'gainFocus' : "displayHint('Enter quantity sold')", \
		'format' : "####" \
		}, \
		'keep_on_hand' : { \
		'label' : 'Keep On Hand', \
		'type' : 'INTEGER', \
		'db_size' : '4', \
		'form_size' : '4', \
		'default' : '0', \
		'display' : 'editable', \
		'value' : '', \
		'display_order' : 5, \
		'required' : 1, \
		'validation_routine' : 'valid_integer', \
		'validation_arguments' : ['form.keep_on_hand',"''","'Keep on Hand'","true"], \
		'leaveFocus' : None, \
		'gainFocus' : "displayHint('Enter the number of items to keep in stock')", \
		'format' : "####" \
		}, \
		'description' : { \
		'label' : 'Short Description', \
		'type' : 'VARCHAR', \
		'db_size' : '40', \
		'form_size' : '40', \
		'default' : None, \
		'display' : 'editable', \
		'value' : '', \
		'display_order' : 6, \
		'required' : 1, \
		'validation_routine' : 'checkBlankField', \
		'validation_arguments' : ['form.description',"'Short Description'"], \
		'leaveFocus' : None, \
		'gainFocus' : "displayHint('Enter short description of product')" \
		}, \
		'long_description' : { \
		'label' : 'Long Description', \
		'type' : 'VARCHAR', \
		'db_size' : '1024', \
		'form_size' : '1024', \
		'default' : None, \
		'display' : 'editable', \
		'value' : '', \
		'display_order' : 7, \
		'leaveFocus' : None, \
		'gainFocus' : "displayHint('Enter the long description')" \
		}, \
		'price' : { \
		'label' : 'Price', \
		'type' : 'FLOAT', \
		'db_size' : '9,2', \
		'form_size' : '10', \
		'default' : '0.00', \
		'display' : 'editable', \
		'value' : '', \
		'display_order' : 8, \
		'required' : 1, \
		'validation_routine' : 'valid_money', \
		'validation_arguments' : ['form.price',"''","'Price'","true"], \
		'leaveFocus' : None, \
		'gainFocus' : "displayHint('Enter the price of product')", \
		'format' : "#######.##" \
		}, \
		'shipping_weight' : { \
		'label' : 'Shipping Weight', \
		'type' : 'INTEGER', \
		'db_size' : '4', \
		'form_size' : '4', \
		'default' : '0', \
		'display' : 'editable', \
		'value' : '', \
		'display_order' : 9, \
		'required' : 1, \
		'validation_routine' : 'valid_integer', \
		'validation_arguments' : ['form.shipping_weight',"''","'Shipping Weight'","true"], \
		'leaveFocus' : None, \
		'gainFocus' : "displayHint('Enter the shipping weight of item')", \
		'format' : "####" \
		}, \
		'image' : { \
		'label' : 'Product Image Filename', \
		'type' : 'VARCHAR', \
		'db_size' : '50', \
		'form_size' : '50', \
		'default' : None, \
		'display' : 'editable', \
		'value' : '', \
		'display_order' : 10, \
		'required' : 1, \
		'validation_routine' : 'checkBlankField', \
		'validation_arguments' : ['form.image',"'Product Image Filename'"], \
		'leaveFocus' : None, \
		'gainFocus' : "displayHint('Enter the image filename of the products picture')" \
		}, \
		'literature' : { \
		'label' : 'Literature Filename', \
		'type' : 'VARCHAR', \
		'db_size' : '50', \
		'form_size' : '50', \
		'default' : None, \
		'display' : 'editable', \
		'value' : '', \
		'display_order' : 11, \
		'leaveFocus' : None, \
		'gainFocus' : "displayHint('Enter the filename for the product literature page')" \
		}} \
		}

	return data_tables
