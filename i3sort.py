# https://github.com/ShadenSmith/csvsorter
# from csvsorter import csvsort

# csvsort('HXProcessedData/HBYC_Line2_Kiln_2021_Jan_12_28.csv', [30])

import csv
with open('HXProcessedData/HBYC_Line2_Kiln_2021_Jan_12_28.csv', newline='') as csvfile:
	rdr = csv.reader(csvfile)
	l = sorted(rdr, key=lambda x: x[29], reverse=True)
	with open('HXProcessedData/HBYC_Line2_Kiln_2021_Jan_12_28sorted.csv', 'w') as csvout:
	    wrtr = csv.writer(csvout)
	    wrtr.writerows(l)