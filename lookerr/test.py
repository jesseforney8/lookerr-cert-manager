from paramiko import SSHClient
from scp import SCPClient

ssh = SSHClient()
ssh.load_system_host_keys()
ssh.connect(hostname='192.168.1.186', username="Administrator", password="10029398aA!")




(stdin, stdout, stderr) = ssh.exec_command("cd Documents && dir")




cmd_output = str(stdout.read())
print(cmd_output)
cmd_output = list(cmd_output.split("<DIR>"))



slash = "\$"
slash = slash.replace("$", "")


for e in cmd_output:
    
    e = e.strip()
    index = e.index(slash)
    e = e[0:index]
    print(e)






    




# SCPCLient takes a paramiko transport as an argument
#scp = SCPClient(ssh.get_transport())

#scp.put('appt.txt', remote_path="/")

#scp.get('test2.txt')

# Uploading the 'test' directory with its content in the
# '/home/user/dump' remote directory
#scp.put('test', recursive=True, remote_path='/home/user/dump')

#scp.close()