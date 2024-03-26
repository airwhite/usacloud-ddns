@ECHO OFF
SET ID=
SET HOST1=
SET HOST2=
SET TEMP1=temp1.json
SET TEMP2=temp2.json

del /f %TEMP2% >NUL 2>&1
usacloud dns read %ID% --query ".[0].Records" > %TEMP1%
python usacloud-ddns.py %HOST1% %HOST2%
if EXIST %TEMP2% (
  GOTO USACLOUD
) ELSE (
  GOTO END
)

:USACLOUD
SET /p JSON=<%TEMP2%
usacloud dns update %ID% --assumeyes --parameters "%JSON%"

:END