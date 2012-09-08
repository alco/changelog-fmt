import re

def sorted_changes(change_list):
    """change_list is a tuple of the form (category, line)"""
    return sorted(change_list, key=lambda x: x[0])

def extract_section(lines, startline):
    PARSE_STATE_SEARCHING = 1
    PARSE_STATE_COLLECTING = 2

    state = PARSE_STATE_SEARCHING
    sect_re = re.compile(r'^\s+\* \[(\w+)\]')

    current_section = []
    start = 0
    end = -1
    for i in range(startline, len(lines)):
        line = lines[i]
        if state == PARSE_STATE_SEARCHING:
            match = sect_re.match(line)
            if match:
                start = i
                current_section.append((match.group(1), line))
                state = PARSE_STATE_COLLECTING
        elif state == PARSE_STATE_COLLECTING:
            match = sect_re.match(line)
            if match:
                current_section.append((match.group(1), line))
            else:
                end = i
                break

    return current_section, start, end

def organize_sections(infile, count=1):
    """Blank line separates sections"""
    def get_line():
        return infile.readline()

    lines = []
    start = 0
    # Skip initial blank lines
    while True:
        line = get_line()
        if not line:
            # Unexpected EOF
            return
        lines.append(line)
        if line.strip():
            break
        start += 1

    # Find out the end of the section
    while True:
        line = get_line()
        if not line:
            # EOF
            break
        lines.append(line)
        if not line.strip():
            break

    section, section_start, section_end = extract_section(lines, start)
    sorted_section = map(lambda x: x[1], sorted_changes(section))

    return lines[start:section_start] + sorted_section + lines[section_end:]

if __name__ == '__main__':
    import shutil
    import sys

    infilename = 'changelog'
    outfilename = 'result'

    # Copy the input file to another location
    shutil.copy(infilename, outfilename)

    infile = open(outfilename, 'r+')
    pos = infile.tell()
    lines = organize_sections(infile)
    infile.seek(pos)
    infile.writelines(lines)
    infile.close()
    exit(0)

    output_lines = []

    index = 0
    while True:
        section, start, end = extract_section(input_lines, index)
        if end == -1:
            output_lines.extend(input_lines[index:])
            break
        print section
        print start
        print end
        output_lines.extend(input_lines[index:start])
        sorted_section = sorted_changes(section)
        output_lines.extend(map(lambda x: x[1], sorted_section))
        index = end

    with open('result', 'w') as outfile:
        outfile.writelines(output_lines)
