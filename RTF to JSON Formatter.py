import base64
import json
from striprtf.striprtf import rtf_to_text
import re
from io import BytesIO
from PIL import Image

def test_data_to_test_output():
    with open("350-401 V41.65_formatted.rtf", "r") as rtf_file:
        with open("test_output.txt", "w") as test_output:
            for line in rtf_file:
                test_output.write(rtf_to_text(line))


def question_parser():
    question_database = {}
    line_count = 0
    line_count_2 = 0
    line_count_3 = 0
    answer_count = 0
    current_question = ""
    image = ""
    with open("350-401 V41.65_formatted.rtf", "r") as question_parser_input:
        for line in question_parser_input:
            if re.search('.{500,}', line):
                line = line.replace(r"\par\pard\fi0\li0\ql\ri0\sb0\sa0\itap0 \plain \f0\fs20", "")
                image = line
            line = rtf_to_text(line)
            #line = line.replace(r"\par\pard\fi0\li0\ql\ri0\sb0\sa0\itap0", "")
            line = line.replace("\n", " ")
            #line = line.replace(r"\f0\fs20", "")
            #line = line.replace(r"\'0d", "")
            #line = line.replace("\plain", "")
            line = line.replace("\r", " ")
            line = line.replace(" ", "", 1)
            line = line + image
            #print(line)
            if re.search('^Q\d*', line):
                split_line = line.split(" ", 1)
                current_question = split_line[0]
                if len(split_line) > 1:
                    question_info = split_line[1]
                else:
                    question_info = "TBD"
                explanation_info = ""
                image_info = ""
                question_database[current_question] = {}
                question_database[current_question]["Question"] = ""
                question_database[current_question]["Options"] = {}
                question_database[current_question]["Answer"] = ""
                question_database[current_question]["Explanation"] = ""
                question_database[current_question]["Num of Answers"] = ""

                line_count += 1
                line_count_2 = 0
                line_count_3 = 0
                answer_count = 0
                print(current_question)
                image = ""
            elif line_count != 0 and not re.search('Q\d*', line):

                if not re.search('^[A-Z][.]', line) and not re.search('^Answer:', line) and answer_count == 0:
                    question_info += line
                    question_database[current_question]["Question"] = question_info.strip()

                if re.search('^[A-Z][.]', line):
                    split_line = line.split(" ", 1)
                    if len(split_line) > 1:
                        question_database[current_question]["Options"][split_line[0]] = split_line[1].strip()
                    else:
                        question_database[current_question]["Options"][split_line[0]] = "TBD"

                elif re.search('^Answer:', line):
                    split_line = line.split(" ", 1)
                    question_database[current_question]["Num of Answers"] = len(split_line[1].strip())
                    question_database[current_question]["Answer"] = split_line[1].strip()
                    answer_count = 1

                elif line_count_2 == 0 and re.search('^Explanation:', line):
                    line_count_2 += 1

                elif line_count_2 != 0:
                    explanation_info += line
                    question_database[current_question]["Explanation"] = explanation_info


    with open("test_output.txt", "w") as test_output:
        test_output.write(json.dumps(question_database, indent=4))


def __main__():
    # test_data_to_test_output()
    question_parser()


__main__()
