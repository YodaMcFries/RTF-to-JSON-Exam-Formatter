from tkinter import *
import json
from random import randrange

# Load JSON data from the file "Question_DB.json"
with open("Question_DB.json") as file:
    json_data = json.load(file)


class PopUpConfirmQuit(Toplevel):
    """A TopLevel popup that asks for confirmation that the user wants to quit.
                                                                              .
    Upon confirmation, the App is destroyed.
    If not, the popup closes and no further action is taken
    """

    def __init__(self, master=None):
        super().__init__(master)
        Label(self, text="Are you sure you wish to end this exam?").pack()
        Button(self, text='No', command=self.destroy).pack(side=RIGHT, fill=BOTH, padx=5, pady=5)
        Button(self, text='Yes', command=master.destroy).pack(side=RIGHT, fill=BOTH, padx=5, pady=5)


# Define the main app class that inherits from Tk (the tkinter root window)
class App(Tk):
    def __init__(self):
        # Initialize the Tk class and set the window size
        super().__init__()
        self.last_question = ""
        self.previous_question = ""
        self.correct_answer = []
        self.geometry('1030x635')
        self.state('zoomed')
        self.title("Exam")
        self.current_question = randrange(1, len(json_data))
        self.current_index = 1  # Start from the first question
        self.answer_viewed = False
        self.checkbuttons = []  # List to hold checkbutton instances
        self.answered_questions = ["","","",""]

        # Label to show the current question number
        self.count_label = Label(self, text=f"Item {self.current_question} of {len(json_data)}  Q{self.current_index}")
        self.count_label.place(x=15, y=40)  # Position it at the top-left corner

        # Display the question text from the JSON data for the current index
        self.Question = Message(self, text=json_data[f"Q{self.current_question}"]["Question"], width=700)
        self.Question.place(x=15, y=75)  # Center the question on the window

        # Display a label asking the user to select the required number of answers
        amount_of_answers = json_data[f"Q{self.current_question}"]["Num of Answers"]
        self.answers = Label(self, text=f"Please select only {amount_of_answers} answer/s.")
        self.answers.place(x=15, y=110)  # Center this label below the question

        # StringVar to hold the selected option for the question
        self.selected_option = StringVar()
        self.show_options(amount_of_answers)  # Show options based on the number of answers

        # Button to move to the precious question
        self.previous_button = Button(self, text="Prevous", command=self.show_previous_question)
        self.previous_button.place(x=0, rely=1, anchor='sw', width=80)  # Keep button 1 at the bottom-left

        # Button to move to the next question
        self.next_button = Button(self, text="Next", command=self.show_next_question)
        self.next_button.place(x=80, rely=1, anchor='sw', width=80)  # Keep button 2 next to button 1

        self.end_exam_button = Button(self, text="End Exam", command=lambda: PopUpConfirmQuit(self))
        self.end_exam_button.place(relx=1, rely=1, anchor='se', width=80)  # Keep button 2 next to button 1

    def show_options(self, amount_of_answers, is_previous_question=False):
        if is_previous_question:
            self.current_question = self.previous_question
        """This method generates checkbuttons or radiobuttons based on the number of answers required."""
        # Remove any existing checkbuttons/radiobuttons from previous questions
        for cb in self.checkbuttons:
            cb.destroy()

        row_counter = 0  # Counter for positioning the options vertically
        self.checkbuttons = []  # Reset the list of checkbuttons (or radiobuttons) for the new question
        option_letter = json_data[f"Q{self.current_question}"]["Options"]  # Options for the current question


        if amount_of_answers > 1:
            # If multiple answers are allowed, use Checkbuttons (for multiple selections)
            for letter in option_letter:
                option_question = json_data[f"Q{self.current_question}"]["Options"][letter]
                option_list = letter + " " + option_question  # Display the option with its letter
                self.selected_option = StringVar()  # A new StringVar for this checkbutton
                cb = Checkbutton(self, text=option_list, variable=self.selected_option)  # Create the checkbutton
                cb.place(x=15, y=130 + row_counter)  # Position the checkbutton in the window
                self.checkbuttons.append(cb)  # Add the checkbutton to the list
                row_counter += 25  # Adjust the row counter for the next option's vertical position
        else:
            # If only one answer is allowed, use Radiobuttons (for single selection)
            for letter in option_letter:
                option_question = json_data[f"Q{self.current_question}"]["Options"][letter]
                option_list = letter + " " + option_question  # Display the option with its letter
                cb = Radiobutton(self, text=option_list, variable=self.selected_option,
                                 value=letter)  # Create the radiobutton
                cb.place(x=15, y=130 + row_counter)  # Position the checkbutton in the window
                self.checkbuttons.append(cb)  # Add the radiobutton to the list
                row_counter += 25  # Adjust the row counter for the next option's vertical position

    def show_next_question(self):
        check_answer = self.check_answer()
        if self.answer_viewed:
            self.answer_viewed = False
            check_answer = True
            for answer in self.correct_answer:
                answer.destroy()
        """This method is triggered when the "Next" button is clicked to show the next question."""
        if check_answer:

            if self.current_index != len(self.answered_questions)-3:
                print(self.current_index, len(self.answered_questions))
                self.current_question = self.answered_questions[self.current_index+3]
                print(self.current_question)

            elif self.current_question == self.last_question:
                print(self.answered_questions)
                self.current_question = randrange(1, len(json_data))
                print(self.current_question)
                self.current_index -= 1
            else:
                self.last_question = self.current_question
                self.answered_questions.append(self.current_question)
                print(self.answered_questions)
                self.current_question = randrange(1, len(json_data))
                print(self.current_question)
            # Check if there are more questions available
            self.current_index += 1  # Increment the question index

            if f"Q{self.current_question}" in json_data:
                # Update the UI with the new question and options
                self.count_label.config(text=f"Item {self.current_question} of {len(json_data)}  Q{self.current_index}")
                self.Question.config(text=json_data[f"Q{self.current_question}"]["Question"])
                amount_of_answers = json_data[f"Q{self.current_question}"]["Num of Answers"]
                self.answers.config(text=f"Please only select {amount_of_answers} answer.")
                self.show_options(amount_of_answers)  # Show options for the next question
            else:
                # If no more questions are available, update the UI to indicate this
                self.Question.config(text="No more questions.")
                self.answers.config(text="")
                #self.next_button.config(state=DISABLED)  # Disable the "Next" button
        elif not self.answer_viewed:
            self.show_correct_answer()

    def show_previous_question(self):
        """This method is triggered when the "Next" button is clicked to show the next question."""
        if self.current_index >= 2:
            self.current_index -= 1  # Increment the question index

        # Check if there are more questions available
        if f"Q{self.current_question}" in json_data and self.current_index > 0:
            self.previous_question = self.answered_questions[self.current_index+3]
            # Update the UI with the new question and options
            self.count_label.config(text=f"Item {self.previous_question} of {len(json_data)}")
            self.Question.config(text=json_data[f"Q{self.previous_question}"]["Question"])
            amount_of_answers = json_data[f"Q{self.previous_question}"]["Num of Answers"]
            self.answers.config(text=f"Please only select {amount_of_answers} answer.")
            self.show_options(amount_of_answers,True)  # Show options for the next question

    def check_answer(self):
        current_answer = json_data[f"Q{self.current_index}"]["Answer"]
        current_option = self.selected_option.get().strip(".")
        if current_option == current_answer:
            return True
        else:
            return False

    def show_correct_answer(self):
        if not self.check_answer():
            correct_answer = Message(self,
                                     text=f'Answer: {json_data[f"Q{self.current_question}"]["Answer"]}'
                                          f'\n\nExplanation:\n{json_data[f"Q{self.current_question}"]["Explanation"]}'
                                     , width=700, bg="yellow")
            correct_answer.place(x=15, y=400)  # Center this label below the question
            self.correct_answer.append(correct_answer)
            self.answer_viewed = True


# Check if the script is being run directly, and then start the app
if __name__ == '__main__':
    app = App()  # Create an instance of the App class
    app.mainloop()  # Start the Tkinter event loop
