import json
import os
import sys

def generate_html_for_value(value):
    """
    Recursively generates HTML for a given Python object (from JSON).
    Handles dictionaries, lists, and primitive values.
    """
    if isinstance(value, dict):
        # If the value is a dictionary, create a nested table
        return generate_html_table(value)
    elif isinstance(value, list):
        # If the value is a list, create an unordered list
        if not value:
            return "<em>Empty list</em>"
        html = "<ul>"
        for item in value:
            # Each list item's value is also processed recursively
            html += f"<li>{generate_html_for_value(item)}</li>"
        html += "</ul>"
        return html
    elif value is None:
        return "<em>null</em>"
    else:
        # For simple values (string, number, boolean), just return them
        # We can add HTML escaping here if needed, but for display it's often fine.
        return str(value)

def generate_html_table(data):
    """
    Generates an HTML table for a dictionary.
    """
    html = '<table class="json-table">'
    for key, value in data.items():
        html += "<tr>"
        # The key is in the first column
        html += f'<td class="key-cell">{key}</td>'
        # The processed value is in the second column
        html += f"<td>{generate_html_for_value(value)}</td>"
        html += "</tr>"
    html += "</table>"
    return html

def create_report(file_list_path, output_filename="report.html"):
    """
    Reads a list of JSON files and generates a single HTML report.
    """
    if not os.path.exists(file_list_path):
        print(f"Error: Input file '{file_list_path}' not found.")
        return

    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>JSON Report</title>
        <style>
            body {
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen,
                             Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif;
                line-height: 1.6;
                color: #333;
                background-color: #f8f9fa;
                margin: 0;
                padding: 20px;
            }
            .container {
                max-width: 900px;
                margin: 0 auto;
                background-color: #ffffff;
                padding: 25px;
                border-radius: 8px;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            }
            h1 {
                color: #0056b3;
                border-bottom: 2px solid #e9ecef;
                padding-bottom: 10px;
            }
            .accordion {
                background-color: #e9ecef;
                color: #343a40;
                cursor: pointer;
                padding: 18px;
                width: 100%;
                border: none;
                text-align: left;
                outline: none;
                font-size: 1.1em;
                font-weight: bold;
                transition: background-color 0.4s;
                border-radius: 5px;
                margin-top: 10px;
            }
            .active, .accordion:hover {
                background-color: #ced4da;
            }
            .accordion:after {
                content: '\\002B'; /* Plus sign */
                color: #343a40;
                font-weight: bold;
                float: right;
                margin-left: 5px;
            }
            .active:after {
                content: "\\2212"; /* Minus sign */
            }
            .panel {
                padding: 0 18px;
                background-color: white;
                max-height: 0;
                overflow: hidden;
                transition: max-height 0.2s ease-out;
                border-bottom-left-radius: 5px;
                border-bottom-right-radius: 5px;
                border: 1px solid #e9ecef;
                border-top: none;
            }
            .json-table {
                width: 100%;
                border-collapse: collapse;
                margin-top: 15px;
                margin-bottom: 15px;
            }
            .json-table td {
                border: 1px solid #dee2e6;
                padding: 10px 12px;
                vertical-align: top;
            }
            .json-table tr:nth-child(even) {
                background-color: #f8f9fa;
            }
            .key-cell {
                font-weight: bold;
                color: #495057;
                width: 25%;
            }
            .json-table .json-table {
                margin-top: 0;
                border-top: 2px solid #adb5bd;
            }
            ul {
                list-style-type: disc;
                margin: 0;
                padding-left: 20px;
            }
            li {
                margin-bottom: 5px;
            }
            em {
                color: #888;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>JSON Files Report</h1>
    """

    # Read the list of JSON file paths
    with open(file_list_path, 'r') as f:
        json_files = [line.strip() for line in f if line.strip()]

    for json_path in json_files:
        if not os.path.exists(json_path):
            print(f"Warning: JSON file '{json_path}' not found. Skipping.")
            continue

        html_content += f'<button class="accordion">{os.path.basename(json_path)}</button>'
        html_content += '<div class="panel">'
        try:
            with open(json_path, 'r') as json_file:
                data = json.load(json_file)
                html_content += generate_html_table(data)
        except json.JSONDecodeError:
            print(f"Error: Could not decode JSON from '{json_path}'. Skipping.")
            html_content += "<p><em>Error: Invalid JSON format.</em></p>"
        except Exception as e:
            print(f"An unexpected error occurred with file '{json_path}': {e}")
            html_content += f"<p><em>Error processing file: {e}</em></p>"
        html_content += '</div>'


    html_content += """
        </div>
        <script>
            var acc = document.getElementsByClassName("accordion");
            var i;
            for (i = 0; i < acc.length; i++) {
                acc[i].addEventListener("click", function() {
                    this.classList.toggle("active");
                    var panel = this.nextElementSibling;
                    if (panel.style.maxHeight) {
                        panel.style.maxHeight = null;
                    } else {
                        panel.style.maxHeight = panel.scrollHeight + "px";
                    }
                });
            }
        </script>
    </body>
    </html>
    """

    # Write the final HTML to a file
    with open(output_filename, 'w') as f:
        f.write(html_content)

    print(f"Successfully generated report: '{output_filename}'")


if __name__ == "__main__":
    create_report("json_file_paths.txt")

