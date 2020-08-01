import json
import glob


def data_count(path):
    files = glob.glob(path + "//*.json")
    types = set()

    for file in files:
        data = json.load(open(file, "r", encoding="UTF-8"))

        for (i, datai) in enumerate(data):
            ents = datai["Results"]
            try:
                for (i, ent) in enumerate(ents):
                    # sent_ents.append({
                    #     "Text":
                    #         ent["Text"],
                    #     "Type":
                    #         ent["Type"] if "Type" in ent.keys() else
                    #         (ent["type"] if "type" in ent.keys() else ent["Typename"]),
                    #     "Start":
                    #         ent["Start"],
                    #     "End":
                    #         ent["End"] if "End" in ent.keys() else ent["Start"] + ent["Length"] - 1
                    # })
                    types.add(str(ent.keys()))
            except Exception as e:
                print(ent)
                raise e
    for tp in types:
        print(tp)


def data_gen(path):
    files = glob.glob(path + "//*.json")
    final_data = []
    tot_sents = 0
    for file in files:
        data = json.load(open(file, "r", encoding="UTF-8"))

        for (i, datai) in enumerate(data):
            ents = datai["Results"]
            sent_ents = []
            try:
                for (i, ent) in enumerate(ents):
                    sent_ents.append({
                        "Text":
                            ent["Text"],
                        "Type":
                            ent["Type"] if "Type" in ent.keys() else
                            (ent["TypeName"] if "TypeName" in ent.keys() else ent["Typename"]),
                        "Start":
                            ent["Start"],
                        "End":
                            ent["End"] if "End" in ent.keys() else ent["Start"] + ent["Length"] - 1
                    })
            except Exception as e:
                print(ent)
                raise e
            final_data.append({"Text": datai["Input"], "Entities": sent_ents})

        print(file)
        print("Sentence Count: ", len(data))
        tot_sents += len(data)

    assert len(final_data) == tot_sents
    print("Total Sentences: ", tot_sents)
    final_data = json.dumps(final_data, indent=4)
    new_file = open("new_data.json", "w+", encoding="UTF-8")
    new_file.writelines(final_data)


def data_analysis(path):
    data = json.load(open(path, "r", encoding="UTF-8"))
    type_set = set()
    for sent in data:
        #print(sent)
        for ent in sent["Entities"]:
            type_set.add(ent["Type"])
    print(type_set)


if __name__ == "__main__":
    #data_count("..//DateTime//English")
    #data_gen("..//DateTime//English")
    data_analysis("new_data.json")