# push roms to remote

"""
handle everything related to pushing things to a remote destination
"""

import os
import paramiko
import msg

def push_romset_ssh(romset,local,dest,ip,port,user,debug):
    sshcon = paramiko.SSHClient()
    sshcon.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        msg.debug(f"SSH:\tconnect to {user}@{ip}:{port}{dest}",debug)
        sshcon.connect(ip, port=port, username=user)
        sftp=sshcon.open_sftp()
        for rom in romset:
            try:
                sftp.stat(dest)
            except FileNotFoundError:
                sftp.mkdir(dest)
                msg.debug(f"SSH:\tcreating remote folder {dest}",debug)
            if '/' in rom:
                try:
                    chdfolder = rom.split('/')[0]
                    sftp.stat(dest + '/' + chdfolder)
                except FileNotFoundError:
                    sftp.mkdir(dest + '/' + chdfolder)
                    msg.debug(f"SSH:\tcreating remote folder {dest + '/' + chdfolder}",debug)
            # if we have a / in the rom name we are dealing with a chd
            local_rom = local + '/' + rom
            remote_rom = dest + '/' + rom
            msg.debug(f"SSH:\tpush local={local_rom},remote={remote_rom}",debug)
            try:
                sftp.stat(remote_rom)
                msg.info(f"SKIPPED:\talready present {remote_rom}")
            except FileNotFoundError:
                sftp.put(local_rom,remote_rom,callback=None,confirm=True)
                msg.ok(f"PUSHED:\t{remote_rom}")
    except paramiko.ssh_exception.NoValidConnectionsError:
        msg.die("Unable to connect to the remote host, check the network parameters")

def push_romset_ftp(folder,rom,remote):
    msg.ok(f"FTP push to {remote['user']}@{remote['ip_addr']}:{remote['port']}/{remote['rom_path']}")

def pushromset(romset,local,folder,remote,debug):
    # remote is exclusive in options
    if remote['protocol'] == 'ssh':
        push_romset_ssh(romset,local,folder,remote['ip_addr'],remote['port'],remote['user'],debug)
    elif remote['protocol'] == 'ftp':
        push_romset_ftp(romset,folder,remote)
    else:
        msg.die("something went very wrong")
