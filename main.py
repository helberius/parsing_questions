import parser_01.parser_funcs as pf
# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    path_source =  "data/Purchase01_T2.txt"
    ls_lines = pf.read_file(path_source)
    print(len(ls_lines))

# See PyCharm help at https://www.jetbrains.com/help/pycharm/


