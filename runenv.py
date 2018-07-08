class myRunenv:
	mode="external"
	command="python -u -"
	inheritenv=1
	env={"PATH" : "C:\\py152\\", 
	"PYTHONPATH" : ".;C:\\py152;C:\\py152\\lib;C:\\py152\\PIL;C:\\py152\\PST;C:\\py152\\lib\\plat-win;C:\\py152\\lib\\lib-tk;C:\\py152\\ext\\pyds;C:\\py152ext\\lib;", 
	"TCL_LIBRARY" : "C:\\py152\\tcl8.2.3\\library",
	"TK_LIBRARY" : "C:\\py152\\tk8.2.3\\library"}

register("runenv","my env",myRunenv)
