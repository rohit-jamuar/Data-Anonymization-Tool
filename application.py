#!/usr/bin/python

from Tkinter import *

class GUI(Frame):
	def __init__(self,parent=None):	
		Frame.__init__(self,parent)
		self.parent=parent
		self.__rows=[None]*8
		self.__entries=[None]*7
		self.__successMsg,self.__errorMsg=None,None
		self.__initUI()

	def __clearWidgets(self):

		if self.__errorMsg:
			self.__errorMsg.destroy()
			self.__errorMsg=None
			
		if self.__successMsg:
			self.__successMsg.destroy()
			self.__successMsg=None
		
		for i in range(8):
			if self.__rows[i]:
				self.__rows[i].destroy()
				self.__rows[i]=None
		
		for i in range(7):
			if self.__entries[i]:
				self.__entries[i].destroy()
				self.__entries[i]=None
	

	def __showWidgets(self,opt):
		self.__clearWidgets()
		
		for i in [1,2,3,4]:
			
			if not self.__rows[i]:
				self.__rows[i]=Frame(self.parent)
			
			if i==1:
				l=Label(self.__rows[i],text='Input file\'s path:')
			elif i==2:
				l=Label(self.__rows[i],text='Output file\'s path:')
			elif i==3:
				l=Label(self.__rows[i],text='Separator:  ')
			elif i==4:
				l=Label(self.__rows[i],text='TXT path:  ')
			
			if not self.__entries[i]:
				self.__entries[i]=Entry(self.__rows[i],bd=5)
				self.__entries[i].configure(justify=CENTER,width=55)
				if i==1:
					self.__entries[i].insert(0,'Input/census-income_1K.txt')
				elif i==2:
					self.__entries[i].insert(0,'Output/'+'Output-%s.txt'%opt)
				elif i==3:
					self.__entries[i].insert(0,'\',\'')	
				elif i==4:
					self.__entries[i].insert(0,'config/config.txt')	

			self.__rows[i].pack(side=TOP,padx=5,pady=5,fill=X)
			l.pack(side=LEFT)
			self.__entries[i].pack(side=RIGHT)

		if opt in ['Datafly','Incognito_k']:
			
			for i in [5,6]:
				
				if not self.__rows[i]:
					self.__rows[i]=Frame(self.parent)
				if i==5:
					l=Label(self.__rows[i],text='k: ')
				else:
					l=Label(self.__rows[i],text='Suppression Threshold:')

				if not self.__entries[i]:
					self.__entries[i]=Entry(self.__rows[i],bd=5)
					self.__entries[i].configure(justify=CENTER,width=55)		
				
					if i==5:
						self.__entries[i].insert(0,'10')
					else:
						self.__entries[i].insert(0,'Defaults to k')

				self.__rows[i].pack(side=TOP,padx=5,pady=5,fill=X)
				l.pack(side=LEFT)
				self.__entries[i].pack(side=RIGHT)
				
			if not self.__rows[7]:
				self.__rows[7]=Frame(self.parent)
				self.__rows[7].pack(side=TOP,padx=5,pady=5,fill=X)
		
			self.menuOpt=StringVar(self.__rows[7])
			self.menuOpt.set('Output Type')
			self.__optMenu=OptionMenu(self.__rows[7],self.menuOpt,'genVals','genValsDist','anatomy')

			self.__optMenu.pack(expand=YES,fill=X)	

		elif opt in ['Incognito_t','Mondrian']:
			
			if not self.__rows[5]:
				self.__rows[5]=Frame(self.parent)
			if opt=='Incognito_t':
				l=Label(self.__rows[5],text='t: ')
			else:
				l=Label(self.__rows[5],text='k: ')
				
			if not self.__entries[5]:
				self.__entries[5]=Entry(self.__rows[5],bd=5)	
				self.__entries[5].configure(justify=CENTER,width=55)
				
				if opt=='Incognito_t':
					self.__entries[5].insert(0,'0.2')
				else:
					self.__entries[5].insert(0,'10')
					
				self.__rows[5].pack(side=TOP,padx=5,pady=5,fill=X)
				l.pack(side=LEFT)
				self.__entries[5].pack(side=RIGHT)	
		
			if not self.__rows[6]:
				self.__rows[6]=Frame(self.parent)
				self.__rows[6].pack(side=TOP,padx=5,pady=5,fill=X)
		
			self.menuOpt=StringVar(self.__rows[6])
			self.menuOpt.set('Output Type')
			self.__optMenu=OptionMenu(self.__rows[6],self.menuOpt,'genVals','genValsDist','anatomy')

			self.__optMenu.pack(expand=YES,fill=X)	
		

		
	def __initUI(self):
		self.parent.title("GaTech Data Anonymizer")
		self.pack()
		
		self.photo=PhotoImage(file='gatech_buzz.gif')
		self.background_label=Label(self.parent,image=self.photo)
		self.background_label.image=self.photo
		self.background_label.pack(pady=20)
		
		if not self.__rows[0]:
			self.__rows[0]=Frame(self.parent)
		self.ConfigL=Label(self.__rows[0],text='Config file\'s path ')
		self.__entries[0]=Entry(self.__rows[0],bd=5)
		
		self.__entries[0].configure(justify=CENTER,width=55)
		self.__entries[0].insert(0,'Defaults to <config.xml>')
		
		self.__rows[0].pack(side=TOP,padx=5,pady=5,fill=X)
		self.ConfigL.pack(side=LEFT)
		self.__entries[0].pack(side=RIGHT)
				
		self.algo_option=StringVar(self.parent)
		self.algo_option.set('Choose Method')
		
		self.options=OptionMenu(self.parent,self.algo_option,'Datafly','Incognito_k','Mondrian','Incognito_t', command=lambda x: self.__showWidgets(self.algo_option.get()))
		self.options.configure(width=35)
		self.options.pack()

		self.quit_button=Button(self.parent,text="QUIT",command=self.parent.destroy,relief=RAISED,justify=RIGHT)
		self.quit_button.configure(background='Grey')
		self.quit_button.pack(side=BOTTOM,anchor=E)

		self.anon_button=Button(self.parent,text="Anonymize",command=self.__anonymize,relief=RAISED,justify=RIGHT)
		self.anon_button.configure(background='Grey')
		self.anon_button.pack(side=BOTTOM,anchor=E,fill=X)	


	def __getValues(self):
		
		if self.algo_option.get()!='Choose Method':
		
			values={}
			
			values['config method']=self.algo_option.get()
			values['input filename']=self.__entries[1].get().strip()
			values['output filename']=self.__entries[2].get().strip()
		
			if self.__entries[3].get() == '\',\'':
				values['separator']=','
			else:
				values['separator']=self.__entries[3].get().strip()

			if self.algo_option.get() == 'Datafly' or self.algo_option.get() =='Mondrian' or self.algo_option.get() == 'Incognito_k':
				values['k']=self.__entries[5].get().strip()
			elif self.algo_option.get() == 'Incognito_t':
				values['t']=self.__entries[5].get().strip()

			if self.algo_option.get() == 'Datafly' or self.algo_option.get() == 'Incognito_k':
				if self.__entries[6].get().strip() == 'Defaults to k':
					values['suppThreshold']=values['k']
				else:	
					values['suppThreshold']=self.__entries[6].get().strip()

			if self.menuOpt.get()== 'Output Type':
				values['format']='genVals'
			else:
				values['format']=self.menuOpt.get().strip()

			values['text file\'s path']=self.__entries[4].get().strip()

			return values
		else:
			
			if self.__entries[0].get() == 'Defaults to <config.xml>':
				return 'config.xml'			
			else:
				return self.__entries[0].get().strip()

	def __sanityCheckInputs(self):
		from os.path import isfile
		x=self.__getValues()
		hasError=False
		if type(x) in [str,dict]:
			if not self.__rows[7]:
				self.__rows[7]=Frame(self.parent)
				
			if type(x)==str:
				if not isfile(x):
					self.__errorMsg=Label(self.__rows[7],text='Invalid config filepath!',background="Red")
					self.__rows[7].pack()
					self.__errorMsg.pack(pady=2)
					hasError=True
			else:
				if not isfile(x['input filename']):
					self.__errorMsg=Label(self.__rows[7],text='Invalid input filepath!',background="Red")
					self.__rows[7].pack()
					self.__errorMsg.pack(pady=2)
					hasError=True
	
				if not isfile(x['text file\'s path']):
					self.__errorMsg=Label(self.__rows[7],text='Invalid TXT filepath!',background="Red")
					self.__rows[7].pack()
					self.__errorMsg.pack(pady=2)
					hasError=True
	
				if 't' in x and int(float(x['t']))>=1:
					self.__errorMsg=Label(self.__rows[7],text='The value of t should be between 0 and 1!',background="Red")
					self.__rows[7].pack()
					self.__errorMsg.pack(pady=2)
					hasError=True
					
		return False if hasError else x

	def __anonymize(self):
		res=self.__sanityCheckInputs()
		from os import system,path
		if type(res) in [str,dict]:
			system('chmod a+x anonymization.sh')
			if type(res)==str:
				if not path.isfile(res):
					system('cp %s .'%res)
					system('./anonymization.sh')
					system('rm %s'%res)
				else:
					system('./anonymization.sh')
			elif type(res)==dict:
			 	from XMLwriter import XMLWriter
				XMLWriter(res).makeXML()
				system('./anonymization.sh')

			self.__successMsg=Label(self.parent,text='Data anonymized successfully!',background="Green")	
			self.__successMsg.pack(pady=2,fill=X)
		
		
def main():
	root=Tk()
	root.geometry("350x700+100+0")
	root.configure(background='white')
	app=GUI(root)
	app.mainloop()

if __name__=='__main__':
	main()
