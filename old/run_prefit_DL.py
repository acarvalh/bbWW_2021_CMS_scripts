#!/usr/bin/env python
import os, subprocess, sys
from subprocess import Popen, PIPE

#mom_datacards = "/home/acaan/bbww_cards_feezinJan2021/2016/datacards_rebined/"
#FolderOut = "/home/acaan/bbww_cards_feezinJan2021/2016/"

mom = "/eos/user/m/mfackeld/DiHiggs/store/bbww_dl/Run2_pp_13TeV_2018/DatacardProducer/prod19/tth/nlo/dnn_score_max/" # */datacard.txt
FolderOut = "/afs/cern.ch/work/a/acarvalh/public/to_HH_bbWW/datacard_Aachen_DL_DNN11_v1/"

def runCombineCmd(combinecmd, outfolder='.', saveout=None):
    print ("Command: ", combinecmd)
    try:
        proc=subprocess.Popen(["cd %s ; %s" % (outfolder, combinecmd)],shell=True,stdout=subprocess.PIPE)
        out = proc.stdout.read()
    except OSError:
        print ("command not known\n", combinecmd)

list_SL_cards = [
    "all_boosted_1b_sr_dnn_node_class_HHGluGlu_NLO",
    "all_boosted_1b_sr_dnn_node_class_HHVBF_NLO",
    #"all_boosted_1b_sr_dnn_node_H",
    #"all_incl_sr_type2_dy_vv",
    #"all_incl_sr_type2_other",
    #"all_resolved_1b_sr_dnn_node_class_HHGluGlu_NLO",
    #"all_resolved_1b_sr_dnn_node_class_HHVBF_NLO",
    #"all_resolved_1b_sr_dnn_node_H",
    #"all_resolved_2b_sr_dnn_node_class_HHGluGlu_NLO",
    #"all_resolved_2b_sr_dnn_node_class_HHVBF_NLO",
    #"all_resolved_2b_sr_dnn_node_H",
]

era = "2018"
"""
rm  *all_boosted_1b_sr_dnn_node_H_2017*
rm  *all_boosted_1b_sr_dnn_node_class_HHVBF_NLO_2017*

rm  *all_boosted_1b_sr_dnn_node_class_HHVBF_NLO_2018*
rm  *all_boosted_1b_sr_dnn_node_class_HHGluGlu_NLO_2018*

combine renamedBin_all_resolved_2b_sr_dnn_node_class_HHVBF_NLO_2018.txt -v 2 -M FitDiagnostics -n .Test

------
condor_all_incl_sr_type2_dy_vv_2018.sh
#!/bin/sh
ulimit -s unlimited
set -e
cd /afs/cern.ch/work/a/acarvalh/CMSSW_8_0_1/src
export SCRAM_ARCH=slc6_amd64_gcc493
eval `scramv1 runtime -sh`
cd /afs/cern.ch/work/a/acarvalh/public/to_HH_bbWW/datacard_Aachen_DL_DNN11_v1

if [ $1 -eq 0 ]; then
  combine all_incl_sr_type2_dy_vv_2018_WS.root --saveShapes --saveWithUncertainties --saveNormalization --skipBOnlyFit -v 2 -M FitDiagnostics -n _shape$
fi

---
condor_all_incl_sr_type2_dy_vv_2018.sub

executable = condor_all_incl_sr_type2_dy_vv_2018.sh
arguments = $(ProcId)
output                = all_incl_sr_type2_dy_vv_2018.$(ClusterId).$(ProcId).out
error                 = all_incl_sr_type2_dy_vv_2018.$(ClusterId).$(ProcId).err
log                   = all_incl_sr_type2_dy_vv_2018.$(ClusterId).log

# Send the job to Held state on failure.
on_exit_hold = (ExitBySignal == True) || (ExitCode != 0)

# Periodically retry the jobs every 10 minutes, up to a maximum of 5 retries.
periodic_release =  (NumJobStarts < 3) && ((CurrentTime - EnteredCurrentStatus) > 600)

+MaxRuntime = 18000
queue 1

----

rm *all_boosted_1b_sr_dnn_node_class_HHGluGlu_NLO_2018*
rm *all_boosted_1b_sr_dnn_node_class_HHVBF_NLO_2018*
rm *all_incl_sr_type2_dy_vv_2018*
rm *all_resolved_1b_sr_dnn_node_H_2018*
rm *all_resolved_1b_sr_dnn_node_class_HHGluGlu_NLO_2018*
rm *all_resolved_1b_sr_dnn_node_class_HHVBF_NLO_2018*
rm *all_resolved_2b_sr_dnn_node_H_2018*
rm *all_resolved_2b_sr_dnn_node_class_HHVBF_NLO_2018*

text2workspace.py renamedBin_all_boosted_1b_sr_dnn_node_class_HHGluGlu_NLO_2018.txt -o /afs/cern.ch/work/a/acarvalh/public/to_HH_bbWW/datacard_Aachen_DL_DNN11_v1//all_boosted_1b_sr_dnn_node_class_HHGluGlu_NLO_2018_WS.root
TClass::Init:0: RuntimeWarning: no dictionary for class ROOT::TIOFeatures is available


rm *all_boosted_1b_sr_dnn_node_class_HHVBF_NLO_2017*
rm *all_resolved_1b_sr_dnn_node_class_HHVBF_NLO_2017*
rm *all_boosted_1b_sr_dnn_node_H_2017*

"""

for era in [  "2018", ] : # "2016", "2018",
    for cards in list_SL_cards :
        mom_datacards = "%s/%s" % (mom.replace("2018", era), cards)
        proc=subprocess.Popen(["mkdir %s" % FolderOut],shell=True,stdout=subprocess.PIPE)
        out = proc.stdout.read()
        fileCardOnlynBinL = "%s_%s" % (cards, era)

        cmd = "combineCards.py "
        cmd += "%s=%s/datacard.txt" % (fileCardOnlynBinL, mom_datacards)
        cmd += ">  %s/renamedBin_%s.txt" % (FolderOut, fileCardOnlynBinL)
        print(cmd)
        runCombineCmd(cmd, mom_datacards)

        cmd = "text2workspace.py"
        cmd += " renamedBin_%s.txt" % fileCardOnlynBinL
        cmd += " -o %s/%s_WS.root" % (FolderOut, fileCardOnlynBinL)
        print(cmd)
        runCombineCmd(cmd, FolderOut)
        print ("done %s/%s_WS.root" % (FolderOut, fileCardOnlynBinL))

        cmd = "combineTool.py -M FitDiagnostics "
        cmd += " %s_WS.root" % fileCardOnlynBinL
        #if blinded :
        #    cmd += " -t -1 "
        cmd += " --saveShapes --saveWithUncertainties "
        cmd += " --saveNormalization "
        cmd += " --skipBOnlyFit "
        cmd += " -v 2 "
        cmd += " -n _shapes_combine_%s" % fileCardOnlynBinL
        cmd += " --job-mode condor --sub-opt '+MaxRuntime = 18000' --task-name %s" % fileCardOnlynBinL
        runCombineCmd(cmd, FolderOut)
        #fileShapes = glob.glob("%s/fitDiagnostics_shapes_combine_%s*root" % (FolderOut, fileCardOnlynBinL))[0]
        #print ( "done %s" % fileShapes )
        print(cmd)

"""


_file0->ls("*DY#dnn_score_max#nominal*")


B - as the DNN is fixed now, after you remove the problematic processes we can launch a postfit
-- with all nondes,  to look at it ***blinded***
-- only with BKG nodes (+ single H node?) to have the option of making it unblided fast, if we decide to do

Do you agree?

===============================

Disclaimer - nothing is yet material to upload to datacards_run2 repo, mostly still ugly.

1 -
Here is a script to make one fitDiagnosis/card -- ok for prefit.


A - It copies a card with full path with a fixed renamed bin to a folder*

B - Runs t2w and submits the fitdiag.
As I want fixed names on the fitdiags files I am doing the commands myself.
As I do not want to write a submission file (lazy again) I am using Havester command line.

Note that as this is for prefit it would not matter to add the appropriate physics model on th t2w.

==> it took ~3:30h h to complete a fitdiagnosis file from one card.

For a global fit -- when the model on the t2w matters -- we use the inference repo fitDiagnosis command.
Copy to datacards_run2 and commit, as it will be the input for quick plots perfurmary.

-------
2 -

Here is the script to make dictionary (assuming bin names and fitdiag file names as above)

python make_DL_dict.py --fitdiag_folder /afs/cern.ch/work/a/acarvalh/public/to_HH_bbWW/datacard_Aachen_DL_DNN11_v1/ --output_dict /afs/cern.ch/work/a/acarvalh/public/to_HH_bbWW/datacard_Aachen_DL_DNN11_v1/dict_DL.dat

As it is all in public you can just run this one as it is to have the dict, just change the --output_dict to a place you have rights to write

-------
3 -

and the command to run the plotter:

As it is all in public you can just run this one as it is to have the plots (with this dictionary, if you do not want to run the poin 2)

This is the point you can ask to unblind the plots, but all the plots on the dictionary will be unblided.
That is why there is an option in poinnt (2) to make the dictionary only with BKG on it.

If you want to run it, this is the dictionary (add '--unblind' to the command above calling this one below):

python dhi/scripts/postfit_plots.py \
--output_folder "/afs/cern.ch/work/a/acarvalh/public/to_HH_bbWW/datacard_Aachen_DL_DNN11/plots/" \
--plot_options_dict "/afs/cern.ch/work/a/acarvalh/public/to_HH_bbWW/datacard_Aachen_DL_DNN11_v1/dict_DL.dat"

=======================================


cheers
Xanda

* I wanted to make a script to bundle all your cards to one folder (or at least reduce the number of subfolders to be easier to copy locally),
but I am lazy, and I know you will have to solve that somehow anyway to put in datacards_run2 repo.
When you do, I adapt these to the way you use to add there.

"""
