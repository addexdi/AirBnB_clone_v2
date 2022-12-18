#!/usr/bin/python3
""" Write a Fabric script (based on the file
 2-do_deploy_web_static.py) that creates and distributes
  an archive to your web servers, using the function
   deploy"""
from fabric.api import local, env, run, put
from datetime import datetime
from os.path import exists

env.hosts = ["44.200.48.169", "3.238.85.27"]


def do_pack():
    """[summary]"""
    local('mkdir -p versions')
    tar_dir = local("tar -czvf versions/web_static_{}.tgz web_static/".format((
        datetime.strftime(datetime.now(), "%Y%m%d%H%M%S"))), capture=True)

    if tar_dir.succeeded:
        return tar_dir
    return None


def do_deploy(archive_path):
    """[summary]"""
    # Returns False if the file at the path archive_path doesn’t exist
    if exists(archive_path):
        # archive_path = versions/web_static_#####.tgz
        # file_path = web_static_#####.tgz
        file_path = archive_path.split("/")[1]
        # serv_path = /data/web_static/releases/web_static_#####
        serv_path = "/data/web_static/releases/{}".format(
            file_path.replace(".tgz", ""))
        # Upload the archive to the /tmp/ directory of the web server
        put('{}'.format(archive_path), '/tmp/')
        # ???
        run('mkdir -p {}'.format(serv_path))
        # Uncompress the archive to the folde <..> on the web server
        run('tar -xzf /tmp/{} -C {}/'.format(
            file_path,
            serv_path))
        # Delete the archive from the web server
        run('rm /tmp/{}'.format(file_path))
        # ???
        run('mv -f {}/web_static/* {}/'.format(serv_path, serv_path))
        # Delete the symbolic link <..> from the web server
        run('rm -rf {}/web_static'.format(
            serv_path))
        # ??
        run('rm -rf /data/web_static/current')
        # run('unlink /data/web_static/current')
        # Create a new Symbolic link, linked to the new version of your code
        run('ln -s {} /data/web_static/current'.format(
            serv_path))
        # Retur  True if all operations have been done correctly
        return True
    else:
        return False


def deploy():
    """ Summary """
    archive = do_pack()
    if archive is None:
        return False
    else:
        value = archive.__dict__["command"].split(" ")[-2]
        print(value)
        return do_deploy(value)
