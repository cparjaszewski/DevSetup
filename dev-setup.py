import os, psutil

# This is the windows dedicated app to be launched on every Windows boot to start the ssh-agent
# On Unix systems the ssh-agent should be booted automatically

def killAllOtherServices(PROCNAME):
	print "=> Killing previous " + PROCNAME + " processes"
	for proc in psutil.process_iter():
		if proc.name == PROCNAME:
			proc.kill()

					 
def startSshAgent():
	# First the old ssh-agents are killed
	killAllOtherServices('ssh-agent.exe')

	# Nextly - we are creating a new ssh-agent
	fh = os.popen('ssh-agent')
	output = fh.read()
	fh.close()
	print "1. Starting the ssh-agent process"

	# preparing the environmental variables to be set locally and globally
	result = output.replace('\n','').replace(' ','').split(';')

	sshAuthSockCommand = result[0]
	sshAgentPid = result[2]

	sshAuthSockCommandKey   = sshAuthSockCommand.split('=')[0]
	sshAuthSockCommandValue = sshAuthSockCommand.split('=')[1]

	sshAgentPidKey   = sshAgentPid.split('=')[0]
	sshAgentPidValue = sshAgentPid.split('=')[1]

	print "2. Setting the environment variables"
	os.system(('setx ' + sshAuthSockCommandKey + ' ' + sshAuthSockCommandValue + ' /M'))
	os.system(('setx ' + sshAgentPidKey + ' ' + sshAgentPidValue + ' /M'))
	os.system(('setx ' + sshAuthSockCommandKey + ' '  + sshAuthSockCommandValue))
	os.system(('setx ' + sshAgentPidKey + ' ' + sshAgentPidValue))
	os.system(('set ' + sshAuthSockCommand)) 
	os.system(('set ' + sshAgentPid))
	os.environ[sshAuthSockCommandKey] = sshAuthSockCommandValue
	os.environ[sshAgentPidKey] = sshAgentPidValue
		
# To use the ssh protocol, we need to add the identities
def addSshIdentities():
	print "3. Adding the identities"
	os.system(('ssh-add.exe'))
		

# To start the Mongo DB service, the old mongod.lock file should be deleted		
def mongoStartup():
	killAllOtherServices('mongod.exe')
	if os.path.exists(('c:\\xampp\\mongodb\\data\\db\\mongod.lock')):
		os.system(('del c:\\xampp\\mongodb\\data\\db\\mongod.lock'))
	os.system(('C:\\xampp\\mongodb\\bin\\mongod.exe --config C:\\xampp\\mongodb\\mongod.cfg --service'))
	print "4. Restarting Mongo DB"
				
# Starting the varnish cache
def varnishStartup():
	killAllOtherServices('varnishd.exe')
	os.system(('cmd /c c:\\xampp\\varnish\\bin\\start-varnish.bat < nul'));
	print "5. Starting Varnish Cache"
    

startSshAgent()
addSshIdentities()
mongoStartup()
varnishStartup()