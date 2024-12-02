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
    in_list = False

    # Add LaTeX preamble
    latex_lines.append(r"\documentclass{article}")
    latex_lines.append(r"\usepackage{hyperref}")  # For links
    latex_lines.append(r"\usepackage{enumitem}")  # For better list formatting
    latex_lines.append(r"\usepackage{amsmath}")   # For mathematical symbols (optional)
    latex_lines.append(r"\usepackage{amssymb}")   # For symbols (optional)
    latex_lines.append(r"\usepackage{graphicx}")  # For images (if needed later)
    latex_lines.append(r"\begin{document}")

    for line in lines:
        line = line.strip()
        if not line:
            continue  # Skip empty lines

        # Handle list environment
        if line.startswith('-') and not in_list:
            latex_lines.append(r'\begin{itemize}')
            in_list = True
        elif not line.startswith('-') and in_list:
            latex_lines.append(r'\end{itemize}')
            in_list = False

        # Parse the line and add the LaTeX translation
        latex_line = parse_line(line)
        latex_lines.append(latex_line)

    # Close any remaining open list environment
    if in_list:
        latex_lines.append(r'\end{itemize}')

    # Add LaTeX document end
    latex_lines.append(r"\end{document}")

    return '\n'.join(latex_lines)



# markdown_text = """

# """

# File paths
input_file = 'example.md'   # Replace with your Markdown file path
output_file = 'output.tex'  # Replace with your desired LaTeX file path

# Read Markdown input
markdown_text = read_markdown_file(input_file)

# Convert Markdown to LaTeX
latex_output = markdown_to_latex(markdown_text)

# Write LaTeX output to file
write_latex_file(output_file, latex_output)

print(f"LaTeX content has been written to {output_file}")