#!/usr/bin/env python

from __future__ import print_function
import os, subprocess, shutil

# shell command helper function
def shell(command):
    proc = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    (out, err) = proc.communicate()
    print(command)
    if out:
          print(out)

# get root path for dotfiles repo
root = os.path.dirname(os.path.realpath(__file__))

# add source statements to rc files if they're not there already
def source(type):
    rc_path = os.path.expanduser("~/.%s" % (type))
    source_cmd = "source %s" %(os.path.join(root, type))
    
    if source_cmd not in open(rc_path).read():
        shell('echo "\n%s" >> %s' % (source_cmd, rc_path))
        
source("bashrc")
source("vimrc")

# set up git config file includes
shell('git config --global core.excludesfile %s' % (os.path.join(root, "gitignore")))
shell('git config --global include.path %s' % (os.path.join(root, "gitconfig")))

# symlink files that can't be sourced
proto = 'ln -sf %s ~/.%s' % (os.path.join(root, "%s"), "%s")
shell(proto % ("tmux.conf", "tmux.conf"))
shell(proto % ("inputrc", "inputrc"))

# add Vim backup and swap directories
shell('mkdir -p ~/.vim-swap')
shell('mkdir -p ~/.vim-tmp')

# create config file using default version
proto = os.path.join(root, "%s")
shutil.copyfile(proto % ("dotfiles.cfg.default"), proto %("dotfiles.cfg"))
