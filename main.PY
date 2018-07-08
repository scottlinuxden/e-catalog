#!/usr/bin/env python
# $Id: gadfly_utils.py,v 1.2 2000/07/16 00:00:17 davis Exp davis $
# Copyright (C) 1999 LinuXden, All Rights Reserved
# Copright Statement at http://www.linuxden.com/copyrighted_apps.html
# 
from   Tkinter import *
import Pmw
import os
import AppShell
import Image, ImageTk
import gadfly_utils
import declarations
import string

# Load the PIL plugins for all image types...
for m in ["GifImagePlugin", "JpegImagePlugin"]:
	try:
		__import__(m)
	except ImportError:
		pass # ignore missing driver for now

Image._initialized = 1

path = ""
imgs = ""

catalog = None
tree_canvas = None
tree_canvas_scrollbar = None
default_font = ('Arial',8,'bold')
default_small_font=('Arial',8,'bold')
copyright_font=('Arial',8,'italic')
display_customer_dialog = 0

class Node:
	def __init__(self, master, tree, icon=None, 
		openicon=None, name=None, db_key=None, action=None):
		self.master, self.tree = master, tree
		self.db_key = db_key
		self.icon = PhotoImage(file=icon)
		if openicon:
			self.openicon = PhotoImage(file=openicon)
		else:
			self.openicon = None
		self.width, self.height = 1.5*self.icon.width(), \
			1.5*self.icon.height()
		self.name = name
		self.var = StringVar()
		self.var.set(name)
		#self.text = Entry(tree, textvariable=self.var, bg=tree.bg,
		#                                 bd=0, width=len(name)+2, font=tree.font,
		#                                 fg=tree.textcolor, insertwidth=1,
		#                                 highlightthickness=1, 
		#                                 highlightbackground=tree.bg,
		#                                 selectbackground="#044484",
		#                                 selectborderwidth=0,
		#                                 selectforeground='white')
		self.action = action
		self.x = self.y = 0  #drawing location
		self.child = []
		self.state = 'colapsed'
		self.selected = 0

	def addChild(self, tree, icon=None, openicon=None, name=None, db_key=None,
		action=None):  
		child = Node(self, tree, icon, openicon, name, db_key, action) 
		self.child.append(child)
		self.tree.display()
		return child             

	def deleteChild(self, child):   
		self.child.remove(child)
		self.tree.display()

	def textForget(self):
		#self.text.place_forget()
		for child in self.child:
			child.textForget()                              

	def deselect(self):
		self.selected = 0
		for child in self.child:
			child.deselect()

	def boxpress(self, event=None):
		global tree_canvas, tree_canvas_scrollbar

		if self.state == 'expanded':
			self.state = 'colapsed'
		elif self.state == 'colapsed':
			self.state = 'expanded'

		catalog.busyStart()
		self.tree.display()
		catalog.busyEnd()
		tree_canvas.configure(scrollregion=tree_canvas.bbox(ALL))

	def invoke(self, event=None):
		if not self.selected:
			self.tree.deselectall()
			self.selected = 1

			#self.tree.display()
			if self.action:
				self.action(self.name, self.db_key)
		#self.name = self.text.get()
		#self.text.config(width=len(self.name)+2)

	def displayIconText(self):
		tree, text = self.tree, None
		if self.selected and self.openicon:
			self.pic = tree.create_image(self.x, self.y,
				image=self.openicon)
		else:
			self.pic = tree.create_image(self.x, self.y,
				image=self.icon)

		tree.create_text(self.x+self.width/2,self.y,text=self.name,anchor=W,tags=('text','rect'))

		#text.place(x=self.x+self.width/2, y=self.y, anchor=W)
		#text.bind("<ButtonPress-1>", self.invoke)
		tree.tag_bind(self.pic, "<ButtonPress-1>", self.invoke, "+")
		#text.bind("<Double-Button-1>", self.boxpress)
		tree.tag_bind(self.pic, "<Double-Button-1>",
			self.boxpress, "+")

	def displayRoot(self):
		if self.state == 'expanded':                                            
			for child in self.child:
				child.display()                 
		self.displayIconText()

	def displayLeaf(self):
		self.tree.hline(self.y, self.master.x+1, self.x)
		self.tree.vline(self.master.x, self.master.y, self.y)
		self.displayIconText()

	def displayBranch(self):
		master, tree = self.master, self.tree
		x, y = self.x, self.y                   
		tree.hline(y, master.x, x)                 
		tree.vline(master.x, master.y, y)
		if self.state == 'expanded' and self.child != []:                  
			for child in self.child:
				child.display()                         
			box = tree.create_image(master.x, y,
				image=tree.minusnode)   
		elif self.state == 'colapsed' and self.child != []: 
			box = tree.create_image(master.x, y,
				image=tree.plusnode) 
		tree.tag_bind(box, "<ButtonPress-1>", self.boxpress, "+")
		self.displayIconText()

	def findLowestChild(self, node):
		if node.state == 'expanded' and node.child != []:
			return self.findLowestChild(node.child[-1])
		else:
			return node             

	def display(self):
		master, tree = self.master, self.tree
		n = master.child.index(self)
		self.x = master.x + self.width
		if n == 0:
			self.y = master.y + (n+1)*self.height
		else:   
			previous = master.child[n-1]                    
			self.y = self.findLowestChild(previous).y + self.height
		if master == tree:
			self.displayRoot()
		elif master.state == 'expanded':
			if self.child == []:
				self.displayLeaf() 
			else:           
				self.displayBranch()
			tree.lower('line')

		#self.tree.viewPortCanvas.wait_visibility()

class Tree(Canvas):

	def __init__(self, master, icon, openicon, treename, action,
		bg='white', relief='sunken', bd=2,
		linecolor='#808080', textcolor='black',
		font=('MS Sans Serif', 8)):

		global tree_canvas, tree_canvas_scrollbar

		Canvas.__init__(self, master,
			bg=bg, relief=relief, bd=bd, highlightthickness=0, height=300,width=130)

		tree_canvas = self

		self.vscroll = Scrollbar(master, command=self.yview)

		tree_canvas_scrollbar = self.vscroll

		self.configure(yscrollcommand=self.vscroll.set)

		self.pack(side=LEFT,expand=YES,fill=BOTH)

		self.configure(scrollregion=('0','0','100','500'))

		self.vscroll.pack(side=LEFT,fill=BOTH)

		self.bg, self.font= bg, font
		self.linecolor, self.textcolor= linecolor, textcolor
		self.master       = master 
		self.plusnode   = PhotoImage(file=path+'plusnode.gif')
		self.minusnode   = PhotoImage(file=path+'minusnode.gif')
		self.inhibitDraw = 1
		self.product_id_Label  = None
		self.imageData   = None
		self.child         = []
		self.x = self.y  = -10
		self.child.append( Node( self, self, action=action,
			icon=icon, openicon=openicon, db_key=None, name=treename) )       

	def display(self):
		if self.inhibitDraw: return
		self.delete(ALL)
		for child in self.child:
			child.textForget()
			child.display()

	def deselectall(self):
		for child in self.child:
			child.deselect()

	def vline(self, x, y, y1):
		for i in range(0, abs(y-y1), 2):
			self.create_line(x, y+i, x, y+i+1, fill=self.linecolor,
				tags='line')

	def hline(self, y, x, x1):
		for i in range(0, abs(x-x1), 2):
			self.create_line(x+i, y, x+i+1, y, fill=self.linecolor,
				tags='line')

class CatalogBrowser(AppShell.AppShell):
	usecommandarea=1
	appversion = '0.5 Beta'
	appname = 'The Electronic Catalog: a2zsolutions.com'            
	copyright = 'Copyright (c) 2000 linuXden.com,\n All Rights Reserved.'
	contactname = 'linuXden.com, LLC'
	contactphone = None
	supportemail = 'support@linuXden.com'
	url='www.linuXden.com'
	frameWidth        = 541
	frameHeight      = 416

	def search_catalog(self):
		pass

	def checkout(self):
		if self.cart == {}:
			self.info_dialog.configure(message_text='You have no items in your shopping cart!')
			self.info_dialog.activate()
			return
		else:
			self.info_dialog.configure(message_text='Establishing connection with a2zsolutions.com.\n\nSubmitting order to a2zsolutions.\n\nThank You for ordering from a2zsolutions.com')
			self.info_dialog.activate()

	def add_to_cart(self):
		quantity = self.quantitytextvar.get()
		if self.productid.cget('text') != '' and quantity != '' and int(quantity) != 0:
			self.cart[self.productid.cget('text')] = int(quantity)

	def order_policies(self):
		self.policy_dialog.activate()

	def createButtons(self):
		#self.buttonAdd('Search',
		#                          helpMessage='Search Catalog',
		#                          statusMessage='Search Catalog',
		#                          command=self.search_catalog)

		self.buttonAdd('Add to Cart',
			helpMessage='Add displayed product to shopping cart',
			statusMessage='Add product item to cart',
			command=self.add_to_cart)

		self.buttonAdd('Check-out',
			helpMessage='Check-out',
			statusMessage='Check-out',
			command=self.checkout)

	def createMain(self):
		result = gadfly_utils.connect_db('tec', 
			"",
			create_if_does_not_exist=0, 
			create_cursor_also=1)
			
		if result['status'] != 'success':
			print 'DB Error: Can not connect to the TEC database backend'
			print result['message']
			sys.exit(1)

		self.db = result['result']

		self.panes = self.createcomponent('panes', (), None,
			Pmw.PanedWidget,
			(self.interior(),),
			orient='horizontal')

		self.panes.add('browserpane', min=155, size=155)
		self.panes.add('displaypane', min=.1)

		f = path+'folder.gif'
		of = path+'openfolder.gif'

		self.browserFrame = Frame(self.panes.pane('browserpane'),height=300)
		self.browserFrame.pack(side=LEFT,expand=YES,fill=BOTH)

		self.browser = self.createcomponent('browse', (), None,
			Tree,
			(self.browserFrame,),
			icon=f,
			openicon=of,
			treename='Catalog',
			action=None)

		self.browser.pack(side=LEFT,expand=YES,fill=BOTH)

		self.datasite = self.createcomponent('datasite', (), None,
			Frame,
			(self.panes.pane('displaypane'),),background='white')

		self.datasite.pack(side=TOP, expand=YES, fill=BOTH)

		f  = path+'folder.gif'
		of = path+'openfolder.gif'
		gf = path+'gif.gif'
		jf = path+'jpg.gif'
		xf = path+'other.gif'

		self.browser.inhibitDraw = 1

		top=self.browser.child[0]
		top.state='expanded'

		# retrieve from product table type types of products available
		# select DISTINCE
		result = self.getProductTypes()

		product_types = result['result']

		product_type_folders = {}

		for i in product_types:

			product_type_folders[i] = {'type' : i, 'node' : top.addChild(self.browser, icon=f, openicon=of, name=i, db_key=None, action=None)}

			# get all products of each type to put in folders
			result = self.getProductsOfType(i)

			products = result['result']

			for j in xrange(0,len(products)):
				product_type_folders[i]['node'].addChild(self.browser, icon=gf, name=products[j]['name'], db_key=products[j]['db_key'], action=self.display_product_info)

		self.browser.inhibitDraw = 0
		self.browser.display()

		self.panes.pack(side=TOP,
			expand=YES,
			fill=BOTH)

		self.create_policy_dialog()
		self.create_view_cart_dialog()
		self.create_info_dialog()
		self.create_customer_data_dialog()

	def create_policy_dialog(self):

		table_data = declarations.define_tables()

		result = gadfly_utils.execute_sql_statement(db=self.db,
			sqlStatement=gadfly_utils.build_select_all_table_columns_statement(table_data,'store_info','1'),
			commit_after=1,
			leave_cursor_open=1,
			create_cursor_also=0)

		if result['status'] != 'success':
			print 'DB Error: Could not retrieve store info'
			return result

		self.policy_dialog = Pmw.Dialog(self._hull, buttons=('Ok',), defaultbutton='Ok', title='Order Policies')

		self.policy_data = Pmw.ScrolledText(
			self.policy_dialog.interior(),
			borderframe=1,
			text_padx=10,
			text_pady=10,
			text_wrap='word')

		order_policies = string.replace(result['result'][0][15],'<CR>','\n')

		self.policy_data.settext(order_policies)
		self.policy_data._textbox.configure(state='disabled')
		self.policy_data.pack(expand=1,fill=BOTH)
		self.policy_dialog.withdraw()

	def create_customer_data_dialog(self):
		table_data = declarations.define_tables()

		result = gadfly_utils.execute_sql_statement(db=self.db,
			sqlStatement=gadfly_utils.build_select_all_table_columns_statement(table_data,'store_info','1'),
			commit_after=1,
			leave_cursor_open=1,
			create_cursor_also=0)

		if result['status'] != 'success':
			print 'DB Error: Could not retrieve store info'
			return result

		self.customer_data_dialog = Pmw.Dialog(self._hull, buttons=('Ok',), defaultbutton='Ok', title='Customer Data Entry')

		self.customer_data = Pmw.ScrolledFrame(
			self.customer_data_dialog.interior(),
			borderframe=1,
			usehullsize=1,
			hull_width = 400,
			hull_height = 220)

		self.customer_data.pack(expand=1,fill=BOTH)

		self.firstnametextvar = StringVar()
		self.initialtextvar = StringVar()
		self.lastnametextvar = StringVar()
		self.streetline1textvar = StringVar()
		self.streetline2textvar = StringVar()
		self.citytextvar = StringVar()
		self.statetextvar = StringVar()
		self.ziptextvar = StringVar()
		self.cardnotextvar = StringVar()
		self.expdatetextvar = StringVar()

		self.first_name = Pmw.EntryField(self.customer_data.interior(),
			labelpos = 'w',
			label_text = 'First Name:',
			value = '',
			validate = {'max' : 40},
			entry_textvariable=self.firstnametextvar)

		#self.first_name._entryFieldEntry.configure(width=40)

		self.initial = Pmw.EntryField(self.customer_data.interior(),
			labelpos = 'w',
			label_text = 'Middle Initial:',
			validate = {'max' : 1},
			entry_textvariable=self.initialtextvar)

		self.last_name = Pmw.EntryField(self.customer_data.interior(),
			labelpos = 'w',
			label_text = 'Last Name:',
			validate = {'max' : 40},
			entry_textvariable=self.lastnametextvar)

		self.street_line1 = Pmw.EntryField(self.customer_data.interior(),
			labelpos = 'w',
			label_text = 'Street Line 1:',
			validate = {'max' : 40},
			entry_textvariable=self.streetline1textvar)

		self.street_line2 = Pmw.EntryField(self.customer_data.interior(),
			labelpos = 'w',
			label_text = 'Street Line 2:',
			validate = {'max' : 40},
			entry_textvariable=self.streetline2textvar)

		self.city = Pmw.EntryField(self.customer_data.interior(),
			labelpos = 'w',
			label_text = 'City:',
			validate = {'max' : 40},
			entry_textvariable=self.citytextvar)

		self.state = Pmw.EntryField(self.customer_data.interior(),
			labelpos = 'w',
			label_text = 'State:',
			validate = {'max' : 2},
			entry_textvariable=self.statetextvar)

		self.zip = Pmw.EntryField(self.customer_data.interior(),
			labelpos = 'w',
			label_text = 'Zip Code:',
			validate = {'max' : 5},
			entry_textvariable=self.ziptextvar)


		result = gadfly_utils.execute_sql_statement(db=self.db,
			sqlStatement='SELECT payment_type FROM payment_methods',
			commit_after=1,
			leave_cursor_open=1,
			create_cursor_also=0)

		if result['status'] != 'success':
			print 'DB Error: Could not retrieve product categories'
			return result

		self.payment_methodvar = StringVar()
		self.payment_methodvar.set(result['result'][0][0])

		payment_options = []

		for i in xrange(0,len(result['result'])):
			payment_options.append(result['result'][i][0])

		self.payment_method = Pmw.OptionMenu(self.customer_data.interior(),
			labelpos = 'w',
			label_text = 'Payment method:',
			menubutton_textvariable = self.payment_methodvar,
			items = payment_options,
			menubutton_width = 15,
			)


		self.card_number = Pmw.EntryField(self.customer_data.interior(),
			labelpos = 'w',
			label_text = 'Credit Card Number:',
			validate = {'max' : 20},
			entry_textvariable=self.cardnotextvar)


		self.expdate = Pmw.EntryField(self.customer_data.interior(),
			labelpos = 'w',
			label_text = 'Expiration Date:',
			value = '1-1-2000',
			validate = {'validator' : 'date', 'separator' : '-',
			'min' : '1-1-2000',
			'minstrict' : 0, 'maxstrict' : 0,
			'format' : 'mdy'},
			entry_textvariable=self.expdatetextvar)
		# payment methods

		# shipping method

		entries = (self.first_name, self.initial, self.last_name,
			self.street_line1,self.street_line2,self.city,
			self.state,self.zip, self.payment_method,self.card_number,self.expdate)

		for entry in entries:
			entry.pack(fill='x', expand=1, padx=10, pady=5)

		Pmw.alignlabels(entries)

		self.customer_data_dialog.withdraw()

	def create_info_dialog(self):
		self.info_dialog = Pmw.MessageDialog(self._hull,
			title = 'Information Dialog',
			defaultbutton=0,
			iconpos = 'w',
			icon_bitmap = 'info',
			buttons=('Ok',))
		self.info_dialog.withdraw()

	def create_view_cart_dialog(self):

		self.view_cart_dialog = Pmw.Dialog(self._hull, buttons=('Ok',), defaultbutton='Ok', title='View Shopping Cart')
		self.view_cart_data = Pmw.ScrolledText(
			self.view_cart_dialog.interior(),
			borderframe=1,
			text_padx=10,
			text_pady=10,
			text_wrap='none')

		self.view_cart_data._textbox.configure(state='disabled')
		self.view_cart_data.pack(expand=1,fill=BOTH)
		self.view_cart_dialog.withdraw()

	def createProductDisplay(self):

		global default_font

		self.cart = {}
		table_data = declarations.define_tables()

		result = gadfly_utils.execute_sql_statement(db=self.db,
			sqlStatement=gadfly_utils.build_select_all_table_columns_statement(table_data,'store_info','1'),
			commit_after=1,
			leave_cursor_open=1,
			create_cursor_also=0)

		if result['status'] != 'success':
			print 'DB Error: Could not retrieve product categories'
			return result

		self.line1frame = self.createcomponent('line1frame', (), None,
			Frame,
			(self.datasite,),
			background='white')

		self.line1frame.pack(side=TOP,fill=Y,expand=YES)

		self.productidlabel = self.createcomponent('productidlabel', (), None,
			Label,
			(self.line1frame,),
			background='white',
			foreground='black',
			font=default_font)

		self.productidlabel.pack(side=LEFT,fill=BOTH,expand=YES)

		self.productid = self.createcomponent('productid', (), None,
			Label,
			(self.line1frame,),
			background='white',
			font=default_font,
			foreground='black')

		self.productid.pack(side=LEFT,fill=BOTH,expand=YES)

		self.browser.productimagedata = ImageTk.PhotoImage(Image.open('%s%s' % (imgs,'store_logo.gif')))

		self.productimagedata = self.browser.productimagedata

		self.productid['image'] = self.browser.productimagedata

		self.line2frame = self.createcomponent('line2frame', (), None,
			Frame,
			(self.datasite,),
			background='white')

		self.line2frame.pack(side=TOP,fill=Y,expand=YES)

		self.productdescription = self.createcomponent('productdescription', (), None,
			Label,
			(self.line2frame,),
			text='To Order by Phone Call: %s' % (result['result'][0][10]),
			font=default_font,
			background='white',
			foreground='black')

		self.productdescription.pack(side=TOP,expand=YES,fill=Y)

		self.line3frame = self.createcomponent('line3frame', (), None,
			Frame,
			(self.datasite,),
			background='white')

		self.line3frame.pack(side=TOP,fill=Y,expand=YES)

		self.productimage = self.createcomponent('productimage', (), None,
			Label,
			(self.line3frame,),
			text=result['result'][0][2],
			font=default_font,
			background='white',
			foreground='black')

		self.productimage.pack(expand=YES,fill=Y)

		self.line4frame = self.createcomponent('line4frame', (), None,
			Frame,
			(self.datasite,),
			background='white')

		self.line4frame.pack(side=TOP,fill=Y,expand=YES)

		self.productlongdescription = self.createcomponent('productlongdescription', (), None,
			Label,
			(self.line4frame,),
			font=default_font,
			background='white',
			foreground='black')



		self.line5frame = self.createcomponent('line5frame', (), None,
			Frame,
			(self.datasite,),
			background='white')

		self.line5frame.pack(side=TOP,fill=Y,expand=YES)

		self.shippingweightlabel = self.createcomponent('shippingweightlabel', (), None,
			Label,
			(self.line5frame,),
			font=default_font,
			background='white',
			foreground='black')

		#self.shippingweightlabel.pack(side=LEFT,expand=YES,fill=Y)

		self.shippingweight = self.createcomponent('shippingweight', (), None,
			Label,
			(self.line5frame,),
			text='%s' % (result['result'][0][14]),
			font=default_font,
			background='white')

		#self.shippingweight.pack(side=LEFT,expand=YES,fill=Y)

		self.line6frame = self.createcomponent('line6frame', (), None,
			Frame,
			(self.datasite,),
			background='white')

		self.line6frame.pack(side=TOP,fill=Y,expand=YES)

		self.productpricelabel = self.createcomponent('productpricelabel', (), None,
			Label,
			(self.line6frame,),
			font=default_font,
			background='white',
			foreground='black')

		self.productpricelabel.pack(side=LEFT,expand=YES,fill=Y)

		self.productprice = self.createcomponent('productprice', (), None,
			Label,
			(self.line6frame,),
			text='%s' % (result['result'][0][14]),
			wraplength=350,
			font=default_font,
			background='white')

		self.productprice.pack(side=LEFT,expand=YES,fill=Y)

		self.line7frame = self.createcomponent('line7frame', (), None,
			Frame,
			(self.datasite,),
			background='white')

		self.line7frame.pack(side=TOP,fill=Y,expand=YES)

		self.quantitylabel = self.createcomponent('quantitylabel', (), None,
			Label,
			(self.line7frame,),
			text='Quantity:',
			font=default_font,
			background='white',
			foreground='black')

		#self.quantitylabel.pack(side=LEFT,fill=Y,expand=YES)

		self.quantitytextvar = StringVar()

		self.quantitytextvar.set('0')

		self.quantitytext = self.createcomponent('quantitytext', (), None,
			Pmw.EntryField,
			(self.line7frame,),
			value='0',
			validate= {"validator" : "numeric", "min" : 0, "max" : 999},
			entry_textvariable=self.quantitytextvar)
		self.quantitytext._entryFieldEntry.configure(width=3)

		self.line8frame = self.createcomponent('line8frame', (), None,
			Frame,
			(self.datasite,),
			background='white')

		self.line8frame.pack(side=TOP,fill=Y,expand=YES)

		self.copyrightimage = self.createcomponent('copyrightimage', (), None,
			Label,
			(self.line8frame,),
			background='white')


		self.browser.copyrightimagedata = ImageTk.PhotoImage(Image.open('%s%s' % (imgs,'linuxdenlogo.jpg')))

		self.copyrightimage['image'] = self.browser.copyrightimagedata

		self.copyrightimage.pack(side=RIGHT,padx=5)

		self.browser.quantitytext = self.quantitytext

		self.copyrightlabel = self.createcomponent('copyrightlabel', (), None,
			Label,
			(self.line8frame,),text='Copyright (c) 2000\nwww.linuXden.com\nAll Rights Reserved.',font=copyright_font,background='white',foreground='blue')

		self.copyrightlabel.pack(side=RIGHT)

		self.browser.copyrightlabel = self.copyrightlabel
		self.browser.copyrightimage = self.copyrightimage
		self.browser.productid = self.productid
		self.browser.productimage = self.productimage
		self.browser.productdescription = self.productdescription
		self.browser.productprice = self.productprice
		self.browser.quantitylabel = self.quantitylabel


	def print_product(self):
		pass

	def view_cart(self,display_customer_data=0):

		if self.cart == {}:
			self.info_dialog.configure(message_text='You have no items in your shopping cart!')
			self.info_dialog.activate()
			return

		else:

			table_data = declarations.define_tables()

			if display_customer_data:
				product_data_lines = 'First Name: ' + self.firstnametextvar.get() + '\n'
				product_data_lines = product_data_lines + 'Middle Initial: ' + self.initialtextvar.get() + '\n'
				product_data_lines = product_data_lines + 'Last Name: ' + self.initialtextvar.get() + '\n'
				product_data_lines = product_data_lines + 'Street Line 1: ' + self.streetline1textvar.get() + '\n'
				product_data_lines = product_data_lines + 'Street Line 2: ' + self.streetline2textvar.get() + '\n'
				product_data_lines = product_data_lines + 'City: ' + self.citytextvar.get() + '\n'
				product_data_lines = product_data_lines + 'State: ' + self.statetextvar.get() + '\n'
				product_data_lines = product_data_lines + 'Zip: ' + self.ziptextvar.get() + '\n'

				product_data_lines = product_data_lines + 'Card Number: ' + self.cardnotextvar.get() + '\n'
				product_data_lines = product_data_lines + 'Expiration Date: ' + self.expdatetextvar.get() + '\n'
				product_data_lines = product_data_lines + 'Payment Method: ' + self.payment_methodvar.get() + '\n\nItems Ordered:\n\n'

			else:
				product_data_lines = ''

			product_data_lines = product_data_lines + string.center('Id',10) + '  ' + string.center('Name',40) + '  ' +  string.center('Weight',6) + '  ' + string.center('Qty',3) + '  ' + string.center('Price',11) + '  ' + string.center('Total',11) + '\n'

			line_total = 0.0

			for product_id in self.cart.keys():
				result = gadfly_utils.execute_sql_statement(db=self.db,
					sqlStatement=gadfly_utils.build_select_all_table_columns_statement(table_data,'products',product_id),
					commit_after=1,
					leave_cursor_open=1,
					create_cursor_also=0)

				if result['status'] != 'success':
					print 'DB Error: Could not retrieve product info'
					return result

				product_data_lines = product_data_lines + '\n' + \
					string.center(result['result'][0][0],10) + '  ' + \
					string.center(result['result'][0][5],40) + '  ' + \
					string.center('%s lbs.' % (result['result'][0][8]),6) + '  ' + \
					string.center(`self.cart[product_id]`,3) + '  ' + \
					string.center('$%9.2f' % (result['result'][0][7]),11) + '  ' + \
					string.center('$%9.2f' % (self.cart[product_id] * float(result['result'][0][7])),11) + '\n'
				line_total = line_total + (self.cart[product_id] * float(result['result'][0][7]))

			product_data_lines = product_data_lines + '\n\nOrder Total: $'
			product_data_lines = product_data_lines + ('%9.2f' % (line_total))

		self.view_cart_data.settext(product_data_lines)
		self.view_cart_dialog.activate()

	def empty_cart(self):
		del self.cart
		self.cart = {}

	def view_order(self):
		self.view_cart(display_customer_data=1)

	def submit_order(self):
		pass

	def save(self):
		pass

	def customer_data(self):
		self.customer_data_dialog.activate()

	def createInterface(self):
		global catalog

		AppShell.AppShell.createInterface(self)

		#self.menuBar.addmenu('Product', 'Product Functions')

		#self.menuBar.addmenuitem('Product', 'command', 'Search by keywords for a product in the catalog',
		#                                                label='Search',
		#                                                command=self.search_catalog)

		#self.menuBar.addmenuitem('Product', 'command', 'Print Product Information',
			#                                        label='Print',
			#                                command=self.print_product)

		self.menuBar.addmenu('Shopping Cart', 'Shopping Cart Functions')


		self.menuBar.addmenuitem('Shopping Cart', 'command', 'View Items in your Shopping Cart',
			label='View',
			command=self.view_cart)

		self.menuBar.addmenuitem('Shopping Cart', 'command', 'Empty your Shopping Cart',
			label='Empty',
			command=self.empty_cart)

		self.menuBar.addmenu('Order', 'Order Functions')

		self.menuBar.addmenuitem('Order', 'command', 'Customer Info required to place an order',
			label='Customer Data Entry',
			command=self.customer_data)

		self.menuBar.addmenuitem('Order', 'command', 'Check-out and Place Order',
			label='Checkout',
			command=self.checkout)

		self.menuBar.addmenuitem('Order', 'command', 'Ordering Policies',
			label='Policies',
			command=self.order_policies)

		self.menuBar.addmenuitem('Order', 'command', 'View Order before Checking Out',
			label='View',
			command=self.view_order)

		#self.menuBar.addmenuitem('File', 'command', 'Save Customer and Order Data for future use',
		#                                                label='Save',
		#                                                command=self.save)

		self.menuBar.addmenuitem('File', 'command', 'Exit the Electronic Catalog',
			label='Exit',
			command=self.quit)
		self.createButtons()
		self.createMain()

		catalog = self

		self.createProductDisplay()

	def display_product_info(self, name, db_key):

		table_data = declarations.define_tables()

		result = gadfly_utils.execute_sql_statement(db=self.db,
			sqlStatement=gadfly_utils.build_select_all_table_columns_statement(table_data,'products',db_key),
			commit_after=1,
			leave_cursor_open=1,
			create_cursor_also=0)
		if result['status'] != 'success':
			print 'DB Error: Could not retrieve product info'
			return result

		self.productidlabel.configure(text='Product Id:')
		self.productid.configure(image='',text=result['result'][0][0],font=default_font)
		self.productid.pack(side=LEFT)
		self.productdescription.configure(text=result['result'][0][5],font=default_font)
		if self.productimagedata:
			del self.productimagedata
		self.productimagedata = ImageTk.PhotoImage(Image.open('%s%s' % (imgs,result['result'][0][9])))
		self.productimage['image'] = self.productimagedata
		self.productlongdescription.configure(text=result['result'][0][6],
			font=default_font,
			wraplength=300)
		self.productlongdescription.pack(side=TOP)
		self.shippingweightlabel.configure(text='Shipping Weight:',font=default_font)
		self.shippingweightlabel.pack(side=LEFT,expand=NO)
		self.shippingweight.configure(text='%s lbs' % (result['result'][0][8]),font=default_font)
		self.shippingweight.pack(side=LEFT,expand=NO)
		self.productpricelabel.configure(text='Price:',font=default_font)
		self.productprice.configure(text="$ %9.2f" % (result['result'][0][7]),font=default_font)
		self.quantitylabel.pack(side=LEFT,expand=NO)

		# initialize quantity to 0
		self.quantitytextvar.set('0')

		self.quantitytext.pack(side=LEFT,expand=NO)

	def getProductTypes(self):
		result = gadfly_utils.execute_sql_statement(db=self.db,
			sqlStatement='SELECT DISTINCT category FROM products',
			commit_after=1,
			leave_cursor_open=1,
			create_cursor_also=0)

		if result['status'] != 'success':
			print 'DB Error: Could not retrieve product categories'
			return result

		product_types = []

		for i in xrange(0,len(result['result'])):
			product_types.append(result['result'][i][0])

		return {'status' : 'success', 'message' : "", 'result' : product_types}

	def getProductsOfType(self, product_type):

		result = gadfly_utils.execute_sql_statement(db=self.db,
			sqlStatement="SELECT id, description FROM products WHERE category = '%s'" % (product_type),
			commit_after=1,
			leave_cursor_open=1,
			create_cursor_also=0)

		if result['status'] != 'success':
			print 'DB Error: Could not retrieve products of type: %s' % (product_type)
			return result

		products = []

		for i in xrange(0,len(result['result'])):
			products.append({'db_key' : result['result'][i][0], 'name' : result['result'][i][1]})

		return {'status' : 'success', 'message' : "Retrieved products for types specified", 'result' : products}

	def showMe(self, dofile):
		if self.browser.imageData: del self.browser.imageData
		self.browser.imageData = ImageTk.PhotoImage(\
			Image.open('%s%s' % \
			(imgs, dofile)))
		self.browser.imageLabel['image'] = self.browser.imageData

catalogBrowser = CatalogBrowser()
catalogBrowser.run()