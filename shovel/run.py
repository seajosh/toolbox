from contextlib import suppress
import docker
import os
from os.path import (abspath,
                     basename,
                     join)
import re
from shovel import task
import shutil
import subprocess
import sys


def run(image, name, runcmd, mount):
    docker_flags = 'docker run -e LOCAL_USER_ID={user_id} --hostname {name} --name {name} --rm'
    docker_flags = docker_flags.format(name=name,
                                       user_id=os.getuid())
    if mount:
        mount = abspath(mount)
        mount_dir = join('/opt/',
                         basename(mount))
        docker_flags = '{docker} -v {mount}:{mount_dir}'.format(docker=docker_flags,
                                                                mount=mount,
                                                                mount_dir=mount_dir)
    if runcmd:
        cmd = '{docker} -ti {image} {runcmd}'.format(docker=docker_flags,
                                                     image=image,
                                                     runcmd=runcmd)
    else:
        cmd = '{docker} {image}'.format(docker=docker_flags,
                                        image=image)
    print('* ' + cmd)
    subprocess.run(cmd.split(' '),
                   stdin=sys.stdin,
                   stdout=sys.stdout,
                   stderr=sys.stderr)


@task
def base(mount=None):
    run(image='idahodata/base',
        name='base',
        runcmd='/bin/bash',
        mount=mount)


@task
def airflow27():
    run(image='idahodata/airflow27',
        name='airflow27',
        runcmd='/bin/bash',
        mount='../incubator-airflow')
