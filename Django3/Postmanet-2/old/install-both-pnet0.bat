
mkdir e:\Postmanet
mkdir e:\Postmanet\robot_jobs
mkdir c:\Postmanet

python install-nihao-lai.py c:\Postmanet\nihao
python copy-pythonscriptsforclient.py c:\Postmanet\nihao

python install-repository-lai.py e:\Postmanet\repository e:\Postmanet\robot_jobs
