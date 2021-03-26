#!/usr/bin/env bash

setup() {
  export task_name='bbWW_round2'

  export DHI_STORE='/eos/cms/store/group/phys_higgs/nonresonant_HH/bbWW'
  export DHI_LOCAL_SCHEDULER='False'

  export SL='/afs/cern.ch/work/m/mfackeld/DiHiggs/public/datacards/round2/sl_*/*/datacard.txt'
  export DL='/afs/cern.ch/work/m/mfackeld/DiHiggs/public/datacards/round2/dl_*/*/datacard.txt'
  export ALL='/afs/cern.ch/work/m/mfackeld/DiHiggs/public/datacards/round2/*/*/datacard.txt'

  export SL_HHnodes_res2b='/afs/cern.ch/work/m/mfackeld/DiHiggs/public/datacards/round2/sl_*/*resolved_2b*_NLO/datacard.txt'
  export DL_HHnodes_res2b='/afs/cern.ch/work/m/mfackeld/DiHiggs/public/datacards/round2/dl_*/*resolved_2b*_NLO/datacard.txt'
  export ALL_HHnodes_res2b='/afs/cern.ch/work/m/mfackeld/DiHiggs/public/datacards/round2/*/*resolved_2b*_NLO/datacard.txt'

  export SL_HHnodes_res='/afs/cern.ch/work/m/mfackeld/DiHiggs/public/datacards/round2/sl_*/*resolved_*_NLO/datacard.txt'
  export DL_HHnodes_res='/afs/cern.ch/work/m/mfackeld/DiHiggs/public/datacards/round2/dl_*/*resolved_*_NLO/datacard.txt'
  export ALL_HHnodes_res='/afs/cern.ch/work/m/mfackeld/DiHiggs/public/datacards/round2/*/*resolved_*_NLO/datacard.txt'

  export SL_HHnodes='/afs/cern.ch/work/m/mfackeld/DiHiggs/public/datacards/round2/sl_*/*_NLO/datacard.txt'
  export DL_HHnodes='/afs/cern.ch/work/m/mfackeld/DiHiggs/public/datacards/round2/dl_*/*_NLO/datacard.txt'
  export ALL_HHnodes='/afs/cern.ch/work/m/mfackeld/DiHiggs/public/datacards/round2/*/*_NLO/datacard.txt'

  export SL_2016='/afs/cern.ch/work/m/mfackeld/DiHiggs/public/datacards/round2/sl_2016/*/datacard.txt'
  export DL_2016='/afs/cern.ch/work/m/mfackeld/DiHiggs/public/datacards/round2/dl_2016/*/datacard.txt'
  export ALL_2016='/afs/cern.ch/work/m/mfackeld/DiHiggs/public/datacards/round2/*_2016/*/datacard.txt'

  export SL_2017='/afs/cern.ch/work/m/mfackeld/DiHiggs/public/datacards/round2/sl_2017/*/datacard.txt'
  export DL_2017='/afs/cern.ch/work/m/mfackeld/DiHiggs/public/datacards/round2/dl_2017/*/datacard.txt'
  export ALL_2017='/afs/cern.ch/work/m/mfackeld/DiHiggs/public/datacards/round2/*_2017/*/datacard.txt'

  export SL_2018='/afs/cern.ch/work/m/mfackeld/DiHiggs/public/datacards/round2/sl_2018/*/datacard.txt'
  export DL_2018='/afs/cern.ch/work/m/mfackeld/DiHiggs/public/datacards/round2/dl_2018/*/datacard.txt'
  export ALL_2018='/afs/cern.ch/work/m/mfackeld/DiHiggs/public/datacards/round2/*_2018/*/datacard.txt'

  export SL_TLL_2016='/afs/cern.ch/work/s/snandan/public/2016/*txt'
  export SL_TLL_2017='/afs/cern.ch/work/s/snandan/public/2017/*txt'
  export SL_TLL_2018='/afs/cern.ch/work/s/snandan/public/2018/*txt'
  export SL_TLL='/afs/cern.ch/work/s/snandan/public/201*/*txt'

  #########################
  # those are for launch postfit plots -- naming is needed

  export SL_BKG_only='/afs/cern.ch/work/a/acarvalh/public/to_HH_bbWW/freze2_March19/round1/datacard_sl_BKGonly.txt'
  export DL_BKG_only='/afs/cern.ch/work/a/acarvalh/public/to_HH_bbWW/freze2_March19/round2/datacards/datacard_dl_BKGonly.txt'
  export ALL_BKG_only='/afs/cern.ch/work/a/acarvalh/public/to_HH_bbWW/freze2_March19/round2/datacards/datacard_BKGonly.txt'


  export SL_plots='/afs/cern.ch/work/a/acarvalh/public/to_HH_bbWW/freze2_March19/round2/datacards/datacard_sl.txt'
  export DL_plots='/afs/cern.ch/work/a/acarvalh/public/to_HH_bbWW/freze2_March19/round2/datacards/datacard_dl.txt'
  export ALL_plots='/afs/cern.ch/work/a/acarvalh/public/to_HH_bbWW/freze2_March19/round2/datacards/datacard.txt'


}

action() {
    if setup '$@'; then
        echo -e '\x1b[0;49;35Paths bbWW roound1 successfully setup\x1b[0m'
        return '0'
    else
        local code='$?'
        echo -e '\x1b[0;49;31msetup failed with code $code\x1b[0m'
        return '$code'
    fi
}
action '$@'
