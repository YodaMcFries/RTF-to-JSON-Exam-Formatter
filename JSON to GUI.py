from tkinter import *
import json

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
        self.geometry('1030x635')
        self.state('zoomed')
        self.title("Exam")
        self.current_index = 1  # Start from the first question
        self.checkbuttons = []  # List to hold checkbutton instances

        # Label to show the current question number
        self.count_label = Label(self, text=f"Item {self.current_index} of {len(json_data)}")
        self.count_label.place(x=15, y=40)  # Position it at the top-left corner

        # Display the question text from the JSON data for the current index
        self.Question = Message(self, text=json_data[f"Q{self.current_index}"]["Question"], width=700)
        self.Question.place(x=15, y=75)  # Center the question on the window

        # Display a label asking the user to select the required number of answers
        amount_of_answers = json_data[f"Q{self.current_index}"]["Num of Answers"]
        self.answers = Label(self, text=f"Please select only {amount_of_answers} answer/s.")
        self.answers.place(x=15, y=110)  # Center this label below the question

        # StringVar to hold the selected option for the question
        self.selected_option = StringVar()
        self.show_options(amount_of_answers)  # Show options based on the number of answers

        # Button to move to the precious question
        self.previous_button = Button(self, text="Prevous", command=self.show_previous_question)
        self.previous_button.place(x=0, rely=1, anchor='sw',width=80)  # Keep button 1 at the bottom-left

        # Button to move to the next question
        self.next_button = Button(self, text="Next", command=self.show_next_question)
        self.next_button.place(x=80, rely=1, anchor='sw',width=80)  # Keep button 2 next to button 1

        self.end_exam_button = Button(self, text="End Exam", command=lambda: PopUpConfirmQuit(self))
        self.end_exam_button.place(relx=1, rely=1, anchor='se',width=80)  # Keep button 2 next to button 1


    def show_options(self, amount_of_answers):
        """This method generates checkbuttons or radiobuttons based on the number of answers required."""
        # Remove any existing checkbuttons/radiobuttons from previous questions
        for cb in self.checkbuttons:
            cb.destroy()

        row_counter = 0  # Counter for positioning the options vertically
        self.checkbuttons = []  # Reset the list of checkbuttons (or radiobuttons) for the new question
        option_letter = json_data[f"Q{self.current_index}"]["Options"]  # Options for the current question

        if amount_of_answers > 1:
            # If multiple answers are allowed, use Checkbuttons (for multiple selections)
            for letter in option_letter:
                option_question = json_data[f"Q{self.current_index}"]["Options"][letter]
                option_list = letter + " " + option_question  # Display the option with its letter
                var = StringVar()  # A new StringVar for this checkbutton
                cb = Checkbutton(self, text=option_list, variable=var)  # Create the checkbutton
                cb.place(x=15, y=130 + row_counter)  # Position the checkbutton in the window
                self.checkbuttons.append(cb)  # Add the checkbutton to the list
                row_counter += 25  # Adjust the row counter for the next option's vertical position
        else:
            # If only one answer is allowed, use Radiobuttons (for single selection)
            for letter in option_letter:
                option_question = json_data[f"Q{self.current_index}"]["Options"][letter]
                option_list = letter + " " + option_question  # Display the option with its letter
                cb = Radiobutton(self, text=option_list, variable=self.selected_option,
                                 value=letter)  # Create the radiobutton
                cb.place(x=15, y=130 + row_counter)  # Position the checkbutton in the window
                self.checkbuttons.append(cb)  # Add the radiobutton to the list
                row_counter += 25 # Adjust the row counter for the next option's vertical position

    def show_next_question(self):
        """This method is triggered when the "Next" button is clicked to show the next question."""
        self.current_index += 1  # Increment the question index

        # Check if there are more questions available
        if f"Q{self.current_index}" in json_data:
            # Update the UI with the new question and options
            self.count_label.config(text=f"Item {self.current_index} of {len(json_data)}")
            self.Question.config(text=json_data[f"Q{self.current_index}"]["Question"])
            amount_of_answers = json_data[f"Q{self.current_index}"]["Num of Answers"]
            self.answers.config(text=f"Please only select {amount_of_answers} answer.")
            self.show_options(amount_of_answers)  # Show options for the next question
        else:
            # If no more questions are available, update the UI to indicate this
            self.Question.config(text="No more questions.")
            self.answers.config(text="")
            self.next_button.config(state=DISABLED)  # Disable the "Next" button

    def show_previous_question(self):
        """This method is triggered when the "Next" button is clicked to show the next question."""
        if self.current_index >= 2:
            self.current_index -= 1  # Increment the question index

        # Check if there are more questions available
        if f"Q{self.current_index}" in json_data and self.current_index > 0:
            # Update the UI with the new question and options
            self.count_label.config(text=f"Item {self.current_index} of {len(json_data)}")
            self.Question.config(text=json_data[f"Q{self.current_index}"]["Question"])
            amount_of_answers = json_data[f"Q{self.current_index}"]["Num of Answers"]
            self.answers.config(text=f"Please only select {amount_of_answers} answer.")
            self.show_options(amount_of_answers)  # Show options for the next question


# Check if the script is being run directly, and then start the app
if __name__ == '__main__':
    app = App()  # Create an instance of the App class
    app.mainloop()  # Start the Tkinter event loop
