import struct
import time
from tkinter import *
from tkinter.ttk import *
import json
from tkinter import filedialog
import os
from striprtf.striprtf import rtf_to_text
import re

global questions


class App(Tk):
    def __init__(self):
        super().__init__()
        self.file_path = ""
        self.style = Style()
        self.style.theme_use("vista")

        self.geometry('1030x635')
        self.state('zoomed')
        self.title("BEN Designer")

        self.menu = Menu(self)
        self.config(menu=self.menu)

        self.create_menu()
        self.questions_treeview = Treeview(self)
        self.questions_treeview.pack(fill=BOTH, expand=True)


    def create_menu(self):
        file_menu = Menu(self.menu)
        self.menu.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Open", command=self.open_json_file)
        file_menu.add_command(label="Import", command=self.start_import_wizard)
        file_menu.add_separator()
        file_menu.add_command(label="Save", command=self.save_open_json)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.quit)

    def start_import_wizard(self):
        wizard = ImportWizard()
        self.wait_window(wizard)  # Wait for wizard to close
        self.populate_treeview()

    def open_json_file(self):
        global questions
        self.file_path = filedialog.askopenfilename(title="Select a File",
                                          filetypes=[("Text files", "*.ben"), ("All files", "*.*")])

        with open(self.file_path, "rb") as f:
            json_size_data = f.read(4)
            if len(json_size_data) < 4:
                raise ValueError("Invalid file format: Missing JSON size header")

            json_size = struct.unpack("I", json_size_data)[0]

            # Read JSON data
            json_bytes = f.read(json_size)
            if len(json_bytes) < json_size:
                raise ValueError("Invalid file format: JSON data truncated")

            questions = json.loads(json_bytes.decode('utf-8'))

            # Read remaining binary data as image
            #img_bytes = f.read()

            self.populate_treeview()

    def save_open_json(self):
        global questions
        self.file_path = self.file_path.strip()
        file_name = os.path.basename(self.file_path)
        dst_file = select_dst_file(file_name)
        if dst_file != "":
            with open(dst_file, "w") as f:
                f.write("[JSON]\n")
                print(questions)
                f.write(json.dumps(questions, indent=4))
                f.write("\n[IMAGE]\n")

    def populate_treeview(self):
        """Populate Treeview with questions from parsed JSON."""
        global questions
        if not questions:
            return  # No questions to load

        self.questions_treeview.delete(*self.questions_treeview.get_children())  # Clear treeview

        data = questions
        for qid, qdata in data.items():
            question_id = self.questions_treeview.insert("", "end", text=qid)
            self.questions_treeview.insert(question_id, "end", text=qdata["Question"])

            options_node = self.questions_treeview.insert(question_id, "end", text="Options")
            for opt_key, opt_text in qdata["Options"].items():
                self.questions_treeview.insert(options_node, "end", text=f"{opt_key}: {opt_text}")

            self.questions_treeview.insert(question_id, "end", text=f"Answer: {qdata['Answer']}")
            self.questions_treeview.insert(question_id, "end", text=f"Explanation: {qdata['Explanation']}")




class ImportWizard(Toplevel):
    def __init__(self):
        super().__init__()

        self.file_path = None
        self.questions = None
        self.parsingtext = None
        self.browse_button = None
        self.file_title = None
        self.centertext = None
        self.toptext = None
        self.pageheading = None
        self.page_counter = 1
        self.style = Style()
        self.style.theme_use("vista")
        self.attributes('-topmost', 'true')
        self.geometry('500x350')
        self.title(f"Import Wizard - {self.page_counter} of X")

        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.topframe = Frame(self)
        self.topframe.grid(row=0, column=0, sticky="w", padx=15, pady=10)
        self.centerframe = Frame(self)
        self.centerframe.grid(row=1, column=0, sticky="nw", padx=15, pady=10)
        self.bottomframe = Frame(self)
        self.bottomframe.grid(row=2, column=0, sticky=SE, columnspan=2, padx=15, pady=15)

        self.pageheading = Label(self.topframe, text="Overview")
        self.pageheading.grid(row=0, column=0, sticky=W)
        self.toptext = Label(self.topframe, text="Import Wizard allows you to import questions from text files")
        self.toptext.grid(row=1, column=0, sticky=W, padx=15)

        self.centertext = Label(self.centerframe, text="This Wizard will help you import questions from RTF Files.\n\n"
                                                       "Click Next to continue")
        self.centertext.grid(row=0, column=0, sticky="nw")

        self.BackButton = Button(self.bottomframe, text="< Back", command=self.page_counter_decrement)
        self.BackButton.grid(row=0, column=0, sticky="e")

        self.NextButton = Button(self.bottomframe, text="Next >", command=self.page_counter_increment)
        self.NextButton.grid(row=0, column=1, sticky="e", padx=10)
        self.CancelButton = Button(self.bottomframe, text="Cancel", command=lambda: self.destroy())
        self.CancelButton.grid(row=0, column=2, sticky="e")

    def page_counter_increment(self):
        self.page_counter += 1
        self.title(f"Import Wizard - {self.page_counter} of X")
        self.page_changer()

    def page_counter_decrement(self):
        if self.page_counter > 1:
            self.page_counter -= 1
            self.title(f"Import Wizard - {self.page_counter} of X")
            self.page_changer()

    def import_file_dialog(self):
        self.file_path = filedialog.askopenfilename(title="Select a File",
                                                    filetypes=[("Text files", "*.rtf"), ("All files", "*.*")])
        self.file_title.config(text=self.file_path)

    def page_changer(self):
        if self.page_counter == 1:
            self.file_title.destroy()
            self.browse_button.destroy()
            self.overview_page()
        elif self.page_counter == 2:
            self.select_source_file_page()
        elif self.page_counter == 3:
            self.file_title.destroy()
            self.browse_button.destroy()
            self.convert_file_page()

    def overview_page(self):
        self.pageheading.config(text="Overview")
        self.toptext.config(text="Import Wizard allows you to import questions from text files")
        self.centertext.config(text="This Wizard will help you import questions from RTF Files.\n\n"
                                    "Click Next to continue")
        self.NextButton.config(text="Next >", command=self.page_counter_increment)

    def select_source_file_page(self):
        self.pageheading.config(text="Select Source File")
        self.toptext.config(text="Select the source file for import")
        self.centertext.config(text="Click Browse and locate the file from which you want to import questions")
        self.file_title = Message(self.centerframe, text="No file selected", width=550)
        self.file_title.grid(row=1, column=0, sticky=W)
        self.browse_button = Button(self.centerframe, text="Browse...", command=self.import_file_dialog)
        self.browse_button.grid(row=1, column=1)
        self.NextButton.config(text="Next >", command=self.page_counter_increment)

    def convert_file_page(self):
        self.pageheading.config(text="File Import")
        self.toptext.config(text="The wizard is preparing to import the file")
        self.centertext.config(text="Please click import to start, the screen may freeze")
        self.NextButton.config(text="Import", command=lambda: self.run_parser())
        if self.file_path == "":
            self.page_counter_decrement()

    def run_parser(self):
        file_to_open = self.file_path
        file_to_open = file_to_open.strip()
        base_name = os.path.splitext(os.path.basename(file_to_open))[0]
        if file_to_open != "":
            with open(file_to_open) as question_parser_input:
                self.question_parser(question_parser_input)

    def finished_page(self):
        self.pageheading.config(text="Ready to Import")
        self.toptext.config(text="Wizard is ready to import")
        self.centertext.config(text="The Import Wizard has enough information to start import questions\n\n"
                                    "To begin importing questions click import")
        self.NextButton.config(text="Done", command=self.destroy)

    def question_parser(self, question_parser_input):
        question_database = {}
        line_count = 0
        line_count_2 = 0
        answer_count = 0
        current_question = ""
        image_count = 0
        init_counter = 0
        for line in question_parser_input:
            image = ""
            if re.search('.{500,}', line):
                image = f" image_{image_count} "
                image_count += 1
            line = rtf_to_text(line)
            # line = line.replace("\n", " ")
            line = line.replace("\r", " ")
            # line = line.replace(" ", "", 1)
            line = line
            # print(line)
            base_line = line.replace("\n", " ", 1)
            base_line = base_line.replace(" ", "", 1)

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
                if len(split_line) > 1:
                    question_info = split_line[1]
                else:
                    question_info = "ERROR"
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
                    question_info += line
                    question_database[current_question]["Question"] = question_info.strip() + image

                if re.search('^[A-Z][.]', base_line):
                    line = line.replace("\n", " ", 1)
                    line = line.replace(" ", "", 1)
                    split_line = line.split(" ", 1)
                    if len(split_line) > 1:
                        question_database[current_question]["Options"][split_line[0]] = split_line[1].strip() + image
                    else:
                        question_database[current_question]["Options"][split_line[0]] = "ERROR"

                elif re.search('^Answer:', base_line):
                    line = line.replace("\n", " ", 1)
                    line = line.replace(" ", "", 1)
                    split_line = line.split(" ", 1)
                    question_database[current_question]["Num of Answers"] = len(split_line[1].strip())
                    question_database[current_question]["Answer"] = split_line[1].strip()
                    answer_count = 1

                elif line_count_2 == 0 and re.search('^Explanation:', base_line):
                    line_count_2 += 1

                elif line_count_2 != 0:
                    line = line.replace("\n", " ", 1)
                    line = line.replace(" ", "", 1)
                    explanation_info += line
                    question_database[current_question]["Explanation"] = explanation_info + image

        global questions
        questions = json.dumps(question_database, indent=4)
        self.page_counter_increment()
        self.finished_page()
        # with open(dst_file, "w") as test_output:
        #    self.finished_page()
        #    test_output.write(json.dumps(question_database, indent=4))


def select_dst_file(default_name):
    dst_file = filedialog.asksaveasfilename(
        defaultextension=".ben",
        initialfile=default_name,  # Default name with .json extension
        filetypes=[("JSON files", "*.ben"), ("All files", "*.*")],
        title="Select Destination File"
    )
    return dst_file


def __main__():
    app = App()
    app.mainloop()


if __name__ == '__main__':
    __main__()
