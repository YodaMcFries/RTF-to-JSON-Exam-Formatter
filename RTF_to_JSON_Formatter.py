import base64
import struct
import time
import zipfile
from tkinter import *
from tkinter import filedialog
from tkinter.ttk import *
import json
import os

from docx2python import docx2python
from striprtf.striprtf import rtf_to_text
import re
from PIL import Image
from io import BytesIO
import win32com.client
import docx2txt

installation_folder = "C:\\Users\\benhu\\PycharmProjects\\pythonProject\\Exam Taker\\"

global absolute_docx_path


def convert_rtf_to_docx(rtf_file_path, docx_file_path):
    rtf_file_path = os.path.normpath(rtf_file_path)

    # Ensure docx_file_path is absolute
    if not os.path.isabs(docx_file_path):
        docx_file_path = os.path.join(os.path.dirname(rtf_file_path), docx_file_path)

    docx_file_path = os.path.normpath(docx_file_path)  # Normalize the path

    print(f"Opening file: {rtf_file_path}")  # Debugging line
    print(f"Saving as: {docx_file_path}")  # Debugging line

    if not os.path.exists(rtf_file_path):
        print(f"Error: The file {rtf_file_path} does not exist.")
        return

    word = win32com.client.Dispatch('Word.Application')
    doc = word.Documents.Open(rtf_file_path)
    doc.SaveAs(docx_file_path, FileFormat=16)
    doc.Close()
    word.Quit()

    # Check if the docx file is created and accessible
    if os.path.exists(docx_file_path):
        print(f"File saved successfully: {docx_file_path}")
    else:
        print(f"Error: File not found at {docx_file_path}.")
        return

    # Ensure the file is fully closed before processing
    # time.sleep(2)  # Adding more time to ensure the file is fully released by Word

    # Ensure the full absolute path is used for docx2txt
    global absolute_docx_path
    absolute_docx_path = os.path.abspath(docx_file_path)  # Get absolute path
    print(f"Absolute path for docx file: {absolute_docx_path}")  # Debugging line
    """
    try:
        # Debugging file access before processing
        if os.path.exists(absolute_docx_path):
            print("File is accessible and exists.")
        else:
            print("File is NOT accessible.")

        # Retry mechanism if file is temporarily locked
        try:
            extracted_text = docx2txt.process(absolute_docx_path)
            print("Text extracted successfully.")
            return extracted_text  # Return extracted text if successful
        except Exception as e:
            print(f"Error extracting text: {e}")
            time.sleep(1)  # Wait a bit before retrying
        print("Failed to extract text after multiple attempts.")
    except Exception as e:
        print(f"Error processing docx file: {e}")
    """


def select_dst_file(default_name):
    dst_file = filedialog.asksaveasfilename(
        defaultextension=".json",
        initialfile=default_name + ".ben",  # Default name with .json extension
        filetypes=[("JSON files", "*.ben"), ("All files", "*.*")],
        title="Select Destination File"
    )
    return dst_file


class DoneWindow(Toplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.iconbitmap(f"{installation_folder}ben_player.ico")

        Label(self, text="Formatting is Done!\nDo you want to close the app?").pack()
        Button(self, text='No', command=self.destroy).pack(side=RIGHT, fill=BOTH, padx=5, pady=5)
        Button(self, text='Yes', command=master.destroy).pack(side=RIGHT, fill=BOTH, padx=5, pady=5)


class App(Tk):
    def __init__(self):
        super().__init__()

        self.style = Style()
        self.style.theme_use("vista")
        self.geometry("600x100")
        self.title("BEN Convertor")
        self.iconbitmap(f"{installation_folder}ben_player.ico")

        self.file_path = ""
        windowframe = Frame(self)
        windowframe.pack(fill=BOTH)
        self.Start_Button = Button(windowframe, text='Start', command=self.open_app)
        self.Start_Button.pack(fill=X)
        self.Exit_Button = Button(windowframe, text='Exit', command=self.destroy)
        self.Exit_Button.pack(fill=X, side=BOTTOM)
        self.Add_Button = Button(windowframe, text='Select File', command=self.open_file_dialog)
        self.Add_Button.pack(fill=X)
        self.file_title = Message(windowframe, text="No file selected", width=550)
        self.file_title.pack(fill=BOTH)

    def window_popup(self):
        DoneWindow(self)

    def open_app(self):
        file_to_open = self.file_path
        file_to_open = file_to_open.strip()
        base_name = os.path.splitext(os.path.basename(file_to_open))[0]
        if file_to_open != "":
            dst_file = select_dst_file(base_name)

            # Convert RTF to DOCX first
            temp_docx_path = f"{base_name}.docx"
            convert_rtf_to_docx(file_to_open, temp_docx_path)

            # Use docx2txt to extract the content from DOCX
            extracted_text = extract_text_docx2python(absolute_docx_path)
            extracted_images = extract_images_docx2python(absolute_docx_path)  # Get images from the extracted content
            #os.remove(temp_docx_path)

            # Save the content to JSON file
            with open(file_to_open, "r") as question_parser_input:
                question_parser(question_parser_input, dst_file, self, extracted_text, extracted_images)
        else:
            self.file_title.config(text=f"Cannot Start.\nNo file selected.")

    def open_file_dialog(self):
        self.file_path = filedialog.askopenfilename(title="Select a File",
                                                    filetypes=[("RTF files", "*.rtf"), ("All files", "*.*")])
        self.file_title.config(text=f"{self.file_path} is selected")


def question_parser(question_parser_input, dst_file, self, extracted_text, images):
    question_database = {}
    line_count = 0
    line_count_2 = 0
    answer_count = 0
    current_question = ""
    image_count = 1
    init_counter = 0
    # Extract images before processing the extracted text (you can modify this part as needed)
    for line in extracted_text.splitlines():
        image = ""
        # if re.search('pichgoal\d{4,}', line):
        # image = f"image_{image_count}"
        # images[image] = extract_images(absolute_docx_path, image_count)
        # image_count += 1
        #line = rtf_to_text(line)
        # line = line.replace("\n", " ")
        #line = line.replace("\r", " ")
        # line = line.replace(" ", "", 1)
        base_line = line
        # print(line)
        #base_line = line.replace("\n", " ", 1)
        #base_line = base_line.replace(" ", "", 1)
        print(base_line)
        if init_counter == 0:
            current_question = "Q0"
            question_database[current_question] = {
                "Question": "Welcome to your Exam",
                "Options": {},
                "Answer": "",
                "Explanation": "",
                "Num of Answers": 0
            }
            init_counter += 1

        if re.search('^Q\d+', base_line):
            split_line = base_line.split(" ", 1)
            current_question = split_line[0]
            question_info = ""
            #if len(split_line) > 1:
            #    question_info = split_line[1]
            #else:
            #    question_info = "ERROR"
            explanation_info = ""
            question_database[current_question] = {
                "Question": "",
                "Options": {},
                "Answer": "",
                "Explanation": "",
                "Num of Answers": 0
            }
            line_count += 1
            line_count_2 = 0
            answer_count = 0
            print(current_question)

        elif line_count != 0 and not re.search('^Q\d+', base_line):

            if not re.search('^[A-Z][.]', base_line) and not re.search('^Answer:', base_line) and answer_count == 0:
                question_info += line + image
                debug = question_database[current_question]["Question"] = question_info.strip()

            elif re.search('^[A-Z][.]', base_line):
                line = line.replace("\n", " ", 1)
                #line = line.replace(" ", "", 1)
                split_line = line.split(" ", 1)
                if len(split_line) > 1:
                    question_database[current_question]["Options"][split_line[0]] = split_line[1].strip() + image
                else:
                    question_database[current_question]["Options"][split_line[0]] = "ERROR"

            elif re.search('^Answer:', base_line):
                line = line.replace("\n", " ", 1)
                #line = line.replace(" ", "", 1)
                split_line = line.split(" ", 1)
                question_database[current_question]["Num of Answers"] = len(split_line[1].strip())
                question_database[current_question]["Answer"] = split_line[1].strip() + image
                answer_count = 1

            elif line_count_2 == 0 and re.search('^Explanation:', base_line):
                line_count_2 += 1

            elif line_count_2 != 0:
                line = line.replace("\n", " ", 1)
                line = line.replace(" ", "", 1)
                explanation_info += line
                question_database[current_question]["Explanation"] = explanation_info + image

    with open(dst_file, "wb") as test_output:
        try:
            json_bytes = json.dumps({"questions": question_database, "images": images}).encode('utf-8')
            json_size = len(json_bytes)

            # Store JSON size (4-byte integer) + JSON data + Image data
            test_output.write(struct.pack("I", json_size))
            test_output.write(json_bytes)
            App.window_popup(self)
        except Exception as e:
            print(e)


def extract_text_docx2python(docx_file_path):
    output = docx2python(docx_file_path)
    text = output.text
    return text


def extract_images_docx2python(docx_file_path):
    output = docx2python(docx_file_path)
    images_dict = output.images  # This is the dictionary
    print(type(images_dict))
    images = {}

    for key, img_data in images_dict.items():  # Iterate over dictionary keys
        if isinstance(img_data, bytes):  # Check if the value is binary image data
            images[key] = base64.b64encode(img_data).decode('utf-8')  # Convert to Base64

    print("Images extracted.")
    return images


def extract_images(docx_file_path, image_count):
    """Extracts images from a DOCX file and returns them as base64 strings."""

    # Open the DOCX file as a ZIP archive
    with zipfile.ZipFile(docx_file_path, 'r') as docx_zip:
        # List all the files in the DOCX archive
        file_list = docx_zip.namelist()

        # Look for the media folder which contains the images
        media_folder = 'word/media/'
        image_files = [file for file in file_list if file.startswith(media_folder)]
        # Extract the image data
        image_data = docx_zip.read(f"word/media/image{image_count}.png")

        # Convert the image data to base64
        encoded_image = base64.b64encode(image_data).decode('utf-8')

        # Store the image with a unique ID

    return encoded_image


def __main__():
    app = App()
    app.mainloop()


if __name__ == '__main__':
    __main__()
