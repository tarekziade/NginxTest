import unittest2
from webtest import TestApp
from nginxtest import NginxServer


class TestMyNginx(unittest2.TestCase):

    def setUp(self):
        self.nginx = NginxServer()
        self.nginx.start()
        self.app = TestApp(self.nginx.root_url)

    def tearDown(self):
        self.nginx.stop()

    def testHello(self):
        resp = self.app.get('/hello')
        self.assertEqual(resp.status_int, 200)
