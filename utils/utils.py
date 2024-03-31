def get_key_from_dict_by_value(dict_to_search, search_val):
    value = [i for i in dict_to_search if dict_to_search[i] == search_val]

    return value[0]


def insert_new_lines(text, line_length):
    if len(text) <= line_length:

        return text
    else:

        return text[:line_length] + '\n' + insert_new_lines(text[line_length:], line_length)


def convert_number_to_status(status_as_number: bool):
    if status_as_number is True:
        return "Да"
    else:
        return "Нет"
