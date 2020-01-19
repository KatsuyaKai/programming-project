import sys, os, shutil
import gbk, blaster, fasta, muscle, prosite, help, plots
from matplotlib import pyplot as plt

def main():
    ## Help module controls that query and genbank are correctly provided.
    query,Genbank = help.main()

    basename = os.path.basename(query)

    ## Results and Data directory are created if they do not exist. 
    ## Within them a directory with the name of the query is created.
    ## All the files will be saved to these directories.
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


    if fasta.is_it_fasta(query,basename):
        pass
    else:
        print ("\n" + (query + ' is not fasta.').center(80))
        print ('Please check the format of your query_file.'.center(80) + "\n")
        os.rmdir('Results/' + str(basename)) ## We delete this empty directory.
        shutil.rmtree('Data/' + str(basename)) ## We delete this directory which is not empty.
        sys.exit()

    if gbk.is_it_genbank(Genbank,basename):
        pass
    else:
        print ("\n" + (Genbank + ' is not a Genbank.').center(80))
        print ('Please check the format of your Genbank_file.'.center(80) + "\n")
        os.rmdir('Results/' + str(basename))
        shutil.rmtree('Data/' + str(basename))
        sys.exit()

    #gbk.Gbk_To_Fasta(Genbank, basename)

    Data_Dir = 'Data/' + str(basename)

    subject = Data_Dir + '/gbk_fasta.fa'

    

    ## Query and Genbank  files and their metadata are copied to Data directory.
    shutil.copy2(query, Data_Dir)
    shutil.copy2(Genbank, Data_Dir)
    
    ## Blast identity and coverage thresholds are asked
    # coverage, identity = blaster.Coverage_Identity()

    with os.scandir(Data_Dir + '/Queries') as it:
        for query_file in it:

            coverage, identity = blaster.Coverage_Identity(query_file.name)
        
            new_query = Data_Dir + '/Queries/' + query_file.name
            ## We define the directories for the results 
            Results_Dir = 'Results/' + str(basename) + '/' + query_file.name + '_Cov_' + str(coverage) + '_Id_' + str(identity) + '/' 
            Results_Blast = Results_Dir + 'Blast/'
            Results_Prosite = Results_Dir + 'Prosite/'
            Results_Muscle = Results_Dir + 'Muscle/'
            ## If they do not exist, we create them
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
            Process_log.close()

            blaster.Blaster(new_query, subject,coverage, identity, basename, results_dir = Results_Dir)
            
            ## If at least one homologue is found for the criteria indicated. The first row of the file is the header.
            if len(open(Results_Blast + 'Blast_result.tsv').readlines()) > 1:
                plots.Blast_plot('Blast_result.tsv', Results_Blast, identity)

                Hits = blaster.BlasterHits('Blast_result.tsv')

                fasta.SeqFromID(subject, Hits)

                ## We add the queries to the hits to have all the proteins together for the subsequent analyses.
                # fasta.AddQueries("HitsFile.txt", 'Data/' + str(basename) + '/Query_In_Fasta.fa') 
                fasta.AddQueries("HitsFile.txt", new_query) 

                HitsFile = "HitsFile.txt"
                
                muscle.Align_Seqs(HitsFile)

                AlignedHitsFile = 'HitsAligned.afa'

                muscle.CreateTree(AlignedHitsFile, Results_Dir = Results_Dir, Results_Muscle = Results_Muscle)

                
                #Tree = muscle.CreateTree(HitsFile)

                Tree = muscle.DrawTree(Results_Muscle + 'NJ_Tree.phy', Results_Dir = Results_Muscle)
    
                #Tree.savefig('Results/Tree.png')
                
                Process_log = open (Results_Dir + 'Process.log',"a") ## The file is closed. We open in append mode.
                Process_log.write('\n\n\n' + ('Domain search in Prosite').center(80))
                prosite_dat = 'prosite.dat'
                try:
                    Process_log.write('\n\n' + ('Parsing ' + prosite_dat + '...').center(80))
                    PatternDict = prosite.DatParser(prosite_dat)
                except:
                    Process_log.write()
                    Process_log.write('\n\n' + ('Errors encountered while parsing ' + prosite_dat).center(80))
                    print ('Errors encountered while parsing ' + prosite_dat)
                    sys.exit()

                Process_log.write('\n\n' + ('Looking for domains in hits...').center(80))
                HitsDict = prosite.HitsFileToDict(HitsFile)

                ResultDict = prosite.PatternSearch(PatternDict,HitsDict)

                prosite.OutputResults (prosite_dat, ResultDict, Results_Prosite)

                ## More information about the domains?
                prosite.WantMoreInfo("prosite.txt", ResultDict, Results_Prosite)
                
                ## Printing information in Process.log file
                Process_log.write('\n\n' + ('Domain search completed').center(80) + '\n')
                Process_log.write (('Check Prosite results at: ' + Results_Prosite).center(80))

                Process_log.write('\n\n\n' + ('Analysis completed').center(80) + '\n\n\n')
                Process_log.close()

            else:
                print ('BLAST analysis yielded no results'.center(80))
                Process_log = open (Results_Dir + 'Process.log',"a") ## The file is closed. We open in append mode.
                Process_log.write('\n\n\n' + ('Analysis ended because BLAST analysis yielded no results').center(80))

    ## Accessory files are deleted.
    try:
        os.remove(HitsFile)
        #os.remove('Blast_result.tsv')
        os.remove('HitsAligned.afa')
        os.remove('HitsAligned.aln')
        shutil.rmtree(Data_Dir + '/Queries')
    except:
        pass


    #Hits_File = open("HitsFile.txt","a")
    #with open (query) as reader:
    #   for line in reader:
    #      print("hola")
    #     Hits_File.write(line)'''

    return basename

def Welcome():
    # Se ejecuta cuando el usuario inicia.
    print ('\n' + ' WELCOME TO EASY PHYLO & DOM '.center(80,'*') + '\n')
    #print ('Este asistente le permitirá interactuar de manera fácil e intuitiva con la base de datos DisGeNET.'.center(100))
    #print ('Navegue por los distintos menús, que le guiarán por las diferentes opciones que le ofrecemos.'.center(100))
    #print ('Puede consultar información de distinta índole y borrar, insertar y modificar datos.'.center(100))
    
    return

def ByeBye(basename):
    # Se ejecuta cuando el usuario no quiere hacer más operaciones.
    print ()
    print('Thank you for using EASY PHYLO & DOM.'.center(80))
    print ()
    print (('You can check your results at Results/' + str(basename)).center(80))
    print (('Data files have been saved in Data/' + str(basename)).center(80))
    print ()
    print('We hope to have been helpful.\n'.center(80))
    print (' SEE YOU SOON '.center(80,'*'))
    print ()
     
    return


Welcome()
basename = main()
ByeBye(basename)