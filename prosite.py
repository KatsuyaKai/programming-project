import re
import csv
import sys
import os

from Bio.ExPASy import Prosite,Prodoc


# prosite.dat parser. We get a dictionary with patterns as keys and accession as values. This way is easier to handle afterwards.
def dat_parser(prosite_dat):
	print ('\n' + ('Parsing prosite file...').center(80))
	handle = open(prosite_dat,"r")
	records = Prosite.parse(handle)
	PatternDict = {}
	for record in records:
		patron = pattern_translation(record.pattern)
		PatternDict[patron] = record.accession

	return PatternDict


# Auxiliary function to translate prosite expressions into re module expressions.
def pattern_translation(pattern):

	Prosite_Expressions = ['.','x','-','{','}','(',')','<','>','>]']
	RE_Expressions = ['','.','','[^',']','{','}','^','$',']?$']
	for cambio in range(len(RE_Expressions)):
		pattern = pattern.replace(Prosite_Expressions[cambio],RE_Expressions[cambio])

	return pattern


# Function to search for patterns in the hit sequences. We obtain a dictionary with hit_id as keys and patterns found as values.
def pattern_search(PatternDict, HitsDict): 
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


# We write the PROSITE information in a file called prosite_result.txt
def output_results(prosite_dat, ResultDict, Results_Dir):

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


def hits_file_to_dict(HitsFile):

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


# We ask the user if he/she wants more information, and, if so, we use prosite.doc
def want_more_info(prosite_doc, ResultDict, Results_Dir):
	while True:
		print ('\nDo you want to obtain more information about the domains detected in the hits?')
		MoreInfo = input('[Y|N]: ').upper()
		if MoreInfo == 'Y' or MoreInfo == '':
			if not os.path.isfile(prosite_doc):
				print ('\n' + "Please, make sure you have a file named prosite.doc".center(80))
				sys.exit()

			for key in ResultDict.keys():
				
				doc_parser(prosite_doc, key, ResultDict, Results_Dir)
			return
		elif MoreInfo == 'N':
			return
		else:
			print ('Sorry, We did not understand you. Please answer yes by typing "y", "Y" or clicking intro, or answer no by typing "n" or "N".' )
	return


# prosite.doc parser
def doc_parser(prosite_doc, key, ResultDict, Results_Dir):
	Ext_Info = open (Results_Dir + 'Extended_Domain_Info_%s.txt' %(key),'w')
	Ext_Info.write('\n' + (' Extended information about the domains in %s ' %(key)).center(78,'#') + '\n\n')
	for Prosite_Id in ResultDict[key]:
		handle = open(prosite_doc)
		records = Prodoc.parse(handle)
		for record in records:
			try:
				if len(record.prosite_refs) > 0:
					for domain in range(len(record.prosite_refs)):
						if Prosite_Id == record.prosite_refs[domain][0]:
							Ext_Info.write(Prosite_Id.center(80))
							Ext_Info.write('\n\n')
							Ext_Info.write(record.text)
			except:
				pass
				
	return
