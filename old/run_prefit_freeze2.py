#!/usr/bin/env python
import os, subprocess, sys
from subprocess import Popen, PIPE

"""
The purpose of this script is to:

- rename bins in cards if necessary
- submit one fitDiagnosis by card

mom = "/afs/cern.ch/work/a/acarvalh/HH_inference/fits_bbWW/Aa_DL_2018_DY_MC_bin_name_sorted/dnn_score_max/"
FolderOut = "/afs/cern.ch/work/a/acarvalh/HH_inference/fits_bbWW/round3_results/prefit_plots/DL_2018_DY_mc_Aa/fitdiag/"
mom_original = "/afs/cern.ch/work/m/mfackeld/DiHiggs/public/datacards/studies/DYmc/dnn_score_max/"
"""
def runCombineCmd(combinecmd, outfolder='.', saveout=None):
    print ("Command: ", combinecmd)
    try:
        proc=subprocess.Popen(["cd %s ; %s" % (outfolder, combinecmd)],shell=True,stdout=subprocess.PIPE)
        out = proc.stdout.read()
    except OSError:
        print ("command not known\n", combinecmd)


from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
parser = ArgumentParser(
    description=__doc__, formatter_class=ArgumentDefaultsHelpFormatter
)
parser.add_argument(
    "--fitdiag_folder",
    dest="fitdiag_folder",
    help="Folder that will contain the fitdiagnosis.root file(s)",
    )
parser.add_argument(
    "--cards_renamed_bin",
    dest="cards_renamed_bin",
    help="If bins need to be renamed, they are copied ibn this local folder. ",
    default="none"
    )
parser.add_argument(
    "--cards_original",
    dest="cards_original",
    help="Folder with original cards (for possible checks) ",
    default="none"
    )
parser.add_argument(
    "--only_era",
    dest="only_era",
    help="If you gine an era, it will makee the dict to draw only this one.",
    default="none"
    )
parser.add_argument(
    "--only_bkg",
    action="store_true",
    dest="unblind_bkg",
    help="dictionary only with bkg nodes",
    default=False
    )
parser.add_argument(
    "--only_sig",
    action="store_true",
    dest="only_sig",
    help="dictionary only with signal nodes",
    default=False
    )
parser.add_argument(
    "--submit_fitdiag_by_card",
    action="store_true",
    dest="submit_fitdiag_by_card",
    help="Self explanatory.",
    default=False
    )
parser.add_argument(
    "--local_cluster",
    action="store_true",
    dest="local_cluster",
    help="On how submit jobs. default is use CombineHavester scheduler to submit to condor in lxplus (combineHavester must be setup!!!).",
    default=False
    )
parser.add_argument(
    "--law",
    action="store_true",
    dest="law",
    help="On how submit jobs. default is use CombineHavester scheduler to submit to condor in lxplus (combineHavester must be setup!!!).",
    default=False
    )
args = parser.parse_args()
fitdiagDL =
dictionary = args.output_dict
unblind_bkg = args.unblind_bkg
only_sig = args.only_sig

mom = args.cards_renamed_bin
FolderOut = args.fitdiag_folder
mom_original = args.cards_original


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
        continue

    cmdChannel = "combineCards.py "
    cmdChannelBKG = "combineCards.py "
    for era in ["2016", "2017", "2018"] :
        if not era == "2018" : continue
        for bin in list_bins :

            #full_path_card_original = "%s/%s_%s_%s/datacard.txt" % (mom_original, channel, era, bin)
            #full_path_card = "%s/%s_%s_%s/datacard.txt" % (mom, channel, era, bin)
            #print(full_path_card)
            #full_path_card_renamedBin = "%s/%s_%s_%s/datacard_renamedBin.txt" % (mom, channel, era, bin)

            full_path_card_original = "%s/%s/datacard.txt" % (mom_original, bin)
            if not mom == "none" :
                full_path_card = "%s/%s/datacard.txt" % (mom, bin)
                print(full_path_card)
                full_path_card_renamedBin = "%s/%s/datacard_renamedBin.txt" % (mom, bin)

                cmd = "combineCards.py "
                cmd += "%s=%s " % (renamedBin, full_path_card)
                cmd += ">  %s" % (full_path_card_renamedBin)
                runCombineCmd(cmd)

            full_path_card_renamedBin = full_path_card_original

            renamedBin = "%s_%s_%s" % (channel, era, bin)

            if args.submit_fitdiag_by_card :
                if args.law :
                    cmd = "law run FitDiagnostics "
                    cmd += " --version  %s" % renamedBin
                    cmd += " --datacards %s=%s " % (renamedBin, full_path_card_renamedBin)
                    cmd += " --pois r --FitDiagnostics-no-poll --FitDiagnostics-workflow htcondor"
                elif args.local_cluster :
                    ## --no-poll
                    ### /afs/cern.ch/work/a/acarvalh/HH_inference/fits_bbWW/running_fits/FitDiagnostics/HHModelPinv__model_default/datacards_7498db6feb/m125.0/poi_r/all_boosted_1b_sr_dnn_node_class_HHGluGlu_NLO/fitdiagnostics__poi_r__params_r1.0_r_qqhh1.0_r_gghh1.0_kl1.0_kt1.0_CV1.0_C2V1.0.root
                    ## law run FitDiagnostics --version all_boosted_1b_sr_dnn_node_class_HHGluGlu_NLO_test --datacards /afs/cern.ch/work/m/mfackeld/DiHiggs/public/datacards/studies/DYmc/dnn_score_max/all_boosted_1b_sr_dnn_node_class_HHGluGlu_NLO/datacard.txt --pois r --FitDiagnostics-no-poll
                    # an example of cluster-like job submission
                    # construct the combine command
                    cmd = "combine -M FitDiagnostics "
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
                    ###############################################
                    # submit card by card
                    jobfile = "%s/fitdiag_%s.sh" % (FolderOut, renamedBin)
                    ff = open(jobfile, "w")
                    ff.write(u'#!/bin/bash\n\n')

                    ff.write(unicode("cd ~/CMSSW_8_1_0/src/ ; cmsenv\n"))
                    ## or the way you source combine

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
                else :
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

            cmdTot += "%s=%s " % (renamedBin, full_path_card_original)
            cmdChannel += "%s=%s " % (renamedBin, full_path_card_original)

            if not "_NLO" in bin :
                cmdTotBKG += "%s=%s " % (renamedBin, full_path_card_original)
                cmdChannelBKG += "%s=%s " % (renamedBin, full_path_card_original)

    cmdChannel += " > %s/datacard_%s.txt" % (mom, channel)
    cmdChannelBKG += " > %s/datacard_%s_BKGonly.txt" % (mom, channel)
    ## if one wants to do a combo card/era
    #runCombineCmd(cmdChannel)
    #runCombineCmd(cmdChannelBKG)

cmdTot += " > %s/datacard.txt" % (mom)
cmdTotBKG += " > %s/datacard_BKGonly.txt" % (mom)
## if one wants to do a combo card/era
#runCombineCmd(cmdTot)
#runCombineCmd(cmdTotBKG)
