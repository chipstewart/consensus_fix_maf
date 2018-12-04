from argparse import ArgumentParser, RawDescriptionHelpFormatter
import sys, os
import numpy as np
import pandas as pd
from pandas import DataFrame

def parseOptions():
    epilog = """Merges oncotated maf with swissprot_ac_id to trimmed maf and sets blank f1r2 fields to -1"""
    desc = "fix rebc_consensus_maf ."
    parser = ArgumentParser(description=desc, formatter_class=RawDescriptionHelpFormatter, epilog=epilog)

    parser.add_argument("-C","--consensus_maf", type=str, help="Input consensus_maf")
    parser.add_argument("-O","--oncotated_maf", type=str, help="Input  oncotated maf")
    parser.add_argument("-i","--id", type=str, help="id stub prepended to output files.  <id>.merged.maflite.tsv")
    args = parser.parse_args()
    return args

def main():
    args = parseOptions()

    consensus_maf = args.consensus_maf
    oncotated_maf = args.oncotated_maf
    id = args.id

    df_consensus_maf = pd.read_csv(consensus_maf, sep="\t", index_col=None, low_memory=False)
    if 'UniProt_AApos' in df_consensus_maf:
        df_consensus_maf.drop('UniProt_AApos', axis=1, inplace=True)

    df_consensus_maf['Chromosome'] = df_consensus_maf['Chromosome'].astype(str)
    
    df_oncotated_maf = pd.read_csv(oncotated_maf, sep="\t", comment='#',index_col=None, low_memory=False)

    key_fields=['Chromosome', 'Start_position', 'End_position', 'Reference_Allele', 'Tumor_Seq_Allele2','SwissProt_acc_Id','UniProt_AApos']
    df_oncotated_maf_lite = pd.DataFrame(index=None, columns=key_fields)
    for f1 in key_fields:
        df_oncotated_maf_lite[f1]=df_oncotated_maf[f1]

    df_merge_maf = pd.merge(df_consensus_maf, df_oncotated_maf_lite,
                             on=['Chromosome', 'Start_position', 'End_position', 'Reference_Allele', 'Tumor_Seq_Allele2'], how='inner', sort=True,
                             suffixes=('', ''), indicator=False)

    df_merge_maf.loc[df_merge_maf['i_t_ALT_F1R2'].isnull(), 'i_t_ALT_F1R2'] = 0
    df_merge_maf.loc[df_merge_maf['i_t_ALT_F2R1'].isnull(), 'i_t_ALT_F2R1'] = 0
    df_merge_maf.loc[df_merge_maf['i_t_REF_F1R2'].isnull(), 'i_t_REF_F1R2'] = 0
    df_merge_maf.loc[df_merge_maf['i_t_REF_F2R1'].isnull(), 'i_t_REF_F2R1'] = 0

    output=os.path.abspath(id+".fix.maf")
    print(output)
    df_merge_maf.to_csv(output, sep="\t", index=None)

    return 0

if __name__ == "__main__":
    sys.exit(main())

