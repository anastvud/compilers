from program import read_markdown_file, markdown_to_latex, write_latex_file


if __name__ == "__main__":
    input_file = 'example.md'
    output_file = 'output.tex'

    # Read Markdown input
    markdown_text = read_markdown_file(input_file)

    # Convert Markdown to LaTeX
    latex_output = markdown_to_latex(markdown_text)

    # Write LaTeX output to file
    write_latex_file(output_file, latex_output)

    print(f"LaTeX content has been written to {output_file}")