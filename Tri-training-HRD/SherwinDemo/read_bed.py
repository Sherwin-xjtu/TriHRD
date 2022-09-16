
bed_list = []
ss = []
se = []
chr = 'chr1'
count = 0
for line in open("chipbed1.csv"):
    li = line.split(',')
    se.append(int(li[1]))
    se.append(int(li[2].strip('\n')))
    if chr == li[0]:
        bed_list.append(se)
    else:
        chr = li[0]
        ss.append(bed_list)
        bed_list = []
        bed_list.append(se)
    se = []
    count +=1
    if count ==2151:
        ss.append(bed_list)
print ss