{
 "cells": [
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "Table of Contents\n",
    "=================\n",
    "\n",
    "* [Easy Phylo & Domain <a href='title'></a>](#title)\n",
    "  * [Workflow of Easy Phylo & Domain <a href='workflow'></a>](#workflow)\n",
    "  * [Requirements <a href='requirements'></a>](#requirements)\n",
    "    * [Biopython <a href='biopython'></a>](#biopython)\n",
    "    * [BLAST <a href='blast'></a>](#blast)\n",
    "    * [MUSCLE <a href='muscle'></a>](#muscle)\n",
    "  * [Input files <a href='input'></a>](#input)\n",
    "  * [USAGE <a href='usage'></a>](#usage)\n",
    "  * [Results <a href='results'></a>](#results)\n",
    "    * [Download test data <a href='download'></a>](#download)\n",
    "    * [BLAST analysis <a href='results-blast'></a>](#results-blast)\n",
    "    * [MUSCLE alignment <a href='results-blast'></a>](#results-muscle)\n",
    "    * [PROSITE domains <a href='results-blast'></a>](#results-prosite)\n",
    "  * [Where to find help <a href='help'></a>](#help)\n",
    "  * [Commercial use <a href='commercial-use'></a>](#commercial-use)\n",
    "  * [Author <a href='author'></a>](#author)\n",
    "\n",
    "<a id='title'></a>\n",
    "# Easy Phylo & Domain\n",
    "\n",
    "Easy Phylo & Domain is a python package for fast phylogenetic analysis and protein domain search. \n",
    "\n",
    "Its modules allow to perform a BLAST analysis, create a phylogenetic tree with the BLAST hits and search for protein domains in them.\n",
    "\n",
    "The output of Easy Phylo & Domain includes easily interpretable plots as well as raw results from each analysis.\n",
    "\n",
    "<a id='workflow'></a>\n",
    "## Workflow of Easy Phylo & Domain \n",
    "\n",
    "Given a protein sequence (query), or several protein sequence (multiquery), this program allows you to:\n",
    "    1. Search for homologue proteins (BLAST) in a Genbank.\n",
    "    2. Align BLAST hits and query and create a Neighbor Joining phylogenetic tree with muscle.\n",
    "    3. Look for PROSITE domains in your query and its homologues. You will  be asked whether you  want extended information about the domains or not.  \n",
    "\n",
    "<a id='requirements'></a>\n",
    "## **Requirements** <a name=\"requirements\"></a>\n",
    "<a id='biopython'></a>\n",
    "#### **Biopython**\n",
    "\n",
    "This program uses biopython, so please make sure it is installed.\n",
    "\n",
    "Should you need to install biopython, please see the link here: https://biopython.org/wiki/Download\n",
    "\n",
    "<a id='blast'></a>\n",
    "#### **BLAST+**\n",
    "\n",
    "Easy Phylo & Domain does local BLAST analysis for which it needs BLAST+ to be installed.\n",
    "\n",
    "For download and instalation instructions, check:\n",
    "https://www.ncbi.nlm.nih.gov/books/NBK52640/\n",
    "<a id='muscle'></a>\n",
    "#### MUSCLE\n",
    "\n",
    "Muscle is required for hits alignment. \n",
    "\n",
    "If not installed, please go to:\n",
    "http://www.drive5.com/muscle/downloads.htm\n",
    "\n",
    "<a id='input'></a>\n",
    "## Input files \n",
    "\n",
    "* **Input file**: query\n",
    "\n",
    "Query file must be a fasta or a multifasta. If your file is not in fasta format, please convert it before using Easy Phylo & Domain.\n",
    "\n",
    "> NOTES: Easy Phylo & Domain checks if query file is in fasta format. If it is in a different format, this message will be displayed:"
   ]
  },
  {
   "cell_type": "raw",
   "metadata": {},
   "source": [
    "\n",
    "                           *query_file* is not fasta.\n",
    "                   Please check the format of your query_file.\n"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "\n",
    "\n",
    "* **Input file**: Genbank\n",
    "\n",
    "Genbank file must be a genbank. If your file is not in fasta format, please convert it before using Easy Phylo & Domain.\n",
    "\n",
    "> NOTES: Easy Phylo & Domain checks if Genbank file is in genbank format. If it is in a different format, this message will be displayed:\n"
   ]
  },
  {
   "cell_type": "raw",
   "metadata": {},
   "source": [
    "\n",
    "                        *genbank_file* is not a Genbank.\n",
    "                   Please check the format of your Genbank_file.\n",
    "                   "
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "\n",
    "Upon completion of the run input files will be saved into a folder, named as the *query_file*, inside *Data* directory. A database with all the sequences in the Genbank will also be generated and saved in this folder.\n",
    "\n",
    "\n",
    "<a id=\"usage\"></a>\n",
    "## USAGE \n",
    "\n",
    "To run Easy Phylo & Domain use the command:"
   ]
  },
  {
   "cell_type": "raw",
   "metadata": {},
   "source": [
    "                            python main.py query_file Genbank_file"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "\n",
    "<a id=\"results\"></a>\n",
    "## Results \n",
    "\n",
    "For each query in the *query_file*, a separate folder is created, inside *Results* directory, named as the *query_file* plus the coverage and identity thresholds for the BLAST analysis.\n",
    "\n",
    "The following results are an example of the expected output.\n",
    "<a id=\"download\"></a>\n",
    "#### Download test data\n",
    "\n",
    "https://gitlab.com/BS-seq/ViewBS_testdata\n",
    "<a id=\"results-blast\"></a>\n",
    "#### BLAST analysis\n",
    "\n",
    "Blast analysis will yield:\n",
    "    1. A *.tsv* file with the raw output.\n",
    "    2. A plot for an easier and faster interpretation of the hits obtained. Only the top ten hits according to the *evalue* will be plotted.\n",
    "<a id=\"results-muscle\"></a>\n",
    "#### MUSCLE alignment\n",
    "\n",
    "BLAST hits will be aligned with the query using Muscle. Muscle phylogenetic analysis will produce:\n",
    "    1. A phylogenetic tree in Newick format.\n",
    "    2. A simple plot of the phylogenetic tree using the Phylo module from biopython.\n",
    "<a id=\"results-prosite\"></a>\n",
    "#### PROSITE domains\n",
    "\n",
    "Upon completion of the search for PROSITE domains in query and hits sequences, the outputs will include:\n",
    "    1. A file named *prosite_results.txt* with a summary of the main characteristics of the domains.\n",
    "    2. If you have asked for more information, a file named *Extended_Domain_Info.txt* will be created.\n",
    "    \n",
    "<a id=\"help\"></a>\n",
    "## Where to find help <a name=\"help\"></a>\n",
    "\n",
    "If you have bugs, feature requests, please report the issues here: (https://github.com/readbio/ViewBS/issues).\n",
    "\n",
    "<a id=\"commercial-use\"></a>\n",
    "## Commercial use\n",
    "\n",
    "Easy Phylo & Domain is free for use by academic users.\n",
    "\n",
    "<a id=\"author\"></a>\n",
    "## Author\n",
    "\n",
    "* Universidad Politécnica de Madrid (UPM)\n",
    "\n",
    "Kai Katsuya Gaviria (kai.kgaviria@alumnos.upm.es).\n",
    "\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": []
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.7.2"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 2
}
