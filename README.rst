NginxTest
=========

This project provides some helpers to write functional tests against
an Nginx server.

Motivation
----------

The main motivation is to test Nginx/Lua scripts in an
OpenResty environment. There's a Perl project to do this called
Test::Nginx which is based on a light DSL to write the tests.

But I like writing plain Python tests better, especially
since I can use WebTest to deal with all the calls against the
Nginx server.


The NginxServer class
---------------------

This project provides a class to drive an Nginx server. The
class has two main method to start and stop a local Nginx
server and takes care of the gory details.

When initialized, the class creates an Nginx configuration on
the fly given a few options, and runs an Nginx server in
a child process in a fresh directory.

Once the server is started, the stdout, stderr and access/errors
logs are intercepted by the class so they can be asserted in the
tests. The stop method kills the server.

Example of usage with WebTest::

    import unittest2
    from webtest import TestApp
    from nginxtest.server import NginxServer


    class TestMyNginx(unittest2.TestCase):

        def setUp(self):
            self.nginx = NginxServer()
            self.nginx.start()
            self.app = TestApp(self.nginx.root_url)

        def tearDown(self):
            self.nginx.stop()

        def testHello(self):
            resp = self.app.get('/')
            self.assertEqual(resp.status_int, 200)
            self.assertTrue('Welcome to nginx!' in resp.body)


Limitations
-----------

This project is very limited compared to Test::Nginx.

Stuff I'd like to add at some point:

- Lua test coverage
- XXX


