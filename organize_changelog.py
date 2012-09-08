#!/usr/bin/env python

"""
Organize your Changelog file by ordering changes by category.

A category is enclosed between brackets [ and ].

Example of the Changelog format:

    * header
      * [Cat1] Description
      * [Cat2] Description
      ...
      * [CatN] Description


    # new release

    ...

"""

import re
import shutil

def sorted_changes(change_list):
    """change_list is a tuple of the form (category, line)"""
    return sorted(change_list, key=lambda x: x[0])

def extract_section(lines, startline):
    """Enumerates lines until a set of changes matching the pattern is found.

    Returns a list of tuples of the form (category, line) and the
    indices of the first and last lines comprising the change set.

    """
    sect_re = re.compile(r'^\s+\* \[([^\]]+)\]')
    changes = []

    def get_match(line):
        m = sect_re.match(line)
        if m:
            # m.group(1) is a category name
            changes.append((m.group(1), line))
            return True

    searching = True

    start, end = startline, startline
    for i in range(startline, len(lines)):
        line = lines[i]
        match = get_match(line)
        if searching:
            if match:
                start = i
                searching = False
        elif not match:
            end = i
            break
    # Fix for the case when the loop has finished before assignment
    # to end
    if end < start:
        end = len(lines)

    return changes, start, end

def organize_sections(infile, count=1, match_release=False, accum=[]):
    release_re = re.compile(r'^# v')

    if count == 0:
        # Base of recursion
        return accum

    lines = []
    def get_line():
        line = infile.readline()
        if line:
            lines.append(line)
            return line

    start = 0
    # Skip initial blank lines
    while True:
        line = get_line()
        if not line:
            # Unexpected EOF
            return accum
        if line.strip():
            # Non-blank line
            break
        start += 1

    if match_release and release_re.match(line):
        return accum + lines

    # Find out the end of the section
    while True:
        line = get_line()
        if not line:
            # EOF
            break
        if not line.strip():
            # blank line
            break

    section, section_start, section_end = extract_section(lines, start)
    sorted_section = map(lambda x: x[1], sorted_changes(section))

    result = accum + lines[start:section_start] + sorted_section + lines[section_end:]
    if sorted_section:
        new_count = count-1
    else:
        new_count = count
    return organize_sections(infile, new_count, match_release, result)

def run(infile, outfilename, section_count):
    if not outfilename or outfilename == infile.name:
        # Modify the input file in-place
        outfile = infile
    else:
        # Copy the input file and then modify the output one
        shutil.copy(infile.name, outfilename)
        outfile = open(outfilename, 'r+')

    pos = infile.tell()
    if section_count == 0:
        lines = organize_sections(infile, -1, True)
    else:
        lines = organize_sections(infile, section_count)

    if lines:
        outfile.seek(pos)
        outfile.writelines(lines)
        status = 0
    else:
        print 'No sections found'
        status = 1

    infile.close()
    outfile.close()

    return status


if __name__ == '__main__':
    import argparse
    import shutil
    import sys

    parser = argparse.ArgumentParser(
            description="Organize changes in a Changelog file by category")
    parser.add_argument("in_file", metavar="file",
            type=argparse.FileType('r+'), help="A Changelog file.")
    parser.add_argument("-o", "--out_file",
            help="Optional output file. By default, the input file is modified in-place.")
    parser.add_argument("-n", "--section_count", type=int, default=0,
            help="Number of sections to organize. 0 means organize all sections until latest stable release. " +
                 "A negative value means organize the whole file. Default: 0.")
    args = parser.parse_args()

    infile = args.in_file
    if infile == sys.stdin:
        raise RuntimeError("Stdin not supported")

    status = run(infile, args.out_file, args.section_count)

    exit(status)
