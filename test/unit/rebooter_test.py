import sys
import os
import unittest
from rebooter import Rebooter, Agent
import ConfigParser


sys.path.insert(0, os.path.abspath('..'))
sys.path.insert(0, os.path.abspath('../..'))

from updater import Updater
import updater_fixtures as fixtures


class updaterTest(unittest.TestCase):
    def setUp(self):
        self.config = ConfigParser.RawConfigParser()
        self.config.read('../resources/test.properties')
        self.teamcity = self.config.get('default', 'teamcity')
        self.username = self.config.get('default', 'username')
        self.password = self.config.get('default', 'password')

    def testget_agents(self):
        rebooter = Rebooter(
            server=self.teamcity,
            username=self.username,
            password=self.password,
        )

        agents = rebooter.get_agents()

        self.assertTrue(agents)

        for agent in agents:
            self.assertTrue(isinstance(agent, Agent))

    def test_reboot_agent(self):
        rebooter = Rebooter(
            server=self.teamcity,
            username=self.username,
            password=self.password,
        )

        resp = rebooter.reboot_agent(9985)

        print resp
        print resp.content
