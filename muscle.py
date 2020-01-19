import sys
from subprocess import Popen, PIPE
from Bio.Align.Applications import MuscleCommandline
from Bio import AlignIO, Phylo
#import networkx, pylab

def main():
    HitsFile=sys.argv[1]
    Align_Seqs(HitsFile)
    Tree = CreateTree('HitsAligned.afa','')
    DrawTree('NJ_Tree.phy')

def Align_Seqs(HitsFile):
    print ('\n' + ('Aligning hit sequences with Muscle...').center(80))
    muscle_cline = MuscleCommandline(input=HitsFile)
    #child = Popen(str(muscle_cline), stdout=PIPE, stderr=PIPE, universal_newlines=True, shell=(sys.platform!='win32'))
    cmdline = MuscleCommandline(input = HitsFile, out = 'HitsAligned.aln', clw = True)
    cmdline()
    AlignIO.convert("HitsAligned.aln", 'clustal', 'HitsAligned.afa', 'fasta')
    #align = AlignIO.read(child.stdout, 'fasta')
    #Alignment = child.stdout.read()
    #Hits_Aligned = open ('HitsAligned.afa', 'w')
    #Hits_Aligned.write(str(Alignment))
    #Tree_process = 'muscle -maketree -in -HitsAligned.afa -out -NJ.phy -cluster neighborjoining'
    #Tree = Popen(['muscle','-maketree', '-in', 'HitsAligned.afa', '-out', 'Results/NJ.phy', '-cluster', 'neighborjoining'], stderr=PIPE)
    #Tree_error = Tree.stderr.read()
    #print (Tree_error)
    #print(align)

def CreateTree(AlignedHitsFile, Results_Dir = '', Results_Muscle = ''):
    print ('\n' + ('Creating Neighbor Joining Tree...').center(80))
    try:
        Tree = Popen(['muscle','-maketree', '-in', AlignedHitsFile, '-cluster', 'neighborjoining'], stdout=PIPE, stderr=PIPE)
        
        Tree_File = open(Results_Muscle + 'NJ_Tree.phy',"w")
        Tree_File.write('\n' + ' Neighbor Joining Tree in Newick format '.center(80,'-') + '\n\n')
        contents = Tree.stdout.read().decode('utf-8')
        newcontents = contents.replace('\n','')
        Tree_File.write(newcontents)

        error_Tree = Tree.stderr.read()
        Muscle_log = open (Results_Dir + 'Process.log',"a")
        if error_Tree:
            Muscle_log.write ('\n\n\n' + ("Creating Neighbor Joining Tree using Muscle...").center(80) + '\n')
            Muscle_log.write (error_Tree.decode('utf-8'))
            Muscle_log.write ('\n' + ("Neighbor Joining Tree successfully created").center(80) + '\n')
            Muscle_log.write (('Check Muscle results at: ' + Results_Dir + 'Muscle').center(80))
    except:
        print('Errors encountered while trying to perform alignment with MUSCLE. Please, check if MUSCLE is correctly installed.')


    return


def DrawTree(NewickFile, Results_Dir = ''):
    tree = Phylo.read(NewickFile, 'newick')
    tree.rooted = True
    tree.ladderize()
    '''import networkx
    import matplotlib.pyplot as plt
    tree = Phylo.read(NewickFile, 'newick')
    net = Phylo.to_networkx(tree)
    networkx.draw(net)
    plt.show()'''

    #tree = Phylo.read('example.xml', 'phyloxml')
    #net = Phylo.to_networkx(tree)
    #networkx.draw(net)
    #pylab.show()

    
    TreeFile = open(Results_Dir + "Tree.txt","w")
    TreeFile.write('\n' + ' Simple plot of Neighbor Joining Tree '.center(80,'-') + '\n\n')
    Phylo.draw_ascii(tree,file = TreeFile)
    #Phylo.draw(tree, branch_labels=lambda c: c.branch_length)
    #print (Arbol)
    #Phylo.draw_graphviz(tree)#, label_func = lambda, prog = 'neato')
    return #Arbol

if __name__ == "__main__":
    main()
    
    