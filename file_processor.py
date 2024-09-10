import os
import pdfplumber
from PIL import Image

class FileProcessor:
    def __init__(self):
        pass

    # case 1: for PDF file, extract text from each page:
    def process_pdf(self, file_path):
        with pdfplumber.open(file_path) as pdf:
            pages = [(page.extract_text() or "").strip() for page in pdf.pages]  # memory-efficient for large docs
            # print(f"💂‍♀️ PDF first page, first 100 chars:\n{pages[0][:100]}")
            # print(f"🥼 PDF third page, first 100 chars:\n{pages[2][:100]}")
            # print(f"👢 PDF last page, last 100 chars:\n{pages[-1][-100:]}")
        return "\n".join(pages)

    # case 2: for text file, read content directly:
    def process_text(self, file_path):
        with open(file_path, 'r', encoding='utf-8') as text_file:
            text_content = text_file.read().strip()
            # print(f"📝 Text file content:\n{text_content}")
            return text_content

    # case 3: for image, return file path for later use:
    def process_image(self, file_path):
        # print(f"🌠 Image file path: {file_path}")
        return file_path

    # determine file type & call the corresponding method:
    def process_file(self, file_path):
        # path = '/home/User/Desktop/file.txt' -> ('/home/User/Desktop/file', '.txt') pair
        file_extension = os.path.splitext(file_path)[1].lower()

        if file_extension == '.pdf':
            return self.process_pdf(file_path)
        elif file_extension == '.txt':
            return self.process_text(file_path)
        elif file_extension in ['.jpg', '.png']:
            return self.process_image(file_path)
        else:
            raise ValueError(f"💥 Unsupported file type: {file_extension}")

# # test:
# processor = FileProcessor()
# list_of_paths = ['./input_dir/paper.pdf', './input_dir/logo.png', './input_dir/sub_dir2/BS.txt', './input_dir/sub_dir1/animal.jpg']

# for file_path in list_of_paths:
#     try:
#         content = processor.process_file(file_path)
#         # print(f"👀 Processed {file_path}")
#         # chunk for summarization ...
#     except Exception as e:
#         print(f"💥 Error processing {file_path}: {str(e)}")
