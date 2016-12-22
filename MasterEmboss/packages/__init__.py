import subprocess
import os
import sys

class run_app:
	def __init__():
		path = "C:\\Program Files\\MasterEmboss\\packages"
		os.chdir( path )
		# subprocess.call("python MasterEmboss.py")
		pro = subprocess.Popen([sys.executable,"MasterEmboss.py"])
		pro.communicate()