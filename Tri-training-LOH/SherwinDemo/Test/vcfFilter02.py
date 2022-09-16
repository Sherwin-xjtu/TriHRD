import sys
import re
import argparse
import vcf

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
        else:
            return False

def checkGenoNormalFail(record, feat, value, smaller):
    FEAT = record.samples[1][feat]
    if smaller == True:
      if float(FEAT) < value:
          return True
      else:
          return False
    else:
      if float(FEAT) > value:
          return True
      else:
          return False

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

def checkFeatureFailList(record, feat, value, smaller):
    FEAT = record.INFO[feat]
    fail_n = 0 
    for v in FEAT:
        if v == "." or v is None:
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
    else:
        if smaller == True:
            if float(FEAT) < value:
                return True
            else:
                return False
        else:
            if float(FEAT) > value:
                return True
            else:
                return False

# def compvcf(nlt,mlt,vcf_writer1,vcf_writer2,vcf_writer3,n,n1):
#     li = []
#     lt = []
#     j = 0
#     sensitivity = 0
#     specificity = 0
#     for record1 in nlt:
#         for record in mlt:
#             if record.pos == record1.POS and record.chrom == record1.CHROM and record.ref == record1.REF:
#                 for ra in record1.ALT:
#                     ra = ra.sequence
#                     if ra in record.alts:
#                         record1.add_info('MAF',record.samples[0]['AF'])
#                         lt.append(record1)
#                         j += 1
#                         li.append(record)
#                         break
#     for rec1 in mlt:
#         if rec1 not in li:
#             vcf_writer1.write(rec1)
#     for rec2 in nlt:
#         if rec2 not in lt:
#             vcf_writer2.write_record(rec2)
#     for rec3 in lt:
#         vcf_writer3.write_record(rec3)
#         sensitivity = j/n
#         specificity = j/n1
#     print ('platypus: %s ,mutect2: %s, sensitivity: %s'%(j, n, sensitivity))

def compvcf(record1,mlt):
    lt = []
    j = 0
    sensitivity = 0
    specificity = 0
    # for record1 in nlt:
    for record in mlt:
        if record.pos == record1.POS and record.chrom == record1.CHROM and record.ref == record1.REF:
            for ra in record1.ALT:
                ra = ra.sequence
                if ra in record.alts:
                    record1.add_info('MAF',record.samples[0]['AF'])
                    record1.add_info('type', 1)
                    lt.append(record1)
                    j += 1
                    return record1
                    # li.append(record)
                    # break

if __name__ == "__main__":
    vcfFile = sys.argv[1]
    m_vcf = sys.argv[2]
    outFile = sys.argv[3]
    outFileType = sys.argv[4]
    vcf_reader = vcf.Reader(open(vcfFile, 'rb'))
    mreader = pysam.VariantFile(m_vcf, 'rb')
    vcf_writer = vcf.Writer(open(outFile, 'w'), vcf_reader)
    vcf_writerTp = vcf.Writer(open(outFileType, 'w'), vcf_reader)
    n = 0
    mlt = []
    for rec in mreader.fetch():
        if rec.samples[0]['AF'][0] > 0.02 and rec.samples[1]['AD'][1] == 0 and rec.samples[0]['AD'][1] > 4:
            for alt in rec.alts:
                if abs(len(rec.ref) - len(alt)) < 10:
                    mlt.append(rec)
    for record in vcf_reader:
        tm = compvcf(record, mlt)
        if tm is not None:
            vcf_writerTp.write_record(tm)
        for alts in record.ALT:
            alt = alts.sequence
            # remove indel with too much length
            if abs(len(record.REF)-len(alt)) > 11:
                continue
            if checkFeatureFail(record, "MMLQ", 25, True):
                continue
            if checkFeatureFailList(record, "MQ", 30, True):
                continue
            if checkFeatureFailList(record, "VAFC", 0.02, True):
                continue
            if checkFeatureFailList(record, "FET", 5, True):
                continue
            if checkFeatureFailList(record, "SCS", 0.86, False):
                continue
            if checkFeatureFail(record, "HP", 4, False):
                continue
            # Platypus only
            if 'Platypus' in record.INFO['Source']:
                if checkGenoFail(record, 'ONV', 5, True):
                    continue
                if checkGenoFail(record, 'NV', 5, True):
                    continue
                if checkGenoNormalFail(record, 'ONV', 0, False):
                    continue
                if checkFeatureFailList(record, "MPOS", 5, True):
                    continue
                if checkFeatureFailList(record, "FS", 30, False):
                    continue
                if "Assembler" not in record.INFO['Source'] and  checkFeatureFailList(record, "BaseQRankSum", 1e-5, True):
                    continue
                if checkFeatureFailList(record, "MQRankSum", 1e-3, True):
                    continue
                if checkFeatureFailList(record, "ReadPosRankSum", 1e-3, True):
                    continue
            n = n+1
            tm1 = compvcf(record, mlt)
            if tm is not None:
                record = tm
            vcf_writer.write_record(record)
    vcf_writer.close()
    print n

