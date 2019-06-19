@ECHO off
SET choices=rualiheq
SET timeout_choice_wait=9999
SET timeout_display_list=5
SET execution_default_choice=e
SET first_execution_timeout_wait=30
SET first_execution_default_choice=r
SET first_execution_flag=true

CD "C:\Users\amit1\Documents\GitHub\anime-download"
CALL .\venv\Scripts\activate.bat "prompt $"

:begin
SET timeout_curr=%timeout_choice_wait%
SET default_choice=%execution_default_choice%
IF %first_execution_flag%==true (
	SET default_choice=%first_execution_default_choice%
	SET timeout_curr=%first_execution_timeout_wait%
)
echo Execution options: [R]un / [U]rl download / [A]dd new anime / [L]ist animes / [I]d download / [H]elp / [E]xit
CHOICE /c %choices% /n /d %default_choice% /t %timeout_curr% /m "Execution type? "

IF %ERRORLEVEL%==1 GOTO option_run
IF %ERRORLEVEL%==2 GOTO option_url
IF %ERRORLEVEL%==3 GOTO option_add
IF %ERRORLEVEL%==4 GOTO option_list
IF %ERRORLEVEL%==5 GOTO option_id
IF %ERRORLEVEL%==6 GOTO option_help
IF %ERRORLEVEL%==7 GOTO option_pause_exit
GOTO quit_execution

:option_run
python AnimeDownload.py -r
GOTO evaluate

:option_url
SET /p url="Enter URL? "
SET /p episodes="Enter episode nos? "
IF NOT DEFINED episodes (
	python AnimeDownload.py -u "%url%"
) ELSE (
	python AnimeDownload.py -u "%url%" -e "%episodes%"
)
GOTO evaluate

:option_add
SET /p url="Enter URL? "
python AnimeDownload.py -a "%url%"
GOTO evaluate

:option_list
CHOICE /c ads /n /d a /t %timeout_display_list% /m "Category ([A]ll/[D]ubbed/[S]ubbed)? "
IF %ERRORLEVEL%==1 SET category="a"
IF %ERRORLEVEL%==2 SET category="d"
IF %ERRORLEVEL%==3 SET category="s"
python AnimeDownload.py -l %category%
GOTO evaluate

:option_id
SET /p id="Enter ID? "
SET /p episodes="Enter episode nos? "
IF NOT DEFINED episodes (
	python AnimeDownload.py -i "%id%"
) ELSE (
	python AnimeDownload.py -i "%id%" -e "%episodes%"
)
GOTO evaluate

:option_help
python AnimeDownload.py -h
GOTO evaluate

:evaluate
SET first_execution_flag=false
GOTO begin

:option_pause_exit
pause
GOTO quit_execution

:quit_execution
EXIT /B 0
