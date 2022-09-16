import sys

def judge_single_alt(chrom, pos, ref, alt):
    if len(ref) == 1 and len(alt) == 1:
        tag = "snv"
        start = int(pos) - 1
        end = int(pos)
        rref = ref
        ralt = alt
    elif len(ref) > 1 and len(alt) == 1:
        tag = "del"
        start = int(pos)
        end = int(pos) + len(ref) - 1
        rref = ref[1:]
        ralt = "."
    elif len(ref) == 1 and len(alt) > 1:
        tag = "ins"
        start = int(pos)
        end = int(pos)
        rref = "."
        ralt = alt[1:]
    elif len(ref) > 1 and len(alt) > 1:
        tag = "delins"
        start = int(pos) - 1
        end = int(pos) + 1
        rref = ref
        ralt = alt
    else:
        tag = "none"
        start = "none"
        end = "none"
        rref = "none"
        ralt = "none"
    return start, end, rref, ralt, tag

def judge_multi_alt(chrom, pos, ref, alt):
    multi_list = []
    alt_list = alt.split(",")
    for palt in alt_list:
        pstart, pend, prref, pralt, ptag = judge_single_alt(chrom, pos, ref, palt)
        multi_list.append("{}\t{}\t{}\t{}\t{}\t{}\n".format(chrom,pstart,pend,prref,pralt,ptag))
    return multi_list

#result_list.append("{}\t{}\t{}\t{}\t{}\t{}\n".format(chrom,start,end,rref,ralt,tag))

result_file = open(sys.argv[1], "a")
with open ("raw.vcf", "r") as fh:
    for line in fh:
        chrom, pos, id_tag, ref, alt, qual, filter_tag, info_tag, format_info, sample = line.strip().split("\t")
        if "," not in alt:
            start, end, rref, ralt, tag = judge_single_alt(chrom, pos, ref, alt)
            result_file.write("{}\t{}\t{}\t{}\t{}\t{}\n".format(chrom,start,end,rref,ralt,tag))
        else:
            multi_list = judge_multi_alt(chrom, pos, ref, alt)
            for pline in multi_list:
                result_file.write(pline)

result_file.close()