import os

def scan_directory(input_dir):
    allowed_extensions = ('.pdf', '.txt', '.jpg', '.png')  # add more
    file_paths = []

    for root, dirs, files in os.walk(input_dir):  # recursively traverse the input dir, topdown=True by default
        for file in files:
            if file.lower().endswith(allowed_extensions):
                file_paths.append(os.path.join(root, file))

    return file_paths

# test:
input_directory = "./input_dir"
files_to_process = scan_directory(input_directory)
# print(f"📚 A list of file paths: {files_to_process}")
# print(f"📚 Found {len(files_to_process)} files to process.")
