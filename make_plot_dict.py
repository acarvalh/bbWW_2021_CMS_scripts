#!/usr/bin/env python
import os, subprocess, sys
from subprocess import Popen, PIPE


"""
Examples of commands:

python /afs/cern.ch/work/a/acarvalh/HH_inference/bbWW_2021_CMS_scripts/make_plot_dict.py \
--fitdiag_folder /eos/user/a/acarvalh/bbWW_fullRun2_results/round3_results/prefit_plots/TLL/fitdiag2/  \
--output_dict /eos/user/a/acarvalh/bbWW_fullRun2_results/round3_results/prefit_plots/TLL/dict_SL_bkg.dat \
--only_bkg --only_chanel sl

python dhi/scripts/postfit_plots.py \
--output_folder /eos/user/a/acarvalh/bbWW_fullRun2_results/round3_results/prefit_plots/TLL/plots/SL/ \
--plot_options_dict /eos/user/a/acarvalh/bbWW_fullRun2_results/round3_results/prefit_plots/TLL/dict_SL_bkg.dat \
--unblind

"""
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
parser = ArgumentParser(
    description=__doc__, formatter_class=ArgumentDefaultsHelpFormatter
)
parser.add_argument(
    "--fitdiag_folder",
    dest="fitdiag_folder",
    help="Folder that contain the fitdiagnosis.root file(s) as done by run_prefit_freeze3_TLL.py (on this folder) with law/law_collect optioon OR the fitDiagnostics.root of the global fit, but with bin naming convetions as done also by run_prefit_freeze3_TLL.py ",
    )
parser.add_argument(
    "--output_dict",
    dest="output_dict",
    help="Full path for output Dictionary",
    )
parser.add_argument(
    "--university",
    dest="university",
    help="To know which naming convention of files to assume. Options TLL , RTW, LLR",
    default="TLL"
    )
parser.add_argument(
    "--only_chanel",
    dest="only_chanel",
    help="Can be 'sl' or 'dl'. dictionary only with that channel.",
    default="none"
    )
parser.add_argument(
    "--only_bkg",
    action="store_true",
    dest="only_bkg",
    help="dictionary only with bkg nodes -- to unblind",
    default=False
    )
parser.add_argument(
    "--only_sig",
    action="store_true",
    dest="only_sig",
    help="dictionary only with signal nodes -- to not unblind",
    default=False
    )
parser.add_argument(
    "--only_era",
    dest="only_era",
    help="If you give an era, it will make only this one.",
    default="none"
    )
args = parser.parse_args()
fitdiagDL = args.fitdiag_folder
dictionary = args.output_dict
only_bkg = args.only_bkg
only_sig = args.only_sig
only_chanel = args.only_chanel

if args.university == "TLL" :
    list_plots = [
        [
            "dynode",
            [ "PREFIX_ERA_DY_boosted", "PREFIX_ERA_DY_resolved"], # name of bin
            "[ ['boosted'], ['resolved'] ]", # label to write on plot, comas in the inner brackets will make new lines
            "[5, 15]",                       # x-position of that label
            "DY node"              # label of plot (can be latex)
        ],
        [
            "wjetsnode",
            [ "PREFIX_ERA_W_boosted", "PREFIX_ERA_W_resolved"],
            "[ ['boosted'], ['resolved'] ]",
            "[5, 15]",
            "Wjets node"
        ],
        [
            "stnode",
            ["PREFIX_ERA_SingleTop_boosted", "PREFIX_ERA_SingleTop_resolved"],
            "[ ['boosted'], ['resolved'] ]",
            "[5, 15]",
            "ST node"
        ],
        [
            "othernode",
            ["PREFIX_ERA_Other"], #
            "[ ['']]",
            "[0]",
            "other BKG node"
        ],
        [
            "ttnode",
            ["PREFIX_ERA_TT_boosted", "PREFIX_ERA_TT_resolved"],
            "[ ['boosted'], ['resolved'] ]",
            "[5, 15]",
            "TT node"
        ],
        [
            "GGFnode",
            ["PREFIX_ERA_HH_boosted", "PREFIX_ERA_HH_resolved_1b_nonvbf", "PREFIX_ERA_HH_resolved_2b_nonvbf",],
            "[ ['res 1b'], ['res 2b'], ['b.']]",
            "[3.5, 17, 28]",
            "HH node (GGF categories)"
        ],
        [
            "VBFnode",
            ["PREFIX_ERA_HH_resolved_1b_vbf", "PREFIX_ERA_HH_resolved_2b_vbf",], #
            "[ ['res 1b'], ['res 2b']]",
            "[5, 22]",
            "HH node (VBF categories)"
        ],
    ]

ff = open(dictionary, "w")
ff.write(unicode('{\n'))

for channel in ["dl", "sl"] :
  if not only_chanel == "none" :
      if not only_chanel == channel :
          continue

  for teste_class in list_plots :

    if channel == "dl" :
        prefix = "SM_lbn_2l_0tau"
    if channel == "sl" :
        prefix = "SM_lbn_1l_0tau"
        if teste_class[0] == "wjetsnode" :
            continue

    if only_bkg :
        if teste_class[0] in ["GGFnode", "VBFnode"] :
            continue
    if only_sig :
        if not teste_class[0] in ["GGFnode", "VBFnode"] :
            continue

    for era in [ "2016", "2017", "2018"] :
        if not args.only_era == "none" :
            if not era == args.only_era :
                continue

        skiped = False
        for bin in teste_class[1] :
            if 0 > 1 : skiped = True
            if channel == "dl" and teste_class[0] == "ttnode" and era == "2017" : skiped = True
            if channel == "dl" and teste_class[0] == "ttnode" and era == "2016" : skiped = True
            if channel == "dl" and  teste_class[0] == "wjetsnode" and era == "2016" : skiped = True
            if channel == "dl" and  teste_class[0] == "wjetsnode" and era == "2017" : skiped = True
            if channel == "dl" and  teste_class[0] == "wjetsnode" and era == "2018" : skiped = True
            if channel == "sl" and teste_class[0] == "ttnode" and era == "2016" : skiped = True
            if channel == "sl" and teste_class[0] == "ttnode" and era == "2017" : skiped = True
            if channel == "sl" and teste_class[0] == "ttnode" and era == "2018" : skiped = True
            if channel == "sl" and teste_class[0] == "stnode" and era == "2018" : skiped = True
            if channel == "sl" and teste_class[0] == "stnode" and era == "2017" : skiped = True
            if channel == "sl" and teste_class[0] == "stnode" and era == "2016" : skiped = True
        if skiped : continue

        if ".root" in fitdiagDL :
            local_merged = fitdiagDL
        else :
            # hadd the fitdiags to draw toguether
            # as we did one by card
            fit_hadd = "fitdiagnostics_hadd_%s_%s_%s.root" % (prefix, era, teste_class[0])
            local_merged = "%s/%s" % (fitdiagDL,  fit_hadd)
            print(only_chanel, channel, prefix, fit_hadd)
            if not os.path.exists(local_merged) :
                cmd = "hadd %s " % (fit_hadd)
                for bin in teste_class[1] :
                    bin = bin.replace("PREFIX", prefix).replace("ERA", era)
                    cmd += " fitdiagnostics_%s.root" % (bin)
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
        plot_dimensions = """        'minY'               : 0.001,
        'maxY'               : 1000000000000.,
        'minYerr'            : -1.28,
        'maxYerr'            : 1.28,
        'useLogPlot'         : True,
        'labelX'             : 'MVA bin #',
        'number_columns_legend' : 3,\n"""
        ff.write(unicode(plot_dimensions))

        # categories being lined up in the plot
        align_cats_string = "        'align_cats' : ["
        for catsbins in teste_class[1] :
            if args.university == "TLL" :
                catsbins = bin.replace("PREFIX", prefix).replace("ERA", era)
            align_cats_string  =  align_cats_string + "'" + catsbins + "',"
        align_cats_string = align_cats_string + "],\n"
        ff.write(unicode(align_cats_string ))
        #ff.write(unicode("        'align_cats'        : %s,\n" % teste_class[1] ))
        ff.write(unicode("        'align_cats_labels' : %s,\n" % teste_class[2] ))
        ff.write(unicode("        'align_cats_labelsX' : %s,\n" % teste_class[3] ))
        ff.write(unicode("        'cats_labels_height' : 1000000.,\n" ))

        bkg_dict = """        'procs_plot_options_bkg' : OrderedDict(
            [
            ('Other_bbWW',  {'color' : 205, 'fillStype' : 1001, 'label' : 'others',          'make border' : True}),
            ('VV',          {'color' : 208, 'fillStype' : 1001, 'label' : 'none',            'make border' : False}),
            ('vvv',         {'color' : 208, 'fillStype' : 1001, 'label' : 'VVV + VV',        'make border' : True}),
            ('VVV',         {'color' : 208, 'fillStype' : 1001, 'label' : 'VVV + VV',        'make border' : True}),
            ('ttZ',         {'color' : 9, 'fillStype' : 1001, 'label' : 'none',              'make border' : False}),
            ('ttW',         {'color' : 9, 'fillStype' : 1001, 'label' : 'none',              'make border' : False}),
            ('ttVV',        {'color' : 9, 'fillStype' : 1001, 'label' : 'ttW + ttZ + ttVV',  'make border' : True}),
            ('Fakes',       {'color' :  12, 'fillStype' : 3345, 'label' : 'Fakes',           'make border' : True}),
            ('DY',          {'color' : 221, 'fillStype' : 1001, 'label' : 'DY',              'make border' : True}),
            ('data_DY',          {'color' : 221, 'fillStype' : 1001, 'label' : 'DY',              'make border' : True}),
            ('ST',          {'color' : 822, 'fillStype' : 1001, 'label' : 'single top',      'make border' : True}),
            ('WJets',       {'color' : 209, 'fillStype' : 1001, 'label' : 'W + jets',          'make border' : True}),
            ('TT',          {'color' : 17, 'fillStype'  : 1001, 'label' : 't#bar{t} + jets', 'make border' : True}),
            ]
        ),\n"""
        ff.write(unicode(bkg_dict))

        sig_dict = """       'procs_plot_options_sig' : OrderedDict(
            [
            ('ggHH_kl_1_kt_1' ,      {'color' : 5,   'fillStype'  : 3351, 'label' : 'GGF SM',                   'scaleBy' : 1.}),
            ('ggHH_kl_5_kt_1',       {'color' : 6, 'fillStype'  : 3351, 'label' : 'GGF #kappa#lambda = 5',    'scaleBy' : 1.}),
            ('ggHH_kl_2p45_kt_1',    {'color' : 2,   'fillStype'  : 3351, 'label' : 'GGF #kappa#lambda = 2.45', 'scaleBy' : 1.}),
            ('qqHH_CV_1_C2V_1_kl_1', {'color' : 8,   'fillStype'  : 3351, 'label' : 'VBF SM',                   'scaleBy' : 1.}),
            ('qqHH_CV_1_C2V_2_kl_1', {'color' : 4,   'fillStype'  : 3351, 'label' : 'VBF c2V = 2',              'scaleBy' : 1.}),
            ]
        ),\n"""
        ff.write(unicode(sig_dict))

        ff.write(unicode("    },\n" ))

ff.write(unicode('}\n'))
ff.close()

print("created %s" % dictionary)
