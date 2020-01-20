# encoding: utf-8
import sys

from Bio import Seq,SeqIO


# If we call the module directly from the shell.
def main():
	Gbk_File = sys.argv[1]
	is_it_genbank(Gbk_File,Gbk_File)


# Saves all the aminoacid sequences from the Genbank in fasta format with their id in a file
# called 'gbk_fasta.fa' in the directory for this query in Data.
# If Gbk_file is not a Genbank it returns False and the main programme ends.
def is_it_genbank(Gbk_File, basename):
	gbk_fasta = open('Data/' + str(basename) + '/gbk_fasta.fa',"w")
	with open(Gbk_File, "r") as input_handle:
		for record in SeqIO.parse(input_handle, "genbank"):
			for feature in record.features:
				if feature.type == 'CDS':
					try:
						locus = feature.qualifiers['locus_tag'][0]
						gbk_fasta.write ('>' + locus + '\n' + feature.qualifiers['translation'][0] + '\n')
					except:
						pass
	# The file was a genbank.
	if len(open('Data/' + str(basename) + '/gbk_fasta.fa').readlines()) > 0:
		return True
	# The file was not a genbank.
	else:
		return False
					

# For usage of this module on its own.		
if __name__=='__main__':
	main()
