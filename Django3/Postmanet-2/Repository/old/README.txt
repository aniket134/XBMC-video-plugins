
Software needed: python, apache

ENVIRONMENT VARIABLES:
	PDRROOT -- contains directory PDRROOT
	set PDRROOT=c:\PDRROOT
	path %path%;c:\program files\python24\

Apache conf:-->
DocumentRoot: C:\PDRROOT\WWW\

ScriptAlias: C:/PDRROOT/cgi-bin/

cgi-bin directory is password protected so that there is authentication
done before executing any of the cgi scripts.

<Directory "C:/PDRROOT/cgi-bin">

AuthType Basic
AuthName "Username"
AuthUserFile "C:/PDRROOT/Passwords"
Require valid-user

</Directory>
