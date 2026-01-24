#!/usr/bin/env bash

if [ ! -f "variables.sh" ]; then
  cp .variables.structure.sh variables.sh
  echo "variables.sh created. Please fill in all of the empty variables, then rerun this script."
  exit 1
fi

echo "Reading variables.sh"
source variables.sh


echo "--------------------------"
echo "Merging into Void Stranger"
echo "--------------------------"


rm "$VOID_STRANGER_PATH/_tmp_data.win"

"$UNDERTALEMODCLI_PATH" load "$VOID_STRANGER_PATH/clean_data.win"  --scripts "ImportGraphics.csx" --scripts "patcher.csx" --output "$VOID_STRANGER_PATH/_tmp_data.win"
rm "$VOID_STRANGER_PATH/data.win"
cp "$VOID_STRANGER_PATH/_tmp_data.win" "$VOID_STRANGER_PATH/data.win"
rm "$VOID_STRANGER_PATH/_tmp_data.win"
echo All done!