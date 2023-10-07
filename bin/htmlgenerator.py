#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import argparse

# Define the HTML template for blastn
blastn_template = """
<html>
<head>
    <title>BlastN Results</title>
    <style>
    table {{
        border-collapse: collapse;
        width: 100%;
    }}
    th, td {{
        border: 1px solid #dddddd;
        text-align: left;
        padding: 8px;
        white-space: normal;
    }}
    </style>
</head>
<body>
    <h1>BLAST Results</h1>
    <table>
        <tr>
            <th>Query ID</th>
            <th>Subject ID</th>
            <th>Subject Description</th>
            <th>Percent Identity</th>
            <th>Query Length</th>
            <th>Alignment Length</th>
            <th>Start Position</th>
            <th>End Position</th>
            <th>Alignment Start</th>
            <th>Alignment End</th>
            <th>E-value</th>
            <th>Bitscore</th>
            <th>Query Sequence</th>
            <th>Subject Database Sequence</th>
        </tr>
        {table_content}
    </table>
</body>
</html>
"""

# Define the HTML template for blastx (without qstart, qend, sstart, send)
blastx_template = """
<html>
<head>
    <title>BlastX Results</title>
    <style>
    table {{
        border-collapse: collapse;
        width: 100%;
    }}
    th, td {{
        border: 1px solid #dddddd;
        text-align: left;
        padding: 8px;
        white-space: normal;
    }}
    </style>
</head>
<body>
    <h1>BLAST Results</h1>
    <table>
        <tr>
            <th>Query ID</th>
            <th>Subject ID</th>
            <th>Subject Description</th>
            <th>Percent Identity</th>
            <th>Query Length</th>
            <th>Alignment Length</th>
            <th>E-value</th>
            <th>Bitscore</th>
            <th>Query Sequence</th>
            <th>Subject Database Sequence</th>
        </tr>
        {table_content}
    </table>
</body>
</html>
"""
# Function to remove duplicates based on Query ID
def remove_duplicates(blast_results):
    unique_results = []
    seen_ids = set()
    for result in blast_results:
        query_id = result[0]  # Assuming the Query ID is in the first column
        if query_id not in seen_ids:
            unique_results.append(result)
            seen_ids.add(query_id)
    return unique_results

# Parse command-line arguments with any order
parser = argparse.ArgumentParser(description='Generate HTML report from BLAST results.', allow_abbrev=False)

# Specify optional arguments with '--' prefix
parser.add_argument('--blast_type', choices=['blastn', 'blastx'], help='Type of BLAST result')
parser.add_argument('--input', help='Input BLAST result file')
parser.add_argument('--output', default='blast_report.html', help='Output HTML file name')

# Allow arguments to be specified in any order
args = parser.parse_args()

# Check if either 'blastn' or 'blastx' was provided, otherwise default to 'blastn'
if args.blast_type not in ('blastn', 'blastx'):
    args.blast_type = 'blastn'

# Open the BLAST result file for reading
with open(args.input, 'r') as blast_file:
    # Initialize a list to store BLAST result rows
    blast_results = []

    # Read each line from the file
    for line in blast_file:
        # Split the line into columns based on tab ('\t') separator
        columns = line.strip().split('\t')

        # For blastx results, remove the columns related to Start Position, End Position, Alignment Start, and Alignment End
        if args.blast_type == 'blastx':
            columns = columns[:7] + columns[11:]

        # Append the modified columns to the blast_results list
        blast_results.append(columns)

# Remove duplicates based on Query ID
blast_results = remove_duplicates(blast_results)

# Select the appropriate HTML template based on the blast_type
if args.blast_type == 'blastn':
    html_template = blastn_template
else:
    html_template = blastx_template

# Generate the table rows from the BLAST results
table_rows = ""
for result in blast_results:
    row = "<tr>"
    for item in result:
        row += f"<td>{item}</td>"
    row += "</tr>"
    table_rows += row

# Replace the {table_content} placeholder in the template with the actual table content
final_html = html_template.format(table_content=table_rows)

# Write the final HTML report to the specified output file
with open(args.output, "w") as html_file:
    html_file.write(final_html)

