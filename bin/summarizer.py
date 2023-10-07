#!/usr/bin/env python
# coding: utf-8

import argparse

# Function to load BLAST results from a file
def load_blast_results(file_path):
    blast_results = []
    try:
        with open(file_path, 'r') as blast_file:
            for line in blast_file:
                columns = line.strip().split('\t')
                blast_results.append(columns)
    except FileNotFoundError:
        pass  # Ignore if the file does not exist
    return blast_results

# Function to filter sequences based on specified criteria
def filter_sequences(blast_results):
    detected_sequences_high = []
    for result in blast_results:
        alignment_length = int(result[5])  # Assuming Alignment Length is in the 6th column
        e_value = float(result[10])  # Assuming E-value is in the 11th column
        bitscore = float(result[11])  # Assuming Bitscore is in the 12th column

        # Check if the sequence meets the criteria for NIPAH detection with HIGH probability
        if alignment_length > 100 and (e_value < 0.00001 or bitscore > 100):
            detected_sequences_high.append(result)

    return detected_sequences_high

# Function to generate the summary table and remove duplicates
def generate_summary_table(blastn_results, blastx_results):
    # Combine both sets of BLAST results
    all_results = blastn_results + blastx_results

    # Initialize the summary table and a set to track unique query sequences
    summary_table = []
    unique_queries = set()

    for result in all_results:
        query_sequence = result[12]  # Assuming Query Sequence is in the 13th column

        # Check if the query sequence has not been added to the summary table yet
        if query_sequence not in unique_queries:
            alignment_length = int(result[5])
            e_value = float(result[10])
            bitscore = float(result[11])

            # Check if the sequence meets the criteria for HIGH probability NIPAH detection
            if alignment_length > 100 and (e_value < 0.00001 or bitscore > 100):
                summary_table.append(result + ["NIPAH DETECTED with HIGH probability"])
            else:
                summary_table.append(result + ["NIPAH DETECTED with LOW probability"])

            # Add the query sequence to the set of unique queries
            unique_queries.add(query_sequence)

    # If no NIPAH detection occurred, add a single entry to indicate that
    if not summary_table:
        summary_table = [["NO NIPAH DETECTED"]]

    return summary_table

# Function to print the summary table in HTML format
def print_summary_html(table, output_html):
    with open(output_html, 'w') as html_file:
        html_file.write("<html>")
        html_file.write("<head>")
        html_file.write("<title>Summary Report</title>")
        html_file.write('<style>')
        html_file.write('table {border-collapse: collapse; width: 100%;}')
        html_file.write('th, td {border: 1px solid #dddddd; text-align: left; padding: 8px;}')
        html_file.write('tr:nth-child(even) {background-color: #f2f2f2;}')  # Alternate row color
        html_file.write('tr.high-detected {background-color: yellow;}')  # Highlighted row color for HIGH probability
        html_file.write('</style>')
        html_file.write("</head>")
        html_file.write("<body>")
        html_file.write("<h1>Summary Report</h1>")
        html_file.write("<table>")
        
        # Print table headers
        html_file.write("<tr>")
        headers = ["Query ID", "Subject ID", "Subject Description", "Percent Identity", "Query Length", 
                   "Alignment Length", "Start Position", "End Position", "Alignment Start", "Alignment End", 
                   "E-value", "Bitscore", "Query Sequence", "Subject Database Sequence", "Result"]
        for header in headers:
            html_file.write(f"<th>{header}</th>")
        html_file.write("</tr>")
        
        # Print table rows with highlighting (only if NIPAH detected)
        if table[0][0] != "NO NIPAH DETECTED":
            for row in table:
                if "NIPAH DETECTED with HIGH probability" in row[-1]:
                    html_file.write('<tr class="high-detected">')
                else:
                    html_file.write('<tr>')
                for item in row:
                    html_file.write(f"<td>{item}</td>")
                html_file.write("</tr>")
        else:
            # Handle the case where no NIPAH detection occurred
            html_file.write('<tr class="no-nipah"><td colspan="15">NO NIPAH DETECTED</td></tr>')
        
        html_file.write("</table>")
        html_file.write("</body>")
        html_file.write("</html>")

# Function to print the summary table in plain text format
def print_summary_txt(table, output_txt):
    with open(output_txt, 'w') as txt_file:
        for row in table:
            txt_file.write('\t'.join(row) + '\n')

# Parse command-line arguments
parser = argparse.ArgumentParser(description='Summarize BLAST results.', allow_abbrev=False)
parser.add_argument('--blastn', help='Input BLASTn result file')
parser.add_argument('--blastx', help='Input BLASTx result file')
parser.add_argument('--output_html', default='summary_report.html', help='Output HTML file name')
parser.add_argument('--output_txt', default='summary_report.txt', help='Output TXT file name')

args = parser.parse_args()

# Load BLAST results
blastn_results = load_blast_results(args.blastn)
blastx_results = load_blast_results(args.blastx)

# Generate the summary table and remove duplicates
summary_table = generate_summary_table(blastn_results, blastx_results)

# Print the summary table in HTML format
print_summary_html(summary_table, args.output_html)

# Print the summary table in plain text format
print_summary_txt(summary_table, args.output_txt)
