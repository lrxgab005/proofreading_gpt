import openai
import glob
import os

# Initialize the OpenAI API with your key
openai.api_key = "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"
model="gpt-4"
# model="gpt-3.5-turbo"

class TextCorrector:
    def __init__(self):
        known_words = ["Kim", "Gabriel", "Martina", "Cordula", "Lea", "Annegret", "Deubner", "Rula"]
        self.system_msg = ("You are a text correcting assistant. A book written by typewriter has been converted "
                           "into plain text using OCR. It will have many errors. I will read it to you page by page. "
                           "Only respond with the corrected version. Nothing else. The text is in German "
                           "and will contain names of German places. Names you must recognize are: ")

        self.system_msg += ", ".join(known_words)
        self.msgs = [
            {"role": "system", "content": self.system_msg},
        ]
        self.corrected_paragraphs = []
        self.current_paragraph = ""

    def parse_line(self, line):
        line = line.strip()
        if len(line) < 4:
            if len(self.current_paragraph) > 5:
                self.correct_text_with_chatgpt(self.current_paragraph)
                # self.corrected_paragraphs.append(self.current_paragraph)
                self.current_paragraph = ""
        else:
            self.current_paragraph += line

    def correct_text_with_chatgpt(self, text):
        try:
            # print("Input:", text)
            self.msgs.append({"role": "user", "content": text})
            response = openai.ChatCompletion.create(
                model=model,
                messages=self.msgs,
                max_tokens=5000,
                temperature=0.5
            )
            corrected_text = response.choices[0].message['content']
            self.corrected_paragraphs.append(corrected_text)
            # print("Corrected:", corrected_text)
        except Exception as e:
            print(f"Error correcting line: {text}. Error: {e}")

def correct_file(input_path, output_path):
    print(f"Reading {input_path}")
    with open(input_path, 'r') as f:
        lines = f.readlines()

    tc = TextCorrector()
    print(f"Processing {len(lines)} lines")
    tc.correct_text_with_chatgpt(" ".join(lines))

    print(f"Writing {output_path}")
    with open(output_path, 'w') as f:
        f.writelines(tc.corrected_paragraphs)

def concatenate_files(input_dir, output_path):
    print(f"Reading {input_dir}")

    half_pages = []
    for path in glob.glob(input_dir + '/*.txt'):
        with open(path, 'r') as f:
            lines = f.readlines()
            half_len = len(lines) / 2
            half_pages.append(" ".join(lines[:half_len]))
            half_pages.append(" ".join(lines[half_len:]))
    
    new_pages = half_pages[0]
    new_pages += [half_pages[page_idx] for page_idx in range(1, len(half_pages) - 1)]

    for page_idx in range(1, len(half_pages)):
        tc = TextCorrector()
        print(f"Processing {len(lines)} lines")
        tc.correct_text_with_chatgpt(" ".join(lines))

def page_analysis(input_dir):
    print(f"Analysing {input_dir}")
    for path in glob.glob(input_dir + '/*.txt'):
        with open(path, 'r') as f:
            lines = f.readlines()
            print(os.path.basename(path), len(lines), [len(l.split(" ")) for l in lines])


# Open the text file and read lines
# input_dir = '/Users/groux/Documents/opa_book/text_conversion/images_0/test'
# output_dir = '/Users/groux/Documents/opa_book/text_conversion/images_0/corrected'
# for path in glob.glob(input_dir + '/*.txt'):
#     correct_file(path, os.path.join(output_dir, os.path.basename(path)))

input_dir = "data/opa_corrected_chapters/*"
for d in sorted(glob.glob(input_dir)):
    page_analysis(d)