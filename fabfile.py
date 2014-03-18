from fabric.api import run
from fabric.api import env
from fabric.api import prompt
from fabric.api import execute
from fabric.api import sudo
from fabric.contrib.project import rsync_project
from fabric.contrib.files import append
from fabric.context_managers import cd
import boto.ec2
import time
import os
import re

env.hosts = ['localhost', ]
env.aws_region = 'us-west-2'


def host_type():
    run('uname -s')


def get_ec2_connection():
    if 'ec2' not in env:
        conn = boto.ec2.connect_to_region(env.aws_region)
        if conn is not None:
            env.ec2 = conn
            print "Connected to EC2 region %s" % env.aws_region
        else:
            msg = "Unable to connect to EC2 region %s"
            raise IOError(msg % env.aws_region)
    return env.ec2


def provision_instance(wait_for_running=False, timeout=60, interval=2):
    wait_val = int(interval)
    timeout_val = int(timeout)
    conn = get_ec2_connection()
    instance_type = 't1.micro'
    key_name = 'pk-aws'
    security_group = 'ssh-access'
    image_id = 'ami-fa9cf1ca'

    reservations = conn.run_instances(
        image_id,
        key_name=key_name,
        instance_type=instance_type,
        security_groups=[security_group, ]
    )
    new_instances = [i for i in reservations.instances if i.state == u'pending']
    running_instance = []
    if wait_for_running:
        waited = 0
        while new_instances and (waited < timeout_val):
            time.sleep(wait_val)
            waited += int(wait_val)
            for instance in new_instances:
                state = instance.state
                print "Instance %s is %s" % (instance.id, state)
                if state == "running":
                    running_instance.append(
                        new_instances.pop(new_instances.index(i))
                    )
                instance.update()


def list_aws_instances(verbose=False, state='all'):
    conn = get_ec2_connection()

    reservations = conn.get_all_reservations()
    instances = []
    for res in reservations:
        for instance in res.instances:
            if state == 'all' or instance.state == state:
                instance = {
                    'id': instance.id,
                    'type': instance.instance_type,
                    'image': instance.image_id,
                    'state': instance.state,
                    'instance': instance,
                }
                instances.append(instance)
    env.instances = instances
    if verbose:
        import pprint
        pprint.pprint(env.instances)


def select_instance(state='running'):
    if env.get('active_instance', False):
        return

    list_aws_instances(state=state)

    prompt_text = "Please select from the following instances:\n"
    instance_template = " %(ct)d: %(state)s instance %(id)s\n"
    for idx, instance in enumerate(env.instances):
        ct = idx + 1
        args = {'ct': ct}
        args.update(instance)
        prompt_text += instance_template % args
    prompt_text += "Choose an instance: "

    def validation(input):
        choice = int(input)
        if not choice in range(1, len(env.instances) + 1):
            raise ValueError("%d is not a valid instance" % choice)
        return choice

    choice = prompt(prompt_text, validate=validation)
    env.active_instance = env.instances[choice - 1]['instance']


def run_command_on_selected_server(command):
    select_instance()
    selected_hosts = [
        'ubuntu@' + env.active_instance.public_dns_name
    ]
    execute(command, hosts=selected_hosts)


def _update():
    sudo('apt-get update')


def update():
    run_command_on_selected_server(_update)


def _python_setup():
    sudo('apt-get install python-all-dev python-setuptools python-pip libpq-dev')


def python_setup():
    run_command_on_selected_server(_python_setup)


def _install_python_reqs():
    sudo('pip install -r requirements.txt')


def _install_postgres():
    sudo('sudo apt-get install postgresql postgresql-contrib')


def install_postgres():
    run_command_on_selected_server(_install_postgres)


def install_python_reqs():
    run_command_on_selected_server(_install_python_reqs)


def _install_nginx():
    sudo('apt-get install nginx')
    sudo('/etc/init.d/nginx start')
    sudo('cp /etc/nginx/sites-available/default /etc/nginx/sites-available/default.backup')


def install_nginx():
    run_command_on_selected_server(_install_nginx)


def _restart_nginx():
    sudo('/etc/init.d/nginx restart')


def restart_nginx():
    run_command_on_selected_server(_restart_nginx)


def _install_supervisor():
    sudo('apt-get install supervisor')


def install_supervisor():
    run_command_on_selected_server(_install_supervisor)


def _restart_supervisor():
    sudo('service supervisor stop')
    sudo('service supervisor start')


def restart_supervisor():
    run_command_on_selected_server(_restart_supervisor)


def stop_selected_server():
    select_instance()
    conn = get_ec2_connection()

    selected_servers = [
        env.active_instance.id
    ]

    conn.stop_instances(instance_ids=selected_servers)


def terminate_selected_server():
    select_instance(state='stopped')
    conn = get_ec2_connection()

    selected_servers = [
        env.active_instance.id
    ]

    conn.terminate_instances(instance_ids=selected_servers)


def start_selected_server():
    select_instance(state='stopped')
    conn = get_ec2_connection()

    selected_servers = [
        env.active_instance.id
    ]

    conn.start_instances(instance_ids=selected_servers)


def deploy():
    run_command_on_selected_server(_deploy)


def _deploy():
    rsync_project('~')

    #sudo('createdb microblog')

    with cd('FlaskMicroblog'):
        _install_python_reqs()
        sudo('export MICROBLOG_CONFIG=`pwd`/config.py')
        #sudo('python microblog.py db upgrade')
        sudo('mv nginx_config /etc/nginx/sites-available/default')
        sudo('cp microblog.conf /etc/supervisor/conf.d')

    _restart_nginx()
    _restart_supervisor()


def setup():
    update()
    python_setup()
    install_nginx()
    install_supervisor()
    install_postgres()
