#!/usr/bin/python

import xml.etree.cElementTree as ET

class XMLWriter:

	def __init__(self,x):
		self.d=x

	def __getEntries(self,fname):
		hid,q_cat,q_hei,s_cat=[],{},{},{}
		#s_hei={}
		with open(fname) as fi:
			for line in fi:
				line=line.split()
				if line[0]=='hid':
					hid=colNums=line[1].split(',')
				elif line[0]=='qid':
					if line[1]=='cat':
						q_cat[line[2]]=[i.split('=') for i in line[3].split(',')]
					else:
						q_hei[line[2]]=line[3].split(',')
				elif line[0]=='sens':
					if line[1]=='cat':
						s_cat[line[2]]=[i.split('=') for i in line[3].split(',')]
					#else:
					#	s_hei[line[2]]=line[3].split(',')
		return 	hid,q_cat,q_hei,s_cat#,s_hei
				


	def makeXML(self):
		self.configParams=ET.Element('config')
		self.configParams.set('method',self.d['config method'])
		for i in ['k','l','c','t','suppThreshold']:
			if i in self.d:
				self.configParams.set(i,self.d[i])

		self.inputs=ET.SubElement(self.configParams,'input')
		self.inputs.set('filename',self.d['input filename'])
		self.inputs.set('separator',self.d['separator'])
		
		self.outputs=ET.SubElement(self.configParams,'output')
		self.outputs.set('filename',self.d['output filename'][:-5]+'_'+self.d['format']+'.data')
		self.outputs.set('format',self.d['format'])
		
		self.hid,self.q_cat,self.q_hei,self.s_cat=self.__getEntries(self.d['text file\'s path'])
		#Also need to add self.s_hei ^^, i.e. when hierarchical sensitive attributes are supported.

		self.ids=ET.SubElement(self.configParams,'id')
		# all the identifiers will be SubElems of ids
		if self.hid:
			for i in self.hid:
				ET.SubElement(self.ids,'att').set('index',i)

		self.qids=ET.SubElement(self.configParams,'qid')
		# all the quasi-identifiers will be SubElems of qids
		if self.q_cat:
			for colIndex in self.q_cat:
				self.l=ET.SubElement(self.qids,'att')
				self.l.set('index',colIndex)
				self.m=ET.SubElement(self.l,'map')
				low,high=None,None
				for index in range(len(self.q_cat[colIndex])):
					self.e=ET.SubElement(self.m,'entry')
					self.e.set('cat',self.q_cat[colIndex][index][0])
					self.e.set('int',self.q_cat[colIndex][index][1])
					if index==0:
						low=self.q_cat[colIndex][index][1]
					if index==len(self.q_cat[colIndex])-1:
						high=self.q_cat[colIndex][index][1]
				self.vgh=ET.SubElement(self.l,'vgh')
				self.vgh.set('value','[%s:%s]'%(low,high))
		
		if self.q_hei:
			for colIndex in self.q_hei:
				self.l=ET.SubElement(self.qids,'att')
				self.l.set('index',colIndex)
				root=None
				for node in self.q_hei[colIndex]:
					if '-' in node:
						nodes=node.split('-')
						self.r=ET.SubElement(self.root,'node')
						self.r.set('value','['+nodes[0]+')')
						for n in range(len(nodes[1:])):
							ET.SubElement(self.r,'node').set('value','['+nodes[1:][n]+')')
					else:
						self.root=ET.SubElement(self.l,'vgh')
						self.root.set('value','['+node+')')


		self.sens=ET.SubElement(self.configParams,'sens')
		# all the sensitive fields will be SubElems of sens
		if self.s_cat:
			for colIndex in self.s_cat:
				self.l=ET.SubElement(self.sens,'att')
				self.l.set('index',colIndex)
				self.m=ET.SubElement(self.l,'map')
				low,high=None,None
				for index in range(len(self.s_cat[colIndex])):
					self.e=ET.SubElement(self.m,'entry')
					self.e.set('cat',self.s_cat[colIndex][index][0])
					self.e.set('int',self.s_cat[colIndex][index][1])
		
		#Currently, the tool doesn't support hierarchical sensitive fields. Once it does, the commented portion can be used un-commented and used.
		'''
		if self.s_hei:
			for colIndex in self.s_hei:
				self.l=ET.SubElement(self.sens,'att')
				self.l.set('index',colIndex)
				self.root=None
				for node in self.s_hei[colIndex]:
					if '-' in node:
						nodes=node.split('-')
						self.r=ET.SubElement(self.root,vgh)
						self.r.set('value','['+nodes[0]+')')
						for n in range(len(nodes[1:])):
							ET.SubElement(self.r,'node').set('value','['+nodes[1:][n]+')')
					else:
						self.root=ET.SubElemet(self.l,'vgh')
					self.root.set('value','['+node+')')
		'''
						
		ET.ElementTree(self.configParams).write('config.xml',method='xml',xml_declaration=True)


