#!/usr/bin/env python
import os, subprocess, sys
workingDir = os.getcwd()
import os, re, shlex
from ROOT import *
import numpy as np
import array as arr
from math import sqrt, sin, cos, tan, exp
import glob

import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt
from subprocess import Popen, PIPE
from io import open

from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
parser = ArgumentParser(
    description=__doc__, formatter_class=ArgumentDefaultsHelpFormatter
)
parser.add_argument(
    "--cards_folder",
    dest="cards_folder",
    help="Folder that contains the datacard.txt/root.",
    )
parser.add_argument(
    "--one_fitdiag_per_bin",
    action="store_true",
    dest="one_fitdiag_per_bin",
    help="Rename bins for each datacard.",
    default=False
    )
args = parser.parse_args()

mom_datacards = args.cards_folder
one_fitdiag_per_bin = args.one_fitdiag_per_bin

def runCombineCmd(combinecmd, outfolder='.', saveout=None):
    print ("Command: ", combinecmd)
    try:
        proc=subprocess.Popen(["cd %s ; %s" % (outfolder, combinecmd)],shell=True,stdout=subprocess.PIPE)
        out = proc.stdout.read()
    except OSError:
        print ("command not known\n", combinecmd)

list_SL_cards = [
    ["DY_boosted_2018", "datacard_hh_bb1l_LBN_DY_boosted_MVAOutput_SM_quantiles_2018_10bins_quantiles"],
    ["DY_resolved_2018", "datacard_hh_bb1l_LBN_DY_resolved_MVAOutput_SM_quantiles_2018_10bins_quantiles"],
    ["HH_boosted_2018", "datacard_hh_bb1l_LBN_HH_boosted_MVAOutput_SM_quantiles_2018_5bins_quantiles"],
    ["HH_resolved_1b_2018", "datacard_hh_bb1l_LBN_HH_resolved_1b_MVAOutput_SM_quantiles_2018_10bins_quantiles"],
    ["HH_resolved_2b_nonvbf_2018", "datacard_hh_bb1l_LBN_HH_resolved_2b_nonvbf_MVAOutput_SM_quantiles_2018_10bins_quantiles"],
    ["HH_resolved_2b_vbf_2018", "datacard_hh_bb1l_LBN_HH_resolved_2b_vbf_MVAOutput_SM_quantiles_2018_10bins_quantiles"],
    ["Other_2018", "datacard_hh_bb1l_LBN_Other_MVAOutput_SM_quantiles_2018_10bins_quantiles"],
    ["SingleTop_boosted_2018", "datacard_hh_bb1l_LBN_SingleTop_boosted_MVAOutput_SM_quantiles_2018_10bins_quantiles"],
    ["SingleTop_resolved_2018", "datacard_hh_bb1l_LBN_SingleTop_resolved_MVAOutput_SM_quantiles_2018_10bins_quantiles"],
    ["TT_boosted_2018", "datacard_hh_bb1l_LBN_TT_boosted_MVAOutput_SM_quantiles_2018_10bins_quantiles"],
    ["TT_resolved_2018", "datacard_hh_bb1l_LBN_TT_resolved_MVAOutput_SM_quantiles_2018_10bins_quantiles"],
    ["W_boosted_2018", "datacard_hh_bb1l_LBN_W_boosted_MVAOutput_SM_quantiles_2018_10bins_quantiles"],
    ["W_resolved_2018", "datacard_hh_bb1l_LBN_W_resolved_MVAOutput_SM_quantiles_2018_10bins_quantiles"],
]


card_all_eras = "combineCards.py "
for era in [2016, 2017, 2018] :
    card_this_era = "combineCards.py "
    for cards in list_SL_cards :

        bin_name = cards[0].replace(str(2018),str(era))
        card_name = cards[1].replace(str(2018),str(era))
        card_location = mom_datacards #.replace(str(2018),str(era))

        if one_fitdiag_per_bin :
            cmd = "combineCards.py "
            cmd += " %s=%s.txt" % (bin_name, card_name)
            cmd += ">  renamedBin_%s_SL.txt" % bin_name
            runCombineCmd(cmd, card_location)

        card_this_era += " %s=%s.txt" % (bin_name, card_name)
        card_all_eras += " %s=%s.txt" % (bin_name, card_name)

    card_this_era += ">  combo_%s_SL.txt" % str(era)
    runCombineCmd(card_this_era, card_location)
    print  ("%s/combo_%s_SL.txt" % (card_location, str(era)))

card_all_eras += ">  combo_all_eras_SL.txt"
runCombineCmd(card_all_eras, card_location)
print  ("%s/combo_all_eras_SL.txt" % (card_location))
