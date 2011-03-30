#-------------------------------------------------------------------------------
# Name:        module2
# Purpose:
#
# Author:      Greg
#
# Created:     20/03/2011
# Copyright:   (c) Greg 2011
# Licence:     <your licence>
#-------------------------------------------------------------------------------
#!/usr/bin/env python

import os

def findFiles(dir):
  files = []

  # remove a trailing slash if it exists
  if dir[-1:] == "/":
    dir = dir[0:-1]

  # loop through files and directories
  for x in os.listdir(dir):
    if os.path.isdir(dir + "/" + x):
      # list this dir also
      files.extend(findFiles(dir + "/" + x))
    else:
      # add the file to the list
      files.append(dir + "/" + x)
  return files



##  # get the list of files
##  files = findFiles(sys.argv[1])
##
##  for file in files:
##    print file