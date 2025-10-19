from typing import List
import re

def clean_lines_one_question(ls_lines_one_question)->List[str]:
    ls_clean_lines = []
    for l in ls_lines_one_question:
        if "(Select two)" in l:
            l = l.replace("? (Select two)"," (Select two)?").strip()
        elif "(Select TWO.)" in l:
            l = l.replace("? (Select TWO.)", " (Select two)?").strip()
        elif ("? (Select THREE.)") in l:
            l = l.replace("? (Select THREE.)", " (Select three)?").strip()
        l = l.replace('\n', '')
        if len(l)>0:
            ls_clean_lines.append(l)
    return ls_clean_lines


def read_file(path_file):
    ls_lines = []
    with open(path_file) as f:
        ls_lines = f.readlines()
    return ls_lines

def group_lines_per_question(ls_lines):
    ld_grouped_lines = []
    ls_new_question = []
    for l in ls_lines:

        if l is not None and   l.startswith("Question"):
            ld_grouped_lines.append(ls_new_question)
            ls_new_question=[]
            ls_new_question.append(l)
        else:
            ls_new_question.append(l)

    ld_grouped_lines.append(ls_new_question)
    return ld_grouped_lines

def get_question_statement(q_lines)->str:
    index_question = -9
    for i in range(0, len(q_lines)):
        l= q_lines[i]
        if l.endswith("?"):
            index_question=i
    ls_question_statement = q_lines[1:index_question+1]
    st_question_statement = '\n'.join(ls_question_statement)
    return st_question_statement


def get_question_possible_answers(q_lines):
    index_question = -9
    for i in range(0, len(q_lines)):
        l= q_lines[i]
        if l.endswith("?"):
            index_question = i
    ls_question_possible_answers=q_lines[index_question+1:]
    return ls_question_possible_answers


def analyze_answers(question_possible_answers):
    ls_correct_answers=[]
    ls_valid_possible_answers=[]
    for i in range(0, len(question_possible_answers)):
        if question_possible_answers[i] in ["Correct answer", "Your answer is correct", "Your selection is correct", "Correct selection"]:
            ls_correct_answers.append(question_possible_answers[i+1])
        if question_possible_answers[i] not in["Correct answer", "Your answer is incorrect", "Your answer is correct", "Your selection is correct", "Correct selection", "Your selection is incorrect"]:
            ls_valid_possible_answers.append(question_possible_answers[i])
    ls_indexes_correct_answers = []
    for j in range(0,len(ls_valid_possible_answers)):
        if ls_valid_possible_answers[j] in ls_correct_answers:
            ls_indexes_correct_answers.append(j)
    return ls_valid_possible_answers, ls_indexes_correct_answers


def get_question_statemant_and_potential_answers(ls_clean_lines_one_question)->List[str]:
    index_overal_explanation = ls_clean_lines_one_question.index("Overall explanation")
    ls_lines_question_statement = ls_clean_lines_one_question[:index_overal_explanation]
    return ls_lines_question_statement

def get_question_id(ls_lines_question_statement)->str:
    st_line_id = ls_lines_question_statement[0]
    match = re.match(r"(Question \d+)", st_line_id)
    st_question_id = ""
    if match:
        st_question_id = match.group(1)
    return st_question_id



def get_overall_explanation(ls_clean_lines_one_question)->(str, str):

    index_overal_explanation = ls_clean_lines_one_question.index("Overall explanation")


    index_domain = ls_clean_lines_one_question.index("Domain")
    ls_lines_overall_explanation = ls_clean_lines_one_question[index_overal_explanation:index_domain]
    ls_domain = ls_clean_lines_one_question[index_domain+1:]
    st_domain = '\n'.join(ls_domain)


    st_overall_explanation = '\n'.join(ls_lines_overall_explanation)
    return st_overall_explanation, st_domain





