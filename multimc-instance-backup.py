#!/bin/python3
import os, sys, shutil
from os import path

# To have this script automatically run when a MultiMC instance shuts down,
# place this script in the folder you wish to back up to and go to MultiMC -> Settings -> Custom Commands -> put this in Post-exit Command:
# python3 path/to/multimc-instance-backup.py "$INST_NAME" "$INST_MC_DIR"
# Pro tip: place the script in a cloud folder to automagically back up your instance to your cloud provider :)

print("----------------------------------------------------------------")
print("MultiMC Instance Backup")
print("Written by Stephen-Hamilton-C")
print("Find the source at https://github.com/Stephen-Hamilton-C/multimc-instance-backup")
print("Usage: 'python3 multimc-instance-backup.py <INSTANCE_NAME> <.MINECRAFT_PATH>'")
print()

if len(sys.argv) < 3:
	print("Improper usage, see above.")
	print(sys.argv)
	sys.exit(64)

# I was thinking of adding more functionality to this, like replace or ignore, but I ended up not
# I still might tho, so I'm leaving this here for now
class Fragment:
	def __init__(self, path):
		self.path = path

# Fill list with files or folders to backup from the .minecraft directory
# These should be relative paths as if you are inside the .minecraft directory
# Use path.join() if you must navigate into a directory as that is platform independent (e.g. path.join("config", "fabric"))
BACKUP = [
	Fragment("options.txt"), # Minecraft options
	Fragment("config"), # Mod settings
	Fragment("shaderpacks"), # Also includes shaderpack settings
	Fragment("resourcepacks"),
	Fragment("screenshots"),
	Fragment("mods"),
	# Fragment("saves"),
]

# Paths derived from script location and arguments
cloudPath = path.dirname(path.realpath(__file__))
backupRootPath = path.join(cloudPath, "Backup", sys.argv[1])
mcPath = path.realpath(sys.argv[2])

print("Cloud Path: "+str(cloudPath))
print("Backup Path: "+str(backupRootPath))
print("MC Dir: "+str(mcPath))
print()

# Make backup dir if necessary
if not path.exists(backupRootPath):
	os.makedirs(backupRootPath)

for fragment in BACKUP:
	# instancePath is the file path in the instance we're backing up
	# backupPath is the file path this fragment will be backed up to
	instancePath = path.join(mcPath, fragment.path)
	backupPath = path.join(backupRootPath, fragment.path)

	# Don't back up if fragment does not exist
	if not path.exists(instancePath):
		print("Fragment "+str(fragment.path)+" does not exist, ignoring...")
		continue

	print("Backing up "+str(instancePath)+" to "+str(backupPath)+"...")

	# Behavior is to replace existing files, so we must delete currently existing files
	if path.exists(backupPath):
		print("Removing old file...")
		if path.isfile(backupPath):
			os.remove(backupPath)
		else:
			shutil.rmtree(backupPath)

	# Copy fragment to backup folder
	if path.isfile(instancePath):
		shutil.copyfile(instancePath, backupPath)
	else:
		shutil.copytree(instancePath, backupPath)

	print("Backed up "+str(instancePath))

print()
print("Finished backup")
print("----------------------------------------------------------------")