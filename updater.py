
'''
    Purpose:  Find the build number on develop and increment the last element by one
'''

import sys
import ConfigParser
import getopt
import base64
import ssl
import re
from github import Github

try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    # Legacy Python that doesn't verify HTTPS certificates by default
    pass
else:
    # Handle target environment that doesn't support HTTPS verification
    ssl._create_default_https_context = _create_unverified_https_context


class Updater:
    def __init__(self, gittoken=None, giturl=None, config=None, org_or_user_name=None, org_or_user=None, repo=None, branch=None, file=None, patterns=None):
        if isinstance(config, basestring):
            self.config = ConfigParser.RawConfigParser()
            self.config.read(config)
        else:
            self.config = config

        if giturl:
            self.giturl = giturl
        elif config:
            self.giturl = config.get('default', 'gh_url')
        else:
            #self.giturl = 'https://github.company.com/api/v3'
            self.giturl = 'https://api.github.com'

        if gittoken:
            self.gittoken = gittoken
        elif config:
            self.gittoken = config.get('default', 'gh_token')
        else:
            self.gittoken = None

        if org_or_user_name:
            self.org_or_user_name = org_or_user_name
        elif config:
            self.org_or_user_name = config.get('default', 'org_or_user_name')
        else:
            self.org_or_user_name = None

        if org_or_user:
            self.org_or_user = org_or_user
        elif config:
            self.org_or_user = config.get('default', 'org_or_user')
        else:
            self.org_or_user = None

        if repo:
            self.repo = repo
        elif config:
            self.repo = config.get('default', 'org')
        else:
            self.repo = None

        if branch:
            self.branch = branch
        elif config:
            self.branch = config.get('default', 'branch')
        else:
            self.branch = 'develop'

        if file:
            self.file = file
        elif config:
            self.file = config.get('default', 'version_file')
        else:
            self.file = None

        self.patterns = []

        if patterns:
            self.pattern_string = patterns

            for pattern in patterns.split('-:-'):
                pat = re.compile(pattern)
                self.patterns.append(pat)

        self.github = Github(self.gittoken, base_url=self.giturl)

    # gets the version file from git
    def get_file_from_git(self):
        if self.org_or_user == 'org':
            return base64.b64decode(self.github.get_organization(self.org_or_user_name).get_repo(self.repo).get_file_contents(self.file, self.branch).content)
        else:
            return base64.b64decode(self.github.get_user(self.org_or_user_name).get_repo(self.repo).get_file_contents(self.file, self.branch).content)

    def get_version_from_string(self, pattern, content):
        match = False

        for line in content.split("\n"):
            m = re.search(pattern, line)
            if m:
                match = True
                oldversion = m.group(1)

                return oldversion

        if not match:
            print "No Match of %s" % self.pattern_string

        return None

    def increment_version(self, oldversion):
        major, minor, patch = oldversion.split('.')

        newpatch = int(patch) + 1

        newversion = "%s.%s.%s" % (major, minor, newpatch)

        return newversion

    # find the version in the contents, increment it, return the results
    def increment_version_in_content(self, content):
        output = ""

        match = {}

        for line in content.split("\n"):
            printed = False
            for pattern in self.patterns:
                m = re.search(pattern, line)
                if m:
                    oldversion = m.group(1)
                    newversion = self.increment_version(oldversion)

                    if not match.get(pattern) and not printed:
                        output += line.replace(oldversion, newversion) + "\n"
                        match[pattern] = True
                        printed = True
            if not printed:
                printed = True
                output += line + "\n"

        output = re.sub(r"\n+$", "\n", output)

        if not match:
            print "No Match of %s" % self.pattern_string

        return output

    def replace_pattern_in_content(self, content, replacement):
        output = ""
        match = {}
        updated = False
        printed = False

        for line in content.split("\n"):
            for pattern in self.patterns:
                m = re.search(pattern, line)
                if m:
                    oldversion = m.group(1)
                    newversion = replacement

                    if not match.get(pattern) and not printed:
                        output += line.replace(oldversion, newversion) + "\n"
                        match[pattern] = True
                        printed = True
            if not printed:
                printed = True
                output += line + "\n"

        output = re.sub(r"\n+$", "\n", output)

        if not match:
            print "No Match of %s" % self.pattern_string

        return output

    # updates the version file in git
    def update_file(self, content):
        msg = 'auto increment of version number in ' + self.file

        if self.org_or_user == 'org':
            oldsha = self.github.get_organization(self.org_or_user_name).get_repo(self.repo).get_file_contents(self.file, self.branch).sha

            self.github.get_organization(self.org_or_user_name).get_repo(self.repo).update_file(self.file, msg, content, oldsha, self.branch)
        else:
            oldsha = self.github.get_user(self.org_or_user_name).get_repo(self.repo).get_file_contents(self.file, self.branch).sha
            self.github.get_user(self.org_or_user_name).get_repo(self.repo).update_file(self.file, msg, content, oldsha, self.branch)


    def read_file_into_string(self, file):
        with open(file, 'r') as f:
            content = ""
            for line in f:
                content += line

        return content

if __name__ == '__main__':
    mode = None
    token = None
    giturl = None
    config = None
    branch = None
    file = None
    patterns = None
    org = None
    repo = None
    newvalue = None

    try:
        opts, args = getopt.getopt(sys.argv[1:], "hm:t:g:c:b:f:p:o:r:n:",
                                   ['help', 'mode=', 'token=', 'giturl=', 'config=', 'branch=', 'file=', 'patterns=', 'org=', 'repo=', 'newvalue='])
    except getopt.GetoptError as err:
        print str(err)
        exit(2)

    for opt, arg in opts:
        if opt in ('-h', '--help'):
            print "updater.py [htgucbfpor]\n" \
                  " -m mode\n" \
                  "-t token\n" \
                  "-g giturl defaults to 'https://api.github.com' \n" \
                  "-c config\n" \
                  "-b branch defaults to 'develop'\n" \
                  "-f file\n" \
                  "-p patterns\n" \
                  "-o org\n"\
                  "-r repo\n"\
                  "-n new value or filename in replace mode"

            sys.exit()
        elif opt in ("-m", "--mode"):
            mode = arg
        elif opt in ("-t", "--token"):
            token = arg
        elif opt in ("-g", "--giturl"):
            giturl = arg
        elif opt in ("-c", "--config"):
            config = arg
        elif opt in ("-b", "--branch"):
            branch = arg
        elif opt in ("-f", "--file"):
            file = arg
        elif opt in ("-p", "--patterns"):
            patterns = arg
        elif opt in ("-o", "--org"):
            org = arg
        elif opt in ("-r", "--repo"):
            repo = arg
        elif opt in ("-n", "--newvalue"):
            newvalue = arg

    u = Updater(gittoken=token, giturl=giturl, config=config, branch=branch, file=file, patterns=patterns, org=org, repo=repo)

    if mode == 'increment':
        content = u.get_file_from_git()
        newcontent = u.increment_version_in_content(content)
        u.update_file(newcontent)
    elif mode == 'update':
        content = u.get_file_from_git()
        newcontent = u.replace_pattern_in_content(content, newvalue)
        u.update_file(newcontent)
    elif mode == 'replace':
        content = u.get_file_from_git()
        newcontent = u.read_file_into_string(newvalue)
        u.update_file(newcontent)

    else:
        raise TypeError("Unknown mode: %s" % mode)





