@echo off

if not exist "variables.bat" (
    copy .variables.structure.bat variables.bat
    echo variables.bat created. Please fill in all of the empty variables, then rerun this script.
    pause
	exit
)
call "variables.bat"

del "%VOID_STRANGER_PATH%\_tmp_data.win"
"%UNDERTALEMODCLI_PATH%" load "%VOID_STRANGER_PATH%\clean_data.win" --scripts "ImportGraphics.csx" --scripts "patcher.csx" --output "%VOID_STRANGER_PATH%\_tmp_data.win"
del "%VOID_STRANGER_PATH%\data.win"
copy "%VOID_STRANGER_PATH%\_tmp_data.win" "%VOID_STRANGER_PATH%\data.win"
del "%VOID_STRANGER_PATH%\_tmp_data.win"
echo All done!