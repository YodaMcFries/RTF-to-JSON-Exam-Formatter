import base64
import re
import struct
from io import BytesIO
from tkinter import *
from tkinter.ttk import *
import json
from random import randrange
from tkinter import filedialog
import os  # For extracting the directory of the file
from PIL import Image, ImageTk

import RTF_to_JSON_Formatter

global json_data

installation_folder = "C:\\Users\\benhu\\PycharmProjects\\pythonProject\\Exam Taker\\"

import json
import base64
import struct
from PIL import Image, ImageTk
from io import BytesIO


def load_custom_file_format(input_file):
    global json_data
    try:
        with open(input_file, "rb") as f:
            json_size_data = f.read(4)
            if len(json_size_data) < 4:
                raise ValueError("Invalid file format: Missing JSON size header")

            json_size = struct.unpack("I", json_size_data)[0]

            # Read JSON data
            json_bytes = f.read(json_size)
            if len(json_bytes) < json_size:
                raise ValueError("Invalid file format: JSON data truncated")

            json_data = json.loads(json_bytes.decode('utf-8'))

    except Exception as e:
        print(f"Error loading file: {e}")


class OpeningMenu(Tk):
    def __init__(self):
        super().__init__()

        self.style = Style()
        self.style.theme_use("vista")

        self.title("BEN Player")
        self.iconbitmap(f"{installation_folder}ben_player.ico")

        with open(f"{installation_folder}opened_files.txt") as file1:
            opened_files = file1.readlines()
            print(opened_files)

        self.menu = Menu(self)
        self.config(menu=self.menu)

        rightframe = Frame(self)
        rightframe.pack(side=RIGHT)

        self.geometry('670x310')
        self.create_menu()

        self.Start_Button = Button(rightframe, text='Start', command=self.open_app)
        self.Start_Button.pack(fill=X)
        self.Add_Button = Button(rightframe, text='Add', command=self.open_file_dialog)
        self.Add_Button.pack(fill=X)
        self.Change_Button = Button(rightframe, text='Change', command=lambda: WIPwindow(self))
        self.Change_Button.pack(fill=X)
        self.Remove_Button = Button(rightframe, text='Remove', command=self.remove_file)
        self.Remove_Button.pack(fill=X)
        self.Properties_Button = Button(rightframe, text='Properties', command=lambda: WIPwindow(self))
        self.Properties_Button.pack(fill=X)
        self.History_Button = Button(rightframe, text='History', command=lambda: WIPwindow(self))
        self.History_Button.pack(fill=X)
        self.Convert_Button = Button(rightframe, text='Convert', command=lambda: RTF_to_JSON_Formatter.__main__())
        self.Convert_Button.pack(fill=X)
        self.Exit_Button = Button(rightframe, text='Exit', command=self.quit)
        self.Exit_Button.pack(fill=X)

        # Create Treeview widget
        self.treeview = Treeview(self, columns=("Title", "File Name"), show="headings")
        self.treeview.heading("Title", text="Title")
        self.treeview.heading("File Name", text="File Name")

        self.treeview.pack(fill=BOTH, expand=True)
        # Insert files into the Treeview
        for i in opened_files:
            file_path = i.strip()
            file_name = os.path.basename(file_path)
            directory = os.path.dirname(file_path)
            self.treeview.insert("", "end", values=(file_name, directory))

    import os

    def remove_file(self):
        selected_item = self.treeview.selection()
        if selected_item:
            # Get file name and directory from Treeview
            file_name, directory = self.treeview.item(selected_item, "values")
            file_path = os.path.join(directory, file_name)

            # Normalize file path to a consistent format (forward slashes)
            file_path = file_path.replace("\\", "/")  # Convert backslashes to forward slashes

            # Read the lines from the opened_files.txt file and strip any extra whitespace
            with open("opened_files.txt", "r") as infile:
                content = infile.readlines()

            # Normalize file paths in opened_files.txt to a consistent format
            content = [line.strip().replace("\\", "/") for line in content]

            # Check if the file_path is in the list of opened files
            if file_path in content:
                content.remove(file_path)  # Remove the matching file path

                # Write the updated content back to opened_files.txt
                with open("opened_files.txt", "w") as outfile:
                    for line in content:
                        outfile.write(f"{line}\n")

                # Also remove the file from the Treeview
                self.treeview.delete(selected_item)
            else:
                print(f"File path '{file_path}' not found in opened_files.txt.")

    def open_file_dialog(self):
        file_path = filedialog.askopenfilename(title="Select a File",
                                               filetypes=[("Text files", "*.json *.ben",), ("All files", "*.*")])

        if file_path:
            with open("opened_files.txt", "r") as infile:
                if file_path not in infile.read():
                    with open("opened_files.txt", "a") as outfile:
                        outfile.write(f"{file_path}\n")
                    file_name = os.path.basename(file_path)
                    directory = os.path.dirname(file_path)
                    self.treeview.insert("", "end", values=(file_name, directory))

    def create_menu(self):
        file_menu = Menu(self.menu)
        self.menu.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Add")
        file_menu.add_separator()
        file_menu.add_command(label="Change")
        file_menu.add_command(label="Remove")
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.quit)

        exam_menu = Menu(self.menu)
        self.menu.add_cascade(label="Exam", menu=exam_menu)
        exam_menu.add_command(label="Start")
        exam_menu.add_separator()
        exam_menu.add_command(label="Select All")
        exam_menu.add_separator()
        exam_menu.add_command(label="History")
        exam_menu.add_command(label="Options")

    def get_selected_item(self):
        selected_item = self.treeview.selection()
        if selected_item:
            file_name, directory = self.treeview.item(selected_item, "values")
            return os.path.join(directory, file_name)

    def open_app(self):
        file_to_open = self.get_selected_item()
        if file_to_open:
            load_custom_file_format(file_to_open)
            App()


class WIPwindow(Toplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.iconbitmap(f"{installation_folder}ben_player.ico")

        Label(self, text="WIP").pack()
        Button(self, text='Ok', command=self.destroy).pack(side=RIGHT, fill=BOTH, padx=5, pady=5)


class PopUpConfirmQuit(Toplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.iconbitmap(f"{installation_folder}ben_player.ico")

        Label(self, text="Are you sure you wish to end this exam?").pack()
        Button(self, text='No', command=self.destroy).pack(side=RIGHT, fill=BOTH, padx=5, pady=5)
        Button(self, text='Yes', command=master.destroy).pack(side=RIGHT, fill=BOTH, padx=5, pady=5)


def get_amount_of_points():
    counter = 0
    for i in json_data["questions"]:
        counter += json_data["questions"][i]["Num of Answers"]
    return counter


class App(Toplevel):
    def __init__(self):
        super().__init__()
        self.geometry('1030x635')
        self.state('zoomed')
        self.title("Exam")
        self.iconbitmap(f"{installation_folder}ben_player.ico")

        self.last_question = ""
        self.previous_question = ""
        self.correct_answer = []
        self.current_question = 0
        self.current_index = 0
        self.correct_counter = 0
        self.answer_viewed = False
        self.checkbuttons = []
        self.answered_questions = ["", "", "", ""]

        self.topframe = Frame(self)
        self.topframe.grid(row=0, column=0, sticky=W, pady=30)
        self.optionframe = Frame(self)
        self.optionframe.grid(row=1, column=0, columnspan=10, sticky=W)
        self.bottomframe = Frame(self)
        self.bottomframe.grid(row=2, column=0, sticky=W)
        # Label to show the current question number
        self.count_label = Label(self.topframe,
                                 text=f"Item {self.current_index} of {len(json_data['questions']) - 1}  Q{self.current_question}")
        self.count_label.grid(row=0, column=0, sticky=W)

        self.correct_counter_label = Label(self,
                                           text=f"Current Score: {self.correct_counter}/{get_amount_of_points()}")
        self.correct_counter_label.place(relx=1, y=20, anchor=E)
        # Display the question text from the JSON data for the current index
        self.Question = Message(self.topframe, text=json_data["questions"][f"Q{self.current_question}"]["Question"],
                                width=700)
        self.Question.grid(row=1, column=0, sticky=W)

        self.image_label = Label(self.topframe)  # Label to hold the image
        self.image_label.grid(row=2, column=0, sticky=W)  # Adjust placement as needed

        # Display a label asking the user to select the required number of answers
        amount_of_answers = json_data["questions"][f"Q{self.current_question}"]["Num of Answers"]
        self.answers = Label(self.optionframe, text=f"Please select only {amount_of_answers} answer/s.")
        self.answers.grid(row=0, column=0, sticky=W)

        # StringVar to hold the selected option for the question
        self.selected_option_radio = StringVar()
        self.selected_option_check = {}
        self.show_options(amount_of_answers)

        # Button to move to the previous question
        self.previous_button = Button(self, text="Previous", command=self.show_previous_question)
        self.previous_button.place(x=0, rely=1, anchor='sw', width=80)

        # Button to move to the next question
        self.next_button = Button(self, text="Next", command=self.show_next_question)
        self.next_button.place(x=80, rely=1, anchor='sw', width=80)

        # Button to end the exam
        self.end_exam_button = Button(self, text="End Exam", command=lambda: PopUpConfirmQuit(self))
        self.end_exam_button.place(relx=1, rely=1, anchor='se', width=80)

    def show_options(self, amount_of_answers, is_previous_question=False):
        if is_previous_question:
            self.current_question = self.previous_question
        """This method generates checkbuttons or radiobuttons based on the number of answers required."""
        for cb in self.checkbuttons:
            cb.destroy()

        row_counter = 1
        self.checkbuttons = []
        option_letter = json_data["questions"][f"Q{self.current_question}"]["Options"]
        self.selected_option_radio = StringVar()
        self.selected_option_check = {}
        # If there are more than 1 answer for a question then initialize the answers in a CheckButtons format
        # for multiple choice
        if amount_of_answers > 1:
            for letter in option_letter:
                option_question = json_data["questions"][f"Q{self.current_question}"]["Options"][letter]
                option_list = letter + " " + option_question
                self.selected_option_check[letter] = IntVar()
                cb = Checkbutton(self.optionframe, text=option_list, variable=self.selected_option_check[letter])
                cb.grid(row=row_counter, column=0, sticky=W)
                self.checkbuttons.append(cb)
                row_counter += 1
        # If there is only 1 answer for a question then initialize the answers in a RadioButtons Format
        else:
            for letter in option_letter:
                option_question = json_data["questions"][f"Q{self.current_question}"]["Options"][letter]
                option_list = letter + " " + option_question  # Display the option with its letter
                cb = Radiobutton(self.optionframe, text=option_list, variable=self.selected_option_radio, value=letter)
                cb.grid(row=row_counter, column=0, sticky=W)
                self.checkbuttons.append(cb)
                row_counter += 1

    def show_next_question(self):

        check_answer = self.check_answer()
        self.image_label.config(image=None)
        self.image_label.image = None  # Keep a reference to the image
        if self.answer_viewed:
            self.answer_viewed = False
            check_answer = True
            for answer in self.correct_answer:
                answer.destroy()
        """This method is triggered when the "Next" button is clicked to show the next question."""
        if check_answer:

            # Check if current question is within number of questions for the whole exam
            if self.current_index != len(json_data["questions"]) - 1:

                # If the currently displayed question is not the same as the last answered question
                # then the current question equals the next question in the list of answered questions
                # instead of randomising a number
                if self.current_index != len(self.answered_questions) - 4:
                    print(self.current_index, len(self.answered_questions) - 4)
                    print(self.current_question)
                    self.current_question = self.answered_questions[self.current_index + 4]
                    print(self.current_question)
                    self.last_question = self.current_question

                else:
                    # Generate a random number in the range of number of questions in the exam and assign
                    # it to the random_question Variable
                    random_question = randrange(1, len(json_data["questions"]))

                    # If the generate number has already been used in the exam then generate a new one
                    # until one is generated that has not been used before
                    while random_question in self.answered_questions:
                        random_question = randrange(1, len(json_data["questions"]))
                        print("randomise!")

                    """
                    if random_question in self.answered_questions:
                        random_question = randrange(1, len(json_data))
                        print(random_question)
                    """

                    # if the current question equals to the last question asked generate a new random question
                    # and take the current_index down by 1
                    if self.current_question == self.last_question:
                        print("previous")
                        print(self.answered_questions)
                        self.current_question = random_question
                        print(self.current_question)
                        self.current_index -= 1
                    # If this is a new question randomise the question and append the current question to the
                    # answered questions list
                    else:
                        self.last_question = self.current_question
                        self.answered_questions.append(self.current_question)
                        print(self.answered_questions)
                        self.current_question = random_question
                        print(self.current_question)

                self.current_index += 1
                self.find_images()

                if f"Q{self.current_index}" in json_data['questions']:

                    self.count_label.config(
                        text=f"Item {self.current_index} of {len(json_data['questions']) - 1}  Q{self.current_question}")
                    self.Question.config(text=json_data["questions"][f"Q{self.current_question}"]["Question"])
                    amount_of_answers = json_data["questions"][f"Q{self.current_question}"]["Num of Answers"]
                    self.answers.config(text=f"Please only select {amount_of_answers} answer.")
                    self.show_options(amount_of_answers)  # Show options for the next question
                    self.correct_counter_label.config(
                        text=f"Current Score: {self.correct_counter}/{get_amount_of_points()}")

            else:
                print("DONE")
                self.Question.config(text="No more questions.")
                self.answers.config(text="")
                self.current_question = 0
                for cb in self.checkbuttons:
                    cb.destroy()

        elif not self.answer_viewed:
            self.show_correct_answer()

    def show_previous_question(self):
        """This method is triggered when the "Next" button is clicked to show the next question."""
        # Remove window that shows the correct answer so that the previous question's answer does
        # not stay on the window when hitting back
        for answer in self.correct_answer:
            answer.destroy()

        # Check to make sure the current position is greater than 1, if so then decrement the current position by 1
        if self.current_index >= 2:
            self.current_index -= 1

        if f"Q{self.current_question}" in json_data and self.current_index > 0:
            self.previous_question = self.answered_questions[self.current_index + 4]
            self.count_label.config(
                text=f"Item {self.current_index} of {len(json_data['questions']) - 1}  Q{self.previous_question}")
            self.Question.config(text=json_data["questions"][f"Q{self.previous_question}"]["Question"])
            amount_of_answers = json_data["questions"][f"Q{self.previous_question}"]["Num of Answers"]
            self.answers.config(text=f"Please only select {amount_of_answers} answer.")
            self.show_options(amount_of_answers, True)

    def check_answer(self):
        if self.current_index == 0:
            return True
        else:

            current_answer = json_data["questions"][f"Q{self.current_question}"]["Answer"].split(",")
            current_answer_rejoined = ""
            current_option = self.selected_option_radio.get().strip(".")

            if len(current_answer) > 1:
                current_answer_joiner_counter = 0
                for _ in current_answer:
                    current_answer_rejoined += current_answer[current_answer_joiner_counter]
                    current_answer_joiner_counter += 1
                current_answer = current_answer_rejoined
            else:
                current_answer = current_answer[0]

            if current_option != "":
                current_option = self.selected_option_radio.get().strip(".")
            else:
                options = []
                options_string = ""
                count = 0
                for letter in self.selected_option_check:
                    if self.selected_option_check[letter].get() != 0:
                        options.append(letter.strip("."))
                for _ in options:
                    options_string += options[count]
                    count += 1
                current_option = options_string

            print(current_option)

            if current_option == current_answer and current_option != "":
                print("right", current_answer, current_option)
                self.correct_counter += 1
                return True
            else:
                print("wrong", current_answer, current_option)
                return False

    def show_correct_answer(self):
        if not self.check_answer():
            correct_answer = Message(self.bottomframe,
                                     text=f'Answer: {json_data["questions"][f"Q{self.current_question}"]["Answer"]}'
                                          f'\n\nExplanation:\n{json_data["questions"][f"Q{self.current_question}"]["Explanation"]}'
                                     , width=950, bg="yellow")
            correct_answer.grid(row=0, column=0, sticky=W, columnspan=3)
            self.correct_answer.append(correct_answer)
            self.answer_viewed = True

    def find_images(self):
        # Display the image if it exists
        for i in json_data["questions"][f"Q{self.current_question}"]:
            current_i = json_data["questions"][f"Q{self.current_question}"][i]
            if "image_" in str(current_i):
                found_image = re.search('image_\d+', str(current_i))
                if found_image:
                    image_key = found_image.group()  # This will return 'image_X'
                    print(image_key)
                    base64_string = json_data["images"].get(image_key, "")
                    if base64_string:
                        image = load_base64_image(base64_string)  # Adjust size if necessary
                        if image:
                            self.image_label.config(image=image)  # Update the label with the new image
                            self.image_label.image = image  # Keep a reference to the image


def load_base64_image(base64_string, width=None, height=None):
    try:
        # Decode the base64 string
        image_data = base64.b64decode(base64_string)
        image = Image.open(BytesIO(image_data))

        # Resize image if width/height is provided
        if width and height:
            image = image.resize((width, height))

        return ImageTk.PhotoImage(image)
    except Exception as e:
        print(f"Error loading image from base64: {e}")
        return None



if __name__ == '__main__':
    menu = OpeningMenu()
    menu.mainloop()
