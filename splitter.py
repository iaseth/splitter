import os
import sys

from PIL import Image



def split_image_into_files(
	input_image_path, output_directory, prefix,
	rows=3, cols=3, output_format='jpg'
):
	"""
	Splits an image containing a nxn grid into n separate images.

	:param input_image_path: Path to the input image
	:param output_directory: Path to the folder where output images will be saved
	:param prefix: Prefix to be added to each output image filename
	:param rows: Number of rows
	:param cols: Number of columns
	:param output_format: Format and file extension of the output file
	"""
	try:
		# Open the input image
		img = Image.open(input_image_path)
		img_width, img_height = img.size
		
		# Calculate the size of each grid cell
		cell_width = img_width // cols
		cell_height = img_height // rows
		
		# Split the image into (rows * cols) separate images
		for row in range(rows):
			print(f"Row {row+1} of {rows} rows:")
			for col in range(cols):
				print(f"\tColumn {col+1} of {cols} columns:")
				# Define the bounding box for each grid cell
				left = col * cell_width
				upper = row * cell_height
				right = left + cell_width
				lower = upper + cell_height
				box = (left, upper, right, lower)
				
				# Crop the grid cell and save it
				cropped_img = img.crop(box)
				output_filename = f"{prefix}_{row+1}_{col+1}.{output_format}"
				output_filepath = os.path.join(output_directory, output_filename)
				cropped_img.save(output_filepath)
				print(f"\t\tSaved: {output_filepath}")
	except Exception as e:
		print(f"Error: {e}")


def main():
	args = sys.argv[1:]
	if len(args) == 0:
		print(f"Usage:\n\tpython image-splitter.py")
		return

	input_image_path = args[0]
	if not os.path.isfile(input_image_path):
		print(f"Not found: {input_image_path}")
		return

	input_image_dirpath = os.path.dirname(input_image_path)
	output_directory = input_image_dirpath

	input_image_filename = os.path.basename(input_image_path)
	prefix = os.path.splitext(input_image_filename)[0]
	output_format = os.path.splitext(input_image_filename)[1].strip('.')

	rows = 2
	cols = 2

	rest = args[1:]
	for arg in rest:
		parts = arg.split("=")
		if len(parts) == 2:
			key = parts[0].strip()
			value = parts[1].strip()
			match key:
				case 'rows' | 'r':
					rows = int(value)
				case 'cols' | 'c':
					cols = int(value)
				case 'output' | 'o':
					output_directory = value
				case 'prefix' | 'p':
					prefix = value
				case 'format' | 'f':
					output_format = value
				case _:
					print(f"Invalid arg: '{arg}'")
		else:
			print(f"Invalid arg: '{arg}'")
			return

	# output_directory = "images/output"
	split_image_into_files(input_image_path, output_directory, prefix=prefix, rows=rows, cols=cols, output_format=output_format)


if __name__ == '__main__':
	main()
