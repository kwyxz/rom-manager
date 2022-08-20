# push roms to remote

"""
handle everything related to pushing things to a remote destination
"""

import paramiko
import msg

def push_ssh(local_file,remote_folder,remote_ip,remote_port,remote_user):
    sshcon = paramiko.SSHClient()
    sshcon.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        sshcon.connect(remote_ip, port=remote_port, username=remote_user)
        sftp=sshcon.open_sftp()
        sftp.put(local_file,remote_folder,callback=None,confirm=True)
    except paramiko.ssh_exception.NoValidConnectionsError:
        msg.die("Unable to connect to the remote host, check the network parameters")

def push_ftp(folder,rom,remote):
    msg.debug(f"FTP push to {remote['user']}@{remote['ip_addr']}:{remote['port']}/{remote['rom_path']}")

def push(local_rom,remote_rom,remote):
    # remote is exclusive in options
    if remote['protocol'] == 'ssh':
        push_ssh(local_rom,remote_rom,remote['ip_addr'],remote['port'],remote['user'])
    elif remote['protocol'] == 'ftp':
        push_ftp(local_rom,remote_rom,remote)
    else:
        msg.die("something went very wrong")