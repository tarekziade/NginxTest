import tempfile
import shutil
import os
import subprocess
import shlex

from mako.template import Template


_TMPL = """\
worker_processes 1;
error_log stderr notice;
daemon off;
events {worker_connections 1024;}

${main_options}

http {
  ${http_options}

  server {
    listen ${port};
    ${server_options}

    %for location in locations:
      location ${location['path']} {
        ${location['definition']}
      }
    %endfor
  }
}
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

        # early rendering so we can stop on error
        config = Template(_TMPL).render(**options)

        self.wdir = tempfile.mkdtemp()
        self.conf = os.path.join(self.wdir, 'nginx.conf')
        with open(self.conf, 'w') as f:
            f.write(config)

        self.root_url = 'http://localhost:%s/' % options['port']
        self.cmd = '%s -c %s' % (options['nginx'], self.conf)
        self.cwd = os.getcwd()
        self._p = None

    def start(self):
        os.chdir(self.wdir)
        self._p = subprocess.Popen(shlex.split(self.cmd))

    def stop(self):
        if self._p is not None:
            self._p.terminate()
        os.chdir(self.cwd)
        shutil.rmtree(self.wdir)
