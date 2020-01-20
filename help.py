import sys
import os


# Checks if arguments passed are valid and gets the path for query and genbank files if they exist.
def main():
    if len(sys.argv) == 1:
        while True:
            query,Genbank = assistant()
            if os.path.exists(query) and os.path.exists(Genbank): 
                break
            else:
                print ('\x1b[1;31;40m' + 'The query and/or the genbank file do not exist.'.center(80) + '\x1b[0m' + '\n')
    elif len(sys.argv) == 2:
        if sys.argv[1] == '-h' or sys.argv[1] == 'help':
            Help()
        else:
            incorrect_arguments()
            sys.exit()
    elif len(sys.argv) == 3:
        if os.path.exists(sys.argv[1]) and os.path.exists(sys.argv[2]):
            query = sys.argv[1]
            Genbank = sys.argv[2]
        else:
            while True:
                print ('\x1b[1;31;40m' + 'The query and/or the genbank file do not exist.'.center(80) + '\x1b[0m' + '\n')
                query,Genbank = assistant()
                if os.path.exists(query) and os.path.exists(Genbank): 
                    break        
    # If the arguments are not valid, it ends the execution after printing a recomendation.
    else:
        incorrect_arguments()
        sys.exit()
    return (query,Genbank)


# If given arguments are invalid
def incorrect_arguments():
    print ('You have not introduced the required arguments.')
    print ('Function should be called as: <python main.py query_file GenBank_file>')
    print ('Should you require an explanation about how to use this programme, type python main.py -h.\n')


# Usage guide
def Help():
    print ('\n' + '\x1b[1;33;40m' + (' EASY_PHYLO_&_DOM Tutorial ').center(80,'#') + '\x1b[0m' + '\n')
    print ('\n' + '\x1b[1;32;40m' + (' What is this programme for? ').center(80,'-') + '\x1b[0m' + '\n')
    print ('Given a protein sequence (query), this programme allows you to:')
    print ('\t1. Search for homologue proteins (BLAST) in a Genbank.')
    print ('\t2. Align BLAST hits and create a Neighbor Joining phylogenetic tree\n\t   with Muscle')
    print ('\t3. Look for prosite domains in your query and its homologues.')
    print ('\n' + '\x1b[1;32;40m' + ' How to use this programme '.center(80,'-') + '\x1b[0m' + '\n')
    print ('You should call this programme as <python main.py query_file Genbank_file>'.center(80)+ '\n')
    print ('query_file must be in fasta and can contain more than a query.'.center(80))
    print ('GenBank_file must be a GenBank.'.center(80) + '\n')
    print ('For each query in the query_file, the programme will ask for a coverage and'.center(80) + '\n' + 'an identity threshold for the BLAST analysis.'.center(80) + '\n')
    print ('After the analysis, query_file and Genbank_file will be saved to Data directory.'.center(80))
    print ('A Results folder will also be created.'.center(80) + '\n')
    print ('For each protein sequence in query_file, a separate folder will be created in'.center(80) + '\n' + 'Results/ indicating BLAST thresholds.'.center(80)) 
    print ('This allows to make several runs with different thresholds without loosing'.center(80) + '\n' +'information.'.center(80) + '\n\n')
    print ('This tutorial can be called with <python main.py -h> or with <python main.py help>'.center(80) + '\n')
    sys.exit()
    return


# Asks whether the user needs to access the tutorial or not.
def assistant():
    
    while True:
        help = input ('Do you want to access the usage tutorial [Y/N]: ').upper()
        if help == 'Y' or help == '':
            Help()
        elif help == 'N':
            break
        else:
            print ('Please, answer yes (Y) or no (N) or press intro.')
    query = input('Please, provide the path to the query file: ')
    GenBank = input('Please, provide the path to the Genbank file: ')
    return (query, GenBank)


if __name__=='__main__':
	main()
