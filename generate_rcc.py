#!/usr/bin/env python

# Script information for the file.
__author__ = "Philippe T. Pinard"
__email__ = "philippe.pinard@gmail.com"
__copyright__ = "Copyright (c) 2015 Philippe T. Pinard"
__license__ = "GPL v3"

# Standard library modules.
import os
import argparse
import xml.etree.ElementTree as etree
import xml.dom.minidom as minidom
import subprocess

try:
    import configparser
except ImportError:
    import ConfigParser as configparser

# Third party modules.

# Local modules.

# Globals and constants variables.

def create_qrc(themefilepath, exts=['.png', '.svg']):
    """
    Generates .qrc file from all images in the directory of the theme path.
    """
    basepath = os.path.dirname(themefilepath)

    # Parse index.theme
    parser = configparser.ConfigParser()
    parser.read(themefilepath)
    theme_name = parser.get('Icon Theme', 'Name')
    directories = parser.get('Icon Theme', 'Directories').split(',')

    # Create root
    root = etree.Element('RCC', version='1.0')
    prefix='icons/%s' % theme_name
    element_qresource = etree.SubElement(root, 'qresource', prefix=prefix)

    element = etree.SubElement(element_qresource, 'file', alias='index.theme')
    #element.text = os.path.abspath(themefilepath)
    element.text = themefilepath[len(prefix)+1:]

    # Find all image files
    for directory in directories:
        for dirpath, _, filenames in os.walk(os.path.join(basepath, directory)):
            for filename in filenames:
                if os.path.splitext(filename)[1] not in exts:
                    continue
                alias = os.path.join(directory, filename)
                #text = os.path.abspath(os.path.join(dirpath, filename))
                text = os.path.join(dirpath, filename)[len(prefix)+1:]
                element = etree.Element('file', alias=alias)
                element.text = text
                element_qresource.append(element)

    # Write
    outfilepath = os.path.join(basepath, theme_name + '.qrc')
    with open(outfilepath, 'w') as fp:
        fp.write(minidom.parseString(etree.tostring(root)).toprettyxml())

    return outfilepath

def convert_qrc(qrcfilepath):

    # remove first line <?xml version="1.0" ?>
    with open(qrcfilepath, "r") as rf:
        print(rf.readline())
        lines = [line for line in rf]

    with open(qrcfilepath, "w") as wf:
        for line in lines:
            wf.write(line)

def run_rcc(qrcfilepath):
    outfilepath = os.path.splitext(qrcfilepath)[0] + '.py'
    args = ['pyrcc5', '-o', outfilepath, '-compress', '9', qrcfilepath]
    print(" ".join(args))
    subprocess.check_call(args)

def run():
    parser = argparse.ArgumentParser(description='Generate rcc')
    parser.add_argument('theme', metavar='FILE', help='Path to .theme file')

    args = parser.parse_args()

    qrcfilepath = create_qrc(args.theme)
    print(qrcfilepath)
    convert_qrc(qrcfilepath)
    run_rcc(qrcfilepath)

if __name__ == '__main__':
    run()
