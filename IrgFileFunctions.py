#!/usr/bin/env python
# -*- coding: utf-8 -*-
# __BEGIN_LICENSE__
#  Copyright (c) 2009-2013, United States Government as represented by the
#  Administrator of the National Aeronautics and Space Administration. All
#  rights reserved.
#
#  The NGT platform is licensed under the Apache License, Version 2.0 (the
#  "License"); you may not use this file except in compliance with the
#  License. You may obtain a copy of the License at
#  http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
# __END_LICENSE__

"""IrgFileFunctions.py - General functions for handling files"""

import sys, os, re, shutil, subprocess, string, time, errno


def createFolder(path):
    """Creates a folder if it does not already exist"""
    if path == '':
        return
    if not os.path.exists(path):
        os.mkdir(path)

def removeIfExists(path):
    """Removes a file if it exists"""
    try:
        os.remove(path)
    except OSError as e: 
        if e.errno != errno.ENOENT: # Continue if the error is "no such file or directory"
            raise # Re-raise the exception if a different error occured

def removeFolderIfExists(directory):
    """Removes a directory and everything in it"""
    try:
        shutil.rmtree(directory)
    except OSError as e: 
        if e.errno != errno.ENOENT: # Continue if the error is "no such file or directory"
            raise # Re-raise the exception if a different error occured

def getFileLineCount(filePath):
    """Counts up the number of lines in a file"""
    f = open(filePath)
    i = 0
    for line in f:
        i = i + 1
    return i

def checkIfToolExists(toolName):
    """Returns true if the system knows about the utility with this name (it is on the PATH)"""

    # Look for the tool using the 'which' command
    cmd = ['which', toolName]
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    translateOut, err = p.communicate()
    

    # Check if that command failed to find the file
    failString = 'no ' + toolName + ' in ('
    if translateOut.find(failString) >= 0:
        raise Exception('Missing requested tool ' + toolName)
    else:
        return True


def getLastGitTag(codePath):
    """Returns the last brief git tag of the repository containing the file""" 

    # Get path to git folder
    codeFolder = os.path.dirname(codePath)
    gitFolder  = os.path.join(codeFolder, '.git/')
    
    # Get the tag using a subprocess call
    cmd = ['git', '--git-dir', gitFolder, 'describe', '--abbrev=0']
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    textOutput, err = p.communicate()
    
    # Check for errors
    if (textOutput.find('fatal:') >=0):
        raise Exception('Error: getLastGitTag failed on code path ' + codePath)

    return textOutput

def tarFileList(fileList, outputPath):
    """Creates a tar file containing a list of files with no absolute paths"""

    # This extra set of commands is needed to strip the absolute path name from each stored file
    cmd = 'tar -jcvf ' + outputPath
    for f in fileList:
        cmd = cmd + ' -C ' + os.path.dirname(f) + ' ' + os.path.basename(f)
    print cmd
    os.system(cmd)



