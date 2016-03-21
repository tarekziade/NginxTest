import tempfile
import shutil
import os
import subprocess
import shlex
import time
import sys
import fcntl

from mako.template import Template
import requests


_TMPL = """\
worker_processes 1;
error_log stderr error;
daemon off;
events {worker_connections 1024;}

${main_options}

http {
  ${http_options}

  server {
    listen ${port};
    ${server_options}

    ${locations}
  }
}
"""

_TMPL_LOCATIONS_LIST = """\
    %for location in locations:
      location ${location['path']} {
        ${location['definition']}
      }
    %endfor
"""

_DEFAULTS = [('nginx', 'nginx'),
             ('port', 1984),
             ('main_options', ''),
             ('http_options', ''),
             ('server_options', ''),
             ('locations', [])]


class NginxServer(object):

    def __init__(self, **options):
        for key, val in _DEFAULTS:
            if key not in options:
                options[key] = val

        if type(options['locations']) is list:
            options['locations'] = Template(_TMPL_LOCATIONS_LIST).render(locations=options['locations'])
        # early rendering so we can stop on error
        self.conf_data = Template(_TMPL).render(**options)
        self.wdir = tempfile.mkdtemp()
        self.conf = os.path.join(self.wdir, 'nginx.conf')
        with open(self.conf, 'w') as f:
            f.write(self.conf_data)

        self.root_url = 'http://localhost:%s/' % options['port']
        self.cmd = '%s -c %s' % (options['nginx'], self.conf)
        self.cwd = os.getcwd()
        self._p = None

    def start(self):
        os.chdir(self.wdir)
        self._p = subprocess.Popen(shlex.split(self.cmd),
                                   stderr=subprocess.PIPE,
                                   stdout=subprocess.PIPE)
        time.sleep(.1)

        # sanity check
        start = time.time()
        resp = None
        while time.time() - start < 2:
            try:
                resp = requests.get(self.root_url)
                break
            except requests.ConnectionError:
                time.sleep(.1)

        if resp is None or resp.status_code != 200:
            self.stop()
            self._forward_messages()
            if resp is None:
                raise IOError('Failed to start Nginx')
            else:
                raise IOError('Nginx root sent back %s' % resp)

    def stop(self):
        if self._p is None:
            return

        self._p.terminate()
        time.sleep(.2)
        try:
            self._forward_messages()
            os.chdir(self.cwd)
            shutil.rmtree(self.wdir)
        finally:
            os.kill(self._p.pid, 9)

    def _forward_messages(self):
        sys.stdout.write(self._p.stdout.read())
        sys.stderr.write(self._p.stderr.read())

