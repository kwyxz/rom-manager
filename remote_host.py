# push roms to remote

"""
handle everything related to pushing things to a remote destination
"""

import os
import paramiko
import msg

def trim_path(folder):
    if folder[-1] == '/':
        folder = folder.rstrip(folder[-1])
    return folder.split('/')[-1]

def push_romset_ssh(romset,folder,dest,ip,port,user,debug):
    sshcon = paramiko.SSHClient()
    sshcon.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        msg.debug(f"Connecting to {user}@{ip}:{port}{dest}",debug)
        sshcon.connect(ip, port=port, username=user)
        sftp=sshcon.open_sftp()
        remote_folder = dest + '/' + trim_path(folder)
        try:
            sftp.stat(remote_folder)
        except FileNotFoundError:
            sftp.mkdir(remote_folder)
            msg.debug(f"creating remote folder {remote_folder}",debug)
        for rom in romset:
            local_rom = folder + '/' + rom
            remote_rom = remote_folder + '/' + rom
            try:
                sftp.stat(remote_rom)
                msg.info(f"SKIPPED: already present {remote_rom}")
            except FileNotFoundError:
                sftp.put(local_rom,remote_rom,callback=None,confirm=True)
                msg.ok(f"PUSHED: {remote_rom}")
    except paramiko.ssh_exception.NoValidConnectionsError:
        msg.die("Unable to connect to the remote host, check the network parameters")

def push_romset_ftp(folder,rom,remote):
    msg.debug(f"FTP push to {remote['user']}@{remote['ip_addr']}:{remote['port']}/{remote['rom_path']}")

def pushromset(romset,folder,remote,debug):
    # remote is exclusive in options
    if remote['protocol'] == 'ssh':
        push_romset_ssh(romset,folder,remote['rom_path'],remote['ip_addr'],remote['port'],remote['user'],debug)
    elif remote['protocol'] == 'ftp':
        push_romset_ftp(romset,folder,remote)
    else:
        msg.die("something went very wrong")
