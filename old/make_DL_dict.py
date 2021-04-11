#!/usr/bin/env python
import os, subprocess, sys
from subprocess import Popen, PIPE

#
"""
commands examples:

============
HH nodes -- draw blinded

python /eos/user/a/acarvalh/bbWW_fullRun2_results/round3_results/prefit_plots/make_DL_dict_Aa.py \
--fitdiag_folder /eos/user/a/acarvalh/bbWW_fullRun2_results/round3_results/prefit_plots/DL_2018_DY_mc_Aa/fitdiag/  \
--output_dict /eos/user/a/acarvalh/bbWW_fullRun2_results/round3_results/prefit_plots/DL_2018_DY_mc_Aa/dict_DL_HH.dat \
--only_sig --only_era 2018

python dhi/scripts/postfit_plots.py \
--output_folder /eos/user/a/acarvalh/bbWW_fullRun2_results/round3_results/prefit_plots/DL_2018_DY_mc_Aa/plots/ \
--plot_options_dict /eos/user/a/acarvalh/bbWW_fullRun2_results/round3_results/prefit_plots/DL_2018_DY_mc_Aa/dict_DL_HH.dat

============
BKG nodes -- draw unblinded

python /eos/user/a/acarvalh/bbWW_fullRun2_results/round3_results/prefit_plots/make_DL_dict_Aa.py \
--fitdiag_folder /eos/user/a/acarvalh/bbWW_fullRun2_results/round3_results/prefit_plots/DL_2018_DY_mc_Aa/fitdiag/  \
--output_dict /eos/user/a/acarvalh/bbWW_fullRun2_results/round3_results/prefit_plots/DL_2018_DY_mc_Aa/dict_DL_bkg.dat \
--unblind_bkg --only_era 2018

python dhi/scripts/postfit_plots.py \
--output_folder /eos/user/a/acarvalh/bbWW_fullRun2_results/round3_results/prefit_plots/DL_2018_DY_mc_Aa/plots/ \
--plot_options_dict /eos/user/a/acarvalh/bbWW_fullRun2_results/round3_results/prefit_plots/DL_2018_DY_mc_Aa/dict_DL_bkg.dat \
--unblind

"""
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
    default="none"
    )
parser.add_argument(
    "--only_era",
    dest="only_era",
    help="If you gine an era, it will makee the dict to draw only this one.",
    default="none"
    )
parser.add_argument(
    "--unblind_bkg",
    action="store_true",
    dest="unblind_bkg",
    help="dictionary only with bkg nodes -- to unblind",
    default=False
    )
parser.add_argument(
    "--only_sig",
    action="store_true",
    dest="only_sig",
    help="dictionary only with bkg nodes -- to unblind",
    default=False
    )
args = parser.parse_args()
fitdiagDL = args.fitdiag_folder
dictionary = args.output_dict
unblind_bkg = args.unblind_bkg
only_sig = args.only_sig

list_plots = [
    [
        "DY_VVVnode",
        ["all_incl_sr_type2_dy_vv"], # name of bin
        "[[' ']]",                   # label to write on plot, comas in the inner brackets will make new lines
        "[0]",                       # x-position of that label
        "DY + VVV node"              # label of plot (can be latex)
    ],
    [
        "TT_ST_TTVX_Rarenode",
        ["all_incl_sr_type2_other"],
        "[ [' '] ]",
        "[2.5]",
        "TT + ST + TTVX + Rare node"
    ],
    [
        "GGFnode",
        ["all_resolved_1b_sr_dnn_node_class_HHGluGlu_NLO", "all_resolved_2b_sr_dnn_node_class_HHGluGlu_NLO", "all_boosted_1b_sr_dnn_node_class_HHGluGlu_NLO"], #
        "[ ['res 1b'], ['res 2b'], ['b.'],]", #
        "[6, 21, 32]", #
        "GGF HH node"
    ],
    [
        "VBFnode",
        ["all_resolved_1b_sr_dnn_node_class_HHVBF_NLO", "all_resolved_2b_sr_dnn_node_class_HHVBF_NLO", "all_boosted_1b_sr_dnn_node_class_HHVBF_NLO"], #
        "[ ['res 1b'], ['res 2b'], ['b.']]", #
        "[4, 16, 24]",
        "VBF HH node"
    ],
    [
        "Hnode",
        ["all_resolved_1b_sr_dnn_node_H", "all_resolved_2b_sr_dnn_node_H", "all_boosted_1b_sr_dnn_node_H", ],
        "[['res 1b'], ['res 2b'], ['boosted']]",
        "[2, 10, 17.5]",
        "single H node"
    ],
]

ff = open(dictionary, "w")
ff.write(unicode('{\n'))

for teste_class in list_plots :
    for era in [ "2016", "2017", "2018"] :
        if not args.only_era == "none" :
            if not era == args.only_era :
                continue

        if unblind_bkg :
            if teste_class[0] in ["GGFnode", "VBFnode"] :
                continue
        if only_sig :
            if not teste_class[0] in ["GGFnode", "VBFnode"] :
                continue

        skiped = False
        for bin in teste_class[1] :
            if 0 > 1 : skiped = True
        if skiped : continue


        if ".root" in fitdiagDL :
            local_merged = fitdiagDL
        else :
            # hadd the fitdiags to draw toguether
            local_merged = "%s/fitDiagnostics_shapes_combine_hadd_dl_%s_%s.root" % (fitdiagDL, era, teste_class[0])
            if not os.path.exists(local_merged) :
                cmd = "hadd fitDiagnostics_shapes_combine_hadd_dl_%s_%s.root " % (era, teste_class[0])
                for bin in teste_class[1] :
                    cmd += " fitDiagnostics_shapes_combine_dl_%s_%s.root" % (era, bin)
                print ("cd %s ; %s; cd -" % (fitdiagDL, cmd))
                proc = subprocess.Popen(["cd %s ; %s" % (fitdiagDL, cmd)],shell=True,stdout=subprocess.PIPE)
                out = proc.stdout.read()
                print(" ============ ")
            else :
                print ("file %s" % local_merged )

        # inputs and legends
        ff.write(unicode("    '%s_%s' : {\n" % (teste_class[0], str(era))))
        ff.write(unicode("        'fitdiagnosis'       : '%s',\n" % (local_merged) ))
        ff.write(unicode("        'bin_name_original'  : 'none',\n" ))
        ff.write(unicode("        'datacard_original'  : 'none',\n" ))
        ff.write(unicode("        'header_legend'      : '%s',\n" % teste_class[4] ))
        ff.write(unicode("        'era'                : %s ,\n" % str(era) ))
        ff.write(unicode("        'merged_eras_fit'    : False ,\n" ))

        # plot dimensions
        if teste_class[0] in ["GGFnode", "VBFnode"] :
            plot_dimensions = """        'minY'               : 0.001,
            'maxY'               : 10000000000.,
            'minYerr'            : -1.01,
            'maxYerr'            : 1.01,
            'useLogPlot'         : True,
            'labelX'             : 'MVA bin #',
            'number_columns_legend' : 3,\n"""
            ff.write(unicode("        'cats_labels_height' : 10000.,\n" ))
        else :
            plot_dimensions = """        'minY'               : 0.001,
            'maxY'               : 100000000000.,
            'minYerr'            : -0.51,
            'maxYerr'            : 0.51,
            'useLogPlot'         : True,
            'labelX'             : 'MVA bin #',
            'number_columns_legend' : 3,\n"""
            ff.write(unicode("        'cats_labels_height' : 100000.,\n" ))
        ff.write(unicode(plot_dimensions))

        # categories being lined up in the plot
        align_cats_string = "        'align_cats' : ["
        for catsbins in teste_class[1] :
            align_cats_string  =  align_cats_string + "'" + "dl_" +str(era) + "_" + catsbins + "',"
        align_cats_string = align_cats_string + "],\n"
        ff.write(unicode(align_cats_string ))
        #ff.write(unicode("        'align_cats'        : %s,\n" % teste_class[1] ))
        ff.write(unicode("        'align_cats_labels' : %s,\n" % teste_class[2] ))
        ff.write(unicode("        'align_cats_labelsX' : %s,\n" % teste_class[3] ))

        bkg_dict = """        'procs_plot_options_bkg' : OrderedDict(
            [
            ('Other_bbWW',  {'color' : 205, 'fillStype' : 1001, 'label' : 'others',          'make border' : True}),
            ('VV',          {'color' : 208, 'fillStype' : 1001, 'label' : 'none',            'make border' : False}),
            ('vvv',         {'color' : 208, 'fillStype' : 1001, 'label' : 'VVV + VV',        'make border' : True}),
            ('ttZ',         {'color' : 9, 'fillStype' : 1001, 'label' : 'none',              'make border' : False}),
            ('ttW',         {'color' : 9, 'fillStype' : 1001, 'label' : 'none',              'make border' : False}),
            ('ttVV',        {'color' : 9, 'fillStype' : 1001, 'label' : 'ttW + ttZ + ttVV',  'make border' : True}),
            ('ST',          {'color' : 822, 'fillStype' : 1001, 'label' : 'single top',      'make border' : True}),
            ('Fakes',       {'color' :  12, 'fillStype' : 3345, 'label' : 'Fakes',           'make border' : True}),
            ('DY',          {'color' : 221, 'fillStype' : 1001, 'label' : 'DY',              'make border' : True}),
            ('dy',          {'color' : 221, 'fillStype' : 1001, 'label' : 'DY',              'make border' : True}),
            ('WJets',       {'color' : 5, 'fillStype' : 1001, 'label' : 'W + jets',          'make border' : True}),
            ('TT',          {'color' : 17, 'fillStype'  : 1001, 'label' : 't#bar{t} + jets', 'make border' : True}),
            ]
        ),\n"""
        ff.write(unicode(bkg_dict))

        sig_dict = """       'procs_plot_options_sig' : OrderedDict(
            [
            ('ggHH_kl_1_kt_1' ,      {'color' : 5,   'fillStype'  : 3351, 'label' : 'GGF SM',                   'scaleBy' : 1.}),
            ('ggHH_kl_5_kt_1',       {'color' : 221, 'fillStype'  : 3351, 'label' : 'GGF #kappa#lambda = 5',    'scaleBy' : 1.}),
            ('ggHH_kl_2p45_kt_1',    {'color' : 2,   'fillStype'  : 3351, 'label' : 'GGF #kappa#lambda = 2.45', 'scaleBy' : 1.}),
            ('qqHH_CV_1_C2V_1_kl_1', {'color' : 8,   'fillStype'  : 3351, 'label' : 'VBF SM',                   'scaleBy' : 1.}),
            ('qqHH_CV_1_C2V_2_kl_1', {'color' : 6,   'fillStype'  : 3351, 'label' : 'VBF c2V = 2',              'scaleBy' : 1.}),
            ]
        ),\n"""
        ff.write(unicode(sig_dict))

        ff.write(unicode("    },\n" ))

ff.write(unicode('}\n'))
ff.close()

print("created %s" % dictionary)
