# encoding: utf-8


import sys
from Bio import Seq
from Bio import SeqIO
import pandas as pd 


#SeqIO.read() for fasta

def main():
	QueryFile = sys.argv[1]
	IsQueryFasta(QueryFile)
	
	return

def is_it_fasta (QueryFile, basename):
	## For each query in the fasta file, the function generates a new file in fasta format.
	## These new files are saved in a folder named Queries inside the experiment folder in Data.
	## QueryFasta = open('Data/' + str(basename) + '/Query_In_Fasta.fa', 'w')
	for record in SeqIO.parse(QueryFile, "fasta"):
		QueryFasta = open('Data/' + str(basename) + '/Queries/' + record.id, 'w')
		QueryFasta.write('>' + record.id + '\n')
		QueryFasta.write(str(record.seq) + '\n')
	try:	
		HaySecuencia = record.seq ## Checks if sequences are in fasta format.
		return True
	except:
		return False ## False if no sequences are in fasta format.
	
	return

def SeqFromID(FastaFile, Hits):
	Hits_File = open("HitsFile.txt","w")
	with open(FastaFile, "r") as input_handle:
		for record in SeqIO.parse(input_handle, "fasta"):
			for hit in Hits:
				if record.id == hit:
					Hits_File.write('>' + record.id + '\n') #The primary ID used to identify the sequence – a string(Acc number)
					Hits_File.write(str(record.seq)+'\n') # The sequence itself, typically a Seq object
			

		#print(record)
		#print ("Hola")
				
			
		#print(record.name) #A “common” name/id for the sequence
		#print(record.description) #A human readable description or expressive name for the sequence – a string
		#print(record.letter_annotations) #Holds per-letter-annotations using a dictionary of additional information about the letters in the sequence
		#print(record.dbxrefs)  #A list of database cross-references as string (Bioproject,Biosample,Assembly)
		#print(record.features)

def AddQueries(HitsFile, query):

	Hits_File = open(HitsFile,"a")
	with open (query) as reader:
		for line in reader:
			Hits_File.write(line)

if __name__=='__main__':
	main()