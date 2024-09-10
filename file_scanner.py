import os

def scan_directory(input_dir):
    allowed_extensions = ('.pdf', '.txt', '.jpg', '.png')  # add more
    file_paths = []

    for root, dirs, files in os.walk(input_dir):  # recursively traverse the input dir, topdown=True by default
        for file in files:
            if file.lower().endswith(allowed_extensions):
                file_paths.append(os.path.join(root, file))

    return file_paths

# # test:
# input_directory = "./input_dir"
# list_of_paths = scan_directory(input_directory)
# print(f"📚 A list of file paths: {list_of_paths}")
# # ['./input_dir/logo.png', './input_dir/paper_2cols.pdf', './input_dir/paper_1col.pdf', './input_dir/sub_dir2/BS.txt', './input_dir/sub_dir1/animal.jpg']
# print(f"📚 Found {len(list_of_paths)} files to process.")
