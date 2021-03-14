@REM call in cli C:>batHelp.bat 1 2

@REM Do not print the use echo off

@echo off
@REM reading Perameter %1 is 1st perameter
set PERA1=%1
set PERA2=%2

@REM set variable
set PATAH = "C:\"
set prog1 = notepad.exe
set input1 = a.txt

@REM Printing
Echo Hi Print PERA1
Echo %PERA1%

@REM conditions with partmaters and variables
IF [%PERA1%] == [] GOTO Label0
GOTO Label2
:Label0
Echo PERA1 is ZERO
IF [%2] == [] GOTO Label1
Echo Positive number
GOTO Lable2
:Label1
Echo number is zero
:Label2

@REM execute PERA1 PERA2
%prog1% %input1%

@REM Deleting existing file
@REM IF EXIST %IMAGEDIROTAPATH% DEL /F %IMAGEDIROTAPATH%

@REM copying file , remove @REM below
@REM COPY %APPOTADIR% %IMAGEDIROTAPATH%

@REM Simply wait , Delay
timeout /t 2 /nobreak

@REM change directory
cd..
