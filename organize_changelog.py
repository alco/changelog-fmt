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

def sorted_changes(change_list):
    """change_list is a tuple of the form (category, line)"""
    return sorted(change_list, key=lambda x: x[0])

def extract_section(lines, startline):
    """ Enumerates lines until a set of changes matching the pattern is found.

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

    return changes, start, end

def organize_sections(infile, count=1):
    """Blank line separates sections"""
    release_re = re.compile(r'^# v')

    if count == 0:
        # Base of recursion
        return []

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
            return []
        if line.strip():
            # Non-blank line
            break
        start += 1

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
    if section:
        sorted_section = map(lambda x: x[1], sorted_changes(section))
        return lines[start:section_start] + sorted_section + lines[section_end:] + organize_sections(infile, count-1)
    return lines


if __name__ == '__main__':
    import argparse
    import shutil
    import sys

    parser = argparse.ArgumentParser(description="Organize changes in a Changelog file by category")
    parser.add_argument("in_file", metavar="file", nargs="?", type=argparse.FileType('r+'), default=sys.stdin, help="A Changelog file. Use - for stdin")
    parser.add_argument("-o", "--out_file", help="Optional output file. By default, the input file is modified in place")
    parser.add_argument("-n", metavar="section_count", help="Number of sections to organize. 0 means organize all sections until latest stable release. A negative value means organize the whole file. Default: 0.")
    args = parser.parse_args()

    infile = args.in_file
    if infile == sys.stdin and not args.out_file:
        raise RuntimeError("Must have output file when reading from stdin")

    if not args.out_file or args.out_file == infile.name:
        outfile = infile
    else:
        shutil.copy(args.in_file.name, args.out_file)
        outfile = open(args.out_file, 'w+')
    pos = infile.tell()

    lines = organize_sections(infile, -1)
    if lines:
        outfile.seek(pos)
        outfile.writelines(lines)
    else:
        print 'No sections found'

    infile.close()
    if outfile != infile:
        outfile.close()
