'''
Tasks: 

1. When the program starts - you should be able to choose 
between the following mode: 

 - Adding questions.
 - Statistics viewing.
 - Disable/enable questions.
 - Practice mode.
 - Test mode.

2. Adding questions:
2.1 Can't access -Practice or -Test mode. until atleast 5
    questions are inputed.

2.2 Choose type of question to add (quizz or free_form). 
    questions should be saved in to .csv file.
    
    #User add question to .csv file and answers. (every question needs to have a number and A.B. answers to choose.)
         
            quizz - input (Nr.)(question)
                    input (A)answer1 
                    input (B)answer2
                    input (Correect answer if A input A if B input B)
                    Save quizz question to .csv quizz qurstion.csv
                    Ask to quite or add another quesiton or quite

            free-form - Input (Question)
                        Input (answer)
                        save to free_form.csv
                        ask to add another qustion or quite.

3. Statistics viewing mode:

    Print out questions from .csv files quizz and free-form
    Question should have: | unicue ID number | Acvtive or Not | question | how many times was print out in Practice or test mode | % how many times was answered correctly |  
    Print {
        ID | Active | question | In use: f"{times}" | 25% | 
    }
4. Disable/Enable questions:

    Input ID 
    Print (question) 
    Print (answers)
    Print (correct answer: )
        Ask to confirm (active or disable)
        save in .csv file. 
        If active - question will show in practise or test mode
        if disable - question will not gonna show in practise or test mode.
        store this information in .csv file. (Choose to save in the same .csv file or different one)

5. Practice mode: 
    Choose  quizz or free_form
    Input ("Choose quizz or free_form: ")
    If quizz 
        run questions for quizz.csv 
    if free_form 
        run questions from free_form
    else:
        print("wrong choise. You can choose "quizz" ir "free_form": )

    loop 
        while True:
            Show question randomly 
            if answer was correct - less show this question in practice mode.
            if answer wrong - show more times in practice mode           # weighted random choices !!!!
        if Error
            break(print: score) and reccored to .csv file

        
6. Test mode:

    Print(Input: Choose quizz ir free_form)


    test_mode = Input("How many quesions you would like to get?: ")
    if test_mode < (number of inputed questions) == run test_mode.
    if test_mode > (questions inputed) == print number should be lower ask for input again.
    show question random but only one time. 
    if all questions answered - print (score: Nr. of correct answers.)
    save to results.txt (score, date, time)
'''
import random
import csv
import sys
import uuid

class Question:
    def __init__(self, uuid, enabled, text, correct_answer, options=None):
        self.id = uuid
        self.enabled = enabled
        self.text = text
        self.correct_answer = correct_answer 
        self.options = options
        self.attempts = 0
        self.correct_attempts = 0

    def is_single_answer(self):
        return self.options is not None

    def is_enabled(self):
        return bool(int(self.enabled)) 

    def enable(self, enable):
        self.enabled = enable
    
    def get_attempts(self):
        return self.attempts
    
    def get_correct_attempts(self):
        return self.correct_attempts

    # Get percentage of correctly answered questions
    def get_percentage_of_answers(self):
        if self.attempts == 0:
            return "0%"
        else: 
            percentage_of_answers = round((self.correct_attempts / self.attempts) * 100)
            return str(percentage_of_answers) + "%"

    def get_uuid(self):
        return self.id

    def display(self):
        print(self.text)
        if self.options:
            for i, option in enumerate(self.options, 1):
                print(f"{i}. {option}")

    def check_answer(self, user_answer):
        self.attempts += 1
        try:
            if self.is_single_answer():
                is_correct = user_answer.lower() == self.correct_answer.lower()
            else:
                user_answer = int(user_answer) - 1
                is_correct = int(user_answer) == int(self.correct_answer)
            if is_correct:
                self.correct_attempts += 1
        except ValueError:
            print("Invalid input. Use numbers, not letters")
            return False
        
        return is_correct

    def get_correct_answer(self):
        if self.is_single_answer():
            answer = self.correct_answer
        else:
            answer_index = int(self.correct_answer)
            answer = self.options[answer_index]
        return answer


    def to_csv(self):
        if self.is_single_answer():
            return [self.id, self.enabled, self.text, "SingleStringAnswer", self.correct_answer, self.attempts, self.correct_attempts]
        else:
            return [self.id, self.enabled, self.text, "MultipleChoice", *self.options, str(self.correct_answer), self.attempts, self.correct_attempts]

    @classmethod
    def from_csv(cls, row):
        question_type = row[3]
        if question_type == "SingleStringAnswer":
            options = None  # SingleStringAnswer question does not have options
            correct_answer = row[4]
            question = SingleStringAnswerQuestion(row[0], row[1], row[2], correct_answer)
        elif question_type == "MultipleChoice":
            options = row[4:-3] 
            correct_answer = row[-3]
            answer_index = row.index(correct_answer)
            question = MultipleChoiceQuestion(row[0], row[1], row[2], correct_answer, options)
        else:
            raise ValueError(f"Unknown question type: {question_type}")

        question.attempts, question.correct_attempts = int(row[-2]), int(row[-1])
        return question

class SingleStringAnswerQuestion(Question):
    def __init__(self, uuid, enabled, text, correct_answer):
        super().__init__(uuid, enabled, text, correct_answer, options=None)

    def is_single_answer(self):
        return True


class MultipleChoiceQuestion(Question):
    def __init__(self, uuid, enabled, text, correct_answer, options):
        super().__init__(uuid, enabled, text, correct_answer, options)

    def is_single_answer(self):
        return False



def save_questions(questions, filename):
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        for question in questions:
            writer.writerow(question.to_csv())

def load_questions(filename):
    questions = []
    with open(filename, mode='r', encoding='utf-8') as file:
        reader = csv.reader(file)
        for row in reader:
            questions.append(Question.from_csv(row))
    random.shuffle(questions)
    return questions

def main():
        questions = load_questions("questions.csv")

        while True:
            print("\nChoose a mode")
            print("1. Adding questions")
            print("2. Statistic viewing")
            print("3. Disable/Enable questions")
            print("4. Practice mode")
            print("5. Test mode")

            choice = int(input("Enter your choice: "))

            if choice == 1:
                question_type = int(input("Enter 1 for quizz or 2 for free_form "))
                if question_type == 1:
                    answers = []
                    question_text = str(input("Enter your question: "))
                    question_answer = str(input("Enter answer or . to end"))
            
                    while question_answer != ".":
                        answers.append(question_answer)
                        question_answer = str(input("Enter answer or . to end: "))

                    print(answers)

                    correct_answer = int(input("Which answer is correct? Enter number:"))
                    correct_answer = correct_answer - 1
                    unique_id = uuid.uuid4()

                    questions.append(MultipleChoiceQuestion(unique_id, 1, question_text, correct_answer, answers))
                    save_questions(questions, "questions.csv")

                elif question_type == 2:
                    question_text = str(input("Enter your question: "))
                    question_answer = str(input("Enter answer: "))
                    unique_id = uuid.uuid4()

                    questions.append(SingleStringAnswerQuestion(unique_id, 1, question_text, question_answer))
                    save_questions(questions, "questions.csv")

                else:
                    print("wrong choice ")


            elif choice == 2:
                print ("\n------------- STATISTICS -------------")
                for question in questions:
                    print("\r")
                    
                    unique_id = str(question.get_uuid())
                    print("ID:" + unique_id + " Enabled: " + str(question.is_enabled()))
                    
                    question.display()
                    attempts = str(question.get_attempts())
                    correct = str(question.get_correct_attempts())
                    percentage = str(question.get_percentage_of_answers())  
                    

                    print("Correctly answered/attempts: " + correct + " / " + attempts + " Percent: " + percentage + "\n")

            elif choice == 3:
                question_id = str(input("Enter question UUID: "))
                for question in questions:
                    if question.get_uuid() == question_id:
                        unique_id = str(question.get_uuid())
                        print("ID:" + unique_id + " Enabled: " + str(question.is_enabled()))
                        question.display()
                        print("Answer: " + question.get_correct_answer())
                        question_enable = str(input("Enter, enable or disable: "))
                        if question_enable == "enable":
                            question.enable(1)
                        elif question_enable == "disable":
                            question.enable(0)
                        else:
                            print("wrong input, try again: ")

                        save_questions(questions, "questions.csv")

            #Practice mode:
            elif choice == 4: 
                      
                while True: 
                    
                    for question in questions:
                
                        if question.is_enabled() == False: 
                            continue
                        question.display()
                        user_answer = input("Your answer: ")
                        if user_answer == ".":
                            break

                        is_correct = question.check_answer(user_answer)
                        print("Correct!\n" if is_correct else "Incorrect!\n")

                    if user_answer == ".":
                        break
                
                save_questions(questions, "questions.csv") 
                        

            elif choice == 5:
                if len(questions) < 5:
                    print("You need to add more questions")
                    continue

                for question in questions:
                
                    if question.is_enabled() == False: 
                        continue

                    question.display()
                    user_answer = input("Your answer: ")
                    is_correct = question.check_answer(user_answer)
                    print("Correct!\n" if is_correct else "Incorrect!\n")
                
                save_questions(questions, "questions.csv") 

            else:
                Print("Invalid choice.Please try again. ")

if __name__ == "__main__":
    main()

    

    
    
# Link to GitHub hands-on: https://github.com/MVizba/war_game 
# Didn't finnished this task, but: 
# README.md file was created 
# Repository was cloned to PC using terminal. 
# through terminal README.md file was updated.abs
# through terminal war.py was uploaded to repository. 
# Issues was created for this card game for further coding.
# 2 issues was solved by me. Uploaded throw terminal from my PC. - git add war.py and git commit -m, git merge and git push to update GitHub
# With pear I will finish this task. He also didn't finnish. And due to deadline there's no time to do it. 
