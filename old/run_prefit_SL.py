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
# ./rebin_datacards.py --channel "4l_0tau"  --BINtype "regular" --doLimits
from io import open

mom_datacards = "/home/acaan/bbww_cards_feezinJan2021/2016/datacards_rebined/"
FolderOut = "/home/acaan/bbww_cards_feezinJan2021/2016/"

def runCombineCmd(combinecmd, outfolder='.', saveout=None):
    print ("Command: ", combinecmd)
    try:
        p = Popen(shlex.split(combinecmd) , stdout=PIPE, stderr=PIPE, cwd=outfolder)
        comboutput = p.communicate()[0]
    except OSError:
        print ("command not known\n", combinecmd)
        comboutput = None
    if not saveout == None :
        if saveout.startswith("/") : saveTo = saveout
        else : saveTo = outfolder + "/" + saveout
        with open(saveTo, "w") as text_file:
            text_file.write(unicode(comboutput))
        print ("Saved result to: " + saveTo)
    print ("\n")
    return comboutput

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

if cards in list_SL_cards :
    # make only HH be considered signal (independent of the card marking)
    FolderOut = "%s/fitdiag/" % mom_datacards
    proc=subprocess.Popen(["mkdir %s" % FolderOut],shell=True,stdout=subprocess.PIPE)
    out = proc.stdout.read()

    cmd = "combineCards.py "
    cmd += "%s=%s" % (cards[0]=cards[1])
    cmd += ">  renamedBin_%s_SL.txt" % cards[0]
    print(cmd)
    #runCombineCmd(cmd, mom_datacards)


    cmd = "text2workspace.py"
    cmd += " renamedBin_%s_SL.txt" % cards[0]
    cmd += " -o %s/%s_WS.root" % (FolderOut, fileCardOnlynBinL)
    print(cmd)
    #runCombineCmd(cmd, mom_datacards)
    #print ("done %s/%s_WS.root" % (FolderOut, fileCardOnlynBinL))

    cmd = "combineTool.py -M FitDiagnostics "
    cmd += " %s_WS.root" % fileCardOnlynBinL
    #if blinded :
    #    cmd += " -t -1 "
    cmd += " --saveShapes --saveWithUncertainties "
    cmd += " --saveNormalization "
    cmd += " --skipBOnlyFit "
    cmd += " -n _shapes_combine_%s" % fileCardOnlynBinL
    #runCombineCmd(cmd, FolderOut)
    #fileShapes = glob.glob("%s/fitDiagnostics_shapes_combine_%s*root" % (FolderOut, fileCardOnlynBinL))[0]
    #print ( "done %s" % fileShapes )
    print(cmd)

    savePlotsOn = "%s/plots/" % (mom_datacards)
    cmd = "mkdir %s" % savePlotsOn
    #runCombineCmd(cmd)
