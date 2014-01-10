#!/usr/bin/env python

# restarts api services if haproxy 
# is not running and service ports
# are bound to 0.0.0.0 .

import os

def cmd_exec(cmd):
  return str(os.system(cmd))

services ={'6080':'nova-novncproxy','8776':'cinder-api',
           '9292':'glance-api','9191':'glance-registry',
           '35357':'keystone','6080':'nova-novncproxy'}

if cmd_exec('/usr/sbin/service haproxy status').find('not running') > -1:
    for port,svc in services.items():
        if cmd_exec('netstat -an | grep 0.0.0.0:%s' % (port)).find('LISTEN') > -1:
            if os.path.exists('/etc/init.d/%s' % (svc)):
                cmd_exec('/usr/sbin/service %s restart' % (svc))

    if os.path.exists('/etc/init.d/apache2'):
        cmd_exec('/usr/sbin/service apache2 stop')
