import parser_01.parser_funcs as pf
import json


def process_one_test(dict_run):
    ls_questions_parsed = []
    ls_lines = pf.read_file(dict_run["path_source"])
    ls_grouped_lines = pf.group_lines_per_question(ls_lines)
    for group_lines  in ls_grouped_lines:
        clean_lines_one_question= pf.clean_lines_one_question(group_lines)
        if "Overall explanation" in clean_lines_one_question:
            overall_explanation, st_domain = pf.get_overall_explanation(clean_lines_one_question)
            question_statement_and_potential_answers = pf.get_question_statemant_and_potential_answers(clean_lines_one_question)
            question_statement = pf.get_question_statement(question_statement_and_potential_answers)
            question_id = pf.get_question_id(question_statement_and_potential_answers)
            ls_possible_answers_raw = pf.get_question_possible_answers(question_statement_and_potential_answers)
            ls_valid_possible_answers_clean, ls_indexes_correct_answers = pf.analyze_answers(ls_possible_answers_raw)
            if len(ls_indexes_correct_answers)>2:
                print(dict_run["test_id"], "filter 1", question_id)
                pass
            elif len(ls_indexes_correct_answers)==1 and ls_indexes_correct_answers[0] > 6:
                print(dict_run["test_id"], "filter 2", question_id)
                pass
            elif len(ls_indexes_correct_answers)==2 and (ls_indexes_correct_answers[0]>6 or ls_indexes_correct_answers[1]>6):
                print(dict_run["test_id"], "filter 3", question_id)
                pass
            else:
                dict_one_parsed_question ={
                    "source":dict_run["test_id"],
                    "question_id":question_id,
                    "question_statement":question_statement,
                    "ls_possible_answers":ls_valid_possible_answers_clean,
                    "index_correct_answers":ls_indexes_correct_answers,
                    "overall_explanation":overall_explanation,
                    "domain":st_domain
                }
                ls_questions_parsed.append(dict_one_parsed_question)
    with open(dict_run["path_output"], 'w', encoding='utf-8') as f:
        json.dump(ls_questions_parsed, f, ensure_ascii=False, indent=4)

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    dict_runs = [{
        "path_source":"data/Purchase01_T2.txt",
        "path_output":"data/Purchase01_T2.json",
        "test_id":"Purchase01_T2"
    },
        {
        "path_source":"data/purchase01_T1.txt",
        "path_output":"data/purchase01_T1.json",
        "test_id":"Purchase01_T1"
    },
        {
        "path_source":"data/purchase01_T3.txt",
        "path_output":"data/purchase01_T3.json",
        "test_id":"Purchase01_T3"
    },
        {
        "path_source":"data/purchase01_T4.txt",
        "path_output":"data/purchase01_T4.json",
        "test_id":"Purchase01_T4"
    },
        {
        "path_source":"data/purchase01_T5.txt",
        "path_output":"data/purchase01_T5.json",
        "test_id":"Purchase01_T5"
    },
        {
        "path_source":"data/purchase01_T6.txt",
        "path_output":"data/purchase01_T6.json",
        "test_id":"Purchase01_T6"
    }]
    for dict_run in dict_runs:
        process_one_test(dict_run)










# See PyCharm help at https://www.jetbrains.com/help/pycharm/


