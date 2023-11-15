import os, csv, argparse, itertools

# command line arguments
parser = argparse.ArgumentParser()
parser.add_argument('-i', '--input-files', type=str, nargs='*', required=True, help="List of input CSV files.")
parser.add_argument('-e', '--input-encoding', type=str, default='utf-8-sig', help="Encoding of the input files (default: utf-8-sig).")
parser.add_argument('-d', '--input-delimiter', type=str, default=';', help="Delimiter of the input files (default: ';').")
parser.add_argument('-s', '--skip-lines', type=int, default=3, help="Number of lines to skip in input files (default: 3).")
parser.add_argument('-x', '--export-file', type=str, required=True, help="Export filename.")
# parser.add_argument('-E', '--export-encoding', type=str, default='utf-8', help="Encoding of the export files (default: utf-8).")
args = parser.parse_args()

# use command line arguments
src_files = args.input_files
src_encoding = args.input_encoding
dst_filename = args.export_file
csv_sep = args.input_delimiter
skip_lines = args.skip_lines

print(src_files)

# get headers from first file
with open(src_files[0], encoding=src_encoding) as src_csv:
	count = 0
	for row in src_csv.readlines():
		if count == skip_lines:
			csv_headers = row.replace(src_csv.newlines, '').split(csv_sep)
			csv_headers = [header.replace('"', '') for header in csv_headers]
		count += 1

# open destination csv
with open(os.path.join(src_dir, dst_filename), 'w', newline='') as dst_file:
	# create csv writer and write header
	csv_writer = csv.DictWriter(dst_file, fieldnames=csv_headers, dialect='excel')
	csv_writer.writeheader()

	# read csv data
	for src_file in src_files:
		with open(os.path.join(src_dir, src_file), encoding=src_encoding) as src_csv:
			# skip first lines of file
			src_csv = itertools.islice(src_csv, skip_lines, None)

			# copy to new file
			csv_reader = csv.DictReader(src_csv, delimiter=csv_sep)
			for row in csv_reader:
				csv_writer.writerow(row)

print("Script execution completed.")
