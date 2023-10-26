import pytest

from sprint3final import SingleStringAnswerQuestion 
from sprint3final import MultipleChoiceQuestion

#  def __init__(self, uuid, enabled, text, correct_answer, options=None):
def test_get_percentage_of_answers():

    question = SingleStringAnswerQuestion("1", 1, "Sample question", "A")
    question.attempts = 5
    question.correct_attempts = 3
    expected_percentage = "60%"
    assert question.get_percentage_of_answers() == expected_percentage

    question.attempts = 0
    assert question.get_percentage_of_answers() == "0%"

    question.attempts = 5
    question.correct_attempts = 5
    assert question.get_percentage_of_answers() == "100%"

def test_check_answer():

    question = SingleStringAnswerQuestion("1", 1, "What is 2 +2 ", "4")

    assert question.check_answer("4") == True
    assert question.check_answer("5") == False


def test_get_uuid():

    question = SingleStringAnswerQuestion("1", 1, "What is 2 +2 ", "4")

    assert question.get_uuid() == "1"
    assert question.get_uuid() != "Namas"

def test_is_single_answer():
    
    question = SingleStringAnswerQuestion("1", 1, "What is 2 +2 ", "4")

    assert question.is_single_answer() == True
    assert question.is_single_answer() != False 

    answers = []
    answers.append("Labas")
    answers.append("Gulbe")

    multiple = MultipleChoiceQuestion("1",1, "text",1,answers)

    assert multiple.is_single_answer() == False

def test_is_enable():

    enabled_object = SingleStringAnswerQuestion("1", 1, "What is 2 +2 ", "4")
    assert enabled_object.enabled == True

    enabled_object.enable(False)
    assert enabled_object.enabled == False











#  def is_single_answer(self):
#         return self.options is not None
if __name__ == "__main__":
    pytest.main()

