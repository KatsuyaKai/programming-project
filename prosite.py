# script para parsear la base de datos prosite presentes en los archivos
# prosite.doc y prosite.dat utilizando el modulo Biopython
import re
from Bio.ExPASy import Prosite,Prodoc,ScanProsite
import csv

'''def ScanProsite():
	sequence = 'MNRISTTTITTITITTGNGAG'
	handle = ScanProsite.scan(seq=sequence)
	result = handle.read()
	print (result)'''


def DatParser(prosite_dat):
	print ('\n' + ('Parsing prosite file...').center(80))
	# con este script podeis parsear el archivo .dat
	handle = open(prosite_dat,"r")
	records = Prosite.parse(handle)
	PatternDict = {}
	for record in records:
		patron = PatternTranslation(record.pattern)
		PatternDict[patron] = record.accession

	return PatternDict

def PatternTranslation(pattern):

	Prosite_Expressions = ['.','x','-','{','}','(',')','<','>','>]']
	RE_Expressions = ['','.','','[^',']','{','}','^','$',']?$']
	for cambio in range(len(RE_Expressions)):
		pattern = pattern.replace(Prosite_Expressions[cambio],RE_Expressions[cambio])
	'''patron = pattern.replace('.','')
	patron1 = patron.replace('x','.')
	patron2 = patron1.replace('-','')
	patron3 = patron2.replace('{','[^')
	patron4 = patron3.replace('}',']')
	patron5 = patron4.replace('(','{')
	patron6 = patron5.replace(')','}')'''
	return pattern

def PatternSearch(PatternDict, HitsDict): #QueryFile):
	print ('\n' + ('Searching for Prosite domains in hits...').center(80))
	Patrones = PatternDict.keys()
	IDs = HitsDict.keys()
	ResultDict = {}
	for id in IDs:
		for patron in Patrones:
			if re.search (patron,HitsDict[id]) and patron != "":
				if id not in ResultDict.keys():
					ResultDict[id] = [PatternDict[patron]]
				else:
					ResultDict[id].append(PatternDict[patron])

	return ResultDict

def OutputResults(prosite_dat, ResultDict, Results_Dir):

	output = open (Results_Dir + 'prosite_result.txt',"w")
	HitIds = ResultDict.keys()
	for protein in HitIds:
		output.write('Protein ' + protein + ' has the following domains:\n\n')
		for dominio in ResultDict[protein]:
			handle = open(prosite_dat, "r")
			records = Prosite.parse(handle)
			for record in records:
				if record.accession == dominio:
					output.write("\tDomain name: "+ record.name + '\n')
					output.write("\tDomain accession: "+ record.accession + '\n')
					output.write("\tDomain description: "+ record.description + '\n')
					output.write("\tPattern found: "+ record.pattern + '\n\n')
				
	return	

def HitsFileToDict(HitsFile):

	HitsDict={}
	file = open (HitsFile, 'r')
	content = csv.reader(file, delimiter='\n')
	for row in content:
		
		if re.search (r'^>.*',row[0]):
			clave = row [0].replace('>','')
			HitsDict[clave] = ''
		else:
			HitsDict[clave] = row[0]

	return HitsDict

def WantMoreInfo(prosite_doc, ResultDict, Results_Dir):
	while True:
		print ('\nDo you want to obtain more information about the domains detected in the hits?')
		MoreInfo = input('[Y|N]: ').upper()
		if MoreInfo == 'Y' or MoreInfo == '':

			for key in ResultDict.keys():
				
				DocParser(prosite_doc, key, ResultDict, Results_Dir)
			return
		elif MoreInfo == 'N':
			return
		else:
			print ('Sorry, We did not understand you. Please answer yes by typing "y", "Y" or clicking intro, or answer no by typing "n" or "N".' )
	return

def DocParser(prosite_doc, key, ResultDict, Results_Dir):
	# con este script podemos parsear el archivo .doc
	Ext_Info = open (Results_Dir + 'Extended_Domain_Info_%s.txt' %(key),'w')
	Ext_Info.write('\n' + (' Extended information about the domains in %s ' %(key)).center(78,'#') + '\n\n')
	for Prosite_Id in ResultDict[key]:
		handle = open(prosite_doc)
		records = Prodoc.parse(handle)
		for record in records:
			try:
				if len(record.prosite_refs) > 0:
					
					for domain in range(len(record.prosite_refs)):
						#print (record.prosite_refs[domain][0],domain,Prosite_Id)
						if Prosite_Id == record.prosite_refs[domain][0]:
#						elif record.prosite_refs[domain][0] == Prosite_Id:
						#if Prosite_Id in record.prosite_refs[domain]:
							#i+=1
							#print(record.accession)
							#print(type(record.prosite_refs))
							Ext_Info.write(Prosite_Id.center(80))
							Ext_Info.write('\n\n')
							Ext_Info.write(record.text.center(80))
							#print(count)
							#print(record.references.decode('utf-8'))
						#print ("Fuera")
			except:
				pass
				
	return

#DocParser()
