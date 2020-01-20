import sys
import os
import csv
from subprocess import Popen, PIPE


def main():
	if not os.path.exists('Results'):
	    os.mkdir('Results')
	if not os.path.exists('Data'):
	    os.mkdir('Data')
	query = sys.argv[1]
	subject = sys.argv[2]
	coverage = sys.argv[3]
	identity = sys.argv[4]
	basename = os.path.basename(query)
	blaster(query, subject,coverage, identity, basename)


# Asks for coverage and identity thresholds and checks if they are between 0 and 100.
def coverage_identity(query):
	while True:
		try:
			coverage = float(input('\nPlease, introduce the coverage threshold for the Blast analysis for %s: ' %(query)))
			if coverage >= 0 and coverage <= 100:
				break		
			else:
				print ('Coverage value is not valid. It must be between 0 and 100.')
		except:
			print ('Coverage value must be a number between 0 and 100.')
	while True:
		try:
			identity = float(input('Please, introduce the identity threshold for the Blast analysis for %s: ' %(query)))
			if identity >= 0 and identity <= 100:
				return (coverage, identity)
			else:
				print ('Identity value is not valid. It must be between 0 and 100.')	
		except:
			print ('Identity value must be a number between 0 and 100.')
	return	


## BLAST analysis ##
def blaster(query,subject,coverage,identity,basename,results_dir='',query_name=''):
	Blast_log = open (results_dir + 'Process.log',"a")
	# We create the database everytime since it is a very fast process. This way we allow to BLAST the same query against different databases.
	Database = Popen(['makeblastdb', '-in',  subject, '-dbtype', 'prot','-out', 'Data/'+str(basename)+'/Blast_DB/'+str(basename)], stdout=PIPE, stderr=PIPE)
		
	# The script enters the try upon creation of the database.
	try:
		log_db = Database.stdout.read()
		print ('\n' + ('Creating database for BLAST analysis...').center(80))
		Blast_log.write('\n\n' + ('Creating database for BLAST analysis...').center(80))
		Blast_log.write(log_db.decode('utf-8'))
		error_db = Database.stderr.read()
		if error_db:
			Blast_log.write("Errors encountered while creating the database: \n")
			Blast_log.write(error_db.decode('utf-8'))
			print ('We have experienced some problems while creating the database for the Blast analysis. Please, check ' + results_dir + 'Process.log')
			sys.exit()
		
		Blast_log.write('\n' + ('Databased created').center(80))

		Database.stderr.close()
		Database.stdout.close()
	
	except:
		print ()
	# With "tries" we check if BLAST+ is installed. 
	try:	
		Blast = Popen(['blastp','-query',query,'-db', 'Data/'+str(basename)+'/Blast_DB/'+ str(basename), '-evalue', '0.000001', \
						'-qcov_hsp_perc', str(coverage), '-outfmt',"6 qseqid sseqid qcovs pident evalue qstart qend qlen sseq ", \
						'-out', 'Blast_result.tsv'], stdout=PIPE, stderr=PIPE)
		
		error_Blast = Blast.stderr.read()
		Blast_log.write ('\n\n\n' + ('Blast analysis...').center(80))
		if error_Blast:
			Blast_log.write("Errors encountered while carrying out Blast analysis: \n")
			Blast_log.write(error_Blast.decode('utf-8'))
			print ('We have experienced some problems while carrying out Blast analysis. Please, check Results/' + str(basename) + '/blast.log')
			sys.exit()
		else:
			print ('\n' + ('Blast analysis...').center(80))

		Blast.stderr.close()
		Blast.stdout.close()

		# Save Blast result with a header in a tsv format.
		my_output = open(results_dir + 'Blast/Blast_result.tsv',"w")
		my_output.write("Query seq ID\tSubject seq ID\t% Coverage\t% Identity\tE value\tAlignment starts (bp)\tAlignment ends (bp)\tQuery length\tAligned part of subject sequence\n") 
		with open ('Blast_result.tsv') as tsvfile:
			reader = csv.reader(tsvfile, delimiter='\t')
			for row in reader:
				if float(row[3]) >= float(identity):
					#for campo in range(len(row)):
					for campo in range(9):
						my_output.write(str(row[campo])+'\t')
					my_output.write('\n')

		Blast_log.write ('\n\n' + ('Blast analysis completed').center(80) + '\n')
		Blast_log.write (('Check Blast results at: ' + results_dir + 'Blast').center(80))
	# If BLAST analysis had issues we end the execution of the main programme.
	except:
		print ('Errors encountered while trying to perform BLAST analysis. Please, check if BLAST+ is installed')
		sys.exit()		

	return


# We create a list with all the hit ids.
def blaster_hits(FilePath):
	hits=[]
	with open (FilePath) as tsvfile:
		reader = csv.reader(tsvfile, delimiter='\t')
		for row in reader:
			if row[1] not in hits:
				hits.append(row[1])
	return(hits)


# For usage of this module on its own.
if __name__=='__main__':
	main()
