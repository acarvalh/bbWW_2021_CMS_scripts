#!/usr/bin/env bash

setup() {
  #export task_name="bbWW_round1"

  export DHI_STORE="/eos/cms/store/group/phys_higgs/nonresonant_HH/bbWW"

  export SL="/afs/cern.ch/work/a/acarvalh/public/to_HH_bbWW/freze2_March19/round1/datacard_sl.txt"
  export DL="/afs/cern.ch/work/a/acarvalh/public/to_HH_bbWW/freze2_March19/round1/datacard_dl.txt"
  export ALL="/afs/cern.ch/work/a/acarvalh/public/to_HH_bbWW/freze2_March19/round1/datacard.txt"

  export SL_BKG_only="/afs/cern.ch/work/a/acarvalh/public/to_HH_bbWW/freze2_March19/round1/datacard_sl_BKGonly.txt"
  export DL_BKG_only="/afs/cern.ch/work/a/acarvalh/public/to_HH_bbWW/freze2_March19/round1/datacard_dl_BKGonly.txt"
  export ALL_BKG_only="/afs/cern.ch/work/a/acarvalh/public/to_HH_bbWW/freze2_March19/round1/datacard_BKGonly.txt"

  export SL_2016="/afs/cern.ch/work/a/acarvalh/public/to_HH_bbWW/freze2_March19/round1/sl_2016/*/datacard.txt"
  export DL_2016="/afs/cern.ch/work/a/acarvalh/public/to_HH_bbWW/freze2_March19/round1/dl_2016/*/datacard.txt"
  export ALL_2016="/afs/cern.ch/work/a/acarvalh/public/to_HH_bbWW/freze2_March19/round1/*_2016/*/datacard.txt"

  export SL_2017="/afs/cern.ch/work/a/acarvalh/public/to_HH_bbWW/freze2_March19/round1/sl_2017/*/datacard.txt"
  export DL_2017="/afs/cern.ch/work/a/acarvalh/public/to_HH_bbWW/freze2_March19/round1/dl_2017/*/datacard.txt"
  export ALL_2017="/afs/cern.ch/work/a/acarvalh/public/to_HH_bbWW/freze2_March19/round1/*_2017/*/datacard.txt"

  export SL_2018="/afs/cern.ch/work/a/acarvalh/public/to_HH_bbWW/freze2_March19/round1/sl_2018/*/datacard.txt"
  export DL_2018="/afs/cern.ch/work/a/acarvalh/public/to_HH_bbWW/freze2_March19/round1/dl_2018/*/datacard.txt"
  export ALL_2018="/afs/cern.ch/work/a/acarvalh/public/to_HH_bbWW/freze2_March19/round1/*_2018/*/datacard.txt"

  export SL_TLL_2016="/afs/cern.ch/work/s/snandan/public/2016/*txt"
  export SL_TLL_2017="/afs/cern.ch/work/s/snandan/public/2017/*txt"
  export SL_TLL_2018="/afs/cern.ch/work/s/snandan/public/2018/*txt"
  export SL_TLL="/afs/cern.ch/work/s/snandan/public/201*/*txt"

}

action() {
    if setup "$@"; then
        echo -e "\x1b[0;49;35Paths bbWW roound1 successfully setup\x1b[0m"
        return "0"
    else
        local code="$?"
        echo -e "\x1b[0;49;31msetup failed with code $code\x1b[0m"
        return "$code"
    fi
}
action "$@"
