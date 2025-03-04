import pickle
from pprint import pprint
import pandas as pd

filename = 'Turgenev'

with open(filename + "_dict_big_words.pickle", "rb") as file:
    big_words_dict: dict = pickle.load(file)
    #pprint(big_words_dict)

with open(filename + "_dict_small_words.pickle", "rb") as file:
    small_words_dict: dict = pickle.load(file)
    #pprint(small_words_dict)

df = pd.DataFrame(columns=["key1", "key2", "key3", "word", "total"] + ["domain" + str(i) for i in range(1, 15)])

index = 2
domains_n = 14
for dict1_key, dict1_item in big_words_dict.items():
    for dict2_key, dict2_item in dict1_item.items():
        for dict3_key, dict3_item in dict2_item.items():
            for word, item in dict3_item['#'].items():
                domains = [item[i] if i in item.keys() else 0 for i in range(1, domains_n + 1)]
                new_row = [dict1_key, dict2_key, dict3_key, word, sum(item.values())] + domains
                df.loc[index] = new_row
                index += 1

for word, item in small_words_dict.items():
    domains = [item[i] if i in item.keys() else 0 for i in range(1, domains_n + 1)]
    new_row = [None, None, None, word, sum(item.values())] + domains
    df.loc[index] = new_row
    index += 1

df.to_excel(filename + ".xlsx", index=False)
