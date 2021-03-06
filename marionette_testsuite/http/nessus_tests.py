#!/usr/bin/env python
# coding: utf-8

import os
import unittest
import time

import marionette_tg.conf
import marionette_testsuite.nessus


def execute(cmd):
    os.system(cmd)


class Tests(unittest.TestCase):

    def startservers(self, format):
        server_proxy_ip = marionette_tg.conf.get("server.proxy_ip")

        execute("marionette_server --proxy_ip %s --proxy_port 8888 --format %s &" %
                (server_proxy_ip, format))
        time.sleep(0.25)

    def stopservers(self):
        execute("pkill -9 -f marionette_server")

    def test_active_probing_http_nessus(self):
        global token
        try:
            self.startservers("active_probing/http_apache_247")
            data = marionette_testsuite.nessus.do_scan('127.0.0.1')
            success = marionette_testsuite.nessus.eval_plugin_output(
                data, 10107, 'tcp', 8080, 'http', 'Apache/2.4.7 (Ubuntu)')
            self.assertTrue(success)
        finally:
            self.stopservers()


if __name__ == '__main__':
    unittest.main()
