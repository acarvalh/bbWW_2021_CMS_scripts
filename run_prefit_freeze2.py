#!/usr/bin/env python
import os, subprocess, sys
from subprocess import Popen, PIPE


mom = "/afs/cern.ch/work/a/acarvalh/public/to_HH_bbWW/freze2_March19/round2/datacards/"
FolderOut = "/afs/cern.ch/work/a/acarvalh/public/to_HH_bbWW/freze2_March19/round2/fitdiag2/"

#mom = "/home/acaan/bbww_cards_feezingMar2021_Aachen/round1/"
#FolderOut = "/home/acaan/bbww_cards_feezingMar2021_Aachen/fitdiag2/"

def runCombineCmd(combinecmd, outfolder='.', saveout=None):
    print ("Command: ", combinecmd)
    try:
        proc=subprocess.Popen(["cd %s ; %s" % (outfolder, combinecmd)],shell=True,stdout=subprocess.PIPE)
        out = proc.stdout.read()
    except OSError:
        print ("command not known\n", combinecmd)

list_DL_cards = [
    "all_boosted_1b_sr_dnn_node_class_HHGluGlu_NLO",
    "all_boosted_1b_sr_dnn_node_class_HHVBF_NLO",
    "all_boosted_1b_sr_dnn_node_H",
    "all_resolved_1b_sr_dnn_node_class_HHGluGlu_NLO",
    "all_resolved_1b_sr_dnn_node_class_HHVBF_NLO",
    "all_resolved_1b_sr_dnn_node_H",
    "all_resolved_2b_sr_dnn_node_class_HHGluGlu_NLO",
    "all_resolved_2b_sr_dnn_node_class_HHVBF_NLO",
    "all_resolved_2b_sr_dnn_node_H",
    "all_incl_sr_type2_dy_vv",
    "all_incl_sr_type2_other",
]

list_SL_cards = [
    "all_boosted_sr_dnn_node_class_HHGluGlu_NLO",
    "all_boosted_sr_dnn_node_class_HHVBF_NLO",
    "all_boosted_sr_dnn_node_H",
    "all_incl_sr_dnn_node_class_other",
    "all_incl_sr_dnn_node_st",
    "all_incl_sr_dnn_node_tt",
    "all_incl_sr_dnn_node_wjets",
    "all_resolved_1b_sr_dnn_node_class_HHGluGlu_NLO",
    "all_resolved_1b_sr_dnn_node_class_HHVBF_NLO",
    "all_resolved_1b_sr_dnn_node_H",
    "all_resolved_2b_sr_dnn_node_class_HHGluGlu_NLO",
    "all_resolved_2b_sr_dnn_node_class_HHVBF_NLO",
    "all_resolved_2b_sr_dnn_node_H",
]

cmdTot = "combineCards.py "
cmdTotBKG = "combineCards.py "
for channel in ["dl", "sl"] :

    if channel == "dl" :
        list_bins = list_DL_cards
    if channel == "sl" :
        list_bins = list_SL_cards
        #continue

    cmdChannel = "combineCards.py "
    cmdChannelBKG = "combineCards.py "
    for era in ["2016", "2017", "2018"] :
        #if not era == "2016" : continue
        for bin in list_bins :
            full_path_card = "%s/%s_%s_%s/datacard.txt" % (mom, channel, era, bin)
            print(full_path_card)
            full_path_card_renamedBin = "%s/%s_%s_%s/datacard_renamedBin.txt" % (mom, channel, era, bin)
            renamedBin = "%s_%s_%s" % (channel, era, bin)

            cmd = "combineCards.py "
            cmd += "%s=%s " % (renamedBin, full_path_card)
            cmd += ">  %s" % (full_path_card_renamedBin)
            #runCombineCmd(cmd)
            #print (full_path_card_renamedBin)

            cmd = "combineTool.py -M FitDiagnostics "
            cmd += " %s" % full_path_card_renamedBin
            #if blinded :
            #    cmd += " -t -1 "
            cmd += " --saveShapes --saveWithUncertainties "
            cmd += " --saveNormalization "
            cmd += " --skipBOnlyFit "
            #cmd += " -v 2 "
            cmd += "  --setParameters r=0 --freezeParameters r "
            cmd += " -n _shapes_combine_%s" % renamedBin
            cmd += " --job-mode condor --sub-opt '+MaxRuntime = 54000' --task-name %s" % renamedBin
            runCombineCmd(cmd, FolderOut)

            if 0 > 1 :
                ########
                jobfile = "%s/fitdiag_%s.sh" % (FolderOut, renamedBin)
                ff = open(jobfile, "w")
                ff.write(u'#!/bin/bash\n\n')

                ff.write(unicode("cd ~/CMSSW_8_1_0/src/ ; cmsenv\n"))
                ff.write(unicode("cd %s\n" % FolderOut))
                ff.write(unicode(cmd))
                ff.close()
                cmd2 = "sbatch "
                cmd2 += " --output=%s " % jobfile.replace(".sh", ".log.job")
                #cmd2 += "--partition=small "
                cmd2 += jobfile
                #print(cmd2)
                #runCombineCmd(cmd2)
                ########

            cmdTot += "%s=%s " % (renamedBin, full_path_card)
            cmdChannel += "%s=%s " % (renamedBin, full_path_card)

            if not "_NLO" in bin :
                cmdTotBKG += "%s=%s " % (renamedBin, full_path_card)
                cmdChannelBKG += "%s=%s " % (renamedBin, full_path_card)

    cmdChannel += " > %s/datacard_%s.txt" % (mom, channel)
    cmdChannelBKG += " > %s/datacard_%s_BKGonly.txt" % (mom, channel)
    runCombineCmd(cmdChannel)
    runCombineCmd(cmdChannelBKG)

cmdTot += " > %s/datacard.txt" % (mom)
cmdTotBKG += " > %s/datacard_BKGonly.txt" % (mom)
runCombineCmd(cmdTot)
runCombineCmd(cmdTotBKG)
