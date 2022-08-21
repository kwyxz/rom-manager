# push roms to remote

"""
handle everything related to pushing things to a remote destination
"""

import os
import paramiko
import msg

def push_ssh(local_file,remote_file,remote_ip,remote_port,remote_user):
    sshcon = paramiko.SSHClient()
    sshcon.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        sshcon.connect(remote_ip, port=remote_port, username=remote_user)
        sftp=sshcon.open_sftp()
        try:
            sftp.stat(os.path.dirname(remote_file))
        except FileNotFoundError:
            sftp.mkdir(os.path.dirname(remote_file))
        try:
            sftp.stat(remote_file)
            msg.info(f"SKIPPED: already present {remote_file}")
        except FileNotFoundError:
            sftp.put(local_file,remote_file,callback=None,confirm=True)
            msg.ok(f"PUSHED: {remote_file}")
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