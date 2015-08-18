#!/usr/bin/python

# TurboStart 1.0
# Copyright (C) 2014-2015 Naveen Kumarasinghe <dndkumarasinghe@gmail.com>
# License: http://www.gnu.org/licenses/gpl.html

import subprocess
import sys
import os
import tarfile
import shutil

# creating cache directory
if not os.path.exists("/opt/TurboStart"):
	os.makedirs("/opt/TurboStart")

# validating parameters
argc = len(sys.argv)

if (argc < 3):
	print("USAGE: turbostart [program_path] [binary_file] [user_name] [configurations_directory] [arg1]...[argn]")
	sys.exit()


# obtaining program's metadata
user = "naveen"
app_name = sys.argv[2].split('.')[0]
app_dir = sys.argv[1]
exe_file = sys.argv[2]
app_cache_file = "/opt/TurboStart/{}.tar.gz".format(app_name)
config_dir = sys.argv[4] if argc > 4 else ""
config_cache_file = "{}.tar.gz".format(config_dir)
ram_dir = "/run/shm/TurboStart"
args = []

for i in range(5,argc):
	args.append(sys.argv[i])

# mounting configuration cache
if not (config_dir == ""):

	# creating configuration cache if does not exist
	if not (os.path.exists(config_cache_file)):
		with tarfile.open(config_cache_file, "w") as tar:
			tar.add(config_dir)

	# extracting configuration cache to ram
	with tarfile.open(config_cache_file) as tar:
      		tar.extractall(ram_dir)

	# disable configurations on the disk
	os.rename(config_dir, config_dir + "_")

	# enable configurations on ram
	os.symlink(ram_dir + config_dir, config_dir)


# creating application cache if does not exist
if not (os.path.isfile(app_cache_file)):
	with tarfile.open(app_cache_file, "w") as tar:
		tar.add(app_dir)


# making ram_dir if does not exist 
if not os.path.exists(ram_dir):
	os.makedirs(ram_dir)


# extract program cache to ram
with tarfile.open(app_cache_file) as tar:
        tar.extractall(ram_dir)


# runs the program
subprocess.call(['su' , user , '-c',  '{}'.format(ram_dir + app_dir + "/" + exe_file + ' ' + ' '.join(args))])


# freeing ram
shutil.rmtree(ram_dir + "/" + app_dir)


# unmounting configuration cache

if not (config_dir == ""):

	# writing configuration cache to the disk
	os.chdir(ram_dir)

	subprocess.call("cd {};tar -cf {} {}".format(ram_dir, config_cache_file, config_dir[1:]), shell=True)

	# disable configurations on ram
	os.remove(config_dir)

	# enable configurations on the disk
	os.rename(config_dir + "_", config_dir)

	# freeing configuration memory
	shutil.rmtree(ram_dir + config_dir)
	
