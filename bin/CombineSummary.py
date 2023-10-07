#!/usr/bin/env python
import os
import argparse

# Function to read and combine summary reports
def combine_summary_reports(input_folder, output_html, output_txt):
    combined_data = {}  # Dictionary to store sample ID and NIPAH detection result

    # Iterate over subfolders in the input folder (sample names)
    for sample_folder in os.listdir(input_folder):
        sample_folder_path = os.path.join(input_folder, sample_folder)

        # Check if the subfolder is a directory
        if os.path.isdir(sample_folder_path):
            report_file_path = os.path.join(sample_folder_path, "06_final_results", f"{sample_folder}_summary_report.txt")

            # Check if the summary report file exists
            if os.path.isfile(report_file_path):
                with open(report_file_path, 'r') as file:
                    content = file.read().strip()

                    # Extract sample ID from the subfolder name
                    sample_id = sample_folder

                    # Determine the NIPAH detection result based on the content of the file
                    if "NO NIPAH DETECTED" in content:
                        detection_result = "negative"
                    else:
                        detection_result = "positive"

                    # Store the result in the dictionary
                    combined_data[sample_id] = detection_result

    # Write the combined data to the output HTML file
    with open(output_html, 'w') as html_output_file:
        html_output_file.write("<html>\n")
        html_output_file.write("<head>\n")
        html_output_file.write("<title>Combined Summary Report</title>\n")
        html_output_file.write('<style>\n')
        html_output_file.write('table {border-collapse: collapse; width: 100%;}\n')
        html_output_file.write('th, td {border: 1px solid #dddddd; text-align: left; padding: 8px;}\n')
        html_output_file.write('tr:nth-child(even) {background-color: #f2f2f2;}\n')  # Alternate row color
        html_output_file.write('tr.positive {background-color: red; color: white;}\n')  # Highlighted row color for positive results
        html_output_file.write('</style>\n')
        html_output_file.write("</head>\n")
        html_output_file.write("<body>\n")
        html_output_file.write("<h1>Combined Summary Report</h1>\n")
        html_output_file.write("<table>\n")
        html_output_file.write("<tr><th>Sample ID</th><th>NIPAH Detection</th></tr>\n")
        
        # Iterate through the combined data and write rows to the HTML file
        for sample_id, detection_result in combined_data.items():
            if detection_result == "positive":
                html_output_file.write(f"<tr class='positive'><td>{sample_id}</td><td>{detection_result}</td></tr>\n")
            else:
                html_output_file.write(f"<tr><td>{sample_id}</td><td>{detection_result}</td></tr>\n")

        html_output_file.write("</table>\n")
        html_output_file.write("</body>\n")
        html_output_file.write("</html>\n")

    # Write the combined data to the output TXT file
    with open(output_txt, 'w') as txt_output_file:
        txt_output_file.write("Sample ID\tNIPAH Detection\n")
        
        # Iterate through the combined data and write rows to the TXT file
        for sample_id, detection_result in combined_data.items():
            txt_output_file.write(f"{sample_id}\t{detection_result}\n")

if __name__ == "__main__":
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description='Combine summary reports into one.', allow_abbrev=False)
    parser.add_argument('--input_folder', help='Path to the folder containing sample subfolders', required=True)
    parser.add_argument('--output_html', default='combined_summary_report.html', help='Output combined HTML file')
    parser.add_argument('--output_txt', default='combined_summary_report.txt', help='Output combined TXT file')

    args = parser.parse_args()

    # Call the function to combine summary reports
    combine_summary_reports(args.input_folder, args.output_html, args.output_txt)
