def read_file(path_file):
    ls_lines = []
    with open(path_file) as f:
        ls_lines = f.readlines()
    return ls_lines

def process_lines(ls_lines):
    ld_grouped_lines = []
    ls_new_question = []
    for l in ls_lines:

        if l is not None and   l.startswith("Question"):
            ld_grouped_lines.append(ls_new_question)
            ls_new_question=[]
            ls_new_question.append(l)
        else:
            ls_new_question.append(l)

    return ld_grouped_lines

def get_question_statement(q_lines):
    question_statement =[]
    q_lines = q_lines[2:]
    for l in q_lines:
        tl= l.strip().replace("\n","")
        if tl.endswith("?"):
            question_statement.append(l)
            return question_statement
        else:
            question_statement.append(l)
    return question_statement


def get_question_possible_answers(q_lines):
    question_possible_answers =[]
    q_lines = q_lines[2:]
    for l in q_lines:
        tl= l.strip().replace("\n","")
        if tl.endswith("?"):
            question_possible_answers=[]
        elif tl.startswith("Overall explanation"):
            return question_possible_answers
        elif tl!="":
            question_possible_answers.append(tl)
    return question_possible_answers


def get_overall_explanation(q_lines):
    question_explanation = []
    for l in q_lines:
        tl= l.strip().replace("\n","")
        if tl.startswith("Overall explanation"):
            question_explanation = []
            question_explanation.append(tl)
        elif tl!="":
            question_explanation.append(tl)
    return question_explanation


def analyze_answers(question_possible_answers):
    ls_correct_answers=[]
    ls_valid_possible_answers=[]
    for i in range(0, len(question_possible_answers)):
        if question_possible_answers[i] in ["Correct answer", "Your answer is correct"]:
            ls_correct_answers.append(question_possible_answers[i+1])
        if question_possible_answers[i] not in["Correct answer", "Your answer is incorrect", "Your answer is correct"]:
            ls_valid_possible_answers.append(question_possible_answers[i])
    ls_indexes_correct_answers = []
    for j in range(0,len(ls_valid_possible_answers)):
        if ls_valid_possible_answers[j] in ls_correct_answers:
            ls_indexes_correct_answers.append(j)
    return ls_valid_possible_answers, ls_indexes_correct_answers
