# encoding: utf-8
import sys

from Bio import Seq, SeqIO
import pandas as pd 


def main():
	QueryFile = sys.argv[1]
	is_it_fasta(QueryFile, QueryFile)
	
	return


# This function first checks if query is in fasta format.
# For each query in the fasta file, the function generates a new file in fasta format.
# These new files are saved in a folder named Queries inside the experiment folder in Data.
def is_it_fasta (QueryFile, basename):
	
	for record in SeqIO.parse(QueryFile, "fasta"):
		QueryFasta = open('Data/' + str(basename) + '/Queries/' + record.id, 'w')
		QueryFasta.write('>' + record.id + '\n')
		QueryFasta.write(str(record.seq) + '\n')
	try:	
		HaySecuencia = record.seq # Checks if sequences are in fasta format.
		return True
	except:
		return False # False if no sequences are in fasta format.
	
	return


# We get the hits sequence from a multifasta and save them into HitsFile.txt.
def seq_from_id(FastaFile, Hits):
	Hits_File = open("HitsFile.txt","w")
	with open(FastaFile, "r") as input_handle:
		for record in SeqIO.parse(input_handle, "fasta"):
			for hit in Hits:
				if record.id == hit:
					Hits_File.write('>' + record.id + '\n') #The primary ID used to identify the sequence – a string(Acc number)
					Hits_File.write(str(record.seq)+'\n') # The sequence itself, typically a Seq object


# We add the query to the hits sequences for subsequent analysis.
def add_queries(HitsFile, query):

	Hits_File = open(HitsFile,"a")
	with open (query) as reader:
		for line in reader:
			Hits_File.write(line)


if __name__=='__main__':
	main()