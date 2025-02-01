from tkinter import *
import json
from random import randrange

with open("Question_DB.json") as file:
    json_data = json.load(file)


class PopUpConfirmQuit(Toplevel):


    def __init__(self, master=None):
        super().__init__(master)
        Label(self, text="Are you sure you wish to end this exam?").pack()
        Button(self, text='No', command=self.destroy).pack(side=RIGHT, fill=BOTH, padx=5, pady=5)
        Button(self, text='Yes', command=master.destroy).pack(side=RIGHT, fill=BOTH, padx=5, pady=5)


class App(Tk):
    def __init__(self):
        super().__init__()
        self.last_question = ""
        self.previous_question = ""
        self.correct_answer = []
        self.geometry('1030x635')
        self.state('zoomed')
        self.title("Exam")
        self.current_question = randrange(1, len(json_data))
        self.current_index = 1  
        self.answer_viewed = False
        self.checkbuttons = []  
        self.answered_questions = ["","","",""]

        # Label to show the current question number
        self.count_label = Label(self, text=f"Item {self.current_question} of {len(json_data)}  Q{self.current_index}")
        self.count_label.place(x=15, y=40)  

        # Display the question text from the JSON data for the current index
        self.Question = Message(self, text=json_data[f"Q{self.current_question}"]["Question"], width=700)
        self.Question.place(x=15, y=75)  

        # Display a label asking the user to select the required number of answers
        amount_of_answers = json_data[f"Q{self.current_question}"]["Num of Answers"]
        self.answers = Label(self, text=f"Please select only {amount_of_answers} answer/s.")
        self.answers.place(x=15, y=110)  

        # StringVar to hold the selected option for the question
        self.selected_option = StringVar()
        self.show_options(amount_of_answers)  

        # Button to move to the previous question
        self.previous_button = Button(self, text="Prevous", command=self.show_previous_question)
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

        row_counter = 0  
        self.checkbuttons = []  
        option_letter = json_data[f"Q{self.current_question}"]["Options"]  


        if amount_of_answers > 1:
            for letter in option_letter:
                option_question = json_data[f"Q{self.current_question}"]["Options"][letter]
                option_list = letter + " " + option_question  
                self.selected_option = StringVar()  
                cb = Checkbutton(self, text=option_list, variable=self.selected_option)  
                cb.place(x=15, y=130 + row_counter)  
                self.checkbuttons.append(cb)  
                row_counter += 25  
        else:
            for letter in option_letter:
                option_question = json_data[f"Q{self.current_question}"]["Options"][letter]
                option_list = letter + " " + option_question  # Display the option with its letter
                cb = Radiobutton(self, text=option_list, variable=self.selected_option,
                                 value=letter)  
                cb.place(x=15, y=130 + row_counter)  
                self.checkbuttons.append(cb)  
                row_counter += 25  

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
            self.current_index += 1  

            if f"Q{self.current_question}" in json_data:
                self.count_label.config(text=f"Item {self.current_question} of {len(json_data)}  Q{self.current_index}")
                self.Question.config(text=json_data[f"Q{self.current_question}"]["Question"])
                amount_of_answers = json_data[f"Q{self.current_question}"]["Num of Answers"]
                self.answers.config(text=f"Please only select {amount_of_answers} answer.")
                self.show_options(amount_of_answers)  # Show options for the next question
            else:
                
                self.Question.config(text="No more questions.")
                self.answers.config(text="")
                #self.next_button.config(state=DISABLED)  
        elif not self.answer_viewed:
            self.show_correct_answer()

    def show_previous_question(self):
        """This method is triggered when the "Next" button is clicked to show the next question."""
        if self.current_index >= 2:
            self.current_index -= 1  

        
        if f"Q{self.current_question}" in json_data and self.current_index > 0:
            self.previous_question = self.answered_questions[self.current_index+3]
            self.count_label.config(text=f"Item {self.previous_question} of {len(json_data)}  Q{self.current_index}")
            self.Question.config(text=json_data[f"Q{self.previous_question}"]["Question"])
            amount_of_answers = json_data[f"Q{self.previous_question}"]["Num of Answers"]
            self.answers.config(text=f"Please only select {amount_of_answers} answer.")
            self.show_options(amount_of_answers,True)  

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
            correct_answer.place(x=15, y=400)  
            self.correct_answer.append(correct_answer)
            self.answer_viewed = True



if __name__ == '__main__':
    app = App()  
    app.mainloop()  
