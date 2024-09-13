import os
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
    print(f"🎬 Found {total_files} files to process.")

    processor = FileProcessor()
    analyzer = FileAnalyzer(nlp_model_path, vlm_model_path)

    for index, file_path in enumerate(list_of_paths, start=1):
        try:
            # step 2: determine file type & call the corresponding method
            content = processor.process_file(file_path)

            # print progress and partial result for veri:
            print(f"Processing file {index}/{total_files}")  # Processing file 1/10
            print(f"Processed: {file_path}")
            # print(f"Preview:\n{content[:300] + '...' if len(content) > 300 else content}")

            # step 3: file analyzer
            new_filename, classification, summary_or_description = analyzer.analyze_file(file_path, content)
            print(f"👀 New filename: {new_filename}")
            print(f"👀 Classification: {classification}")
            # print(f"👀 Summary/Description: {summary_or_description[:100]}")
            print("------" * 6)

            # step 4: reorganize file

        except Exception as e:
            print(f"💥 Error processing {file_path}: {str(e)}")

    print(f"✅ Completed processing {total_files} files.")

if __name__ == "__main__":
    main()
