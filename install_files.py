#!/usr/bin/env python
# $Id$
# Copyright (C) 1999 LinuXden, All Rights Reserved
# Copright Statement at http://www.linuxden.com/copyrighted_apps.html
# 
import install
import os

if __name__ == '__main__':
	install_engine = install.install('tec',
		'tec',
		os.path.join(os.sep,'home','tec','db'))
	install_engine.install_to_destination()
