import json
import glob
import logging
import os
import sys
import optparse


def get_logger(name,
               level=logging.INFO,
               stream_handler=sys.stdout,
               log_name="log.log",
               formatter='%(asctime)s [%(levelname)s] %(name)s: %(message)s'):
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter(formatter)
    stream_handler = logging.StreamHandler(stream_handler)
    stream_handler.setLevel(level)
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

    file_handler = logging.FileHandler(log_name)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    return logger


def cotain_chinese(text):
    """
    check if the input text contains Chinese
    """
    for char in text:
        if '\u4e00' <= char <= '\u9fa5':
            return True
    return False


logger = get_logger("Specs")


def data_conversion(path):
    """
    convert the EdiLU json files into BIO conll formated files
    """

    logger.info("Processing " + path + "//processed_data.json")
    data = json.load(open(path + "//processed_data.json", "r", encoding="UTF-8"))
    final_data = []

    for sent in data:
        pt_text = 0
        pt_ent = 0

        text_list = sent["Text"].split(" ")
        if cotain_chinese(sent["Text"]):
            text_list = [char for char in sent["Text"]]
        while pt_text < len(text_list):
            if pt_ent < len(sent["Entities"]) and sent["Entities"][pt_ent]["Start"] == pt_text:
                final_data.append(" ".join([text_list[pt_text], "NN", "NN", "B-" + sent["Entities"][pt_ent]["Type"]]))
            elif pt_ent < len(sent["Entities"]) \
                 and sent["Entities"][pt_ent]["Start"] < pt_text <= sent["Entities"][pt_ent]["End"]:
                final_data.append(" ".join([text_list[pt_text], "NN", "NN", "I-" + sent["Entities"][pt_ent]["Type"]]))
            else:
                final_data.append(" ".join([text_list[pt_text], "NN", "NN", "O"]))

            if pt_ent < len(sent["Entities"]) and pt_text == sent["Entities"][pt_ent]["End"]:
                pt_ent += 1
            pt_text += 1
            final_data[-1] += "\n"
        final_data.append("\n")

    new_file = open(path + "//processed_data.conll", "w+", encoding="UTF-8")
    new_file.writelines(final_data)


if __name__ == "__main__":
    type_path = "..//Number//"
    optparser = optparse.OptionParser()
    optparser.add_option('--type', default='Number', help='Specify which type you wanna aggregrate')
    opts = optparser.parse_args()[0]
    type_path = type_path.replace("Number", opts.type)
    for lang in glob.glob(type_path + "*"):
        data_conversion(type_path + lang)
