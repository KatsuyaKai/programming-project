# encoding: utf-8

import sys
from Bio import Seq
from Bio import SeqIO

def main():
	Gbk_File = sys.argv[1]
	Gbk_To_Fasta(Gbk_File)


## Saves all the aminoacid sequences from the Genbank in fasta format with their id in a file
## called 'gbk_fasta.fa' in the Data directory.
## If Gbk_file is not a Genbank it returns False and the main program ends.

def is_it_genbank(Gbk_File, basename):
	gbk_fasta = open('Data/' + str(basename) + '/gbk_fasta.fa',"w")
	with open(Gbk_File, "r") as input_handle:
		for record in SeqIO.parse(input_handle, "genbank"):
			#pass
			#print()
			#print(record)
			#print(record.seq) # The sequence itself, typically a Seq object
			#print(record.id) #The primary ID used to identify the sequence – a string(Acc number)
			#print(record.name) #A “common” name/id for the sequence
			#print(record.description) #A human readable description or expressive name for the sequence – a string
			#print(record.letter_annotations) #Holds per-letter-annotations using a dictionary of additional information about the letters in the sequence
			#print(record.dbxrefs)  #A list of database cross-references as string (Bioproject,Biosample,Assembly)
			#print(record.features)

		
			#feature object	
			for feature in record.features:
				#print feature
				#print feature.type # Description of the type of feature (for instance,‘CDS’ or ‘gene’)
				
				#location attribute
				#print feature.location 
				#print feature.location.start
				#print feature.location.end
				#print feature.location.strand

				#qualifiers attribute
				#print feature.qualifiers #This is a Python dictionary of additional information about the feature

				if feature.type == 'CDS':
					#if feature.qualifiers['locus_tag'][0] == 'STM4600':
					# print (">"+feature.qualifiers['locus_tag'][0])
					# try:
					# 	print (feature.qualifiers['gene'][0])
					# except:
					# 	print "NA" 
					# try:
					# 	print feature.qualifiers['EC_number'][0]
					# except:
					# 	print "NA"

					#print feature.qualifiers['product'][0]
					try:
						locus = feature.qualifiers['locus_tag'][0]
						gbk_fasta.write ('>' + locus + '\n' + feature.qualifiers['translation'][0] + '\n')
					except:
						pass
	if len(open('Data/' + str(basename) + '/gbk_fasta.fa').readlines()) > 0:
		return True
	else:
		return False
					#print feature.location.start
					#print feature.location.end
					#print feature.location.strand
					#print "\n"



					#how to extract DNA position (Be careful with strand)
	"""start = feature.location.start
	end = feature.location.end
	strand = feature.location.strand
	
	#print strand
	#print record.seq[start:end]
	



	#how to extract DNA position (Be careful with strand)

	if strand < 0:
		sequence =  record.seq[start:end]
		

		locus = feature.qualifiers['locus_tag'][0]
		print(">"+locus+"\n"+sequence.reverse_complement()+"\n")
	else:
		sequence =  record.seq[start:end]
		#print sequence

		locus = feature.qualifiers['locus_tag'][0]
		print(">"+locus+"\n"+sequence+"\n")"""
		


if __name__=='__main__':
	main()






