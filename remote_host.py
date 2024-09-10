# push roms to remote

"""
handle everything related to pushing things to a remote destination
"""

import msg
import os
import paramiko
import shutil
import ftplib
from ftplib import FTP

def push_romset_local(romset,local,dest,debug):
    """push romset locally to another folder"""
    msg.debug(f"LOCAL:\tpushing to ROM folder {local}",debug)
    os.makedirs(dest, mode=0o0755, exist_ok=True)
    for rom in romset:
        # if we have a / in the rom name we are dealing with a CHD
        if '/' in rom:
            chdfolder = rom.split('/')[0]
            os.makedirs(dest + '/' + chdfolder, mode=0o0755, exist_ok=True)
            msg.debug(f"LOCAL:\tcreated local folder {dest + '/' + chdfolder}",debug)
        local_rom = local + '/' + rom
        remote_rom = dest + '/' + rom
        msg.debug(f"LOCAL:\tcopy local={local_rom},remote={remote_rom}",debug)
        if os.path.isfile(remote_rom):
            msg.debug(f"SKIPPED:\talready present {remote_rom}",debug)
        else:
            if os.path.isfile(local_rom):
                try:
                    msg.debug(f"LOCAL:\tcopy {local_rom}",debug)
                    shutil.copyfile(local_rom,remote_rom)
                    msg.ok(f"LOCAL:\tcopied {remote_rom}")
                except IOError:
                    msg.die(f"{remote_rom} is identical to {local_rom}")
    msg.ok(f"LOCAL:\t{dest}")

def push_romset_ssh(romset,local,dest,ip_addr,port,user,debug): # pylint: disable=too-many-arguments
    """push romset using SSH"""
    sshcon = paramiko.SSHClient()
    sshcon.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        msg.debug(f"SSH:\tconnecting to {user}@{ip_addr}:{port}{dest}",debug)
        sshcon.connect(ip_addr, port=port, username=user)
        msg.ok(f"SSH:\tconnected to {user}@{ip_addr}:{port}{dest}")
        sftp=sshcon.open_sftp()
        try:
            sftp.stat(dest)
        except FileNotFoundError:
            sftp.mkdir(dest)
            msg.debug(f"SSH:\tcreated remote folder {dest}",debug)
        for rom in romset:
            # if we have a / in the rom name we are dealing with a CHD
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
                if os.path.exists(local_rom):
                    sftp.put(local_rom,remote_rom,callback=None,confirm=True)
                    msg.ok(f"PUSHED:\t{remote_rom}")
    except paramiko.ssh_exception.NoValidConnectionsError:
        msg.die(f"SSH:\tunable to connect to remote host, check the network parameters")
    sshcon.close()
    msg.ok(f"SSH:\tdisconnected")

def push_romset_ftp(romset,local,dest,ip_addr,port,user,passwd,debug): # pylint: disable=too-many-arguments
    """push romset using FTP"""
    ftp = FTP()
    try:
        msg.debug(f"FTP:\tconnecting to {ip_addr}:{port}",debug)
        ftp.connect(host=ip_addr,port=int(port))
        msg.ok(f"FTP:\tconnected to to {ip_addr}:{port}")
        msg.debug(f"FTP:\tlogin={user},password={passwd}",debug)
        ftp.login(user=user,passwd=passwd)
        try:
            ftp.size(dest)
        except ftplib.error_perm:
            ftp.mkd(dest)
            msg.debug(f"FTP:\tcreated folder {dest}",debug)
        for rom in romset:
            # if we have a / in the rom name we are dealing with a CHD
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
        msg.die("FTP:\tunable to connect to remote host, check the network parameters")
    ftp.quit()
    msg.ok(f"FTP:\tdisconnected")

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
    elif remote['protocol'] == 'local':
        push_romset_local(romset,local,folder,debug)
    else:
        msg.die("something went very wrong")
