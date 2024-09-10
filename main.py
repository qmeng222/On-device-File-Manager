import os

from file_scanner import scan_directory
from file_processor import FileProcessor

def main():
    # step 1: file scanner
    input_directory = "./input_dir"
    list_of_paths = scan_directory(input_directory)
    total_files = len(list_of_paths)
    print(f"🎬 Found {total_files} files to process.")

    # step 2: file processor
    processor = FileProcessor()

    for index, file_path in enumerate(list_of_paths, start=1):
        try:
            # determine file type & call the corresponding method:
            content = processor.process_file(file_path)

            # print progress and partial result for veri:
            print(f"Processing file {index}/{total_files}")  # Processing file 1/100
            print(f"Processed: {file_path}")
            print(f"Preview:\n{content[:300] + '...' if len(content) > 300 else content}")
            print("------" * 6)

        except Exception as e:
            print(f"💥 Error processing {file_path}: {str(e)}")

    print(f"✅ Completed processing {total_files} files.")

if __name__ == "__main__":
    main()
