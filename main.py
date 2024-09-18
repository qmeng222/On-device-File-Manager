import os
import shutil  # do high-level operations on a file (eg: moving)
import traceback  # print stack traces of Python programs
from multiprocessing import Pool, cpu_count
from functools import partial
from file_scanner import scan_directory
from file_processor import FileProcessor
from file_analyzer import FileAnalyzer


def process_file(file_path, output_directory, nlp_model_path, vlm_model_path):
   try:
       processor = FileProcessor()
       analyzer = FileAnalyzer(nlp_model_path, vlm_model_path)

       # step 2: determine file type & call the corresponding method
       content = processor.process_file(file_path)
       # print(f"Preview:\n{content[:300] + '...' if len(content) > 300 else content}")

       # step 3: File analyzer
       print(f"Processing: {file_path}")
       new_filename, classification, summary_or_description = analyzer.analyze_file(file_path, content)
       print(f"1️⃣ New filename: {new_filename}")
       print(f"2️⃣ Classification: {classification}")
       # print(f"3️⃣ Summary/Description: {summary_or_description[:100]}")

       # step 4: move the file from source to destination
       _, file_extension = os.path.splitext(file_path)
       new_file_path = os.path.join(output_directory, classification, new_filename)

       # create the category directory if it doesn't exist
       os.makedirs(os.path.dirname(new_file_path), exist_ok=True)

       shutil.move(file_path, new_file_path)
       print(f"✅ Moved file to {new_file_path}")
       print("------" * 6)
   except Exception as e:
       print(f"💥 Error processing {file_path}: {str(e)}")
       traceback.print_exc()
       print("⏭️ Continuing with next file...")
       print("------" * 6)

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

   if total_files == 0:
       print("💥 No files to process. Exiting.")
       return

   # determine the number of processes:
   num_processes = min(cpu_count(), total_files)
   # print(f"❓ Number of processes: {num_processes}")

   # a pool of worker processes:
   with Pool(processes=num_processes) as pool:
       results = pool.starmap(process_file, [(file_path, output_directory, nlp_model_path, vlm_model_path) for file_path in list_of_paths])
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
