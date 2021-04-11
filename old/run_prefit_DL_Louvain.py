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

mom_datacards = "/afs/cern.ch/work/a/acarvalh/public/to_HH_bbWW/datacards_louvain_Jan2020/dataset_fit_TTHIDLoose_DNN10_2018_syst/merging/datacards/"
FolderOut = "/afs/cern.ch/work/a/acarvalh/public/to_HH_bbWW/datacards_louvain_Jan2020/dataset_fit_TTHIDLoose_DNN10_2018_syst/merging/datacards/fitdiag/"

def runCombineCmd(combinecmd, outfolder='.', saveout=None):
    print ("Command: ", combinecmd)
    try:
        proc=subprocess.Popen(["cd %s ; %s" % (outfolder, combinecmd)],shell=True,stdout=subprocess.PIPE)
        out = proc.stdout.read()
    except OSError:
        print ("command not known\n", combinecmd)

list_DL_cards = [

    ["DY_VVVnode_2018",          "datacard_HH_cat_DNN10_DY_VVVnode_2018_10_bins_quantiles"],
    ["TT_ST_TTVX_Rarenode_2018", "datacard_HH_cat_DNN10_TT_ST_TTVX_Rarenode_2018_10_bins_quantiles"],
    ["boosted1b_GGFnode_2018",   "datacard_HH_cat_boosted1b_DNN10_GGFnode_2018_2_bins_quantiles"],
    ["boosted1b_Hnode_2018",     "datacard_HH_cat_boosted1b_DNN10_Hnode_2018_5_bins_quantiles"],
    ["boosted1b_VBFnode_2018",   "datacard_HH_cat_boosted1b_DNN10_VBFnode_2018_2_bins_quantiles"],
    ["resolved1b_GGFnode_2018",  "datacard_HH_cat_resolved1b_DNN10_GGFnode_2018_20_bins_quantiles"],
    ["resolved1b_Hnode_2018",    "datacard_HH_cat_resolved1b_DNN10_Hnode_2018_5_bins_quantiles"],
    ["resolved1b_VBFnode_2018",  "datacard_HH_cat_resolved1b_DNN10_VBFnode_2018_7_bins_quantiles"],
    ["resolved2b_GGFnode_2018",  "datacard_HH_cat_resolved2b_DNN10_GGFnode_2018_10_bins_quantiles"],
    ["resolved2b_Hnode_2018",    "datacard_HH_cat_resolved2b_DNN10_Hnode_2018_4_bins_quantiles"],
    ["resolved2b_VBFnode_2018",  "datacard_HH_cat_resolved2b_DNN10_VBFnode_2018_5_bins_quantiles"],
]

for cards in list_DL_cards :
    FolderOut = "%s/fitdiag/" % mom_datacards
    proc=subprocess.Popen(["mkdir %s" % FolderOut],shell=True,stdout=subprocess.PIPE)
    out = proc.stdout.read()
    print(cards[0])
    fileCardOnlynBinL = cards[1]
    nameCardOnlynBinL = cards[0]

    cmd = "combineCards.py "
    cmd += "%s=%s.txt" % (cards[0], fileCardOnlynBinL)
    cmd += ">  renamedBin_%s_SL.txt" % nameCardOnlynBinL
    print(cmd)
    runCombineCmd(cmd, mom_datacards)

    cmd = "text2workspace.py"
    cmd += " renamedBin_%s_SL.txt" % nameCardOnlynBinL
    cmd += " -o %s/%s_WS.root" % (FolderOut, fileCardOnlynBinL)
    #cmd += " --freezeParameters rgx{CMS_.*}"
    print(cmd)
    runCombineCmd(cmd, mom_datacards)
    print ("done %s/%s_WS.root" % (FolderOut, fileCardOnlynBinL))

    cmd = "combineTool.py -M FitDiagnostics "
    cmd += " %s_WS.root" % fileCardOnlynBinL
    #if blinded :
    #    cmd += " -t -1 "
    cmd += " --saveShapes --saveWithUncertainties "
    cmd += " --saveNormalization "
    cmd += " --skipBOnlyFit "
    cmd += " -n _shapes_combine_%s" % nameCardOnlynBinL
    cmd += " --job-mode condor --sub-opt '+MaxRuntime = 18000' --task-name %s" % nameCardOnlynBinL
    runCombineCmd(cmd, FolderOut)
    #fileShapes = glob.glob("%s/fitDiagnostics_shapes_combine_%s*root" % (FolderOut, nameCardOnlynBinL))[0]
    #print ( "done %s" % fileShapes )
    #print(cmd)
