#!/usr/bin/python3
""" write a Fabric script that generates a .tgz archive
 from the contents of the web_static folder of your
  AirBnB Clone repo, using the function do_pack.
"""
from fabric.api import local
from datetime import datetime


def do_pack():
    """Creats a .tgz file
    from web_static directory
    """
    local('mkdir -p versions')
    tar_dir = local("tar -czvf versions/web_static_{}.tgz web_static/".format((
        datetime.strftime(datetime.now(), "%Y%m%d%H%M%S"))), capture=True)

    if tar_dir.succeeded:
        return tar_dir
    return None
