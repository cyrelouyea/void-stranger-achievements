#!/usr/bin/env bash

if [ ! -f "variables.sh" ]; then
  cp .variables.structure.sh variables.sh
  echo "variables.sh created. Please fill in all of the empty variables, then rerun this script."
  exit 1
fi

echo "Reading variables.sh"
source variables.sh


if [ ! -f "$VOID_STRANGER_PATH/clean_data.win" ]; then
  echo "clean_data.win not found, copying data.win"
  cp "$VOID_STRANGER_PATH/data.win" "$VOID_STRANGER_PATH/clean_data.win"
fi

rm "_tmp_data.win"
"$UNDERTALEMODCLI_PATH" load "$VOID_STRANGER_PATH/clean_data.win"  --scripts "ImportGraphics.csx" --scripts "patcher.csx" --output "_tmp_data.win"
rm "$VOID_STRANGER_PATH/data.win"
cp "_tmp_data.win" "$VOID_STRANGER_PATH/data.win"
cp "_tmp_data.win" "./data.win"
rm "_tmp_data.win"
echo All done!