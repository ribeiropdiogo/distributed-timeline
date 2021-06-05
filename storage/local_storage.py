import yaml

DATABASE_PATH = 'database/'

'''
    import all data from the provided yaml file 
'''


def __importData(path_to_file):
    try:
        with open(path_to_file) as file:
            data = yaml.full_load(file)
            file.close()
            return data
    except Exception:
        pass


''' 
    read the data from the provided file path to the yaml database and
    return the timeline and the peers that I am following.
'''


def read_data(path_to_file):
    data = __importData(path_to_file)
    if data:
        print(data[0].get('timeline'))
        return data[0].get('timeline'),data[1].get('following')
    else:
        return [], []


'''
    save the data in a peer to the local database
'''


def save_data(timeline, following, output_file_name):
    dict_file = [{'timeline': timeline}, {'following': following}]
    with open(DATABASE_PATH + output_file_name + '.yaml', 'w') as file:
        yaml.dump(dict_file, file, sort_keys=True)
    file.close()
