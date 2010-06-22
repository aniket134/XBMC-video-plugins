
Demo-1

Nihao: runs on the consumer machine
======

 For consumer, it is software installed: apache, python, Nihao (cgi-bin\Nihao\, WWW\Nihao, httpd.conf, resources.txt)

 For server (such as repository), it is just a specification

---

Repository: runs on pnet0
===========

Software in PDRROOT: bin, cgi-bin, pythonscriptsforclient, WWW
State in PDRROOT: DATA, QUEUES, TMP, Endpoints.pk, httpd.conf, Passwords


Robot runs in \JOBS folder

Demo-1 features:
	- Allows web-access on Pnet0
	- p-http
		* repository produces a generic CD for consumer (with default small-initial-set-of-objects, latest catalog,
		  repository specific p-http scripts for the client
		* consumer receives CD, interacts with the scripts
		* consumer pushes the 'Create outgoing CD' button on his web-browser
		* CD comes back to repository. repository can mass-read incoming CDs
