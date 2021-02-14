import sys
import re
import paramiko

class Host:
    def __init__(self, hostname, credentials, port = 22):
        self.port = port
        self.username = credentials[0]
        self.password = credentials[1]

        # Verify hostname format (ip_address or plain text hostname)
        regex_ip = '^((\d){1,3}\.){3}(\d){1,3}$'
        regex_fqdn = '^(\w*\.)*\w*[^\.]$'

        if re.match(regex_fqdn, hostname): self.hostname = hostname
        elif re.match(regex_ip, hostname):
            for byte in hostname.split('.'):
                if int(byte) < 0 or int(byte) > 255: sys.exit('ERROR:INVALID_IP_ADDRESS')
            self.hostname = hostname
        else: sys.exit('ERROR:INVALID_HOSTNAME')
    
        # Verify port format (in range 0-65535)
        try: int(port)
        except: sys.exit('ERROR:INVALID_PORT_VALUE')
        if int(port) < 0 or int(port) > 65535: sys.exit('ERROR:INVALID_PORT_RANGE')
        
    
    def getInfo(self):
        print('host:', self.hostname)
        if self.port == 22: print('port:', self.port, '(default)')
        else: print('port:', self.port)
        print('username:', self.username)
        print('password:', self.password)
    
    def execute(self, command):
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        try: ssh.connect(self.hostname, self.port, self.username, self.password)
        except: sys.exit('ERROR:WRONG_CREDENTIALS')

        stdin, stdout, stderr = ssh.exec_command(command)
        lines = stdout.readlines()
        return lines