<p align="center">
  <img src="Images/cover.png">
</p>

Table of Contents
=================

* [Easy Phylo & Domain <a href='title'></a>](#title)
  * [Workflow of Easy Phylo & Domain <a href='workflow'></a>](#workflow)
  * [Requirements <a href='requirements'></a>](#requirements)
    * [Biopython <a href='biopython'></a>](#biopython)
    * [BLAST <a href='blast'></a>](#blast)
    * [MUSCLE <a href='muscle'></a>](#muscle)
  * [Input files <a href='input'></a>](#input)
  * [USAGE <a href='usage'></a>](#usage)
  * [Results <a href='results'></a>](#results)
    * [Download test data <a href='download'></a>](#download)
    * [BLAST analysis <a href='results-blast'></a>](#results-blast)
    * [MUSCLE alignment <a href='results-blast'></a>](#results-muscle)
    * [PROSITE domains <a href='results-blast'></a>](#results-prosite)
  * [Where to find help <a href='help'></a>](#help)
  * [Commercial use <a href='commercial-use'></a>](#commercial-use)
  * [Author <a href='author'></a>](#author)

<a id='title'></a>
# Easy Phylo & Domain

Easy Phylo & Domain is a python package  developed in python 3 for fast phylogenetic analysis and protein domain search. 

Its modules allow to perform a BLAST analysis, create a phylogenetic tree with the BLAST hits and search for protein domains in them.

The output of Easy Phylo & Domain includes easily interpretable plots as well as raw results from each analysis.

<a id='workflow'></a>
## Workflow of Easy Phylo & Domain 

Given a protein sequence (query), or several protein sequence (multiquery), this program allows you to:
    1. Search for homologue proteins (BLAST) in a Genbank.
    2. Align BLAST hits and query and create a Neighbor Joining phylogenetic tree with muscle.
    3. Look for PROSITE domains in your query and its homologues. You will  be asked whether you  want extended information about the domains or not.  

<a id='requirements'></a>
## **REQUIREMENTS** <a name="requirements"></a>
<a id='biopython'></a>
### **Biopython**

This programme uses biopython, so please make sure it is installed.

Should you need to install biopython, please see the link here: https://biopython.org/wiki/Download

<a id='blast'></a>
### **BLAST+**

Easy Phylo & Domain does local BLAST analysis for which it needs BLAST+ to be installed.

For download and instalation instructions, check:
https://www.ncbi.nlm.nih.gov/books/NBK52640/
<a id='muscle'></a>
### MUSCLE

Muscle is required for hits alignment. 

If not installed, please go to:
http://www.drive5.com/muscle/downloads.htm

<a id='input'></a>
## INPUT FILES 

* **Input file**: query

Query file must be a fasta or a multifasta. If your file is not in fasta format, please convert it before using Easy Phylo & Domain.

> NOTES: Easy Phylo & Domain checks if query file is in fasta format. If it is in a different format, this message will be displayed:

                                            query_file is not fasta.
                                    Please check the format of your query file.

* **Input file**: Genbank

Genbank file must be a genbank. If your file is not in fasta format, please convert it before using Easy Phylo & Domain.

> NOTES: Easy Phylo & Domain checks if Genbank file is in genbank format. If it is in a different format, this message will be displayed:

                                         genbank_file is not a Genbank.
                                   Please check the format of your Genbank file.

Upon completion of the run input files will be saved into a folder, named as the *query_file*, inside *Data* directory. A database with all the sequences in the Genbank will also be generated and saved in this folder.

* **PROSITE files**

For PROSITE domains search, both a *prosite.dat* and a *prosite.doc* files are required. Both are provided in this repository. Please, unzip *prosite.dat.zip* before using this programme. Should you want to use a more updated version of *prosite.doc*, you might have to edit with it a text editor as errors may arise.

<a id="usage"></a>
## USAGE 

To run Easy Phylo & Domain use the command:

                                      python main.py query_file genbank_file

For each protein sequence in the query you wil be asked BLAST identity and coverage thresholds as follows:
 
    Please, introduce the coverage threshold for the BLAST analysis for query_name:
    Please, introduce the identity threshold for the BLAST analysis for query_name:

You will have to enter a number between 0 and 100.    

After the search for PROSITE domains, you will be asked whether you  want extended information about the domains or not.

    Do you want to obtain more information about the domains detected in the hits?
    [Y|N]:
    
You need to answer either yes --> [y]  or no --> [n].

<a id="results"></a>
## RESULTS 

For each query in the *query_file*, a separate folder is created, inside *Results* directory, named as the *query_file* plus the coverage and identity thresholds for the BLAST analysis.

The following results are an example of the expected output running the programme with the test data:
  
                                python main.py Queries/query.fa Queries/genbank.gbff

The identity and coverage thresholds used to obtain the following results have been both 0.

<a id="download"></a>
### Download test data

https://github.com/KatsuyaKai/programming-project/tree/master/Queries
<a id="results-blast"></a>
### BLAST analysis

Blast analysis will yield:

    1. A blast_result.tsv file with the raw output.
    2. A plot for an easier and faster interpretation of the hits obtained. 
    * Only the top ten hits according to the evalue will be plotted.
<p align="center">
  <img src="Images/Blast_Plot.png">
</p>

<a id="results-muscle"></a>
### MUSCLE alignment

BLAST hits will be aligned with the query using Muscle. Muscle phylogenetic analysis will produce:

    1. The alignment file
    2. A phylogenetic tree in Newick format.
    3. A simple plot of the phylogenetic tree using the Phylo module from biopython.
<a id="results-prosite"></a>
### PROSITE domains

Upon completion of the search for PROSITE domains in query and hits sequences, the outputs will include:

    1. A file named prosite_results.txt with a summary of the main characteristics of the domains.
    2. If you have asked for more information, a file named Extended_Domain_Info.txt will be created.
    
<a id="help"></a>
## WHERE TO FIND HELP <a name="help"></a>

If you have bugs, feature requests, please report the issues here:

https://github.com/KatsuyaKai/programming-project/issues

<a id="commercial-use"></a>
## COMMERCIAL USE

Easy Phylo & Domain is free for use by academic users.

<a id="author"></a>
## AUTHOR

* Universidad Politécnica de Madrid (UPM)

Kai Katsuya Gaviria (kai.kgaviria@alumnos.upm.es).
