import json
import os
from tkinter import filedialog

from striprtf.striprtf import rtf_to_text
import re
from tkinter import *


class DoneWindow(Toplevel):
    def __init__(self, master=None):
        super().__init__(master)
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
        with open("C:\\Users\\benhu\\PycharmProjects\\pythonProject\\Exam Taker\\formatter_opened_files.txt") as file1:
            opened_files = file1.readlines()
            print(opened_files)
        self.geometry("600x300")

        rightframe = Frame(self)
        rightframe.pack(side=RIGHT)
        self.Start_Button = (Button(rightframe, text='Start', command=self.open_app))
        self.Start_Button.pack(fill=X)
        self.Exit_Button = (Button(rightframe, text='Exit', command=self.destroy))
        self.Exit_Button.pack(fill=X)

        counter = 1
        self.file_select = Listbox(self)
        for i in opened_files:
            self.file_select.insert(counter, i)
            counter += 1
        self.file_select.pack(fill=BOTH, expand=True)

    def get_selected_item(self):
        selected_indices = self.file_select.curselection()
        if selected_indices:
            selected_index = selected_indices[0]
            selected_item = self.file_select.get(selected_index)
            return selected_item

    def window_popup(self):
        DoneWindow(self)

    def open_app(self):
        file_to_open = self.get_selected_item()
        file_to_open = file_to_open.strip()
        base_name = os.path.splitext(os.path.basename(file_to_open))[0]

        dst_file = select_dst_file(base_name)
        if dst_file:
            with open(file_to_open) as question_parser_input:
                question_parser(question_parser_input, dst_file, self)
        else:
            print("No destination file selected.")



def question_parser(question_parser_input, dst_file, self):
    question_database = {}
    line_count = 0
    line_count_2 = 0
    answer_count = 0
    current_question = ""
    image_count = 0
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
