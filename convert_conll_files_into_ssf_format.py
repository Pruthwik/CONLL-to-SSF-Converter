"""Convert files in CONLL format into SSF format."""
from argparse import ArgumentParser
import os
from re import search


def read_conll_file_convert_to_ssf_and_write(input_file_path, opr, output_file_path):
    """
    Read a conll file, convert it into SSF, and write to another file.
    :param input_file_path: Enter the input file path
    :param opr: Operation: 0 for POS, 1 for Chunk, 2 for Morph
    :param output_file_path: Enter the output file path where the data will be written in SSF

    :return: None
    """
    sent_count = 1
    cntr = 1
    subcntr = 1
    sent_string = ''
    prev_tag = ''
    prev_sent_count = 0
    sentences = []
    lines = open(input_file_path, 'r', encoding='utf-8').readlines()
    sent_string += "<Sentence id='" + str(sent_count) + "'>\n"
    if opr in [1, 2]:
        for line in lines:
            line = line.strip()
            if line:
                features = line.split('\t')
                chnk_info = features[2].split('-')
                if search('B-', features[2]) is not None:
                    subcntr = 1
                    if prev_sent_count != sent_count:
                        sent_string += str(cntr) + '\t((\t' + chnk_info[1] + '\t\n'
                        prev_sent_count = sent_count
                    else:
                        cntr += 1
                        sent_string += '\t))\n' + str(cntr) + '\t((\t' + chnk_info[1] + '\t\n'
                    if opr == 1:
                        sent_string += str(cntr) + '.' + str(subcntr) + '\t' + features[0] + '\t' + features[1] + '\t\n'
                    else:
                        if features[3][: 3] == '<fs':
                            pass
                        else:
                            features[3] = "<fs af='" + features[3] + "'>"
                        sent_string += str(cntr) + '.' + str(subcntr) + '\t' + features[0] + '\t' + features[1] + '\t' + features[3] + '\n'
                        subcntr += 1
                    prev_tag = chnk_info[1]
                elif prev_tag and search('I-' + prev_tag, features[2]) is not None:
                    if opr == 1:
                        sent_string += str(cntr) + '.' + str(subcntr) + '\t' + features[0] + '\t' + features[1] + '\t\n'
                    else:
                        if features[3][: 3] == '<fs':
                            pass
                        else:
                            features[3] = "<fs af='" + features[3] + "'>"
                        sent_string += str(cntr) + '.' + str(subcntr) + '\t' + features[0] + '\t' + features[1] + '\t' + features[3] + '\n'
                    subcntr += 1
                    prev_tag = chnk_info[1]
                if prev_tag and prev_tag != chnk_info[1] and chnk_info[0] == 'I':
                    subcntr = 1
                    cntr += 1
                    sent_string += '\t))\n' + str(cntr) + '\t((\t' + chnk_info[1] + '\t\n'
                    if opr == 1:
                        sent_string += str(cntr) + '.' + str(subcntr) + '\t' + features[0] + '\t' + features[1] + '\t\n'
                    else:
                        if features[3][: 3] == '<fs':
                            pass
                        else:
                            features[3] = "<fs af='" + features[3] + "'>"
                        sent_string += str(cntr) + '.' + str(subcntr) + '\t' + features[0] + '\t' + features[1] + '\t' + features[3] + '\n'
                    subcntr += 1
                    prev_tag = chnk_info[1]
                if not prev_tag and chnk_info[0] == 'I':
                    sent_string += str(cntr) + '\t((\t' + chnk_info[1] + '\t\n'
                    if opr == 1:
                        sent_string += str(cntr) + '.' + str(subcntr) + '\t' + features[0] + '\t' + features[1] + '\t\n'
                    else:
                        if features[3][: 3] == '<fs':
                            pass
                        else:
                            features[3] = "<fs af='" + features[3] + "'>"
                        sent_string += str(cntr) + '.' + str(subcntr) + '\t' + features[0] + '\t' + features[1] + '\t' + features[3] + '\n'
                    prev_sent_count = sent_count
                    prev_tag = chnk_info[1]
                    subcntr += 1
            else:
                if not search("<Sentence id='" + str(sent_count) + "'>\n$", sent_string):
                    sent_string += "\t))\n</Sentence>\n"
                    sentences.append(sent_string)
                    sent_count += 1
                    sent_string = "<Sentence id='" + str(sent_count) + "'>\n"
                    cntr = 1
                    subcntr = 1
                    prev_tag = ''
    else:
        for line in lines:
            line = line.strip()
            if line:
                features = line.split('\t')
                sent_string += str(cntr) + '\t' + features[0] + '\t' + features[-1] + '\t\n'
                cntr += 1
            else:
                if not search("<Sentence id='" + str(sent_count) + "'>\n$", sent_string):
                    sent_string += '</Sentence>\n'
                    sentences.append(sent_string)
                    sent_count += 1
                    cntr = 1
                    subcntr = 1
                    sent_string = "<Sentence id='" + str(sent_count) + "'>\n"
    if sent_string and not search("<Sentence id='" + str(sent_count) + "'>\n$", sent_string):
        sent_string += '</Sentence>\n'
        sentences.append(sent_string)
    write_lines_to_file(sentences, output_file_path)


def read_conll_files_convert_to_ssf_and_write(input_folder_path, opr, output_folder_path):
    """
    Read conll files in a folder, convert them into SSF, and write them to files in a folder.

    :param input_file_path: Enter the input file path
    :param opr: Operation: 0 for POS, 1 for Chunk, 2 for Morph
    :param output_file_path: Enter the output file path where the data will be written in SSF

    :return: None
    """
    for root, dirs, files in os.walk(folder_path):
        for fl in files:
            input_file_path = os.path.join(input_folder_path, fl)
            output_file_path = os.path.join(output_folder_path, fl)
            read_conll_file_convert_to_ssf_and_write(input_file_path, opr, output_file_path)


def write_lines_to_file(lines, file_path):
    '''
    Write lines to a file.

    :param lines: Enter a list of lines/string
    :param file_path: Enter the file path where the lines will be written

    :return: None
    '''
    with open(file_path, 'w', encoding='utf-8') as file_write:
        file_write.write('\n'.join(lines) + '\n')


def main():
    """
    Pass arguments and call functions.
    
    :param: None

    :return: None
    """
    parser = ArgumentParser()
    parser.add_argument('--input', dest='inp', help="Add the input path from where tokens and its features will be extracted")
    parser.add_argument('--output', dest='out', help="Add the output file where the features will be saved")
    parser.add_argument('--opr', dest='opr', help="Add the operation 0 pos tagging, 1 POS+chunking 2, for morph+pos+chunk", type=int, choices=[0, 1, 2])
    args = parser.parse_args()
    if not os.path.isdir(args.inp):
        read_conll_file_convert_to_ssf_and_write(args.inp, args.opr, args.out)
    else:
        if not os.path.isdir(args.out):
            os.makedirs(args.out)
        read_conll_files_convert_to_ssf_and_write(args.inp, args.opr, args.out)


if __name__ == '__main__':
    main()

