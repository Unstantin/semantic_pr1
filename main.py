import re


def remove_non_cyrillic(text):
    pattern = r'[^а-яА-ЯёЁ\s]'
    cleaned_text = re.sub(pattern, '', text)
    return cleaned_text


def add_to_dict_recursive(word, current_dict, part_of_word):
    if len(part_of_word) == depth:
        if "#" not in current_dict:
            current_dict["#"] = dict()
        if word + part_of_word not in current_dict["#"]:
            current_dict["#"][word + part_of_word] = 0
        current_dict["#"][word + part_of_word] += 1
        return

    current_dict[part_of_word] = dict()
    print(word + " " + part_of_word)
    add_to_dict_recursive(word[1:], current_dict[part_of_word], part_of_word + word[0])


result_dict = dict()
depth = 4
dict_of_small_words = dict()
with open('Pushkin.txt', 'r', encoding='UTF-8') as file:
    while True:
        line = file.readline().strip()
        if line == '':
            break
        words_from_line = remove_non_cyrillic(line).split(' ')
        for word in words_from_line:
            if len(word) < depth:
                if word not in dict_of_small_words:
                    dict_of_small_words[word] = 0
                dict_of_small_words[word] += 1

            add_to_dict_recursive(word, result_dict, "")






