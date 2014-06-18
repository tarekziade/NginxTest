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
        self.nginx = options['nginx']
        self.nginx_config = Template(_TMPL).render(**options)
        self.root_url = 'http://localhost:%s/' % options['port']

    def start(self):
        pass

    def stop(self):
        pass
