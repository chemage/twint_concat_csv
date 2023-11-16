import csv, argparse, itertools, glob

# expand filenames (necessary on Windows as wildcards are not interpreted)
def expand_filenames(files:[str]):
	matched_files = []
	for file in files:
		if glob.escape(file) != file:
			# -> There are glob pattern chars in the string
			matched_files.extend(glob.glob(file))
		else:
			matched_files.append(file)
	return matched_files

# command line arguments
parser = argparse.ArgumentParser()
parser.add_argument('-i', '--input-files', type=str, nargs='+', required=True, help="List of input CSV files.")
parser.add_argument('-e', '--input-encoding', type=str, default='utf-8-sig', help="Encoding of the input files (default: utf-8-sig).")
parser.add_argument('-d', '--input-delimiter', type=str, default=';', help="Delimiter of the input files (default: ';').")
parser.add_argument('-s', '--skip-lines', type=int, default=3, help="Number of lines to skip in input files (default: 3).")
parser.add_argument('-x', '--export-file', type=str, required=True, help="Export filename.")
parser.add_argument('-D', '--export-delimiter', type=str, default=';', help="Delimiter of the export file (default: ';').")
args = parser.parse_args()

# use command line arguments
src_files = expand_filenames(args.input_files)
src_encoding = args.input_encoding
dst_filename = args.export_file
csv_import_delim = args.input_delimiter
csv_export_delim = args.export_delimiter
skip_lines = args.skip_lines

# get headers from first file
try:
	with open(src_files[0], encoding=src_encoding) as src_csv:
		count = 0
		for row in src_csv.readlines():
			if count == skip_lines:
				csv_headers = row.replace(src_csv.newlines, '').split(csv_import_delim)
				csv_headers = [header.replace('"', '') for header in csv_headers]
			count += 1
except Exception as e:
	csv_headers = None
	print(f"Error: could not read CSV headers from file '{src_files[0]}'. {e}")

# open destination csv
if csv_headers is not None:
	try:
		with open(dst_filename, 'w', newline='') as dst_file:
			# create csv writer and write header
			csv_writer = csv.DictWriter(dst_file, fieldnames=csv_headers, dialect='excel', delimiter=csv_export_delim)
			csv_writer.writeheader()

			# read csv data
			for src_file in src_files:
				with open(src_file, encoding=src_encoding) as src_csv:
					# skip first lines of file
					src_csv = itertools.islice(src_csv, skip_lines, None)

					# copy to new file
					csv_reader = csv.DictReader(src_csv, delimiter=csv_import_delim)
					for row in csv_reader:
						csv_writer.writerow(row)
	except Exception as e:
		print(f"Error: could not concatenate CSV files to file '{dst_filename}'. {e}")

print("Script execution completed.")
