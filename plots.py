import csv

import matplotlib.pyplot as plt
import numpy as np



# This function plots the best hits, ordered by Blast evalues. It plots up to ten hits apart from the query.
# It needs the file with the BLAST results, the directory where it has to save the plot and the identity threshold. BLAST+ does not filter the identity.
def blast_plot(Blast_result_file, Results_Dir, identity):
    with open (Blast_result_file) as tsvfile:
        
        reader = csv.reader(tsvfile, delimiter='\t')
        fig, ax = plt.subplots()
        number_of_hit = 0
        qstart = []        # Where the hit starts to align with the query.
        qend = []          # Where the hit ends to align with the query
        hit_ids = []
        hit_identity = []
        same_id = 2        # Variable for repeated hit_ids
        Total_Hits = len(open(Blast_result_file).readlines(  )) # Each line of the file is a hit
        
        for hit in reader:
            if number_of_hit < 10 and number_of_hit < Total_Hits: # We plot all the hits up to ten hits
                if float(hit[3]) >= identity:  # We only plot those who meet the identity threshold.
                    qlen = float(hit[7])   # query length
                    
                    # We define the different colours to indicate the % of identity of the hits with the query
                    category_names = ['0-20 %', '21-40 %', '41-60 %', '61-80 %', '81-100 %']  # % of identity
                    Color_Bars = np.array([qlen/5,qlen/5,qlen/5,qlen/5,qlen/5])
                    Color_Bars_cum = Color_Bars.cumsum()
                    category_colors = plt.get_cmap('RdYlGn')(np.linspace(0.15, 0.85, 5))
                    ax.text(qlen/2, -0.7, s = 'Identity', ha='center', va='center')

                    # We plot the hits.
                    for i, (colname, color) in enumerate(zip(category_names, category_colors)):
                        # Variables to control the plot parameters
                        widths = Color_Bars[i]
                        starts = Color_Bars_cum[i] - widths
                        ax.barh("", widths, left=starts, height=1.0,
                                label=colname, color=color)
                        xcenters = starts + widths / 2

                        r, g, b, _ = color
                        text_color = 'white' if r * g * b < 0.5 else 'darkgrey'
                        ax.text(xcenters, 0, s = colname, ha='center', va='center',
                                    color=text_color)
                    
                    # We first plot the query
                    if number_of_hit == 0:
                        plt.hlines('query', 0.0, float(qlen), colors='b', label = 'query' )
                    
                    # We then plot the hits.                            
                    qstart.append(float(hit[5]))
                    qend.append(float(hit[6]))
                    if len(hit[1]) <= 7: # Maximum length that fits in the y axis.
                        hit_id = hit [1]
                    else:
                        hit_id = hit[1][0:6]                   
                    while hit_id in hit_ids: # For cases in which different hits have the same id. The second one will be .2, the third one .3, etc.
                        if hit_id + '.' + str(same_id) in hit_ids:
                            same_id += 1
                        else:
                            hit_ids.append(hit_id + '.' + str(same_id))
                            same_id = 2
                            break
                    else:
                        hit_ids.append(hit_id)
                        
                    hit_identity.append(float(hit[3]))
                    evalue = hit[4]

                    # Colour of the bar depends on the % of identity.                    
                    if number_of_hit >= 0 and number_of_hit < len(qstart):
                        ax.text((qstart[number_of_hit] + qend[number_of_hit])/2, number_of_hit + 1.7, s = 'E value: ' + evalue, ha='center', va='center', fontsize=6, wrap=True) # Label on top of each hit.
                        if hit_identity[number_of_hit] <= 20: 
                            plt.hlines(hit_ids[number_of_hit], qstart[number_of_hit], qend[number_of_hit], color='r')#, label = hit_id[number_of_hit] + ' Identity = ' + str(hit_identity[number_of_hit])
                        if hit_identity[number_of_hit] > 20 and hit_identity[number_of_hit] <= 40: 
                            plt.hlines(hit_ids[number_of_hit], qstart[number_of_hit], qend[number_of_hit], color='orange')#, label = hit_id[number_of_hit] + ' Identity = ' + str(hit_identity[number_of_hit])
                        if hit_identity[number_of_hit] > 40 and hit_identity[number_of_hit] <= 60: 
                            plt.hlines(hit_ids[number_of_hit], qstart[number_of_hit], qend[number_of_hit], color='yellow')#, label = hit_id[number_of_hit] + ' Identity = ' + str(hit_identity[number_of_hit])
                        if hit_identity[number_of_hit] > 60 and hit_identity[number_of_hit] <= 80: 
                            plt.hlines(hit_ids[number_of_hit], qstart[number_of_hit], qend[number_of_hit], color='lightgreen')#, label = hit_id[number_of_hit] + ' Identity = ' + str(hit_identity[number_of_hit])
                        if hit_identity[number_of_hit] > 80 and hit_identity[number_of_hit] <= 100: 
                            plt.hlines(hit_ids[number_of_hit], qstart[number_of_hit], qend[number_of_hit], color='g')#, label = hit_id[number_of_hit] + ' Identity = ' + str(hit_identity[number_of_hit])
            # Once there are no more hits or 10 hits have already been plotted.        
            else:
                break
            
            number_of_hit += 1
        # To maintain the dimensions if there are less than 10 hits.    
        for hits_left in range(number_of_hit,10):
            plt.hlines(hits_left, 0, 1, color='yellow', alpha = 0)
            number_of_hit +=1

        ax.invert_yaxis()
        ax.set_xlabel('Query length (bp)')
        ax.set_ylabel('Hits')
        ax.set_title('Query Coverage')
        plt.yticks(fontsize = "xx-small")
        ax.set_xlim(-(qlen*0.02), qlen*1.02) ## There is a space between the figure limits and the start and begining of the axes.
        plt.savefig(Results_Dir + 'Blast_Plot.png')
            
    return