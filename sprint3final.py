'''
How to use a program. 

Navigate in this program by entering numbers to select or to answer the question(if it's not a free_form) and a "." to quit the module. 
1. You must choose mode, entering numbers 1 to 5. 
2. Choice 1 is to input questions. But first, you need to choose what kind of questions you will input, quiz type or free form, by entering number 1 or 2.
    If you input quiz, after question input, you press Enter, then input all the answers individually. When you finish, input  ".". 
Then, input a number whose answer is correct. 
   If you choose a free_form, enter a question, then press enter, input an answer, and press enter. 
3, Choice 2 - will show all the questions with unic ID, the question with answers and statistics, how many attempts it has, how many were answered correctly, and the percentage of this question. 
4, Choice 3 - Disable/Enable. To use it, input UUID from a .csv file, 
then write turn the question on or off. 
5, Choice 4 - Practice mode. to enter this mode, you must be inputed at least five questions. Questions are shown randomly by the weight it has (weight is assigned to correct_attempts). If your answer is correct, it's likely not to be shown again.
6, Choice 5 - Test mode. To enter, you need to have at least five questions. Input the number of questions you would like to answer. The score is saved in txt. 
'''


import random
import csv
import sys
import uuid
import datetime

class Question:
    def __init__(self, uuid, enabled, text, correct_answer, options=None):
        self.id = uuid
        self.enabled = enabled
        self.text = text
        self.correct_answer = correct_answer 
        self.options = options
        self.attempts = 0
        self.correct_attempts = 0

    # Check if question is single or multiple boolen
    def is_single_answer(self):
        return self.options is not None

    # Ceck if question is enable or disable
    def is_enabled(self):
        return bool(int(self.enabled)) 

    # Enable or disable question
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

        #Check if answeer is correct or not
    def check_answer(self, user_answer):
        self.attempts += 1
        print(self.is_single_answer())
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

    # COnvert a question to csv format
    def to_csv(self):
        if self.is_single_answer():
            return [self.id, self.enabled, self.text, "SingleStringAnswer", self.correct_answer, self.attempts, self.correct_attempts]
        else:
            return [self.id, self.enabled, self.text, "MultipleChoice", *self.options, str(self.correct_answer), self.attempts, self.correct_attempts]

    @classmethod
    # Create a question object from CSV data
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
 
    # Subclass to define different question type
class SingleStringAnswerQuestion(Question):
    def __init__(self, uuid, enabled, text, correct_answer):
        super().__init__(uuid, enabled, text, correct_answer, options=None)

    def is_single_answer(self):
        return True

      # Subclass to define different question type
class MultipleChoiceQuestion(Question):
    def __init__(self, uuid, enabled, text, correct_answer, options):
        super().__init__(uuid, enabled, text, correct_answer, options)

    def is_single_answer(self):
        return False


# Function to save question to csv file
def save_questions(questions, filename):
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        for question in questions:
            writer.writerow(question.to_csv())

# Function to load a question from csv file
def load_questions(filename):
    questions = []
    with open(filename, mode='r', encoding='utf-8') as file:
        reader = csv.reader(file)
        for row in reader:
            questions.append(Question.from_csv(row))
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
            print("6. For exiting the program")

            choice = int(input("Enter your choice: "))

            if choice == 1:
                question_type = int(input("Enter 1 for quizz or 2 for free_form "))
                if question_type == 1:
                    answers = []
                    question_text = str(input("Enter your question: "))
                    
                    for _ in range(3):      # Added range to limit answer input
                        question_answer = str(input("Enter answer or . to end "))
                        if question_answer == "." or len(answers) >= 3:
                            break
            
                    
                        answers.append(question_answer)
                        

                    correct_answer = int(input("Which answer is correct? Enter number:"))
                    correct_answer = correct_answer - 1
                    unique_id = uuid.uuid4()

                    questions.append(MultipleChoiceQuestion(unique_id, 1, question_text, correct_answer, answers))
                    save_questions(questions, "questions.csv")

                    print("\nQuestion added to .csv file! ") # Added message that question is added

                elif question_type == 2:
                    question_text = str(input("Enter your question: "))
                    question_answer = str(input("Enter answer: "))
                    unique_id = uuid.uuid4()

                    questions.append(SingleStringAnswerQuestion(unique_id, 1, question_text, question_answer))
                    save_questions(questions, "questions.csv")

                    print("\nQuestion added to .csv file! ") # Added message that question is added

                else:
                    print("wrong choice ")


            elif choice == 2:
                print ("\n------------- STATISTICS -------------")
                for question in questions:
                    print("\r")
                    
                    unique_id = str(question.get_uuid())
                    print("UUID:" + unique_id + " Enabled: " + str(question.is_enabled()))
                    
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
                        question_enable = str(input("Enter, 1 for enable or 2 for disable: ")) # Changed to 1 - enable and 2 for disable
                        if question_enable == "1": #
                            question.enable(1)
                        elif question_enable == "2":#
                            question.enable(0)
                        else:
                            print("wrong input, try again: ")

                        save_questions(questions, "questions.csv")

            #Practice mode:
            elif choice == 4: 

                num_questions = len(questions)
                if num_questions < 5:
                    print("You need to add more questions to start.")
                    continue

                while True:
                    weights = [question.correct_attempts for question in questions]   # Changed to correct attepts
                    question = random.choices(questions, k=1, weights=weights)[0]
                
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
                            
                num_questions = len(questions)
                if num_questions < 5:
                    print("You need to add more questions to start.")
                    continue

                enabled_questions = []      # Changed to get list of enabled questions to choose for answering
                for question in questions:
                    if question.is_enabled() == True:
                        enabled_questions.append(question)
                num_enabled_questions = len(enabled_questions)

                print(f"maximum number of possible questions to answer is {num_enabled_questions}")
                num_to_answer = int(input("How many questions will you answer? "))
                if num_to_answer > num_enabled_questions:
                    print("Choose lower number of questions!")
                    continue

                correct_answers = 0

                enabled_questions = []             #Changed to enabled question
                for question in questions:
                    if question.is_enabled() == True:
                        enabled_questions.append(question)

                for question in random.sample(enabled_questions, num_to_answer): # Changed to enabled questions

                    question.display()
                    user_answer = input("Your answer: ")
                    is_correct = question.check_answer(user_answer)
                    print("Correct!\n" if is_correct else "Incorrect!\n")

                    if is_correct:
                        correct_answers += 1
                
                score = f"Score: {correct_answers}/{num_to_answer}"
                with open("results.txt", "a") as results_file:
                    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    results_file.write(f"{score} - {current_time}\n")
                print(score)
                save_questions(questions, "questions.csv") 
        
            elif choice == 6:
                print("Goodbye!")
                sys.exit()  # Exit the program

            else:
                Print("Invalid choice.Please try again. ")

if __name__ == "__main__":
    main()

# change disable=enable to 1 and 2. 
# change quite choice 6.  
# and print (message in "question was added.")
# 

    
    
# Link to GitHub hands-on: https://github.com/MVizba/war_game 
# Didn't finish this task, but: 
# README.md file was created 
# Repository was cloned to PC using the terminal. 
# Through the terminal README.md file was updated.abs
# through terminal war.py was uploaded to the repository. 
# Issues were created for this card game for further coding.
# 2 issues were solved by me. Uploaded through the terminal from my PC. - git add war.py and git commit -m, git merge and git push to update GitHub
# With pear, I will finish this task. He also didn't finish. And due to the deadline, there's no time to do it. 
