import os, csv, datetime, itertools

src_pattern = "TWINT_association"
src_dir = "P:\Documents\Assoc\PrendsMoiSec\Twint\decomptes"
src_encoding = 'utf-8-sig'
dst_filename = f"TWINT_{datetime.datetime.now().year}.csv"
csv_sep = ';'
skip_lines = 3

# read source files
src_files = []
for (dirpath, dirnames, filenames) in os.walk(src_dir):
	for filename in filenames:
		if filename.startswith(src_pattern) and filename.endswith('.csv'):
			src_files.append(filename)

# get headers from first file
with open(os.path.join(src_dir, src_files[0]), encoding=src_encoding) as src_csv:
	count = 0
	for row in src_csv.readlines():
		if count == skip_lines:
			csv_headers = row.replace(src_csv.newlines, '').split(csv_sep)
			csv_headers = [header.replace('"', '') for header in csv_headers]
		count += 1
print("CSV headers: " + str(csv_headers))

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
				print(row)
				csv_writer.writerow(row)

# write destination file
# csv_headers = csv_data[0].keys()
# 	csv_writer.fieldnames = csv_headers
# 	csv_writer.writeheader()
# 	csv_writer.writerows(csv_data)
