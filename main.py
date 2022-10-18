#!/bin/python3

import json
from deep_translator import GoogleTranslator

# Options
# ----------------------------
lang_code = 'ru_cu'
lang_region = "Russia"
lang_name = "Cursed Translate MC"
target_lang = "ru"
orig_file_name = "en_us.json"
file_name = f"{lang_code}.json"
method = "new"  # (new, cursed)
temp_lang = "zh-TW"  # (Only for new method)
temp_lang2 = "zh-CN"  # (Only for new method)
pass_number = 3  # (Only for new method)
charset = "gbk"  # shift_jis, euc_rk, big5, gbk, ... (only for cursed method)
# ----------------------------


def read_lang_file():
    print("[INFO] Reading original lang file...")
    try:
        json_file = open(orig_file_name, 'r')
        json_data = json.load(json_file)
        json_file.close()
        return json_data
    except FileNotFoundError:
        print("[ERROR] Lang file not found!")
        exit()


def create_json():
    file = open(file_name, 'w')
    file.write("{}")
    file.close()


def translate(string):
    if method != "new":
        locale = GoogleTranslator(source='auto', target="ru").translate(text=string)
        try:
            encoded_text = locale.encode("utf-8").decode(charset)
        except UnicodeDecodeError:
            print("[ERROR] UnicodeDecodeError => Skip encoding")
            encoded_text = locale
        string = GoogleTranslator(source='auto', target=target_lang).translate(text=encoded_text)
        return string
    else:
        for a in range(pass_number):
            pass1 = GoogleTranslator(source='auto', target=temp_lang).translate(text=string)
            pass2 = GoogleTranslator(source='auto', target=target_lang).translate(text=pass1)
            pass3 = GoogleTranslator(source='auto', target=temp_lang2).translate(text=pass2)
            string = GoogleTranslator(source='auto', target=target_lang).translate(text=pass3)
        return string


def finalize():
    json_file = open(file_name, 'r')
    json_data = json.load(json_file)
    json_file.close()
    json_data["language.name"] = lang_name
    json_data["language.region"] = lang_region
    json_data["language.code"] = lang_code
    json_file = open(file_name, 'w')
    json.dump(json_data, json_file, indent=4)
    json_file.close()


if __name__ == "__main__":
    print("[INFO] Starting...")

    result = {}
    data = read_lang_file()
    print("[INFO] Started. The process can take a long time!")
    for name in data:
        value = data[name]
        result[name] = translate(value)
        print(
            '[INFO] Progress: {}% ({}/{}) ({})'.format((len(result) * 100) // len(data), len(result), len(data), name))

    print("[INFO] Saving to file...")
    create_json()
    result_file = open(file_name, 'w')
    json.dump(result, result_file, indent=4)
    result_file.close()

    print("[INFO] Finalizing...")
    finalize()
    print("[INFO] Done!")
