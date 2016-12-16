import os, re
import shutil
import subprocess
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
import time, ctypes, re, os
from CreateEmbossIni import EmbossInit
from EmailScript import AutomateEmail

class bossinit(tk.Tk):
	def __init__(self,*args,**kwargs):
		tk.Tk.__init__(self,*args,**kwargs)

		tk.Tk.iconbitmap(self,default="hieta_icon.ico")

		self.container = tk.Frame(self)
		self.container.pack(side="top",fill="both",expand=True)
		self.container.grid_rowconfigure(0,weight=1)
		self.container.grid_columnconfigure(0,weight=1)
		self.frames = {}

		frame = IntroPage(self.container,self)
		self.frames[IntroPage] = frame
		frame.grid(row=0,column=0,sticky="nsew")
		self.show_frame(IntroPage)

	def activate(self):
		self.frames = {}
		for F in (IntroPage,RenamePage,ProcessPage):
			if(F == ProcessPage):
				frame = F(self.container,self)
			else:
				frame = F(self.container,self)
			self.frames[F] = frame
			frame.grid(row=0,column=0,sticky="nsew")

	def show_frame(self,cont):	
		if cont == RenamePage:
			size = "823x" + str(135 + (50 * globalNum))
			app.geometry(size)				
		elif cont == ProcessPage:
			app.geometry("615x395")
			
		frame = self.frames[cont]
		frame.tkraise()

	def get_page(self, page_class):
		return self.frames[page_class]


def regex(data,pattern):
	for d in data:
		print(d)
		print(pattern)
		if pattern.match(d) == False:
			print("False")
			return False
		elif (d.strip(" ") == ""):
			print("False")
			return False
	return True
	
def get_version_info():
	filename1 = "patch_notes.txt"
	filename2 = "versions.txt"
	notes_list = []
	versions = []	
	
	file = open(filename1,'r')
	line = file.readline()
	while line is not "":
		notes_list.append(line)
		line = file.readline()
	
	file = open(filename2,'r')
	line = file.readline()
	while line is not "":
		versions.append(line)
		line = file.readline()
	
	info = []
	info.append(versions)
	info.append(notes_list)
	
	return info
	
def menuevent(n):
	if n == 1:
		helpDialog = HelpDialog(app)
		app.wait_window(helpDialog.top)
	elif n == 2:
		aboutDialog = AboutDialog(app)
		app.wait_window(aboutDialog.top)
	elif n == 3:
		version_info = []
		version_info = get_version_info()
		
		v = version_info[0]
		a = version_info[1]
		
		versionDialog = VersionDialog(app)
		app.wait_window(versionDialog.top)

class IntroPage(ttk.Frame):
	def __init__(self, parent,controller):
		ttk.Frame.__init__(self,parent)
		self.controller = controller

		self.v = tk.BooleanVar()
		self.dirNum = ttk.Entry(self,width=5)
		self.l = tk.Label(self,text="How Many Directories:")

		t = tk.Label(self,text="Welcome To MasterEmboss")
		t.grid(row=0,column=0,columnspan=5,padx=10,pady=5)
		l = tk.Label(self,text="This App has 3 stages. 1) Renaming Photos, if you have several directories of photos to rename click the 'Multiple Dirs?'\nat the bottom and declare how many you have. 2) Processing the renamed photos, this includes cropping and embossing.\n3) Creating Timelapses from EOL and PRC pictures. ")
		l.grid(row=1,column=0,columnspan=5,padx=5,pady=15)
		self.multipleDir = ttk.Checkbutton(self,text="Multiple Dirs?",variable=self.v,command=self.expandFrame)
		self.multipleDir.grid(row=2,column=1,columnspan=3)

		self.exitRow = 4
		self.goRow = 4

		exit = ttk.Button(self,text="Exit")
		exit.grid(row=self.exitRow,column=0,columnspan=2,padx=5,pady=20)
		go = ttk.Button(self,text="Go",command=self.validate)
		go.grid(row=self.goRow,column=3,columnspan=2,padx=5,pady=20)

	def expandFrame(self):
		self.exitRow += 1
		self.goRow += 1
		if(self.exitRow == 5)&(self.goRow == 5):
			#self.l = tk.Label(self,text="How Many Directories:")
			#self.dirNum = ttk.Entry(self,width=5)
			self.l.grid(row=3,column=1,columnspan=2,padx=5,pady=10)		
			self.dirNum.grid(row=3,column=3,padx=5,pady=10)
		elif(self.exitRow >= 6)&(self.goRow >= 6):
			self.exitRow = self.exitRow - 2
			self.goRow = self.goRow - 2
			self.l.grid_forget()
			self.dirNum.grid_forget()

	def validate(self):
		self.controller.activate()
		if(self.v.get() == True):
			pattern = re.compile("[0-9]+")
			try:
				if(pattern.match(self.dirNum.get())):	
					global globalNum	
					rename = self.controller.get_page(RenamePage)
					rename.add_widgets(int(self.dirNum.get()))
					globalNum = int(self.dirNum.get())
					self.controller.show_frame(RenamePage)
				else:
					print("Please Fill the Box")
			except ValueError:
				print("You have caused a ValueError")
		elif(self.v.get() == False):
			self.controller.show_frame(RenamePage)

class RenamePage(tk.Frame):
	def __init__(self, parent, controller):
		tk.Frame.__init__(self,parent)
		self.controller = controller

		self.v1 = tk.StringVar()
		v2 = tk.StringVar()
		
		self.wdDirLbl = []
		self.wdDirEnt = []
		self.wdDirBut = []
		self.sNumL = []
		self.sNumE = []
		self.eNumL = []
		self.eNumE = []

		self.rowOn = 2

		title1 = ttk.Label(self,text="Re-naming Parameters:")
		title1.grid(row=0,column=0,padx=10,pady=10)

		count = 1
		for i in range(0,11):
			self.dirLabel = ttk.Label(self,text="Working Directory %s:"%count)
			self.wdDirLbl.append(self.dirLabel)
			self.wdDirRe = ttk.Entry(self,width=40)
			self.wdDirEnt.append(self.wdDirRe)
			self.wdDirRe.config(state='readonly')
			self.findDirBut = ttk.Button(self,text="...",command=lambda r=count: self.findWdDirectory(r))
			self.wdDirBut.append(self.findDirBut)

			count += 1

		self.outLbl = ttk.Label(self,text="Output Directory:")
		self.outDir = ttk.Entry(self,width=40,textvariable=v2)
		self.outDir.config(state='readonly')
		self.outBut = ttk.Button(self,text="...",command=self.findOutDirectory)
		
		for i in range(0,11):
			startNumLbl = ttk.Label(self,text="Start Number:")
			self.sNumL.append(startNumLbl)
			self.startNumEnt = ttk.Entry(self,width=5)
			self.sNumE.append(self.startNumEnt)
			label = ttk.Label(self,text="End Number:")
			self.eNumL.append(label)
			self.endNumEnt = ttk.Entry(self,width=5)
			self.eNumE.append(self.endNumEnt)
		
		self.wLbl = ttk.Label(self,text="Write Start:")
		self.writeNumEnt = ttk.Entry(self,width=5)
		self.preLbl = ttk.Label(self,text="Preffix:")
		self.preffix = ttk.Entry(self,width=5)
		self.sufLbl = ttk.Label(self,text="Suffix:")
		self.suffix = ttk.Entry(self,width=5)

		x = 100
		#self.p = tk.DoubleVar()
		#self.p = 0
		var = False
		self.progressBar = ttk.Progressbar(self,orient="horizontal",length=300,mode="determinate",maximum=x)
		self.button = ttk.Button(self,text="Run",width=20,command=self.run)

	def findWdDirectory(self,num):
		directory = tk.filedialog.askdirectory()
		self.wdDirEnt[num - 1].config(state='normal')
		self.wdDirEnt[num - 1].insert("end",directory)
		self.wdDirEnt[num - 1].config(state='readonly')

	def findOutDirectory(self):
		directory = tk.filedialog.askdirectory()
		self.outDir.config(state='normal')
		self.outDir.insert("end",directory)
		self.outDir.config(state='readonly')

	def add_widgets(self,amount):
		self.rowOn = 1
		for i in range(0,amount):
			self.wdDirLbl[i].grid(row=self.rowOn,column=0,padx=10,pady=10)
			self.wdDirEnt[i].grid(row=self.rowOn,column=1,columnspan=2,padx=10,pady=10)
			self.wdDirBut[i].grid(row=self.rowOn,column=3,padx=10,pady=10)
			self.sNumL[i].grid(row=self.rowOn,column=4,padx=10,pady=10)
			self.sNumE[i].grid(row=self.rowOn,column=5,padx=10,pady=10)
			self.eNumL[i].grid(row=self.rowOn,column=6,padx=10,pady=10)
			self.eNumE[i].grid(row=self.rowOn,column=7,padx=10,pady=10)
			self.rowOn += 1		
		self.preLbl.grid(row=self.rowOn,column=4,padx=10,pady=10)
		self.preffix.grid(row=self.rowOn,column=5,padx=10,pady=10)
		self.sufLbl.grid(row=self.rowOn,column=6,padx=10,pady=10)
		self.suffix.grid(row=self.rowOn,column=7,padx=10,pady=10)
		self.outLbl.grid(row=(self.rowOn),column=0,padx=10,pady=10)
		self.outDir.grid(row=(self.rowOn),column=1,padx=10,pady=10,columnspan=2)
		self.outBut.grid(row=(self.rowOn),column=3,padx=10,pady=10)
		self.progressBar.grid(row=self.rowOn+2,column=0,padx=10,pady=10,columnspan=3)
		self.wLbl.grid(row=self.rowOn+2,column=3,padx=10,pady=10)
		self.writeNumEnt.grid(row=self.rowOn+2,column=4,padx=10,pady=10)
		self.button.grid(row=self.rowOn+2,column=5,padx=10,pady=10,columnspan=2)

	def run(self):
		print("- - - RUN - - -")		

		print(self.validate)
		carry = 0
		if(self.validate() == True):
			for i in range(0,globalNum):
				print("- - - - - - - - - - - - - - - - - - - - - - - -")
				sNum = int(self.sNumE[i].get())
				print("start number: %s"%sNum)
				eNum = int(self.eNumE[i].get())
				print("end Numer: %s"%eNum)
				if i == 0:
					wNum = int(self.writeNumEnt.get())
					print("write number: %s"%wNum)
				elif i > 0:
					wNum += carry
					print("write number: %s"%wNum)
				preffix = self.preffix.get()
				suffix = "."+self.suffix.get()
				wd = self.wdDirEnt[i].get() + "/"#working directory, picture store path
				print("Working Directory: %s"%wd)
				nd = self.outDir.get() + "/"#new directory to which renamed photos will be saved
				print("Out Directory: %s"%nd)
				NamePreffix = preffix
				NameSuffix = suffix

				StartPhotoNo = sNum
				EndPhotoNo = eNum

				Photo_count = EndPhotoNo - StartPhotoNo
				k = 0
				progress_track = 10  # number of photos, after which, progress report is shown

				m = 0  #Process track of the photo number that is being processed.
				pb = 0
				self.progressBar["maximum"] = Photo_count
				
				for i in range(StartPhotoNo, EndPhotoNo+1, 1):
					iPhoto = NamePreffix + '%04d' %i + NameSuffix
					print("Photo: %s"%iPhoto)
					NewiPhoto = NamePreffix + '%05d' %(wNum) + NameSuffix
					print("NewiPhoto: %s"%NewiPhoto)
					wNum+=1
					print("Copy: %s to new Dir: %s"%(os.path.expanduser(wd+iPhoto),os.path.expanduser(nd+NewiPhoto)))
					shutil.copy2(os.path.expanduser(wd+iPhoto), os.path.expanduser(nd+NewiPhoto))
					k +=1
					m +=1
					pb+=1
					self.progressBar["value"] = (pb)
					self.progressBar.update()
					#self.p.set(self.p + 1)
					if k == progress_track:
						#print ("Processing photo %d of %d..." % (m, Photo_count))
						k=0
				carry = wNum
				print("Carry: %s"%wNum)
				
				self.controller.show_frame(ProcessPage)
		else:
			print("Validated - Not Acceptable")
			tk.messagebox.showinfo("Validation Error","You have failed to enter valid data into all the fields please ammend and try again.")
		#self.controller.show_frame(ProcessPage)

	def validate(self):
		print("- - - VALIDATING - - -")

		# sNum = self.startNumEnt.get()
		# eNum = self.endNumEnt.get()
		# wNum = self.writeNumEnt.get()
		preffix = self.preffix.get()
		suffix = self.suffix.get()
		wd = self.wdDirRe.get()
		od = self.outDir.get()
		validated = False

		data=[]
		urls=[]
		for i in range(0,globalNum):
			data.append(self.sNumE[i].get())
			data.append(self.eNumE[i].get())
			urls.append(self.wdDirEnt[i].get())
		data.append(self.writeNumEnt.get())
		urls.append(self.outDir.get())
		print(data)
			
		name=[preffix,suffix]
		
		#urls=[wd,od]
		print("URLS: %s"%urls)
		pattern = re.compile("[0-9]+")

		if regex(data,pattern) == False:
			return False

		pattern = re.compile("[a-z|0-9]*(_)*")
		if pattern.match(name[0]) == False:
			return False

		pattern = re.compile("(.)[a-z]+")
		if pattern.match(name[1]) == False:
			return False

		urlPattern = re.compile("(C:/)^(.*/)([^/]*)$")
		if regex(urls,urlPattern) == False:
			return False

		return True

class ProcessPage(tk.Frame):
	def __init__(self,parent,controller):
		tk.Frame.__init__(self,parent)
		self.controller = controller

		self.cropV = tk.IntVar()
		self.eolV = tk.IntVar()
		self.prcV = tk.IntVar()
		self.feolV = tk.IntVar()
		self.oddV = tk.IntVar()

		title = ttk.Label(self,text="Processing Parameters:")
		title.grid(row=0,column=0,padx=0,pady=10)
		l = tk.Label(self,text="Build Number:")
		l.grid(row=0,column=2,padx=0,pady=10)
		self.buildNum = ttk.Entry(self,width=10)
		self.buildNum.grid(row=0,column=3,padx=0,pady=10)
		breaker = tk.Label(self,text="- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -")
		breaker.grid(row=1,column=0,columnspan=4,padx=0,pady=5)
		
		label = tk.Label(self,text="IfranView Directory:")
		label.grid(row=2,column=0,padx=0,pady=5)
		self.ivEnt = ttk.Entry(self,width=30)
		self.ivEnt.insert("end","C:\\Program Files\\IrfanView\\i_view64.exe")
		self.ivEnt.config(state="readonly")
		self.ivEnt.grid(row=2,column=1,padx=0,pady=5,columnspan=2)
		self.ivBut = ttk.Button(self,text="Change",command=self.change)
		self.ivBut.grid(row=2,column=3,padx=0,pady=5)
		breaker3 = tk.Label(self,text="- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -")
		breaker3.grid(row=3,column=0,columnspan=4)

		#label = tk.Label(self,text="StartNum:") #Remove all of these values and grab them
		#label.grid(row=4,column=0,padx=0,pady=5) #From the second window. saves input and time
		#self.snEnt = ttk.Entry(self,width=5)
		#self.snEnt.grid(row=4,column=1,padx=0,pady=5)
		#label = tk.Label(self,text="EndNum:")
		#label.grid(row=4,column=2,padx=0,pady=5)
		#self.enEnt = ttk.Entry(self,width=5)
		#self.enEnt.grid(row=4,column=3,padx=0,pady=5)
		#label = tk.Label(self,text="Start Layer:")
		#label.grid(row=5,column=0,padx=0,pady=5)
		#self.slEnt = ttk.Entry(self,width=5)
		#self.slEnt.grid(row=5,column=1,padx=0,pady=5)
		#breaker2 = tk.Label(self,text="- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -")
		#breaker2.grid(row=6,column=0,columnspan=4)

		l = tk.Label(self,text="Crop X:")
		l.grid(row=4,column=0,padx=0,pady=5)
		self.xEnt = ttk.Entry(self,width=5)
		self.xEnt.grid(row=4,column=1,padx=0,pady=5)
		l = tk.Label(self,text="Crop Y:")
		l.grid(row=4,column=2,padx=0,pady=5)
		self.yEnt = ttk.Entry(self,width=5)
		self.yEnt.grid(row=4,column=3,padx=0,pady=5)
		l = tk.Label(self,text="Crop Width:")
		l.grid(row=5,column=0,padx=0,pady=5)
		self.wEnt = ttk.Entry(self,width=5)
		self.wEnt.grid(row=5,column=1,padx=0,pady=5)
		l = tk.Label(self,text="Crop Height:")
		l.grid(row=5,column=2,padx=0,pady=5)
		self.hEnt = ttk.Entry(self,width=5)
		self.hEnt.grid(row=5,column=3,padx=0,pady=5)
		brk = tk.Label(self,text="- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -")
		brk.grid(row=6,column=0,pady=5,columnspan=4)

		self.crop = ttk.Checkbutton(self,text="Crop",variable=self.cropV)
		self.crop.grid(row=7,column=0,padx=0,pady=5)
		self.EOLEmb = ttk.Checkbutton(self,text="EOL Emboss",variable=self.eolV)
		self.EOLEmb.grid(row=7,column=1,padx=0,pady=5,columnspan=2)
		self.prcEmb = ttk.Checkbutton(self,text="PRC Emboss",variable=self.prcV)
		self.prcEmb.grid(row=7,column=3,padx=0,pady=5)
		brk = tk.Label(self,text="- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -")
		brk.grid(row=8,column=0,columnspan=4,padx=0,pady=5)

		self.firstIsEOL = ttk.Checkbutton(self,text="First Photo Is EOL",variable=self.feolV)
		self.firstIsEOL.grid(row=9,column=0,columnspan=2,padx=0,pady=5)
		self.EOLisODD = ttk.Checkbutton(self,text="EOL Is Odd",variable=self.oddV)
		self.EOLisODD.grid(row=9,column=2,columnspan=2,padx=0,pady=5)
		brk = tk.Label(self,text="- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -")
		brk.grid(row=10,column=0,padx=0,pady=5,columnspan=4)

		self.progress = ttk.Progressbar(self,orient="horizontal",length=200,mode="determinate")
		self.progress.grid(row=14,column=0,padx=0,pady=5,columnspan=2)
		run = ttk.Button(self,text="Run",width=30,command=self.run)
		run.grid(row=14,column=2,padx=0,pady=5,columnspan=2)

	def change(self):
		directory = tk.filedialog.askdirectory()
		self.ivEnt.config(state='normal')
		self.ivEnt.config(text=directory)
		self.ivEnt.config(state='readonly')

	def run(self):
		page1 = self.controller.get_page(RenamePage)
		self.pb = tk.IntVar()
		self.pb = 0

		wd = page1.outDir.get()
		print(wd)

		IrfanView = "C:\\Program Files\\IrfanView\\i_view64.exe"

		NamePreffix = page1.preffix.get()
		NameSuffix = page1.suffix.get()

		namepage = self.controller.get_page(RenamePage)
				
		endVal = 0
		for i in range(0,len(namepage.eNumE)):
			testString = namepage.eNumE[i].get().strip(" ")
			print("Testing string: %s"%testString)
			if (testString == ""):
				endVal = i - 1
				break
		print(namepage.sNumE[0].get())
		StartPhotoNo = int(namepage.sNumE[0].get())
		EndPhotoNo = int(namepage.eNumE[endVal].get())
		StartLayer = int(namepage.writeNumEnt.get())
		#StartPhotoNo = int(self.snEnt.get())
		#EndPhotoNo = int(self.enEnt.get())
		#StartLayer = int(self.slEnt.get())
		LayerCount = int((EndPhotoNo - StartPhotoNo)*0.5)
		LastLayerNo = StartLayer + LayerCount
		
		self.progress["maximum"] = (LayerCount * 4) + 20 

		FirstPhotoIsEOL = self.eolV.get()
		EOLisODD = self.oddV.get() #Make this value True if EOL photos are odd numbered, and False if they're even numbered.

		self.Build_No = self.buildNum.get()
		
		CropX = int(self.xEnt.get())  #Left-hand edge of start of crop
		CropY = int(self.yEnt.get())  #Top edge of start of crop
		CropW = int(self.wEnt.get())  #Resulting image width
		CropH = int(self.hEnt.get())  #Resulting image height

		wd = wd.replace("/","\\")

		self.EOLDir = wd + "\\EOL"
		self.PRCDir = wd + "\\PRC"

		if os.path.exists(self.EOLDir)==0:
			os.mkdir(self.EOLDir)

		if os.path.exists(self.PRCDir) ==0:
			os.mkdir(self.PRCDir)
			
		i = StartLayer  #Layer number initialised as the initial layer number

		if FirstPhotoIsEOL == 0:
			j = 1  #EOL or PRC identifier
		else:
			j = 0

		k = 0    #Identifier for if both EOL and PRC photos have been processed
		l = 1  #Counter to print progress to screen

		ProgressTrack = 10  #The interval at which progress is printed to screen

		if (self.cropV.get()):
			print("Cropping photos...")
			for PhotoNo in range(StartPhotoNo, EndPhotoNo):
				PhotoName = NamePreffix + '%05d' %PhotoNo + NameSuffix
				PhotoPath = wd + '\\' + PhotoName
				if j ==0:  #EOL photo        
					OutputPhotoName = self.Build_No + '_EOL_' + '%05d' %i + '.JPG'
					subprocess.call(IrfanView+' '+PhotoPath+' /crop=(' +str(CropX)+ ',' +str(CropY)+ ',' +str(CropW)+ ',' +str(CropH)+ ',0) /convert='+self.EOLDir+'\\'+OutputPhotoName)
					j+=1
					k +=1
					if k == 2:
						i +=1
						k = 0
						l += 1
				elif j ==1:  #PRC photo        
					OutputPhotoName = self.Build_No + '_PRC_' + '%05d'%i + '.JPG'
					subprocess.call(IrfanView+' '+PhotoPath+' /crop=(' +str(CropX)+ ',' +str(CropY)+ ',' +str(CropW)+ ',' +str(CropH)+ ',0) /convert='+self.PRCDir+'\\'+OutputPhotoName)
					j-=1
					k +=1
					if k == 2:
						i += 1
						k = 0
						l += 1
				if l == ProgressTrack:
					print ("Cropping layer %d of %d..." %(i,LastLayerNo))
					l = 0
					
				self.pb += 1
				self.progress["value"] = self.pb
				self.progress.update()

		self.EOLEmbossDir = self.EOLDir + '\\Embossed'
		self.PRCEmbossDir = self.PRCDir + '\\Embossed'

		if os.path.exists(self.EOLEmbossDir)==0:
			os.mkdir(self.EOLEmbossDir)

		if os.path.exists(self.PRCEmbossDir) ==0:
			os.mkdir(self.PRCEmbossDir)

		EmbossIniPath = 'C:\\Users\\jscull\\AppData\\Roaming\\Irfanview\\Emboss.ini'

		print('Preparing for photo embossing')
		EmbossInit()

		if (self.eolV.get()):
			print('Emobssing EOL photos')
			l = 0
			for PhotoNo in range(StartLayer,LastLayerNo):
				PhotoName = self.Build_No + '_EOL_'+'%05d' %PhotoNo+'.JPG'
				PhotoPath = self.EOLDir +'\\'+ PhotoName
				EmbossedPhotoDir = self.EOLEmbossDir + '\\' + PhotoName  #Outputfile directory
				SubProcessCommand = IrfanView+ ' ' + PhotoPath + ' /advancedbatch /convert='+EmbossedPhotoDir
				subprocess.call(SubProcessCommand)
				l += 1
				if l == ProgressTrack:
					print('Embossing EOL photo %d of %d...' %(PhotoNo,LayerCount))
					l = 0

				self.pb += 1
				self.progress["value"] = self.pb
				self.progress.update()

		if (self.prcV.get()):
			l = 0
			print('Emobssing PRC photos')
			for PhotoNo in range(StartLayer,LastLayerNo):
				PhotoName = self.Build_No + '_PRC_'+'%05d' %PhotoNo+'.JPG'
				PhotoPath = self.PRCDir +'\\'+ PhotoName
				EmbossedPhotoDir = self.PRCEmbossDir + '\\' + PhotoName  #Outputfile directory
				SubProcessCommand = IrfanView+ ' ' + PhotoPath + ' /advancedbatch /convert='+EmbossedPhotoDir
				subprocess.call(SubProcessCommand)
				l += 1
				if l == ProgressTrack:
					print('Emobssing PRC photo %d of %d...' %(PhotoNo,LayerCount))
					l=0

				self.pb += 1
				self.progress["value"] = self.pb
				self.progress.update()
				
		self.ffmpegDir = "C:\FFMPEG\\bin\\ffmpeg.exe "
		self.frameRate = "-framerate 60 "
		self.startnumber = "-start_number 1 "
		self.format = "-c:v libx264 "
		self.output = "-r 30 "+self.buildNum.get()
		
		self.createEOLTL()		
		
		self.createPRCTL()

		#add an ending protocol, open directory of output ask user if they want to be redirected into it or if they want to quit
		self.end_protocol()		

	def createEOLTL(self):
		print("Creating EOL TL")
		path = self.EOLEmbossDir
		path.replace("\\","/")
		os.chdir( path )
		command = self.ffmpegDir+self.frameRate+self.startnumber+" -i "+self.Build_No+"_EOL_%05d.JPG "+self.format+self.output+"_EOL.mp4"	
		print("Command must match this format: C:\FFMPEG\bin\ffmpeg.exe -framerate 60 -start_number 1 -i B00000_PRC_%05d.JPG -c:v libx264 -r 30 B00000_PRC.mp4")
		print(command)
		try:
			subprocess.call(command)
			self.pb += 10
			self.progress["value"] = self.pb
			self.progress.update()
		except:
			print("Error calling command")

	def createPRCTL(self):
		print("Creating PRC TL")
		path = self.PRCEmbossDir
		path.replace("\\","/")
		os.chdir( path )
		command = self.ffmpegDir+self.frameRate+self.startnumber+" -i "+self.Build_No+"_PRC_%05d.JPG "+self.format+self.output+"_PRC.mp4"
		try:
			subprocess.call(command)
			self.pb += 10
			self.progress["value"] = self.pb
			self.progress.update()
		except:
			print("Error calling command")

	def end_protocol(self):
		self.controller.show_frame(EndPage)

class EndPage(ttk.Frame):
	def __init__(self,parent,controller):
		ttk.Frame.__init__(self,parent)
		self.controller = controller

		l = ttk.Label(self,text="MasterEmboss is complete!")
		l.pack()
		l = ttk.Label(self,text="Output Directory: %s"%od)
		l.pack()
		b = ttk.Button(self,text="Open Dir & Quit",command=self.open_dir)
		b.pack()
		b = ttk.Button(self,text="Send Automated Email",command=AutomateEmail)
		b = ttk.Button(self,text="Just Quit",command=self.quit)
		b.pack()

	def quit(self):
		app.destroy()

	def open_dir(self):
		data = self.controller.get_page(RenamePage)
		explorer = 'start %windir%\explorer.exe '
		path = data.outDir.get()

		app.destroy()
			
class VersionDialog:
	def __init__(self,parent):
		top = self.top = tk.Toplevel(parent)
		self.placed = False
		
		self.pointer = 0
		info = get_version_info()
		self.v = info[0]
		self.currentV = self.v
		self.oldestVersion = self.get_oldest_version()
		self.a = info[1]
		
		self.vNum = tk.Label(top,text="Version: %s"%self.v[self.pointer])
		self.vInfo = tk.Label(top,text="Version notes: %s"%self.a[self.pointer])
		self.prev = ttk.Button(top,text="Previous Version",command=self.previous_version)
		self.next = ttk.Button(top,text="Next Version",command=self.next_version)
		
		self.vNum.pack()
		self.vInfo.pack()
		self.prev.pack()
		
	def previous_version(self):
		print("Before method: %s"%self.pointer)
		print("Arr lens: %s, %s"%(len(self.v),len(self.a)))
		if (self.pointer + 1) < self.oldestVersion:			
			if self.placed == False:
				self.placed = True
				self.next.pack()
			
			self.pointer += 1
			print("During: %s"%self.pointer)
			self.vNum.config(text="Version: %s"%self.v[self.pointer])
			self.vInfo.config(text="Version info: %s"%self.a[self.pointer])
		
	def next_version(self):
		print("Before method: %s"%self.pointer)
		print("Arr lens: %s, %s"%(len(self.v),len(self.a)))
		if (self.pointer - 1) >= 0:
			self.pointer -= 1
			print("During: %s"%self.pointer)
			if self.pointer == 0:
				self.placed = False
				self.next.pack_forget()
			
			self.vNum.config(text="Version: %s"%self.v[self.pointer])
			self.vInfo.config(text="Version info: %s"%self.a[self.pointer])
	
	def get_oldest_version(self):
		c = len(self.v)
		return c
		
class HelpDialog:
	def __init__(self,parent):
		top = self.top = tk.Toplevel(parent)
		self.elements = []
		
		self.currentPage = "menu"
		self.l = ttk.Label(top,text="Help Options:")
		self.rename = ttk.Button(top,text="Rename Page help",command=lambda t=top: self.init_rename(t))
		self.process = ttk.Button(top,text="Processing Page Help",command=lambda t=top: self.init_process(t))
		self.works = ttk.Button(top,text="How it works",command=lambda t=top: self.init_works(t))
		
		self.back = ttk.Button(top,text="Back",command=self.go_back)
		
		self.l.pack()
		self.elements.append(self.rename)
		self.elements.append(self.process)
		self.elements.append(self.works)
		
		self.e_pack(self.elements)
		
	def init_rename(self,top):
		self.e_forget(self.elements)
	
		self.l.config(text="Rename Page Help")
		self.currentPage = "rename"
		self.renameArr = []
		
		self.head1 = ttk.Label(top,text="Directories:")
		self.wdHelp = ttk.Label(top,text="Working Directories are the directories that your photographs are stored in.\nSelected them in the correct order for them to be processed in the correct order.")
		self.odHelp = ttk.Label(top,text="Output Directory is the directory where all the output files will be stored.")
		self.head2 = ttk.Label(top,text="Start / End Numbers")
		self.nums = ttk.Label(top,text="Start and End numbers of all the directories are the first and last number that the pictures are saved with.\n(e.g. starts on DSC_0001 and ends on DSC_0567, start number for that directory is 1 and end number is 567).")
		self.wnum = ttk.Label(top,text="Write Start is the number you want the new names to start on (Usually use 1).")
		self.head3 = ttk.Label(top,text="Preffix / Suffix")
		self.presuff = ttk.Label(top,text="Preffix is the lead of the file name (e.g. DSC_0001 preffix is 'DSC_')\n\n- Suffix is the type of file the picture is stored as (Most likely PNG or JPG)")
				
		self.renameArr.append(self.head1)
		self.renameArr.append(self.wdHelp)
		self.renameArr.append(self.odHelp)
		self.renameArr.append(self.head2)
		self.renameArr.append(self.nums)
		self.renameArr.append(self.wnum)
		self.renameArr.append(self.head3)
		self.renameArr.append(self.presuff)
		self.renameArr.append(self.back)
		
		self.e_pack(self.renameArr)
		
	def init_process(self,top):
		self.e_forget(self.elements)
		
		self.l.config(text="Processing Help")
		self.currentPage = "process"
		self.processArr = []
		
		self.l1 = ttk.Label(top,text="Place Holder")
		
		self.processArr.append(self.l1)
		self.processArr.append(self.back)
		
		self.e_pack(self.processArr)
	
	def init_works(self,top):
		self.e_forget(self.elements)
		
		self.l.config(text="How it works")
		self.currentPage = "works"
		self.worksArr = []
		
		self.l = ttk.Label(top,text="In order for this to run you will need to install both FFMPEG and IrfanView (use default directories)")
		self.l1 = ttk.Label(top,text="Place Holder")
		
		self.worksArr.append(self.l)
		self.worksArr.append(self.l1)
		self.worksArr.append(self.back)
		
		self.e_pack(self.worksArr)
	
	def go_back(self):
		if self.currentPage == "rename":
			self.e_forget(self.renameArr)
			self.e_pack(self.elements)
		elif self.currentPage == "process":
			self.e_forget(self.processArr)
			self.e_pack(self.elements)
		elif self.currentPage == "works":
			self.e_forget(self.worksArr)
			self.e_pack(self.elements)
			
	def e_pack(self,arr):
		for a in arr:
			a.pack(pady=1)
	
	def e_forget(self,arr):
		for a in arr:
			a.pack_forget()
			
class AboutDialog:
	def __init__(self,parent):
		top = self.top = tk.Toplevel(parent)
		#"About MasterEmboss","MasterEmboss is a small GUI based application coded by Joe Scull.\nHowever credit must be given to Adrian Schmieder due to his work on the orginal scripts for processing the images.
		#\n\nThis program was made in order to reduce the workload the orginal scripts created whilst being as efficient. Any bugs or questions contact joescull@hieta.biz"
		self.l = ttk.Label(top,text="About Master Emboss")
		self.l.pack()
		self.l = ttk.Label(top,text="MasterEmboss is a small GUI based application coded by Joe Scull.")
		self.l.pack()
		self.l = ttk.Label(top,text="For this program to run you will need to install FFMPEG and IfranView installed in their default directories")
		self.l = ttk.Label(top,text="However credit must be given to Adrian Schmieder for his work on the orginal scripts for processing the images.")
		self.l.pack()
		self.l = ttk.Label(top,text="This program was made in order to reduce the workload the orginal scripts created whilst being as efficient.\nAny bugs or questions contact joescull@hieta.biz",justify='center')
		self.l.pack()
		
def main():
	global app
	app = bossinit()
	app.title("MasterEmboss")
	menubar = tk.Menu(app)
	optionsmenu = tk.Menu(menubar,tearoff=0)
	optionsmenu.add_command(label="Help",command=lambda n=1: menuevent(n))
	optionsmenu.add_command(label="About..",command=lambda n=2: menuevent(n))
	optionsmenu.add_separator()
	optionsmenu.add_command(label="Version",command=lambda n=3: menuevent(n))
	menubar.add_cascade(label="Options",menu=optionsmenu)
	app.config(menu=menubar)
	app.resizable(False,False)
	app.mainloop()

if __name__ == '__main__':
	main()

 