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

def organize_sections(infile, outfile):
    """Blank line separates sections"""
    lines = infile.

if __name__ == '__main__':
    with open('changelog') as infile:
        input_lines = infile.readlines()

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
