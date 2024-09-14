import os
import shutil  # do high-level operations on a file (eg: moving)
import traceback  # print stack traces of Python programs
from file_scanner import scan_directory
from file_processor import FileProcessor
from file_analyzer import FileAnalyzer

def main():
    # configuration:
    input_directory = "./input_dir"
    output_directory = "./output_organized_dir"
    nlp_model_path = "llama2"
    vlm_model_path = "nanollava"

    # step 1: file scanner
    list_of_paths = scan_directory(input_directory)
    total_files = len(list_of_paths)
    print(f"👀 Found {total_files} files to process.")

    try:
        processor = FileProcessor()
        analyzer = FileAnalyzer(nlp_model_path, vlm_model_path)
    except Exception as e:
        print(f"💥 Error initializing FileProcessor or FileAnalyzer: {str(e)}")
        traceback.print_exc()
        return

    for index, file_path in enumerate(list_of_paths, start=1):
        try:
            # step 2: determine file type & call the corresponding method
            content = processor.process_file(file_path)

            print(f"Processing file {index}/{total_files}")  # Processing file 1/10
            print(f"Processed: {file_path}")
            # print(f"Preview:\n{content[:300] + '...' if len(content) > 300 else content}")

            # step 3: file analyzer
            new_filename, classification, summary_or_description = analyzer.analyze_file(file_path, content)
            print(f"1️⃣ New filename: {new_filename}")
            print(f"2️⃣ Classification: {classification}")
            # print(f"3️⃣ Summary/Description: {summary_or_description[:100]}")

            # step 4: move the file from source (file_path) to destination (new_file_path)
            _, file_extension = os.path.splitext(file_path)
            new_file_path = os.path.join(output_directory, classification, new_filename)

            # create the category directory if it doesn't exist:
            os.makedirs(os.path.dirname(new_file_path), exist_ok=True)

            shutil.move(file_path, new_file_path)
            print(f"✅ Moved file to {new_file_path}")
            print("------" * 6)

        except Exception as e:
            print(f"💥 Error processing {file_path}: {str(e)}")
            traceback.print_exc()
            print("⏭️ Continuing with next file...")
            print("------" * 6)

    print(f"🎉 Completed processing {total_files} files.")

    # step 5: remove empty subdirectories in the input_directory
    try:
        for root, dirs, _ in os.walk(input_directory, topdown=False):
            for dir_name in dirs:
                os.rmdir(os.path.join(root, dir_name))
        print(f"👉 All subdirectories in '{input_directory}' have been removed.")
    except Exception as e:
        print(f"💥 Error removing subdirectories: {str(e)}")
        traceback.print_exc()

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"💥 Unhandled error in main: {str(e)}")
        traceback.print_exc()
