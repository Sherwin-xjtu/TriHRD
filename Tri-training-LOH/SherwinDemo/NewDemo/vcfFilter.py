import sys
import re
import argparse
import vcf

# def checkGenoFail(buff, featIndex, value, smaller):
#     c = buff.split()
#     d = c[len(c) -2].split(":")
#     arr = d[featIndex].split(",")
#     fail_n = 0
#     for v in arr:
#       if smaller == True:
#           if float(v) < value:
#               fail_n += 1
#     if fail_n == len(arr):
#        return True
#     else:
#        return False
def checkGenoFailList(record, feat, value, smaller):
    FEAT = record.samples[0][feat]
    fail_n = 0
    for v in FEAT:
      if smaller == True:
          if float(v) < value:
              fail_n += 1
    if fail_n == len(FEAT):
       return True
    else:
       return False
def checkGenoFail(record, feat, value, smaller):
    FEAT = record.samples[0][feat]
    if smaller == True:
        if float(FEAT) < value:
            return True

def checkGenoNormalFail(record, feat, value, smaller):
    FEAT = record.samples[1][feat]
    if smaller == True:
      if float(FEAT) < value:
          return True
    else:
      if float(FEAT) > value:
          return True

def checkGenoNormalFailList(record, feat, value, smaller):
    FEAT = record.samples[1][feat]
    fail_n = 0
    for v in FEAT:
      if smaller == True:
          if float(v) < value:
              fail_n += 1
      else:
          if float(v) > value:
              fail_n += 1
    if fail_n == len(FEAT):
       return True
    else:
       return False


# def checkGenoNormalFail(buff, featIndex, value, smaller):
#     c = buff.split()
#     d = c[len(c) -1].split(":")
#     arr = d[featIndex].split(",")
#     fail_n = 0
#     for v in arr:
#       if smaller == True:
#           if float(v) < value:
#               fail_n += 1
#       else:
#           if float(v) > value:
#               fail_n += 1
#
#     if fail_n == len(arr):
#        return True
#     else:
#        return False

# def checkFeatureFail(buff,feat, value, smaller):
#    m = re.search(feat + "=([^;]+)", buff)
#    if m:
#        featStr = m.group(1)
#        if featStr == ".":
#            return False
#            #print ("[ERROR]\t" +  buff)
#            #sys.exit(1)
#    arr = featStr.split(",")
#    fail_n = 0
#    for v in arr:
#       if v == ".":
#           continue
#       if smaller == True:
#           if float(v) < value:
#               fail_n += 1
#       else:
#           if float(v) > value:
#               fail_n += 1
#
#    if fail_n == len(arr):
#        return True
#    else:
#        return False

def checkFeatureFailList(record, feat, value, smaller):
    FEAT = record.INFO[feat]
    fail_n = 0
    for v in FEAT:
        if v == ".":
            continue
        if smaller == True:
            if float(v) < value:
                fail_n += 1
        else:
            if float(v) > value:
                fail_n += 1
    if fail_n == len(FEAT):
        return True
    else:
        return False

def checkFeatureFail(record, feat, value, smaller):
    FEAT = record.INFO[feat]
    if FEAT == ".":
        return False
    if smaller == True:
        if float(FEAT) < value:
            return True
    else:
        if float(FEAT) > value:
            return True

if __name__ == "__main__":
    vcfFile = sys.argv[1]
    outFile = sys.argv[2]
    IN = open(vcfFile)
    vcf_reader = vcf.Reader(open(vcfFile, 'rb'))
    vcf_writer = vcf.Writer(open(outFile, 'w'), vcf_reader)
    # for buff in IN:
    for record in vcf_reader:
        for alts in record.ALT:
            alt = alts.sequence
            # remove indel with too much length
            if abs(len(record.REF)-len(alt)) > 11:
                continue
            if checkFeatureFail(record, "MMLQ", 25, True):
                continue
            if checkFeatureFail(record, "MQ", 30, True):
                continue
            if checkFeatureFail(record, "VAFC", 0.02, True):
                continue
            if checkFeatureFail(record, "FET", 5, True):
                continue
            if checkFeatureFail(record, "SCS", 0.80, False):
                continue
            if checkFeatureFail(record, "HP", 4, False):
                continue
            # Platypus only
            if record.INFO['Source'] == 'Platypus':
                if checkGenoFail(record, 'ONV', 5, True):
                    continue
                if checkGenoFail(record, 'NV', 5, True):
                    continue
                if checkGenoNormalFail(record, 'ONV', 0, False):
                    continue
                if checkFeatureFail(record, "MPOS", 5, True):
                # will skip  21      42866960
                    continue
                if checkFeatureFail(record, "FS", 30, False):
                # will skip  21      42866960
                    continue
                if record.INFO['Source'] != "Assembler" and checkFeatureFail(record, "BaseQRankSum", 1e-5, True):
                    continue
                if checkFeatureFail(record, "MQRankSum", 1e-3, True):
                    continue
                if checkFeatureFail(record, "ReadPosRankSum", 1e-3, True):
                    continue
        # # buff = buff.rstrip()
        # if buff[0] != '#':
        #     c = buff.split()
        #     # remove indel with too much length
        #     if abs(len(c[3]) - len(c[4])) > 11:
        #         continue
        #     if checkFeatureFail(buff, "MMLQ", 25, True):
        #         continue
        #     if checkFeatureFail(buff, "MQ", 30, True):
        #         continue
        #     if checkFeatureFail(buff, "VAFC", 0.02, True):
        #         continue
        #     if checkFeatureFail(buff, "FET", 5, True):
        #         continue
        #     if checkFeatureFail(buff, "SCS", 0.80, False):
        #         continue
        #     if checkFeatureFail(buff, "HP", 4, False):
        #         continue
        #     # Platypus only
        #     if re.search("Platypus", buff):
        #     #if not re.search("Assembler", buff):
        #         if checkGenoFail(buff, 6, 5, True):
        #             continue
        #         if checkGenoFail(buff, 5, 5, True):
        #             continue
        #         if checkGenoNormalFail(buff, 6, 0, False):
        #             continue
        #
        #         if checkFeatureFail(buff, "MPOS", 5, True):
        #         # will skip  21      42866960
        #             continue
        #         if checkFeatureFail(buff, "FS", 30, False):
        #         # will skip  21      42866960
        #             continue
        #         if not re.search("Assembler", buff) and  checkFeatureFail(buff, "BaseQRankSum", 1e-5, True):
        #             continue
        #         if checkFeatureFail(buff, "MQRankSum", 1e-3, True):
        #             continue
        #         if checkFeatureFail(buff, "ReadPosRankSum", 1e-3, True):
        #             continue
        #     print (buff)
            vcf_writer.write_record(record)
    vcf_writer.close()


