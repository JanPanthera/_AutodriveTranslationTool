import re

def create_dictionary(input_path):
    # open the file
    with open(input_path, 'r', encoding='utf-8') as f:
        # read the file
        text = f.read()
        # find all the names and groups
        names = re.findall(r'<name>(.*?)</name>', text)
        groups = re.findall(r'<group>(.*?)</group>', text)
        # create a dictionary
        dictionary = {}
        # iterate through the names and groups
        for name, group in zip(names, groups):
            # if the name is not in the dictionary
            if name not in dictionary:
                # add the name and the group to the dictionary
                dictionary[name] = group
        # create a new file
        with open('dictionary.txt', 'w', encoding='utf-8') as f:
            # write the dictionary to the file
            for name, group in dictionary.items():
                f.write(name + ',\n')
        # print the dictionary
        print(dictionary)
