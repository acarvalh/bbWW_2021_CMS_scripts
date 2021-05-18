#!/usr/bin/env python
import os, subprocess, sys
from subprocess import Popen, PIPE


def runCombineCmd(combinecmd, outfolder='.', print_command=False, saveout=None):
    if print_command : print ("Command: ", combinecmd)
    try:
        proc=subprocess.Popen(["cd %s ; %s" % (outfolder, combinecmd)],shell=True,stdout=subprocess.PIPE)
        out = proc.stdout.read()
    except OSError:
        print ("command not known\n", combinecmd)


datacards = "/afs/cern.ch/work/a/acarvalh/public/to_HH_bbWW/datacatds_RWTH_round3/boosted_nuissances_lnN/issue69_CH_set1_ERA/BIN/dnn_score_max/"

channel = {
    "sl" : [
        ["all_boosted_sr_prompt_dnn_node_class_HHGluGlu_NLO"     , "ggHH_B"],
        ["all_boosted_sr_prompt_dnn_node_class_HHVBF_NLO"        , "qqHH_B"],
        ["all_boosted_sr_prompt_dnn_node_H"                      , "H_B"],
        ["all_boosted_sr_prompt_top"                             , "top_B"],
        ["all_incl_sr_prompt_dnn_node_class_other"               , "other"],
        ["all_incl_sr_prompt_dnn_node_wjets"                     , "wjets"],
        ["all_resolved_1b_sr_prompt_dnn_node_class_HHGluGlu_NLO" , "ggHH_1b"],
        ["all_resolved_1b_sr_prompt_dnn_node_class_HHVBF_NLO"    , "qqHH_1b"],
        ["all_resolved_1b_sr_prompt_dnn_node_H"                  , "H_1b"],
        ["all_resolved_2b_sr_prompt_dnn_node_class_HHGluGlu_NLO" , "ggHH_2b"],
        ["all_resolved_2b_sr_prompt_dnn_node_class_HHVBF_NLO"    , "qqHH_2b"],
        ["all_resolved_2b_sr_prompt_dnn_node_H"                  , "H_2b"],
        ["all_resolved_sr_prompt_top"                            , "top_res"]
    ],
    "dl" : [
        ["all_boosted_1b_sr_dnn_node_class_HHGluGlu_NLO"  , "ggHH_B_dl"],
        ["all_boosted_1b_sr_dnn_node_class_HHVBF_NLO"     , "qqHH_B_dl"],
        ["all_boosted_1b_sr_dnn_node_H"                   , "H_B_dl"],
        ["all_boosted_1b_sr_type2_dy_vv"                  , "dy_B_dl"],
        ["all_boosted_1b_sr_type2_other"                  , "other_B_dl"],
        ["all_resolved_1b_sr_dnn_node_class_HHGluGlu_NLO" , "ggHH_1b_dl"],
        ["all_resolved_1b_sr_dnn_node_class_HHVBF_NLO"    , "qqHH_1b_dl"],
        ["all_resolved_1b_sr_dnn_node_H"                  , "H_1b_dl"],
        ["all_resolved_2b_sr_dnn_node_class_HHGluGlu_NLO" , "ggHH_2b_dl"],
        ["all_resolved_2b_sr_dnn_node_class_HHVBF_NLO"    , "qqHH_2b_dl"],
        ["all_resolved_2b_sr_dnn_node_H"                  , "H_2b_dl"],
        ["all_resolved_sr_type2_dy_vv"                    , "dy_res_dl"],
        ["all_resolved_sr_type2_other"                    , "other_res_dl"]
    ]
}

name_changes="""
CMS_bbwwCH_FakeRate_m_pt_ERA=CMS_bbwwCH_FakeRate_m_pt_BIN_ERA
CMS_bbwwCH_FakeRate_m_norm_ERA=CMS_bbwwCH_FakeRate_m_norm_BIN_ERA
CMS_bbwwCH_FakeRate_m_nc_res_ERA=CMS_bbwwCH_FakeRate_m_nc_res_BIN_ERA
CMS_bbwwCH_FakeRate_m_nc_nom_ERA=CMS_bbwwCH_FakeRate_m_nc_nom_BIN_ERA
CMS_bbwwCH_FakeRate_m_barrel_ERA=CMS_bbwwCH_FakeRate_m_barrel_BIN_ERA
CMS_bbwwCH_FakeRate_e_pt_ERA=CMS_bbwwCH_FakeRate_e_pt_BIN_ERA
CMS_bbwwCH_FakeRate_e_norm_ERA=CMS_bbwwCH_FakeRate_e_norm_BIN_ERA
CMS_bbwwCH_FakeRate_e_nc_res_ERA=CMS_bbwwCH_FakeRate_e_nc_res_BIN_ERA
CMS_bbwwCH_FakeRate_e_nc_nom_ERA=CMS_bbwwCH_FakeRate_e_nc_nom_BIN_ERA
CMS_bbwwCH_FakeRate_e_barrel_ERA=CMS_bbwwCH_FakeRate_e_barrel_BIN_ERA\n"""
name_changes_norm ="CMS_bbwwCH_fakes_norm=CMS_bbwwCH_fakes_norm_CH_BIN_ERA"

counter = 0
for year in ["2016", "2017", "2018"] :
  for key in channel:
    for ch in channel[key] :
        if counter > 0 : continue
        print(key, ch[0], ch[1])
        base = datacards.replace("BIN", ch[0]).replace("CH", key).replace("ERA", year)
        name_changes_loc = name_changes.replace("BIN", ch[1]).replace("CH", key).replace("ERA", year)
        name_changes_norm_loc = name_changes_norm.replace("BIN", ch[1]).replace("CH", key).replace("ERA", year)

        for type in ["fake_shape_uncorr", "fake_uncorr"] :
            dir_fake_shape_uncorr = "%s/%s" % (base, type)
            if not os.path.exists(dir_fake_shape_uncorr) :
                runCombineCmd("mkdir %s" % dir_fake_shape_uncorr)

            filesyst_loc = "%s/%s/filesyst.txt"  % (base, type)
            ff = open(filesyst_loc, "w")
            ff.write(unicode(name_changes_loc))
            if type == "fake_uncorr" :
                ff.write(unicode(name_changes_norm_loc))
            ff.close()
            print("done %s" % filesyst_loc)

            runCombineCmd("rename_parameters.py %s/datacard.txt %s -d %s/%s/" % (base, filesyst_loc, base, type))
