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


logger = get_logger("Specs")


def data_gen(path):
    """
    aggregrate all specs json files under this path into one EdiLU format json file
    """
    files = glob.glob(path + "//*.json")
    final_data = []
    tot_sents = 0
    for file in files:
        if "processed_data.json" in file or "merged_data.json" in file:
            print(file)
            continue
        logger.info("Processing " + file)
        data = json.load(open(file, "r", encoding="UTF-8"))
        for (i, datai) in enumerate(data):
            try:
                ents = datai["Results"]
                sent_ents = []
                for (i, ent) in enumerate(ents):
                    # make up lost tokens
                    if "Start" not in ent.keys():
                        ent["Start"] = datai["Input"].find(ent["Text"])
                        #logger.warning("Can't find Start in original, find one according to the entity text")
                    if "Length" not in ent.keys():
                        ent["Length"] = len(ent["Text"])
                        #logger.warning("Can't find Length in original, find one according to the entity text")

                    # extract key information as a entity
                    ent_type = ent["Type"] if "Type" in ent.keys() else (ent["TypeName"] if "TypeName" in ent.keys() else ent["Typename"])
                    # convert datetimeV2.* to *
                    ent_type = ent_type.split(".")[-1] if "datetimeV2" in ent_type else ent_type
                    
                    # remove entities with null typename
                    if len(ent_type) == 0:
                        logger.warning("Null entities occured in "+str(ents))
                        continue

                    sent_ents.append({
                        "Text":
                            ent["Text"],
                        "Type":
                            ent_type,
                        "Start":
                            ent["Start"],
                        "End":
                            ent["End"] if "End" in ent.keys() else ent["Start"] + ent["Length"] - 1
                    })
            except Exception as e:
                # in case of any un-expected formats
                logger.debug(file)
                logger.debug(datai)
                #print(ent)
                raise e
            final_data.append({"Text": datai["Input"], "Entities": sent_ents})
        tot_sents += len(data)
        assert len(final_data) == tot_sents

    # robustness check and get basic statistics about current dataset
    data_analysis(final_data)
    # dump the processed data
    final_data = json.dumps(final_data, indent=4)
    new_file = open(path + "//processed_data.json", "w+", encoding="UTF-8")
    new_file.writelines(final_data)


def data_analysis(data):
    """
    Analyze the data

    Args:
        data : list of EdiLU objects
    """

    cnt_ent = 0
    avg_len = 0
    cnt_no_ent_sent = 0
    type_dict = {}

    for sent in data:
        if len(sent["Entities"]) == 0:
            cnt_no_ent_sent += 1
        for ent in sent["Entities"]:
            type_dict[ent["Type"]] = type_dict.get(ent["Type"], 0) + 1
            avg_len += len(ent["Text"])
        cnt_ent += len(sent["Entities"])
    avg_len  =  avg_len/cnt_ent if cnt_ent!=0 else -1

    logger.info("Total Sentences: {0}, Totel Entities: {1}, Avg Entity Length: {2}, Sentence w/o Entities: {3}".format(
        len(data), cnt_ent, round(avg_len, 2), cnt_no_ent_sent))
    for (tp, no) in sorted(type_dict.items(),key=lambda item: item[0]):
        logger.info(": ".join([str(tp), str(no)]))
    
    logger.info("============================================================================================")

def data_merge(path, dataset_name="processed_data"):
    """
    Merge the processed datasets with the name input 

    """
    files = glob.glob(path+"**//"+dataset_name+".json")
    logger.info("Found {} files under the path {}".format(len(files),path))
    final_data = []

    for file in files:
        assert dataset_name in file
        data = json.load(open(file,"r",encoding="utf-8"))
        final_data += data

    data_analysis(final_data)
    final_data = json.dumps(final_data,indent=4)
    new_file = open(path + "//merged_data.json", "w+", encoding="UTF-8")
    new_file.writelines(final_data)


if __name__ == "__main__":
    type_path = "..//Number//"
    optparser = optparse.OptionParser()
    optparser.add_option('--type', default='Number', help='Specify which type you wanna aggregrate')
    optparser.add_option('--do_merge', type="int", default='1', help='Specify whether to merge every dataset after aggregration')
    opts = optparser.parse_args()[0]
    type_path = type_path.replace("Number", opts.type)
    for lang in glob.glob(type_path + "*//"):
        data_gen(type_path + lang)
    if opts.do_merge:
        data_merge(type_path)
