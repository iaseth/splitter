
# splitter
`Splitter` is a python program that splits any grid-like image into separate files.
Consider the below image:

![Input Image](animated-female-faces.jpg)

You can use `splitter` to split this image into 9 separate files:
```
python3 splitter.py animated-female-faces.jpg rows=3 cols=3
```

This will produce the following output:
```
Row 1 of 3 rows:
	Column 1 of 3 columns:
		Saved: animated-female-faces_1_1.jpg [341x341]
	Column 2 of 3 columns:
		Saved: animated-female-faces_1_2.jpg [341x341]
	Column 3 of 3 columns:
		Saved: animated-female-faces_1_3.jpg [341x341]
Row 2 of 3 rows:
	Column 1 of 3 columns:
		Saved: animated-female-faces_2_1.jpg [341x341]
	Column 2 of 3 columns:
		Saved: animated-female-faces_2_2.jpg [341x341]
	Column 3 of 3 columns:
		Saved: animated-female-faces_2_3.jpg [341x341]
Row 3 of 3 rows:
	Column 1 of 3 columns:
		Saved: animated-female-faces_3_1.jpg [341x341]
	Column 2 of 3 columns:
		Saved: animated-female-faces_3_2.jpg [341x341]
	Column 3 of 3 columns:
		Saved: animated-female-faces_3_3.jpg [341x341]

```

The command generated the 9 images shown below:
![Output Image 1](output/animated-female-faces_1_1.jpg)
![Output Image 2](output/animated-female-faces_1_2.jpg)
![Output Image 3](output/animated-female-faces_1_3.jpg)
![Output Image 4](output/animated-female-faces_2_1.jpg)
![Output Image 5](output/animated-female-faces_2_2.jpg)
![Output Image 6](output/animated-female-faces_2_3.jpg)
![Output Image 7](output/animated-female-faces_3_1.jpg)
![Output Image 8](output/animated-female-faces_3_2.jpg)
![Output Image 9](output/animated-female-faces_3_3.jpg)


I am using [`readmix`](https://github.com/iaseth/readmix) for generating this README.
You can view the source file [here](https://github.com/iaseth/splitter/blob/master/README.md.rx).


## Args
In addition to the input file path, `splitter` accepts the following optional arguments:

| `Arg`    | `Shortcut` | `Description` |
| -------- | ---- | ------------------- |
| `rows`   | `r`  | Number of rows.                         |
| `cols`   | `c`  | Number of columns.                      |
| `output` | `o`  | Output directory path.                  |
| `prefix` | `p`  | Prefix to be added to each output file. |
| `format` | `f`  | Output format and file extension.       |


## Code
```py
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
				print(f"\t\tSaved: {output_filepath} [{cropped_img.size[0]}x{cropped_img.size[1]}]")
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

```


## License
MIT License

Copyright (c) Ankur Seth.

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.


## Credit

This file was generated using [`readmix`](https://github.com/iaseth/readmix).


