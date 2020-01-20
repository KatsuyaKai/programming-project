import sys
from subprocess import Popen, PIPE

from Bio.Align.Applications import MuscleCommandline
from Bio import AlignIO, Phylo


def main():
    HitsFile=sys.argv[1]
    align_seqs(HitsFile)
    Tree = create_tree('HitsAligned.afa','')
    draw_tree('NJ_Tree.phy')


# We use MUSCLE to align a set of sequences. We save the output to a temporary file HitsAligned.afa.
def align_seqs(HitsFile):
    print ('\n' + ('Aligning hit sequences with Muscle...').center(80))
    try:
        muscle_cline = MuscleCommandline(input=HitsFile)
        cmdline = MuscleCommandline(input=HitsFile, out='HitsAligned.aln', clw=True)
        cmdline()
        AlignIO.convert("HitsAligned.aln", 'clustal', 'HitsAligned.afa', 'fasta')
    # Issues arised while using MUSCLE. Is it installed?
    except:
        print('Errors encountered while trying to perform alignment with MUSCLE. Please, check if MUSCLE is correctly installed.')


# With the alignment file, we create a Tree in Newick format.
def create_tree(AlignedHitsFile, Results_Dir='', Results_Muscle=''):
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
    # Issues arised while using MUSCLE. Is it installed?
    except:
        print('Errors encountered while trying to perform alignment with MUSCLE. Please, check if MUSCLE is correctly installed.')

    return


# Easy plot of Neighbor Joining tree.
def draw_tree(NewickFile, Results_Dir=''):
    tree = Phylo.read(NewickFile, 'newick')
    tree.rooted = True
    tree.ladderize()   
    TreeFile = open(Results_Dir + "Tree.txt","w")
    TreeFile.write('\n' + ' Simple plot of Neighbor Joining Tree '.center(80,'-') + '\n\n')
    Phylo.draw_ascii(tree,file = TreeFile)

    return 


if __name__ == "__main__":
    main()
    
    