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

def get_paths_outputs():
    print(dt_now.isoformat())
    iso_dt_now = dt_now.isoformat()
    iso_dt_now= iso_dt_now.split(".")[0]
    iso_dt_now = iso_dt_now.replace(":","_")
    iso_dt_now = iso_dt_now.replace("-", "_")
    print(iso_dt_now)
    path_output_md = "output/md/output{iso_now}.md".format(iso_now = iso_dt_now)
    path_output_pdf = "output/pdf/output{iso_now}.pdf".format(iso_now = iso_dt_now)
    path_output_epub = "output/epub/output{iso_now}.epub".format(iso_now=iso_dt_now)
    title = iso_dt_now
    return path_output_md, path_output_pdf, path_output_epub, title


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

    ls_sample_questions = random.sample(ls_q_json, 20)
    st_test = ""
    st_answers = "# Solution" + '\n'
    st_overal_explanation="# Overall Explanation" + '\n'

    path_output_md, path_output_pdf, path_output_epub, title = get_paths_outputs()
    print(title)

    pdf = MarkdownPdf(toc_level=2)

    for j in range(0, len(ls_sample_questions)):
        q = ls_sample_questions[j]
        st_q = ""
        st_q = st_q +  "# " + str(j+1) + ") "  +q["source"] + " " + q["question_id"]  + '\n'

        st_q = st_q  + "<font size='1'>"  + q["question_statement"]  + "</font>" +'\n'
        st_q = st_q + '\n'
        for i in range(0,len(q["ls_possible_answers"])):
            st_q = st_q  +  "- " +str(i)  + " " + "<font size='1'>" +  q["ls_possible_answers"][i] + "</font>" + '\n'
        st_q = st_q +'\n'
        pdf.add_section(Section(st_q, toc=False))
        st_test = st_test + st_q

        st_overal_explanation =  st_overal_explanation + "\n" +  "## " + str(j+1) + ") "  +q["source"] + " " + q["question_id"]  + '\n\n' + "Index Correct Anwers: " + str(q["index_correct_answers"]) + '\n' + get_pretty_string(q["overall_explanation"]) + "\n\n\n"
        st_answers = st_answers + str(j+1) + ") "  +q["source"] + " " + q["question_id"] + " " + str(q["index_correct_answers"]) + '\n'


    st_test = st_test + st_answers
    st_test =st_test + "\n" + st_overal_explanation

    pdf.add_section(Section(st_answers, toc=False))
    pdf.add_section(Section(st_overal_explanation, toc=False))

    pdf.save(path_output_pdf)


    with open(path_output_md, "w", encoding="utf-8") as file:
        file.write(st_test)

    markdown_to_epub(path_output_md, path_output_epub, title)



    print("job done")