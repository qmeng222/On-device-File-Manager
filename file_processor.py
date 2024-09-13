import os
import pymupdf

class FileProcessor:
    def __init__(self):
        pass

    # case 1: for PDF file, extract text from each page:
    def process_pdf(self, file_path):
        with pymupdf.open(file_path) as doc:
            pages = []
            for page in doc:
                text = page.get_text()
                pages.append(text.strip())
        return "\n".join(pages)

    # case 2: for text file, read content directly:
    def process_text(self, file_path):
        with open(file_path, 'r', encoding='utf-8') as text_file:
            text_content = text_file.read().strip()
            return text_content

    # case 3: for image, return file path for later use:
    def process_image(self, file_path):
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
# list_of_paths = ['./input_dir/logo.png', './input_dir/paper_2cols.pdf', './input_dir/paper_1col.pdf', './input_dir/sub_dir2/BS.txt', './input_dir/sub_dir1/animal.jpg']

# for file_path in list_of_paths:
#     try:
#         content = processor.process_file(file_path)
#         print(f"👀 Processed {file_path}")
#         # chunk for summarization ...
#     except Exception as e:
#         print(f"💥 Error processing {file_path}: {str(e)}")
