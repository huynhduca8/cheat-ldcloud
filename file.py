import json
def write_file(file_name, data):
    json_object = json.dumps(data, indent=4)
    with open(file_name, "w") as outfile:
        outfile.write(json_object)
def read_file(file_name):
    f = open(file_name)
    return json.load(f)