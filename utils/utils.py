def get_key_from_dict_by_value(dict_to_search, search_val):
    value = [i for i in dict_to_search if dict_to_search[i] == search_val]
    return value[0]
