import re
import pickle


class Settings:
    depth = None
    domain_n = None
    split_domain_word = 'глава'


def remove_non_cyrillic(text):
    pattern = r'[^а-яА-ЯёЁ\s]'
    cleaned_text = re.sub(pattern, '', text)
    return cleaned_text


def add_to_dict_recursive(word, current_dict, current_depth, current_domain):
    if current_depth == settings.depth:
        if "#" not in current_dict:
            current_dict["#"] = dict()
        if word not in current_dict["#"]:
            current_dict["#"][word] = dict()
        if current_domain not in current_dict["#"][word]:
            current_dict["#"][word][current_domain] = 0

        current_dict["#"][word][current_domain] += 1
        return

    if len(word[:current_depth]) == 0:
        next_dict = current_dict
        if word[:current_depth] not in current_dict:
            current_dict[word[:current_depth]] = dict()
    else:
        if word[:current_depth] not in current_dict:
            current_dict[word[:current_depth]] = dict()
        next_dict = current_dict[word[:current_depth]]

    add_to_dict_recursive(word, next_dict, current_depth + 1, current_domain)


def get_words_from_file(filename):
    dict_of_big_words = dict()
    depth = 4
    dict_of_small_words = dict()
    current_domain = 0
    turgenev_mode = filename.startswith("T")
    turgenev_index = 0
    with open(filename, 'r', encoding='UTF-8') as file:
        while True:
            line = file.readline()
            if line == '':
                break

            words_from_line = remove_non_cyrillic(line.strip().lower()).split(' ')
            for word in words_from_line:
                if word == '':
                    continue

                if word == settings.split_domain_word:
                    if turgenev_mode:
                        if turgenev_index % 2 == 0:
                            current_domain += 1
                        turgenev_index += 1
                    else:
                        current_domain += 1
                print(word)

                if len(word) < depth:
                    if word not in dict_of_small_words:
                        dict_of_small_words[word] = dict()
                    if current_domain not in dict_of_small_words[word]:
                        dict_of_small_words[word][current_domain] = 0
                    dict_of_small_words[word][current_domain] += 1
                    continue

                add_to_dict_recursive(word, dict_of_big_words, 1, current_domain)

    with open(filename[:-4] + "_dict_big_words.pickle", "wb") as file:
        pickle.dump(dict_of_big_words, file)

    with open(filename[:-4] + "_dict_small_words.pickle", "wb") as file:
        pickle.dump(dict_of_small_words, file)


settings = Settings()
settings.depth = 4
settings.domain_n = 14
get_words_from_file("Pushkin.txt")
get_words_from_file("Turgenev.txt")


