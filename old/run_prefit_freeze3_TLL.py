#!/usr/bin/env python
import os, subprocess, sys
from subprocess import Popen, PIPE
import glob
import ROOT

#from dhi.tasks.postfit import PlotNuisanceLikelihoodScans_standalone
from dhi.plots.likelihoods import plot_nuisance_likelihood_scans

"""
The purpose of this script is to:

- rename bins in cards (if necessary), if a "cards_renamed_bin" is given (to use in making fitDiagnosis of global fits)
- submit one fitDiagnosis by card / following bin naming that goes with the plot dictionary maker on this same folder
- plot law-implemented plots from the fitdiag by card

Example of usage ()

python /afs/cern.ch/work/a/acarvalh/HH_inference/bbWW_2021_CMS_scripts/run_prefit_freeze3_TLL.py \
--cards_original  "/afs/cern.ch/work/a/acarvalh/HH_inference/fits_bbWW/TLL_splitted_bins/" \
--fitdiag_folder /eos/user/a/acarvalh/bbWW_fullRun2_results/round3_results/prefit_plots/DL_TLL/fitdiag_blinded/ \
--submit_fitdiag_by_card law_collect \
--only_era 2016 --university TLL

Ideally you run with:
law

After all jobs done:

1) To collect root files to do the plots after (and check if all done)
law_collect

2) To do NLL scans of systematics


/eos/user/a/acarvalh/bbWW_fullRun2_results/round3_results/prefit_plots/make_DL_dict_Aa.py

law run PlotNuisanceLikelihoodScans \
    --version dev \
    --datacards $DHI_EXAMPLE_CARDS \
    --parameters-per-page 20 --only-parameters "CMS*JES*" --y-log


=================
While 2017 root files are all ready, most of 2018 and 2016 crashed
(will check why, but was 48h job runtime -- Aa ones takes at maximum 3h)
--print-status


law run PlotNuisanceLikelihoodScans  --version  TLL_SM_lbn_2l_0tau_2017_TT_resolved --datacards SM_lbn_2l_0tau_2017_TT_resolved=/afs/cern.ch/work/a/acarvalh/HH_inference/fits_bbWW/TLL_splitted_bins//DL/bb2l_2017/SM_lbn_2l_0tau_2017_TT_resolved.txt  --pois r --parameters-per-page 20 --only-parameters "CMS*JES*" --y-log --FitDiagnostics-no-poll --FitDiagnostics-workflow htcondor --FitDiagnostics-max-runtime 48 --print-status 4

ls /afs/cern.ch/work/a/acarvalh/HH_inference/fits_bbWW/running_fits/FitDiagnostics/HHModelPinv__model_default/datacards_*/m125.0/poi_r/*0tau*/

ls /afs/cern.ch/work/a/acarvalh/HH_inference/fits_bbWW/running_fits/FitDiagnostics/HHModelPinv__model_default/datacards_*/m125.0/poi_r/TLL*0tau*/

ls /afs/cern.ch/work/a/acarvalh/HH_inference/fits_bbWW/running_fits/CreateWorkspace/HHModelPinv__model_default/datacards_*/m125.0/TLL*0tau*/
                                                         $DHI_STORE/CreateWorkspace/HHModelPinv__model_default/datacards_920aee2b0b/m125.0/TLL_SM_lbn_2l_0tau_2016_DY_boosted/workspace.root
9363.pts-151.lxplus736
757.pts-14.lxplus710
11933.pts-151.lxplus736

/afs/cern.ch/work/a/acarvalh/HH_inference/fits_bbWW/running_fits/FitDiagnostics/HHModelPinv__model_default/datacards_fd5a19cd31/m125.0/poi_r/TLL_SM_lbn_2l_0tau_2017_SingleTop_resolved/fitdiagnostics__poi_r__params_r1.0_r_qqhh1.0_r_gghh1.0_kl1.0_kt1.0_CV1.0_C2V1.0.root


===========================================
python /afs/cern.ch/work/a/acarvalh/HH_inference/bbWW_2021_CMS_scripts/run_prefit_freeze3_TLL.py --cards_original  "/afs/cern.ch/work/a/acarvalh/HH_inference/fits_bbWW/TLL_splitted_bins/" --fitdiag_folder /eos/user/a/acarvalh/bbWW_fullRun2_results/round3_results/prefit_plots/DL_TLL/fitdiag2/ --submit_fitdiag_by_card law --only_channel dl --only_era 2016

python /afs/cern.ch/work/a/acarvalh/HH_inference/bbWW_2021_CMS_scripts/run_prefit_freeze3_TLL.py --cards_original  "/afs/cern.ch/work/a/acarvalh/HH_inference/fits_bbWW/TLL_splitted_bins/" --fitdiag_folder /eos/user/a/acarvalh/bbWW_fullRun2_results/round3_results/prefit_plots/DL_TLL/fitdiag2/ --submit_fitdiag_by_card law --only_channel dl --only_era 2017

python /afs/cern.ch/work/a/acarvalh/HH_inference/bbWW_2021_CMS_scripts/run_prefit_freeze3_TLL.py --cards_original  "/afs/cern.ch/work/a/acarvalh/HH_inference/fits_bbWW/TLL_splitted_bins/" --fitdiag_folder /eos/user/a/acarvalh/bbWW_fullRun2_results/round3_results/prefit_plots/DL_TLL/fitdiag2/ --submit_fitdiag_by_card law --only_channel dl --only_era 2018

python /afs/cern.ch/work/a/acarvalh/HH_inference/bbWW_2021_CMS_scripts/run_prefit_freeze3_TLL.py --cards_original  "/afs/cern.ch/work/a/acarvalh/HH_inference/fits_bbWW/TLL_splitted_bins/" --fitdiag_folder /eos/user/a/acarvalh/bbWW_fullRun2_results/round3_results/prefit_plots/DL_TLL/fitdiag2/ --submit_fitdiag_by_card law --only_channel sl --only_era 2016

python /afs/cern.ch/work/a/acarvalh/HH_inference/bbWW_2021_CMS_scripts/run_prefit_freeze3_TLL.py --cards_original  "/afs/cern.ch/work/a/acarvalh/HH_inference/fits_bbWW/TLL_splitted_bins/" --fitdiag_folder /eos/user/a/acarvalh/bbWW_fullRun2_results/round3_results/prefit_plots/DL_TLL/fitdiag2/ --submit_fitdiag_by_card law --only_channel sl --only_era 2017

python /afs/cern.ch/work/a/acarvalh/HH_inference/bbWW_2021_CMS_scripts/run_prefit_freeze3_TLL.py --cards_original  "/afs/cern.ch/work/a/acarvalh/HH_inference/fits_bbWW/TLL_splitted_bins/" --fitdiag_folder /eos/user/a/acarvalh/bbWW_fullRun2_results/round3_results/prefit_plots/DL_TLL/fitdiag2/ --submit_fitdiag_by_card law --only_channel sl --only_era 2018

law run FitDiagnostics  --version  TLL_SM_lbn_2l_0tau_2016_DY_boosted_data --datacards SM_lbn_2l_0tau_2016_DY_boosted=/afs/cern.ch/work/a/acarvalh/HH_inference/fits_bbWW/TLL_splitted_bins//DL/bb2l_2016/SM_lbn_2l_0tau_2016_DY_boosted.txt  --pois r  --unblinded --PullsAndImpacts-custom-args='--X-rtd MINIMIZER_no_analytic'  --FitDiagnostics-no-poll --FitDiagnostics-workflow htcondor --FitDiagnostics-max-runtime 48


law run PlotNuisanceLikelihoodScans  --version  TLL_SM_lbn_2l_0tau_2016_DY_boosted --datacards SM_lbn_2l_0tau_2016_DY_boosted=/afs/cern.ch/work/a/acarvalh/HH_inference/fits_bbWW/TLL_splitted_bins//DL/bb2l_2016/SM_lbn_2l_0tau_2016_DY_boosted.txt  --pois r  --FitDiagnostics-no-poll --FitDiagnostics-workflow htcondor --FitDiagnostics-max-runtime 48


----

python /afs/cern.ch/work/a/acarvalh/HH_inference/bbWW_2021_CMS_scripts/run_prefit_freeze3_TLL.py --cards_original  "/afs/cern.ch/work/a/acarvalh/HH_inference/fits_bbWW/TLL_splitted_bins/" --fitdiag_folder /eos/user/a/acarvalh/bbWW_fullRun2_results/round3_results/prefit_plots/DL_TLL/fitdiag2/ --submit_fitdiag_by_card nuissances --only_channel dl --only_era 2016

  PlotNuisanceLikelihoodScans(version=TLL_SM_lbn_2l_0tau_2016_DY_boosted, hh_model=HHModelPinv.model_default, datacards=hash:920aee2b0b, mass=125.0, parameter_values=, pois=r, frozen_parameters=, frozen_groups=, unblinded=False, y_log=False, parameters_per_page=1)
"""
def runCombineCmd(combinecmd, outfolder='.', print_command=False, saveout=None):
    if print_command : print ("Command: ", combinecmd)
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
    "--university",
    dest="university",
    help="To know which naming convention of files to assume. Options TLL , RTW, LLR",
    default="TLL"
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
    "--only_channel",
    dest="only_chanel",
    help="Can be 'sl' or 'dl'. dictionary only with that channel.",
    default="none"
    )
parser.add_argument(
    "--only_era",
    dest="only_era",
    help="If you give an era, it will make only this one.",
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
    dest="submit_fitdiag_by_card",
    help="On how submit jobs. \n CombineHavester: scheduler to submit to condor in lxplus (combineHavester must be setup!!!). \n local_cluster (you must setup yours) \n law \n law_collect: only collects the outputs to fitdiag_folder \n nuissances: make and collect NLL JES nuissances plots (if law + same DHI_STORE)",
    default="none"
    )
args = parser.parse_args()


mom = args.cards_renamed_bin
FolderOut = args.fitdiag_folder
mom_original = args.cards_original
submit_fitdiag_by_card = args.submit_fitdiag_by_card
only_chanel = args.only_chanel

if args.university == "TLL" :
    list_DL_cards = [
     "DL/bb2l_ERA/SM_lbn_2l_0tau_ERA_DY_boosted",
     "DL/bb2l_ERA/SM_lbn_2l_0tau_ERA_DY_resolved",
     "DL/bb2l_ERA/SM_lbn_2l_0tau_ERA_HH_boosted",
     "DL/bb2l_ERA/SM_lbn_2l_0tau_ERA_HH_resolved_1b_nonvbf",
     "DL/bb2l_ERA/SM_lbn_2l_0tau_ERA_HH_resolved_1b_vbf",
     "DL/bb2l_ERA/SM_lbn_2l_0tau_ERA_HH_resolved_2b_nonvbf",
     "DL/bb2l_ERA/SM_lbn_2l_0tau_ERA_HH_resolved_2b_vbf",
     "DL/bb2l_ERA/SM_lbn_2l_0tau_ERA_Other",
     "DL/bb2l_ERA/SM_lbn_2l_0tau_ERA_SingleTop_boosted",
     "DL/bb2l_ERA/SM_lbn_2l_0tau_ERA_SingleTop_resolved",
     "DL/bb2l_ERA/SM_lbn_2l_0tau_ERA_TT_boosted",
     "DL/bb2l_ERA/SM_lbn_2l_0tau_ERA_TT_resolved",
    ]

    list_SL_cards = [
     "SL/ERA/SM_lbn_1l_0tau_ERA_DY_boosted",
     "SL/ERA/SM_lbn_1l_0tau_ERA_DY_resolved",
     "SL/ERA/SM_lbn_1l_0tau_ERA_HH_boosted",
     "SL/ERA/SM_lbn_1l_0tau_ERA_HH_resolved_1b_nonvbf",
     "SL/ERA/SM_lbn_1l_0tau_ERA_HH_resolved_1b_vbf",
     "SL/ERA/SM_lbn_1l_0tau_ERA_HH_resolved_2b_nonvbf",
     "SL/ERA/SM_lbn_1l_0tau_ERA_HH_resolved_2b_vbf",
     "SL/ERA/SM_lbn_1l_0tau_ERA_Other",
     "SL/ERA/SM_lbn_1l_0tau_ERA_SingleTop_boosted",
     "SL/ERA/SM_lbn_1l_0tau_ERA_SingleTop_resolved",
     "SL/ERA/SM_lbn_1l_0tau_ERA_TT_boosted",
     "SL/ERA/SM_lbn_1l_0tau_ERA_TT_resolved",
     "SL/ERA/SM_lbn_1l_0tau_ERA_W_boosted",
     "SL/ERA/SM_lbn_1l_0tau_ERA_W_resolved",
    ]

cmdTot = "combineCards.py "
cmdTotBKG = "combineCards.py "
for channel in ["dl", "sl"] :

    if not only_chanel == "none" :
        if not only_chanel == channel :
            continue

    if channel == "dl" :
        list_bins = list_DL_cards
        #continue
    if channel == "sl" :
        list_bins = list_SL_cards
        #continue

    cmdChannel = "combineCards.py "
    cmdChannelBKG = "combineCards.py "
    for era in ["2016", "2017", "2018"] :
        if not args.only_era == "none" :
            if not era == args.only_era :
                continue

        for bin in list_bins :

            bin = bin.replace("ERA", era)
            renamedBin = bin.split("/")[len(bin.split("/"))-1]

            full_path_card_original = "%s/%s.txt" % (mom_original, bin)
            full_path_card_renamedBin = full_path_card_original
            if not mom == "none" :
                full_path_card = "%s/%s.txt" % (mom, bin)
                print(full_path_card)
                full_path_card_renamedBin = "%s/%s_renamedBin.txt" % (mom, bin)

                cmd = "combineCards.py "
                cmd += "%s=%s " % (renamedBin, full_path_card)
                cmd += ">  %s" % (full_path_card_renamedBin)
                runCombineCmd(cmd)

            if not submit_fitdiag_by_card == "none" :
                if "law" in submit_fitdiag_by_card :
                    #version = "TLL_%s_data" % renamedBin
                    version = "TLL_%s" % renamedBin
                    cmd = "law run FitDiagnostics "
                    cmd += " --version  %s" % version
                    cmd += " --datacards %s=%s " % (renamedBin, full_path_card_renamedBin)
                    cmd += " --pois r  --unblinded --PullsAndImpacts-custom-args='--X-rtd MINIMIZER_no_analytic' "
                    cmd += " --FitDiagnostics-no-poll --FitDiagnostics-workflow htcondor --FitDiagnostics-max-runtime 48"

                    ## concentrate results adding to the command
                    if submit_fitdiag_by_card == "law" :
                        runCombineCmd(cmd, FolderOut, print_command=True)
                    elif submit_fitdiag_by_card == "law_collect" :
                        # print-satatus 0 is not the root file, so we need to use the actual path to paste
                        #    cmd += " --fetch-output 0" ## the output is not the .root, that does not work
                        law_fitdiag_result_pattern = "%s/FitDiagnostics/HHModelPinv__model_default/datacards_*/m125.0/poi_r/%s/fitdiagnostics__poi_r__params_r1.0_r_qqhh1.0_r_gghh1.0_kl1.0_kt1.0_CV1.0_C2V1.0.root" % (os.environ["DHI_STORE"], version)
                        law_ws_result_pattern = "%s/CreateWorkspace/HHModelPinv__model_default/datacards_*/m125.0/%s/workspace.root" % (os.environ["DHI_STORE"], version)
                        for result in [law_fitdiag_result_pattern, law_ws_result_pattern] :
                            fileShapes = glob.glob(result)
                            if not len(fileShapes) == 1 :
                                print("WARNING: found %s fitdiagnosis (if more delete one, if less resubmit) for bin %s") % (str(len(fileShapes)), renamedBin)
                                for ff in fileShapes : print(ff)
                                if len(fileShapes) == 0 :
                                    runCombineCmd(cmd, FolderOut, print_command=True)
                            else :
                                file_final = "%s/fitdiagnostics_%s.root" % (FolderOut, renamedBin)
                                print("Copying result of %s to fitdiagnostics_%s.root in fitdiag_folder") % (renamedBin, renamedBin)
                                runCombineCmd("cp %s %s" % (fileShapes[0], file_final))
                                if "FitDiagnostics" in result : law_fitdiag_result = fileShapes[0]
                                if "CreateWorkspace" in result : law_ws_result = fileShapes[0]
                        #elif submit_fitdiag_by_card == "nuissances" :
                        # to repeat the coommand does not always work
                        save_plot = "%s/NLL_JES_%s.pdf" % (FolderOut, renamedBin)
                        only_parameters="CMS*JES*"
                        parameters_per_page=15
                        y_log=False
                        unblinded=True
                        pois="r"
                        #mass=125.0
                        #fitdiagnostics_path=  "/afs/cern.ch/work/a/acarvalh/HH_inference/fits_bbWW/running_fits/FitDiagnostics/HHModelPinv__model_default/datacards_fd5a19cd31/m125.0/poi_r/TLL_SM_lbn_2l_0tau_2017_SingleTop_resolved/fitdiagnostics__poi_r__params_r1.0_r_qqhh1.0_r_gghh1.0_kl1.0_kt1.0_CV1.0_C2V1.0.root"
                        #ws_path = "/afs/cern.ch/work/a/acarvalh/HH_inference/fits_bbWW/running_fits/CreateWorkspace/HHModelPinv__model_default/datacards_fd5a19cd31/m125.0/TLL_SM_lbn_2l_0tau_2017_SingleTop_resolved/workspace.root"
                        result_file = ROOT.TFile(law_ws_result)
                        ww = result_file.Get("w")
                        datasetw = ww.data("data_obs") if unblinded else result_file.Get("toys/toy_asimov")
                        plot_nuisance_likelihood_scans(
                            save_plot,
                            poi="r",
                            workspace=ww,
                            dataset=datasetw,
                            fit_diagnostics_path=law_fitdiag_result,
                            fit_name="fit_s",
                            skip_parameters=None,
                            only_parameters=only_parameters,
                            parameters_per_page=parameters_per_page,
                            scan_points=101,
                            x_min=-2.,
                            x_max=2,
                            y_log=False,
                            model_parameters=None,
                            campaign=None,
                        )
                elif submit_fitdiag_by_card == "local_cluster" :
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
    if not mom == "none" :
        runCombineCmd(cmdChannel)
        runCombineCmd(cmdChannelBKG)

cmdTot += " > %s/datacard.txt" % (mom)
cmdTotBKG += " > %s/datacard_BKGonly.txt" % (mom)
## if one wants to do a combo card/era
if not mom == "none" :
    runCombineCmd(cmdTot)
    runCombineCmd(cmdTotBKG)
