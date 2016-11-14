import unittest
import sys
import os
import ConfigParser

sys.path.insert(0, os.path.abspath('..'))
sys.path.insert(0, os.path.abspath('../..'))

from updater import Updater
from fixtures import updater_fixtures as fixtures


class updaterTest(unittest.TestCase):
    def setUp(self):
        self.config = ConfigParser.RawConfigParser()
        self.config.read('../resources/test.properties')
        self.org_or_user_name = self.config.get('default', 'org_or_user_name')
        self.org_or_user = self.config.get('default', 'org_or_user')
        self.repo = self.config.get('default', 'repo')
        self.branch = self.config.get('default', 'branch')
        self.gh_token = self.config.get('default', 'gh_token')
        self.gh_url = self.config.get('default', 'gh_url')

    def testGetSetup(self):
        test_setup = fixtures.setup()
        file = '/setup.py'

        u = Updater(
            gittoken=self.gh_token,
            config=self.config,
            branch='master',
            file=file,
            repo=self.repo
        )

        setup = u.get_file_from_git()

        self.assertEqual(setup, test_setup, 'Setup from Git equals test setup')

    def testGetMetadata(self):
        test_metadata = fixtures.metadata()
        file = '/metadata.rb'

        u = Updater(
            gittoken=self.gh_token,
            config=self.config,
            branch='master',
            file=file,
            repo=self.repo
        )

        metadata = u.get_file_from_git()

        self.assertEqual(metadata, test_metadata, 'Metadata from Git equals test metadata')

    def testIncrementSetup(self):
        file = '/setup.py'
        pattern = "\s+version='(\d+\.\d+\.\d+)',"

        u = Updater(
            gittoken=self.gh_token,
            config=self.config,
            branch='master',
            file=file,
            patterns=pattern,
            repo=self.repo
        )

        setup = u.get_file_from_git()

        newsetup = u.increment_version_in_content(setup)

        self.assertEqual(newsetup, fixtures.setup_incremented(), "Incremented Setup equals test incremented setup")

    def testIncrementMetadata(self):
        file = '/metadata.rb'
        pattern = "version\s+'(\d+\.\d+\.\d+)'"

        u = Updater(
            gittoken=self.gh_token,
            config=self.config,
            branch='master',
            file=file,
            patterns=pattern,
            repo=self.repo
        )

        metadata = u.get_file_from_git()

        newmetadata = u.increment_version_in_content(metadata)

        self.assertEqual(newmetadata, fixtures.metadata_incremented(), "Incremented Metadata equals test incremented metadata")

    def testGetVersionFromString(self):
        file = '/setup.py'
        pattern = "\s+version='(\d+\.\d+\.\d+)',"

        u = Updater(
            gittoken=self.gh_token,
            config=self.config,
            branch='master',
            file=file,
            patterns=pattern,
            repo=self.repo
        )

        setup = u.get_file_from_git()

        version = u.get_version_from_string(pattern, setup)

        self.assertEqual(version, '1.0.0', "Extracted Version matches expected value")

    def testIncrementRemoteSetup(self):
        file = '/setup.py'
        pattern = "\s+version='(\d+\.\d+\.\d+)',"

        u = Updater(
            gittoken=self.gh_token,
            config=self.config,
            branch='develop',
            file=file,
            patterns=pattern,
            repo=self.repo
        )

        setup = u.get_file_from_git()

        version = u.get_version_from_string(pattern, setup)

        incremented = u.increment_version(version)

        newsetup = u.increment_version_in_content(setup)

        u.update_file(newsetup)

        brand_new_setup = u.get_file_from_git()

        newversion = u.get_version_from_string(pattern, brand_new_setup)

        self.assertEqual(newversion, incremented, "Version from Git matches expected value")

    def testGetPom(self):
        test_pom = fixtures.pom()
        file = '/pom.xml'
        pattern = ''

        u = Updater(
            gittoken=self.gh_token,
            config=self.config,
            branch='master',
            file=file,
            patterns=pattern,
            repo=self.repo
        )

        setup = u.get_file_from_git()

        self.assertEqual(setup, test_pom, 'Pom from Git equals test pom')

    def testIncrementPom(self):
        file = '/pom.xml'
        pattern = "<version>\s*(\d+\.\d+\.\d+)</version>"

        u = Updater(
            gittoken=self.gh_token,
            config=self.config,
            branch='master',
            file=file,
            patterns=pattern,
            repo=self.repo
        )

        pom = u.get_file_from_git()

        newpom = u.increment_version_in_content(pom)

        self.assertEqual(newpom, fixtures.pom_incremented(), "Incremented pom.xml equals test pom.xml")


if __name__ == '__main__':
        unittest.main()
