# -*- coding: utf-8 -*-

import hashlib
import re
from typing import List, Set, Union, Dict
import nltk


def complex_formatter(text: Set[str]) -> str:
    text = sorted(text)
    temp = ' '.join(text) \
        .replace(',', ' ').lower() \
        .replace('"', "").replace("'", '') \
        .replace('\n', ' ').replace('  ', ' ') \
        .replace(' ', ' ').replace('ё', 'е').replace(';', '').strip()
    temp = temp.encode("utf-8", "ignore").decode()
    new = re.sub(r'^https?:\/\/.*[\r\n]*', '', temp, flags=re.MULTILINE)
    return new


def scrapper(text: str, keys: List[str]) -> str:
    text = text.replace(',', '').replace('"', "").replace("'", '').replace('\n', ' ').strip()
    q = rf"[^.]*?(?:{'|'.join(keys)})[^.]*\."
    try:
        a = ' '.join(re.findall(q, text)).lower().strip()
        return a
    except Exception as e:
        print(e)
        return ' '


def nltk_scrapper(text: str, keys: dict) -> Union[Dict[str, Union[str, list]], int]:
    """забрать предложение с ключом и предложения вокруг него"""
    splited_text = nltk.sent_tokenize(text)
    answer = set()
    formatted_keys_id = ''

    for index, sentence in enumerate(splited_text):
        for k_id, key in keys.items():
            if key in sentence:
                if index - 1 >= 0:
                    answer.add(str(splited_text[index - 1]))

                answer.add(str(sentence))

                if index + 1 < len(splited_text):
                    answer.add(str(splited_text[index + 1]))

                formatted_keys_id += str(k_id) + ','

    formatted_text = complex_formatter(answer)
    id_text = hashlib.md5(formatted_text.encode('utf-8')).hexdigest()

    if formatted_text:
        return {"text": formatted_text, 'id_text': id_text, 'keys_id': formatted_keys_id}
    else:
        return 0
