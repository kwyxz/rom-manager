# push roms to remote

"""
handle everything related to pushing things to a remote destination
"""

import msg
import paramiko
import ftplib
from ftplib import FTP

def push_romset_ssh(romset,local,dest,ip_addr,port,user,debug): # pylint: disable=too-many-arguments
    """push romset using SSH"""
    sshcon = paramiko.SSHClient()
    sshcon.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        msg.debug(f"SSH:\tconnect to {user}@{ip_addr}:{port}{dest}",debug)
        sshcon.connect(ip_addr, port=port, username=user)
        sftp=sshcon.open_sftp()
        for rom in romset:
            try:
                sftp.stat(dest)
            except FileNotFoundError:
                sftp.mkdir(dest)
                msg.debug(f"SSH:\tcreated remote folder {dest}",debug)
            # if we have a / in the rom name we are dealing with a chd
            if '/' in rom:
                try:
                    chdfolder = rom.split('/')[0]
                    sftp.stat(dest + '/' + chdfolder)
                except FileNotFoundError:
                    sftp.mkdir(dest + '/' + chdfolder)
                    msg.debug(f"SSH:\tcreated remote folder {dest + '/' + chdfolder}",debug)
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
        msg.die("Unable to connect to the remote SSH host, check the network parameters")
    sshcon.close()

def push_romset_ftp(romset,local,dest,ip_addr,port,user,passwd,debug): # pylint: disable=too-many-arguments
    """push romset using FTP"""
    ftp = FTP()
    msg.debug(f"FTP:\tconnecting to {ip_addr}:{port}",debug)
    try:
        ftp.connect(host=ip_addr,port=int(port))
        msg.debug(f"FTP:\tlogin={user},password={passwd}",debug)
        ftp.login(user=user,passwd=passwd)
        for rom in romset:
            try:
                ftp.size(dest)
            except ftplib.error_perm:
                ftp.mkd(dest)
                msg.debug(f"FTP:\tcreated folder {dest}",debug)
            # if we have a / in the rom name we are dealing with a chd
            if '/' in rom:
                try:
                    chdfolder = rom.split('/')[0]
                    ftp.size(dest + '/' + chdfolder)
                except ftplib.error_perm:
                    ftp.mkd(dest + '/' + chdfolder)
                    msg.debug(f"FTP:\tcreated remote folder {dest + '/' + chdfolder}",debug)
            local_rom = local + '/' + rom
            remote_rom = dest + '/' + rom
            msg.debug(f"FTP:\tpush local={local_rom},remote={remote_rom}",debug)
            try:
                ftp.size(remote_rom)
                msg.info(f"SKIPPED:\talready present {remote_rom}")
            except ftplib.error_perm:
                with open(local_rom, 'rb') as local_romfile:
                    ftp.storbinary("STOR " + remote_rom, local_romfile)
                msg.ok(f"PUSHED:\t{remote_rom}")
    except OSError:
        msg.die("Unable to connect to the remote FTP host, check the network parameters")
    ftp.quit()

def pushromset(romset,local,folder,remote,debug):
    """select push protocol based on settings"""
    # remote is exclusive in options
    if remote['protocol'] == 'ssh':
        push_romset_ssh(romset,local,folder,remote['ip_addr'],remote['port'],remote['user'],debug)
    elif remote['protocol'] == 'ftp':
        push_romset_ftp(
            romset,local,folder,remote['ip_addr'],
            remote['port'],remote['user'],remote['passwd'],debug
        )
    else:
        msg.die("something went very wrong")
