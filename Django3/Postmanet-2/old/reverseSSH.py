import subprocess, os

def reverseTunnel(sshExe, remoteHost, remotePort, user = None):
	cmdline = [sshExe]
	if user:
		cmdline.append("-l")
		cmdline.append(user)
	cmdline.append("-R")
	cmdline.append("%d:localhost:22" % (remotePort,))
	cmdline.append(remoteHost)
	while True:
		tunnel = subprocess.Popen(cmdline, shell=True)
		tunnel.wait()

ssh =  r"C:\Program Files\SSH Communications Security\SSH Secure Shell\ssh2.exe"
remoteHost = "128.112.139.210"
remotePort = 2048

if __name__ == "__main__":
	reverseTunnel(ssh, remoteHost, remotePort)


