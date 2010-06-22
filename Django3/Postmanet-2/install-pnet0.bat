@ECHO OFF
python bizarro.py nt
IF ERRORLEVEL 1 exit /B

mkdir e:\Postmanet
mkdir e:\Postmanet\robot_jobs

python install-repository-lai.py e:\Postmanet\repository e:\Postmanet\robot_jobs
