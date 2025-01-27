import json
from striprtf.striprtf import rtf_to_text
import re




def test_data_to_test_output():
    with open("350-401 V41.65_formatted.rtf", "r") as rtf_file:
        with open("test_output.txt", "w") as test_output:
            for line in rtf_file:
                test_output.write(rtf_to_text(line))


def question_parser():
    question_database = {}
    line_count = 0
    line_count_2 = 0
    answer_count = 0
    current_question = ""
    image_count = 0
    with open("350-401 V41.65_formatted.rtf", "r") as question_parser_input:
        for line in question_parser_input:
            image = ""
            if re.search('.{500,}', line):
                image = f" image_{image_count} "
                image_count += 1
            line = rtf_to_text(line)
            line = line.replace("\n", " ")
            line = line.replace("\r", " ")
            line = line.replace(" ", "", 1)
            line = line
            # print(line)
            if re.search('^Q\d+', line):
                split_line = line.split(" ", 1)
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
            elif line_count != 0 and not re.search('Q\d+', line):

                if not re.search('^[A-Z][.]', line) and not re.search('^Answer:', line) and answer_count == 0:
                    question_info += line
                    question_database[current_question]["Question"] = question_info.strip() + image

                if re.search('^[A-Z][.]', line):
                    split_line = line.split(" ", 1)
                    if len(split_line) > 1:
                        question_database[current_question]["Options"][split_line[0]] = split_line[1].strip() + image
                    else:
                        question_database[current_question]["Options"][split_line[0]] = "ERROR"

                elif re.search('^Answer:', line):
                    split_line = line.split(" ", 1)
                    question_database[current_question]["Num of Answers"] = len(split_line[1].strip())
                    question_database[current_question]["Answer"] = split_line[1].strip()
                    answer_count = 1

                elif line_count_2 == 0 and re.search('^Explanation:', line):
                    line_count_2 += 1

                elif line_count_2 != 0:
                    explanation_info += line
                    question_database[current_question]["Explanation"] = explanation_info + image

    with open("Question_DB.json", "w") as test_output:
        test_output.write(json.dumps(question_database, indent=4))


def __main__():
    # test_data_to_test_output()
    question_parser()


__main__()
