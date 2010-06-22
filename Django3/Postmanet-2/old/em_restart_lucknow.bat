cd Common
cd emnet

python emnet_main_service.py stop
python emnet_main_service.py remove

rm -rf c:\EMNET-LUCKNOW

python emnet_install.py -d c:\EMNET-LUCKNOW -f myself-lucknow.txt

python emnet_main_service.py install
python emnet_main_service.py start




cd ..

python q2q_incoming_server_service.py stop
python q2q_incoming_server_service.py remove

rm -rf e:\Postmanet\repository\WWW\q2q

python q2q_install.py -r e:\Postmanet\repository

python q2q_incoming_server_service.py install
python q2q_incoming_server_service.py start

