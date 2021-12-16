enable_debugging = False

def format_string(string):
    string_list = string.translate({ord(','): None})

    return string_list

def debug_data(msg):
    print(msg)
