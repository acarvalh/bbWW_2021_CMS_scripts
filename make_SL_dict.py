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

#
list_SL_cards = [
    [
        "DY",
        ["DY_boosted", "DY_resolved"],
        "[[\"boosted\"], [\"resolved\"]]",
        "[3, 13]",
        "DY node"
    ],
    [
        "HH_boosted",
        ["HH_boosted"],
        "[ [\" \"] ]",
        "[2.5]",
        "HH_boosted"
    ],
    [
        "HH_resolved_1b",
        ["HH_resolved_1b"],
        "[ [\" \"]]",
        "[2.5]",
        "HH_resolved_1b"
    ],
    [
        "HH_resolved_2b_nonvbf",
        [ "HH_resolved_2b_nonvbf"],
        "[ [\" \"] ]",
        "[2.5]",
        "HH_resolved_2b_nonvbf"
    ],
    [
        "HH_resolved_2b_vbf",
        [ "HH_resolved_2b_vbf"],
        "[ [\" \"]]",
        "[2.5]",
        "HH_resolved_2b_vbf"
    ],

    [
        "SingleTop",
        ["SingleTop_boosted", "SingleTop_resolved"],
        "[[\"boosted\"], [\"resolved\"]]",
        "[3, 13]",
        "ST node"
    ],
    [
        "TT",
        ["TT_boosted", "TT_resolved"],
        "[ [\"boosted\"], [\"resolved\"]]",
        "[3, 13]",
        "TT node"
    ],
    [
        "W_other",
        ["W_boosted", "W_resolved"],
        "[[\"boosted\"], [\"resolved\"]]",
        "[5,15]",
        "Wjets  node"
    ],
    [
        "Other",
        ["Other"],
        "[[\" \"]]",
        "[5]",
        "others node"
    ],
]
fitdiagDL = "/afs/cern.ch/work/a/acarvalh/public/to_HH_bbWW/datacard_TLL_27Jan2020/fitdiag/"

"""

hadd fitDiagnostics_shapes_combine_DY_2018.root fitDiagnostics_shapes_combine_DY_boosted_2018.root fitDiagnostics_shapes_combine_DY_resolved_2018.root

hadd fitDiagnostics_shapes_combine_HH_2018.root fitDiagnostics_shapes_combine_HH_boosted_2018.root fitDiagnostics_shapes_combine_HH_resolved_1b_2018.root fitDiagnostics_shapes_combine_HH_resolved_2b_nonvbf_2018.root fitDiagnostics_shapes_combine_HH_resolved_2b_vbf_2018.root

hadd fitDiagnostics_shapes_combine_SingleTop_TT_2018.root fitDiagnostics_shapes_combine_SingleTop_boosted_2018.root fitDiagnostics_shapes_combine_SingleTop_resolved_2018.root fitDiagnostics_shapes_combine_TT_boosted_2018.root fitDiagnostics_shapes_combine_TT_resolved_2018.root

hadd fitDiagnostics_shapes_combine_SingleTop_2018.root fitDiagnostics_shapes_combine_SingleTop_boosted_2018.root fitDiagnostics_shapes_combine_SingleTop_resolved_2018.root

hadd fitDiagnostics_shapes_combine_TT_2018.root fitDiagnostics_shapes_combine_TT_boosted_2018.root fitDiagnostics_shapes_combine_TT_resolved_2018.root

hadd fitDiagnostics_shapes_combine_W_2018.root fitDiagnostics_shapes_combine_W_boosted_2018.root fitDiagnostics_shapes_combine_W_resolved_2018.root

hadd fitDiagnostics_shapes_combine_W_other_2018.root fitDiagnostics_shapes_combine_W_boosted_2018.root fitDiagnostics_shapes_combine_W_resolved_2018.root fitDiagnostics_shapes_combine_Other_2018.root
"""
dictionary = "%s/dict_SL.dat" % fitdiagDL
ff = open(dictionary, "w")
ff.write(unicode('{\n'))

for tt, teste_class in enumerate(list_SL_cards) :
    for ee, era in enumerate([2016, 2017, 2018]) :
        #if tt > 0 : continue
        #if ee > 0 : continue
        print(teste_class[0])
        if era == 2018 :
            continue
        if teste_class[0] == "DY" and era == 2018 :
            continue
        ff.write(unicode("    \"%s_%s\" : {\n" % (teste_class[0], str(era))))
        ff.write(unicode("        \"fitdiagnosis\"       : \"%s/fitDiagnostics_shapes_combine_%s_%s.root\",\n" % (fitdiagDL, teste_class[0], str(era)) ))
        ff.write(unicode("        \"bin_name_original\"  : \"none\",\n" ))
        ff.write(unicode("        \"datacard_original\"  : \"none\",\n" ))
        ff.write(unicode("        \"minY\"               : 0.1,\n" ))
        ff.write(unicode("        \"maxY\"               : 100000000000.,\n" ))
        ff.write(unicode("        \"minYerr\"            : -0.28,\n" ))
        ff.write(unicode("        \"maxYerr\"            : 0.28,\n" ))
        ff.write(unicode("        \"useLogPlot\"         : True,\n" ))
        ff.write(unicode("        \"era\"                : %s ,\n" % str(era) ))
        ff.write(unicode("        \"labelX\"             : \"MVA bin #\",\n" ))
        ff.write(unicode("        \"header_legend\"          : \"%s\",\n"  % teste_class[4] ))
        ff.write(unicode("        \"number_columns_legend\" : 3,\n" ))
        align_cats_string = "        \"align_cats\" : ["
        #ff.write(unicode("        \"align_cats\" : [ \"mumu_%s_%s\", \"emu_%s_%s\", \"ee_%s_%s\"],\n" % (teste_class, str(era), teste_class, str(era), teste_class, str(era)) ))
        for catsbins in teste_class[1] :
            align_cats_string  = align_cats_string + "\"" + catsbins + "_" +str(era) + "\","
        align_cats_string = align_cats_string + "],\n"
        ff.write(unicode(align_cats_string ))

        ff.write(unicode("        \"align_cats_labels\" : %s,\n" % teste_class[2] ))
        ff.write(unicode("        \"align_cats_labelsX\" : %s,\n" % teste_class[3] ))
        ff.write(unicode("        \"cats_labels_height\" : 1000000.,\n" ))
        ff.write(unicode("        \"single_H_major\" : \"ttH_hww\",\n" ))
        ff.write(unicode("        \"procs_plot_options_bkg\" : OrderedDict(\n" ))
        ff.write(unicode("            [\n" ))
        ff.write(unicode("            (\"Other_bbWW\",       {\"color\" : 205, \"fillStype\"   : 1001, \"label\" : \"others\"           , \"make border\" : True}),\n" ))
        ff.write(unicode("            (\"VV\",          {\"color\" : 823, \"fillStype\"   : 1001, \"label\" : \"ZZ + WZ\"          , \"make border\" : True}),\n" ))
        ff.write(unicode("            (\"ST\",         {\"color\" : 822, \"fillStype\" : 1001, \"label\" : \"single top\"         , \"make border\" : True}),\n" ))
        ff.write(unicode("            (\"Fakes\",  {\"color\" :  12, \"fillStype\" : 3345, \"label\" : \"Fakes\"  , \"make border\" : True}),\n" ))
        ff.write(unicode("            (\"DY\",          {\"color\" : 221, \"fillStype\" : 1001, \"label\" : \"DY\"         , \"make border\" : True}),\n" ))
        ff.write(unicode("            (\"WJets\",           {\"color\" : 5, \"fillStype\" : 1001, \"label\" : 'W + jets'   , \"make border\" : True}),\n" ))
        ff.write(unicode("            (\"TT\",          {\"color\" : 17, \"fillStype\"  : 1001, \"label\" : 't#bar{t} + jets'   , \"make border\" : True})\n" ))
        ff.write(unicode("            ]\n" ))
        ff.write(unicode("        ),\n" ))
        ff.write(unicode("        \"procs_plot_options_sig\" : OrderedDict(\n" ))
        ff.write(unicode("            [\n" ))
        ff.write(unicode("            ( \"GGF_SM\",\n" ))
        ff.write(unicode("              {\n" ))
        ff.write(unicode("              \"processes\" : [\"ggHH_kl_1_kt_1_hbbhww\", \"ggHH_kl_1_kt_1_hbbhtt\"],\n" ))
        ff.write(unicode("              \"color\" : 5, \"fillStype\"  : 3351, \"label\" : 'GGF HH SM', \"scaleBy\" : 1.\n" ))
        ff.write(unicode("              }\n" ))
        ff.write(unicode("            ),\n" ))
        ff.write(unicode("            ( \"GGF_kl5\",\n" ))
        ff.write(unicode("              {\n" ))
        ff.write(unicode("              \"processes\" : [\"ggHH_kl_5_kt_1_hbbhww\", \"ggHH_kl_5_kt_1_hbbhtt\"],\n" ))
        ff.write(unicode("              \"color\" : 221, \"fillStype\"  : 3351, \"label\" : 'GGF HH #kappa#lambda = 5', \"scaleBy\" : 1.\n" ))
        ff.write(unicode("              }\n" ))
        ff.write(unicode("            ),\n" ))
        ff.write(unicode("            ( \"VBF_SM\",\n" ))
        ff.write(unicode("              {\n" ))
        ff.write(unicode("              \"processes\" : [\"qqHH_CV_1_C2V_1_kl_1_hbbhtt\", \"qqHH_CV_1_C2V_1_kl_1_hbbhww\"],\n" ))
        ff.write(unicode("              \"color\" : 8, \"fillStype\"  : 3351, \"label\" : 'VBF HH SM', \"scaleBy\" : 1.\n" ))
        ff.write(unicode("              }\n" ))
        ff.write(unicode("            )\n" ))
        ff.write(unicode("            ]\n" ))
        ff.write(unicode("        ),\n" ))
        ff.write(unicode("    },\n" ))


ff.write(unicode('}\n'))
ff.close()

print("created %s" % dictionary)
