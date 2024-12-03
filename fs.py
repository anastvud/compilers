import re

header_pattern = re.compile(r'^(#{1,6})\s*(.*)')
bold_pattern = re.compile(r'\*\*(.*?)\*\*')
italic_pattern = re.compile(r'\*(.*?)\*')
list_item_pattern = re.compile(r'^-\s+(.*)')
link_pattern = re.compile(r'\[(.*?)\]\((.*?)\)')
code_pattern = re.compile(r'`([^`]+)`')


def read_markdown_file(file_path):
    """Reads Markdown content from a file."""
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

def write_latex_file(file_path, latex_content):
    """Writes LaTeX content to a file."""
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(latex_content)

def parse_line(line):
    header_match = header_pattern.match(line)
    if header_match:
        level = len(header_match.group(1))
        text = header_match.group(2)
        return f"\\section{'*' * (level - 1)}{{{text}}}"

    list_match = list_item_pattern.match(line)
    if list_match:
        item_text = parse_inline_elements(list_match.group(1))
        return f"\\item {item_text}"

    return parse_inline_elements(line)


def parse_inline_elements(text):
    text = bold_pattern.sub(r'\\textbf{\1}', text)
    text = italic_pattern.sub(r'\\textit{\1}', text)
    text = link_pattern.sub(r'\\href{\2}{\1}', text)

    return text


def markdown_to_latex(markdown):
    """Convert an entire Markdown document to a standalone LaTeX document."""
    latex_lines = []
    lines = markdown.splitlines()
    list_stack = []  # Keeps track of nested list levels
    current_indent = 0

    # Add LaTeX preamble
    latex_lines.append(r"\documentclass{article}")
    latex_lines.append(r"\usepackage{hyperref}")  # For links
    latex_lines.append(r"\usepackage{enumitem}")  # For better list formatting
    latex_lines.append(r"\usepackage{amsmath}")   # For mathematical symbols (optional)
    latex_lines.append(r"\usepackage{amssymb}")   # For symbols (optional)
    latex_lines.append(r"\usepackage{graphicx}")  # For images (if needed later)
    latex_lines.append(r"\begin{document}")

    for line in lines:
        line = line.rstrip()
        if not line:
            continue  # Skip empty lines

        # Determine the current indentation level
        stripped_line = line.lstrip()
        indent_level = len(line) - len(stripped_line)
        
        # Handle list environments
        if stripped_line.startswith('-'):
            if not list_stack or indent_level > current_indent:
                # Start a new nested list
                latex_lines.append(r'\begin{itemize}')
                list_stack.append('itemize')
            elif indent_level < current_indent:
                # Close lists until we match the current indentation
                while list_stack and indent_level < current_indent:
                    latex_lines.append(r'\end{' + list_stack.pop() + '}')
                    current_indent -= 2
            current_indent = indent_level
            item_text = parse_inline_elements(stripped_line[1:].strip())
            latex_lines.append(r'\item ' + item_text)
        elif re.match(r'^\d+[\.\)]', stripped_line):
            if not list_stack or indent_level > current_indent:
                # Start a new ordered list
                latex_lines.append(r'\begin{enumerate}')
                list_stack.append('enumerate')
            elif indent_level < current_indent:
                # Close lists until we match the current indentation
                while list_stack and indent_level < current_indent:
                    latex_lines.append(r'\end{' + list_stack.pop() + '}')
                    current_indent -= 2
            current_indent = indent_level

            # Process the current and subsequent lines as part of the ordered list
            while re.match(r'^\d+[\.\)]', stripped_line):
                # Extract the text after the number and period/parenthesis
                item_text = parse_inline_elements(stripped_line.split(maxsplit=1)[1].strip())
                latex_lines.append(r'\item ' + item_text)
                
                # Move to the next line
                next_index = lines.index(line) + 1
                if next_index < len(lines):
                    line = lines[next_index].rstrip()
                    stripped_line = line.lstrip()
                    indent_level = len(line) - len(stripped_line)
                else:
                    break
        else:
            # Close all open lists if a non-list item is encountered
            while list_stack:
                latex_lines.append(r'\end{' + list_stack.pop() + '}')
            current_indent = 0

            # Parse and add non-list content
            latex_line = parse_line(line)
            latex_lines.append(latex_line)

    # Close any remaining open lists
    while list_stack:
        latex_lines.append(r'\end{' + list_stack.pop() + '}')

    # Add LaTeX document end
    latex_lines.append(r"\end{document}")

    return '\n'.join(latex_lines)




input_file = 'example.md'   # Replace with your Markdown file path
output_file = 'output.tex'  # Replace with your desired LaTeX file path

# Read Markdown input
markdown_text = read_markdown_file(input_file)

# Convert Markdown to LaTeX
latex_output = markdown_to_latex(markdown_text)

# Write LaTeX output to file
write_latex_file(output_file, latex_output)

print(f"LaTeX content has been written to {output_file}")