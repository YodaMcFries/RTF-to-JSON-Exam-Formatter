from tkinter import *
from tkinter import filedialog
from tkinter.ttk import *
import json
import os
from striprtf.striprtf import rtf_to_text
import re


class DoneWindow(Toplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.iconbitmap("C:\\Users\\benhu\\PycharmProjects\\pythonProject\\Exam Taker\\ben_player.ico")

        Label(self, text="Formatting is Done!\nDo you want to close the app?").pack()
        Button(self, text='No', command=self.destroy).pack(side=RIGHT, fill=BOTH, padx=5, pady=5)
        Button(self, text='Yes', command=master.destroy).pack(side=RIGHT, fill=BOTH, padx=5, pady=5)


def select_dst_file(default_name):
    dst_file = filedialog.asksaveasfilename(
        defaultextension=".json",
        initialfile=default_name + ".json",  # Default name with .json extension
        filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
        title="Select Destination File"
    )
    return dst_file


class App(Tk):
    def __init__(self):
        super().__init__()

        self.style = Style()
        self.style.theme_use("vista")
        self.geometry("600x100")
        self.title("BEN Convertor")
        self.iconbitmap("C:\\Users\\benhu\\PycharmProjects\\pythonProject\\Exam Taker\\ben_player.ico")

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
            with open(file_to_open) as question_parser_input:
                question_parser(question_parser_input, dst_file, self)
        else:
            self.file_title.config(text=f"Cannot Start.\nNo file selected.")

    def open_file_dialog(self):
        self.file_path = filedialog.askopenfilename(title="Select a File",
                                                    filetypes=[("Text files", "*.rtf"), ("All files", "*.*")])
        self.file_title.config(text=f"{self.file_path} is selected")


def question_parser(question_parser_input, dst_file, self):
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

    with open(dst_file, "w") as test_output:
        App.window_popup(self)
        test_output.write(json.dumps(question_database, indent=4))


def __main__():
    app = App()
    app.mainloop()
    # test_data_to_test_output()
    # question_parser()


if __name__ == '__main__':
    __main__()
