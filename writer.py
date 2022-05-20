import json

def write_json(data):
    json_string = json.dumps(data)

    out = open('json_data.json', 'w')
    out.write(json_string)

    out.close()
    print('Written successfully')