# build_tools

Tools for building stuff

## Build Status: [![CircleCI](https://circleci.com/gh/nikogura/build-tools.svg?style=svg)](https://circleci.com/gh/nikogura/build-tools)

## updater.py
Increments or updates the last number of a version string in a file in git.

So, if used in a job that publishes artifacts from a master branch, it would, as part of the job, increment the version number in the appropriate file in the develop branch for further work.

### config file

        [default]
        username        = iautobot
        gh_token        = <github token>
        gh_url          = https://github.pie.apple.com/api/v3
        org             = iossys-devops
        repo            = build-tools-test-repo
        branch          = develop
        
### usage

        python updater.py -f /setup.py -p "\s+version='(\d+\.\d+\.\d+)'," -t token -o github-org -r github-repo -b branch -m increment
        
        python updater.py -f /setup.py -p "\s+version='(\d+\.\d+\.\d+)'," -t token -o github-org -r github-repo -b branch -m increment
        

