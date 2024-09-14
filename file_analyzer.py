import os
import re  # regular expressions
from typing import List, Tuple
from nexa.gguf import NexaTextInference, NexaVLMInference

class FileAnalyzer:
    def __init__(self, nlp_model_path: str, vlm_model_path: str):
        self.classifications = [
            "research_papers",
            "financial_documents",
            "family_photos",
            "landscape_photos",
        ]

        try:
            self.nlp_inference = NexaTextInference(
                model_path=nlp_model_path,
                local_path=None,
                stop_words=[],
                temperature=0,
                max_new_tokens=512,
                top_k=3,
                top_p=0.3,
                profiling=False
            )

            self.vlm_inference = NexaVLMInference(
                model_path=vlm_model_path,
                local_path=None,
                stop_words=[],
                temperature=0.3,
                max_new_tokens=2048,
                top_k=3,
                top_p=0.2,
                profiling=False
            )

        except Exception as e:
            raise RuntimeError(f"💥 Failed to initialize inference models: {str(e)}")

    def analyze_file(self, file_path: str, content: str) -> Tuple[str, str, str]:
        # return (new_filename, classification, text_summary/image_description)
        _, ext = os.path.splitext(file_path)  # (root, ext) tuple
        file_extension = ext.lower()

        if file_extension in ['.pdf', '.txt']:
            new_filename, classification, summary = self._analyze_text(content)
        elif file_extension in ['.jpg', '.png']:
            new_filename, classification, description = self._analyze_image(file_path)
        else:
            raise ValueError(f"💥 Unsupported file type: {file_extension}")

        return new_filename, classification, summary if file_extension in ['.pdf', '.txt'] else description

    def _analyze_text(self, content: str) -> Tuple[str, str, str]:
        # return (new_filename, classification, text_summary)
        try:
            summary = self._recursive_summarize(content)
            classification = self._classify_text(summary)
            new_filename = self._generate_text_filename(summary)
            return new_filename, classification, summary
        except Exception as e:
            raise RuntimeError(f"💥 Error analyzing text: {str(e)}")

    def _analyze_image(self, file_path: str) -> Tuple[str, str, str]:
        # return (new_filename, classification, image_description)
        try:
            description = self._generate_image_description(file_path)
            classification = self._classify_image(description)
            new_filename = self._generate_image_filename(description)
            return new_filename, classification, description
        except Exception as e:
            raise RuntimeError(f"💥 Error analyzing image: {str(e)}")

    ######### process TEXTS:

    def _chunk_text_by_sentences(self, text: str, chunk_size: int = 2048) -> List[str]:
        sentences = re.split(r'(?<=[.!?])\s+', text)
        chunks = []
        current_chunk = ""

        # expand `current_chunk` up to `chunk_size` & append it to the `chunks` list:
        for sentence in sentences:
            if len(current_chunk) + len(sentence) <= chunk_size:
                current_chunk += sentence + " "
            else:
                chunks.append(current_chunk.strip())
                current_chunk = sentence + " "

        # ensure remaining text after the main loop is not lost:
        if current_chunk:
            chunks.append(current_chunk.strip())

        return chunks

    def _summarize_chunk(self, chunk: str, max_summary_length: int = 256) -> str:
        prompt = f"""Summarize the following text concisely and accurately, capturing main ideas and key details. Maintain original meaning and context. Aim for less than {max_summary_length} characters.
        Text to summarize: {chunk}
        Summary:"""

        response = self.nlp_inference.create_completion(prompt)
        # extract summary text from the response:
        summary = response['choices'][0]['text'].strip() if response and 'choices' in response else ''
        return summary

    def _recursive_summarize(self, text: str, max_length: int = 2048) -> str:
        if len(text) <= max_length:
            return text

        chunks = self._chunk_text_by_sentences(text)
        summaries = [self._summarize_chunk(chunk) for chunk in chunks]
        combined_summary = " ".join(summaries)

        return self._recursive_summarize(combined_summary, max_length)

    def _classify_text(self, summary: str, max_attempts: int = 3) -> str:
        prompt = f"""Based on the following summary, choose the single most appropriate category from the list below. The category should best reflect the document's main theme. Respond with one and only one chosen category, exactly as it appears in the list.
        Categories: {', '.join(self.classifications)}
        Summary: {summary}
        Category:"""

        response = self.nlp_inference.create_completion(prompt)
        classification = response['choices'][0]['text'].strip().lower()
        return classification if classification in self.classifications else 'miscellaneous'

    def _generate_text_filename(self, summary: str) -> str:
        prompt = f"""Generate a short (max 3 words), descriptive filename (without file extension) for a document with the following summary. Use only lowercase letters and collect words with underscores.
        Summary: {summary}
        Filename:"""
        response = self.nlp_inference.create_completion(prompt)
        filename = response['choices'][0]['text'].strip().lower() if response and 'choices' in response else 'unnamed_file'
        return filename.split()[0]

    ######### process IMAGES:

    def _generate_image_description(self, file_path: str) -> str:
        user_input = "Analyze this image and provide a concise description in 1 sentence. Focus on the main subject and key elements."
        description_generator = self.vlm_inference._chat(user_input=user_input, image_path=file_path)
        description = self._get_response_text_from_generator(description_generator)

        max_length = 200
        if len(description) <= max_length:
            return description

        # truncate the description if it's too long:
        # split the resulting string (up to the max_length) ONCE from the right side at the first period it encounters:
        return description[:max_length].rsplit('.', 1)[0] + '.'

    def _get_response_text_from_generator(self, generator):
        response_text = ""
        try:
            while True:
                response = next(generator)
                choices = response.get('choices', [])

                for choice in choices:
                    delta = choice.get('delta', {})
                    if 'content' in delta:
                        response_text += delta['content']
        except StopIteration:
            pass
        return response_text

    def _classify_image(self, description: str) -> str:
        prompt = f"""Based on the following image description, choose the single most appropriate category from the list below. The category should best reflect the image's main subject or theme. Respond with one and only one chosen category, exactly as it appears in the list.
        Categories: {', '.join(self.classifications)}
        Image description: {description}
        Category:"""

        response = self.nlp_inference.create_completion(prompt)
        classification = response['choices'][0]['text'].strip().lower()
        return classification if classification in self.classifications else 'miscellaneous'

    def _generate_image_filename(self, description: str) -> str:
        prompt = f"""Generate a short (max 3 words), descriptive filename (without file extension) for an image with the following description. Use only lowercase letters and collect words with underscores.
        Description: {description}
        Filename:"""
        response = self.nlp_inference.create_completion(prompt)
        filename = response['choices'][0]['text'].strip().lower() if response and 'choices' in response else 'unnamed_file'
        return filename.split()[0]
