@echo off
set PYROOT=c:\py152
PATH %PYROOT%;%PATH%
set PYTHONPATH=.;%PYROOT%;%PYROOT%\lib;%PYROOT%\lib\plat-win;%PYROOT%\lib\lib-tk;%PYROOT%\PIL;%PYROOT%ext\pyds;%PYROOT%ext\lib;
set TCL_LIBRARY=%PYROOT%\tcl8.2.3\library
set TK_LIBRARY=%PYROOT%\tk8.2.3\library
python main.py
