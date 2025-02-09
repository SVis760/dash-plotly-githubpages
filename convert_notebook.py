import nbformat
from nbconvert import HTMLExporter
import argparse
import os

def convert_notebook(notebook_path, output_path=None):
    """Convert a Jupyter Notebook to an HTML file."""
    
    # Load the Jupyter Notebook
    with open(notebook_path, "r", encoding="utf-8") as f:
        notebook_content = nbformat.read(f, as_version=4)

    # Convert notebook to HTML
    html_exporter = HTMLExporter()
    html_exporter.exclude_input = False  # Include input cells
    body, _ = html_exporter.from_notebook_node(notebook_content)

    # Determine output path
    if not output_path:
        output_path = notebook_path.replace(".ipynb", ".html")

    # Save the converted HTML file
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(body)

    print(f"✅ Successfully converted {notebook_path} to {output_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert Jupyter Notebook to HTML")
    parser.add_argument("notebook", help="Path to the Jupyter Notebook (.ipynb)")
    parser.add_argument("--output", help="Path to save the HTML file", default=None)
    args = parser.parse_args()

    convert_notebook(args.notebook, args.output)
