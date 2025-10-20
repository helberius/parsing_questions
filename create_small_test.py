import os
import json
import random
from datetime import datetime
from ctypes import c_ssize_t
import pypandoc

from click import style
from markdown_pdf import MarkdownPdf
from markdown_pdf import Section

# Get the list of all files and directories
def get_list_of_json(path_folder):
    ls_json_files = []
    dir_list = os.listdir(path_folder)
    for f in dir_list:
        if f.endswith(".json"):
            ls_json_files.append(f)
    return ls_json_files

def get_paths_outputs(case):
    print(dt_now.isoformat())
    iso_dt_now = dt_now.isoformat()
    iso_dt_now= iso_dt_now.split(".")[0]
    iso_dt_now = iso_dt_now.replace(":","_")
    iso_dt_now = iso_dt_now.replace("-", "_")
    print(iso_dt_now)
    path_output_md = "output/md/output_{case}.md".format(case = case)

    path_output_epub = "output/epub/case_{case}.epub".format(case=case)
    title = "Case {case} {iso_now}".format(case=case, iso_now=iso_dt_now)
    return path_output_md, path_output_epub, title


def build_case(ls_q_json, sample_size, case):
    ls_sample_questions = random.sample(ls_q_json, sample_size)
    st_test = ""
    st_answers = "# Solution" + '\n'
    st_overal_explanation="# Overall Explanation" + '\n'

    path_output_md,  path_output_epub, title = get_paths_outputs(case)
    print(title)

    # pdf = MarkdownPdf(toc_level=2)

    for j in range(0, len(ls_sample_questions)):
        q = ls_sample_questions[j]
        st_q = ""
        st_q = st_q +  "# " +  " <font size='2'> "  + str(j+1) + " "   +q["source"] + " " + q["question_id"]  +"</font>"  + '\n\n'

        st_q = st_q   + q["question_statement"]  +'\n\n'
        st_q = st_q + '\n'
        st_options = ""
        for i in range(0,len(q["ls_possible_answers"])):
            st_options = st_options  +  "- " +str(i)  + " " +  q["ls_possible_answers"][i] + '\n\n'

        st_q = st_q + '\n\n'  + st_options + '\n\n'


        st_test = st_test + st_q


        st_overal_explanation =  st_overal_explanation + "\n" +  "# " +   " <font size='2'>"   + str(j+1) + ") "  +q["source"] + " " + q["question_id"] +  "</font>" +'\n\n' + "Index Correct Anwers: " + str(q["index_correct_answers"]) + '\n\n' + get_pretty_string(q["question_statement"]) + '\n\n' +  st_options  +  '\n\n' +   get_pretty_string(q["overall_explanation"]) + "\n\n"
        st_answers = st_answers + str(j+1) + ") "  +q["source"] + " " + q["question_id"] + " " + str(q["index_correct_answers"]) + '\n'


    st_test = st_test + st_answers
    st_test =st_test + "\n" + st_overal_explanation

    # pdf.add_section(Section(st_answers, toc=False))
    # pdf.add_section(Section(st_overal_explanation, toc=False))
    #
    # pdf.save(path_output_pdf)


    with open(path_output_md, "w", encoding="utf-8") as file:
        file.write(st_test)

    markdown_to_epub(path_output_md, path_output_epub, title)


def markdown_to_epub(md_file, output_epub, title):
    """Convert a Markdown file to EPUB using pandoc."""
    pypandoc.convert_file(
        md_file,
        'epub',
        outputfile=output_epub,
        extra_args=['--toc', '--toc-depth=2', "--metadata", "title:{title}".format(title=title)]
    )
    print(f"EPUB saved as {output_epub}")


def get_pretty_string(source_string):
    ls_lines = source_string.split('\n')
    st_lines = '\n\n '.join(ls_lines)
    return st_lines


if __name__== "__main__":
    dt_now = datetime.now()
    path_folder = "data"
    ls_json_files = get_list_of_json(path_folder)
    ls_q_json = []
    for j in ls_json_files:
        path_json_file = os.path.join(path_folder, j)

        with open (path_json_file) as json_data:
            ls_q = json.load(json_data)
            json_data.close()
            ls_q_json = ls_q_json + ls_q

    SAMPLE_SIZE = 20
    ls_cases = ["red","green", "blue"]
    for case in ls_cases:
        build_case(ls_q_json, SAMPLE_SIZE,case)





    print("job done")