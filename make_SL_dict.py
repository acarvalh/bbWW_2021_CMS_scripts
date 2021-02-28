#!/usr/bin/env python
import os, subprocess, sys
workingDir = os.getcwd()
import os, re, shlex
from ROOT import *
import numpy as np
import array as arr
from math import sqrt, sin, cos, tan, exp
import glob

from subprocess import Popen, PIPE
from io import open

from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
parser = ArgumentParser(
    description=__doc__, formatter_class=ArgumentDefaultsHelpFormatter
)
parser.add_argument(
    "--fitdiag_folder",
    dest="fitdiag_folder",
    help="Folder that contain the fitdiagnosis.root file(s)",
    )
parser.add_argument(
    "--output_dict",
    dest="output_dict",
    help="Full path for output Dictionary",
    )
args = parser.parse_args()


list_SL_cards = [
    [
        "DY",
        ["DY_boosted", "DY_resolved"],
        "[['boosted'], ['resolved']]",
        "[3, 13]",
        "DY node"
    ],
    [
        "HH_boosted",
        ["HH_boosted"],
        "[ [' '] ]",
        "[2.5]",
        "HH_boosted"
    ],
    [
        "HH_resolved_1b",
        ["HH_resolved_1b"],
        "[ [' ']]",
        "[2.5]",
        "HH_resolved_1b"
    ],
    [
        "HH_resolved_2b_nonvbf",
        [ "HH_resolved_2b_nonvbf"],
        "[ [' '] ]",
        "[2.5]",
        "HH_resolved_2b_nonvbf"
    ],
    [
        "HH_resolved_2b_vbf",
        [ "HH_resolved_2b_vbf"],
        "[ [' ']]",
        "[2.5]",
        "HH_resolved_2b_vbf"
    ],

    [
        "SingleTop",
        ["SingleTop_boosted", "SingleTop_resolved"],
        "[['boosted'], ['resolved']]",
        "[3, 13]",
        "ST node"
    ],
    [
        "TT",
        ["TT_boosted", "TT_resolved"],
        "[ ['boosted'], ['resolved']]",
        "[3, 13]",
        "TT node"
    ],
    [
        "W_other",
        ["W_boosted", "W_resolved"],
        "[['boosted'], ['resolved']]",
        "[5,15]",
        "Wjets  node"
    ],
    [
        "Other",
        ["Other"],
        "[[' ']]",
        "[5]",
        "others node"
    ],
]
fitdiagDL = args.fitdiag_folder

dictionary = args.output_dict #"%s/dict_SL.dat" % fitdiagDL
ff = open(dictionary, "w")
ff.write(unicode('{\n'))

for tt, teste_class in enumerate(list_SL_cards) :
    if "HH" in teste_class[0] :
        continue
    for ee, era in enumerate([2016, 2017, 2018]) :
        print(teste_class[0])
        #if not era == 2016 :
        #    continue
        if teste_class[0] == "DY" and era == 2018 :
            continue
        # inputs and legends
        ff.write(unicode("    '%s_%s' : {\n" % (teste_class[0], str(era))))
        ff.write(unicode("        'fitdiagnosis'       : '%s/fitDiagnostics_shapes_combine_%s_%s.root',\n" % (fitdiagDL, teste_class[0], str(era)) ))
        ff.write(unicode("        'bin_name_original'  : 'none',\n" ))
        ff.write(unicode("        'datacard_original'  : 'none',\n" ))
        ff.write(unicode("        'era'                : %s ,\n" % str(era) ))
        ff.write(unicode("        'header_legend'          : '%s',\n"  % teste_class[4] ))

        # plot dimensions
        plot_dimensions = """        'minY'               : 0.1,
        'maxY'               : 100000000000.,
        'minYerr'            : -0.28,
        'maxYerr'            : 0.28,
        'useLogPlot'         : True,
        'labelX'             : 'MVA bin #',
        'number_columns_legend' : 3,\n"""
        ff.write(unicode(plot_dimensions))

        # categories being lined up in the plot
        align_cats_string = "        'align_cats' : ["
        for catsbins in teste_class[1] :
            align_cats_string  = align_cats_string + "'" + catsbins + "_" +str(era) + "',"
        align_cats_string = align_cats_string + "],\n"
        ff.write(unicode(align_cats_string ))
        ff.write(unicode("        'align_cats_labels' : %s,\n" % teste_class[2] ))
        ff.write(unicode("        'align_cats_labelsX' : %s,\n" % teste_class[3] ))
        ff.write(unicode("        'cats_labels_height' : 1000000.,\n" ))

        bkg_dict = """        'procs_plot_options_bkg' : OrderedDict(
            [
            ('Other_bbWW',  {'color' : 205, 'fillStype'   : 1001, 'label' : 'others'           , 'make border' : True}),
            ('VV',          {'color' : 823, 'fillStype'   : 1001, 'label' : 'ZZ + WZ'          , 'make border' : True}),
            ('VVV',         {'color' : 6, 'fillStype'   : 1001, 'label' : 'VVV'          , 'make border' : True}),
            ('ST',          {'color' : 822, 'fillStype' : 1001, 'label' : 'single top'         , 'make border' : True}),
            ('Fakes',       {'color' :  12, 'fillStype' : 3345, 'label' : 'Fakes'  , 'make border' : True}),
            ('DY',          {'color' : 221, 'fillStype' : 1001, 'label' : 'DY'         , 'make border' : True}),
            ('WJets',       {'color' : 5, 'fillStype' : 1001, 'label' : 'W + jets'   , 'make border' : True}),
            ('TT',          {'color' : 17, 'fillStype'  : 1001, 'label' : 't#bar{t} + jets'   , 'make border' : True})
            ]
        ),\n"""
        ff.write(unicode(bkg_dict))

        sig_dict = """       'procs_plot_options_sig' : OrderedDict(
            [
            ('ggHH_kl_1_kt_1' ,      {'color' : 5, 'fillStype'  : 3351, 'label' : 'GGF HH SM', 'scaleBy' : 1.}),
            ('ggHH_kl_5_kt_1',       {'color' : 221, 'fillStype'  : 3351, 'label' : 'GGF HH #kappa#lambda = 5', 'scaleBy' : 1.}),
            ('ggHH_kl_2p45_kt_1',    {'color' : 2, 'fillStype'  : 3351, 'label' : 'GGF HH #kappa#lambda = 2.45', 'scaleBy' : 1.}),
            ('qqHH_CV_1_C2V_1_kl_1', {'color' : 8, 'fillStype'  : 3351, 'label' : 'VBF HH SM', 'scaleBy' : 1.}),
            ]
        ),\n"""
        ff.write(unicode(sig_dict))

        ff.write(unicode("    },\n" ))

ff.write(unicode('}\n'))
ff.close()

print("created %s" % dictionary)
