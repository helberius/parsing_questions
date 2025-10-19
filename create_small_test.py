import os
import json
import random
from datetime import datetime
from ctypes import c_ssize_t

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
    st_answers = "### Solution" + '\n'
    for j in range(0, len(ls_sample_questions)):
        q = ls_sample_questions[j]
        st_test = st_test + '<font size ="1">' + "**" + str(j+1) + ") "  +q["source"] + " " + q["question_id"] + '**' + "</font>" + '\n'
        st_answers = st_answers  + str(j+1) + ") "  +q["source"] + " " + q["question_id"] + " " +  str(q["index_correct_answers"]) +  '\n'

        st_test = st_test + '\n'
        st_test = st_test + '<font size ="1">'  + q["question_statement"]  + '</font>' + '\n'
        #st_test = st_test +  q["question_statement"] + '\n'
        st_test = st_test + '\n'
        for i in range(0,len(q["ls_possible_answers"])):
            st_test = st_test  +  "- " +str(i)  + " " + "<font size='1'>" +  q["ls_possible_answers"][i] + "</font>" + '\n'
        st_test = st_test + '\n'

    print(dt_now.isoformat())
    iso_dt_now = dt_now.isoformat()
    iso_dt_now= iso_dt_now.split(".")[0]
    iso_dt_now = iso_dt_now.replace(":","_")
    iso_dt_now = iso_dt_now.replace("-", "_")
    print(iso_dt_now)
    path_output = "markup_output/output{iso_now}.md".format(iso_now = iso_dt_now)
    path_output_pdf = "markup_output/output{iso_now}.pdf".format(iso_now = iso_dt_now)
    with open(path_output, "w", encoding="utf-8") as file:
        file.write(st_test)

    pdf = MarkdownPdf(toc_level=2)
    pdf.add_section(Section(st_test, toc=False))
    pdf.add_section(Section(st_answers, toc=False))
    pdf.save(path_output_pdf)





    print("job done")