import sys
import os
import shutil

import gbk
import blaster
import fasta
import muscle
import prosite
import help
import plots


def main():
    # Help module controls that query and genbank are correctly provided and has a tutorial.
    query,Genbank = help.main()

    basename = os.path.basename(query) # We do not want the full path as the query name.

    # Results and Data directory are created if they do not exist. 
    # Within them a directory with the basename of the query is created.
    # All the files will be saved to these directories.
    if not os.path.exists('Results'):
        os.mkdir('Results')
    if not os.path.exists('Results/' + str(basename)):
        os.mkdir('Results/' + str(basename))
    if not os.path.exists('Data'):
        os.mkdir('Data')
    if not os.path.exists('Data/' + str(basename)):
        os.mkdir('Data/' + str(basename))
    if not os.path.exists('Data/' + str(basename) + '/Queries'):
        os.mkdir('Data/' + str(basename) + '/Queries')

    # We check the query is in fasta format. If it is not, we end the execution.
    # If it is fasta, we create a separate fasta file for each sequence in the query.
    if fasta.is_it_fasta(query,basename):
        pass
    else:
        print ("\n" + (query + ' is not fasta.').center(80))
        print ('Please check the format of your query_file.'.center(80) + "\n")
        try: 
            os.rmdir('Results/' + str(basename)) # We delete this directory if it is empty. 
        except:
            pass   # If it is not empty we do not delete it. We do not want to delete previous analysis.
        shutil.rmtree('Data/' + str(basename)) # We delete this directory which is not empty. We do not loose important information by deleting this directory.
        sys.exit() 

    # We check the genbank file is in genbank format and do the same as with the query file.
    # If it is a genbank, this function gets al the protein sequences to make a multifasta.
    if gbk.is_it_genbank(Genbank,basename): 
        pass
    else:
        print ("\n" + (Genbank + ' is not a Genbank.').center(80))
        print ('Please check the format of your Genbank_file.'.center(80) + "\n")
        try: 
            os.rmdir('Results/' + str(basename)) # We delete this empty directory.
        except:
            pass
        shutil.rmtree('Data/' + str(basename)) 
        sys.exit()

    Data_Dir = 'Data/' + str(basename)
    subject = Data_Dir + '/gbk_fasta.fa'

    # Query and Genbank files and their metadata are copied to Data directory.
    shutil.copy2(query, Data_Dir)
    shutil.copy2(Genbank, Data_Dir)
    
    # We run the program for each sequence in the query.
    with os.scandir(Data_Dir + '/Queries') as it:
        for query_file in it:
            # First, we ask for the coverage and identity thresholds.
            coverage, identity = blaster.coverage_identity(query_file.name)
        
            new_query = Data_Dir + '/Queries/' + query_file.name
            # We define the directories for the results. 
            Results_Dir = 'Results/' + str(basename) + '/' + query_file.name + '_Cov_' + str(coverage) + '_Id_' + str(identity) + '/' 
            Results_Blast = Results_Dir + 'Blast/'
            Results_Prosite = Results_Dir + 'Prosite/'
            Results_Muscle = Results_Dir + 'Muscle/'
            # If they do not exist, we create them.
            if not os.path.exists(Results_Dir):
                os.mkdir(Results_Dir)
            if not os.path.exists(Results_Blast):
                os.mkdir(Results_Blast)
            if not os.path.exists(Results_Prosite):
                os.mkdir(Results_Prosite)
            if not os.path.exists(Results_Muscle):
                os.mkdir(Results_Muscle)
            
            Process_log = open (Results_Dir + 'Process.log',"w")
            Process_log.write(' Analysis for query: %s '.center(80,'*') % (query_file.name))
            Process_log.close() # We close the log file because other functions are going to open it.

            ## BLAST analysis ##
            blaster.blaster(new_query, subject, coverage, identity, basename, results_dir = Results_Dir) # BLAST analysis.
            
            # We continue with the analysis if at least one homologue is found for the criteria indicated. 
            if len(open(Results_Blast + 'Blast_result.tsv').readlines()) > 1: # The first row of the file is the header.
                
                plots.blast_plot('Blast_result.tsv', Results_Blast, identity)

                Hits = blaster.blaster_hits(Results_Blast + 'Blast_result.tsv') # List containing all the hits_ids.

                fasta.seq_from_id(subject, Hits) # We get the hit sequences from the genbank converted to fasta.

                # We add the queries to the hits to have all the proteins together for the subsequent analyses.
                fasta.add_queries("HitsFile.txt", new_query) 

                HitsFile = "HitsFile.txt" # Temporary fasta file with all the sequences. 
                
                ## MUSCLE analysis ##
                muscle.align_seqs(HitsFile)

                # We save the alignment to MUSCLE folder
                shutil.copy2('HitsAligned.aln', Results_Muscle)

                AlignedHitsFile = 'HitsAligned.afa'  # Temporary alignment file. 
                # With the alignment, we create the Neighbor Joining tree with muscle in newick format.
                muscle.create_tree(AlignedHitsFile, Results_Dir = Results_Dir, Results_Muscle = Results_Muscle)
                # With the newick format tree, we draw a simple plot.
                Tree = muscle.draw_tree(Results_Muscle + 'NJ_Tree.phy', Results_Dir = Results_Muscle)
                
                ## PROSITE analysis ##
                Process_log = open (Results_Dir + 'Process.log',"a") ## The file is closed. We open in append mode.
                Process_log.write('\n\n\n' + ('Domain search in Prosite').center(80))
                prosite_dat = 'prosite.dat'

                # We check the prosite.dat file is in the directory and has the correct format.
                if not os.path.isfile(prosite_dat):
                    print ('\n' + "Please, make sure you have a file named prosite.dat" .center(80))
                    sys.exit()
                try:
                    Process_log.write('\n\n' + ('Parsing ' + prosite_dat + '...').center(80))
                    PatternDict = prosite.dat_parser(prosite_dat)
                except:
                    Process_log.write()
                    Process_log.write('\n\n' + ('Errors encountered while parsing ' + prosite_dat).center(80))
                    print ('Errors encountered while parsing ' + prosite_dat)
                    sys.exit()

                Process_log.write('\n\n' + ('Looking for domains in hits...').center(80))
                
                HitsDict = prosite.hits_file_to_dict(HitsFile) # Dictionary with BLAST hits as keys and no values.
                # We look for PROSITE domains in the hit sequences.
                ResultDict = prosite.pattern_search(PatternDict,HitsDict) 

                prosite.output_results (prosite_dat, ResultDict, Results_Prosite)

                # More information about the domains?
                prosite.want_more_info("prosite.doc", ResultDict, Results_Prosite)
                
                # Printing information in Process.log file
                Process_log.write('\n\n' + ('Domain search completed').center(80) + '\n')
                Process_log.write (('Check Prosite results at: ' + Results_Prosite).center(80))

                Process_log.write('\n\n\n' + ('Analysis completed').center(80) + '\n\n\n')
                Process_log.write(('Analysis summary').center(80) + '\n\n')
                Process_log.write('BLAST'.center(80) + '\n\n')
                Process_log.write('Coverage threshold: ' + str(coverage) + '\n')
                Process_log.write('Identity threshold: ' + str(identity) + '\n')
                Process_log.write('Query name: ' + query_file.name + '\n')
                Process_log.write('Genbank: ' + os.path.basename(Genbank) + '\n')
                Process_log.write('Number of hits: ' + str(len(open('Blast_result.tsv').readlines())) + '\n\n')
                Process_log.write('PROSITE'.center(80) + '\n\n')
                for protein in ResultDict.keys():
                    Process_log.write('Number of domains found in ' + protein + ': ' + str(len(ResultDict[protein])) + '\n')
                
                Process_log.close()
            
            # If no homologues are found for the query protein with the thresholds indicated.
            else:
                print ('BLAST analysis yielded no results'.center(80))
                Process_log = open (Results_Dir + 'Process.log',"a") ## The file is closed. We open in append mode.
                Process_log.write('\n\n\n' + ('Analysis ended because BLAST analysis yielded no results').center(80))

    # Accessory files are deleted.
    try:
        os.remove(HitsFile)
        os.remove('Blast_result.tsv')
        os.remove('HitsAligned.afa')
        os.remove('HitsAligned.aln')
        shutil.rmtree(Data_Dir + '/Queries')
    except:
        pass

    return basename # byebye function needs basename to indicate where the results have been saved.


# Welcome message.
def welcome():
    print ('\n' + ' WELCOME TO EASY PHYLO & DOM '.center(80,'*') + '\n')
    return


# Byebye message.
def byebye(basename):
    print('\n' + 'Thank you for using EASY PHYLO & DOM.'.center(80))
    print ('\n' + ('You can check your results at Results/' + str(basename)).center(80))
    print ('\n' + ('You will find a summary at Process.log file').center(80))
    print ('\n' + ('Data files have been saved in Data/' + str(basename)).center(80))
    print('\n' + 'We hope to have been helpful.\n'.center(80))
    print (' SEE YOU SOON '.center(80,'*') + '\n')
    return


welcome()
basename = main()
byebye(basename)