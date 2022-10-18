#!/bin/python3

import json
import deep_translator.exceptions
from datetime import datetime
from memory_profiler import memory_usage
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
pass_number = 1  # (Only for new method)
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


def translate(key, string):
    if method == "new":
        for a in range(pass_number):
            try:
                pass1 = GoogleTranslator(source='auto', target=temp_lang).translate(text=string)
                pass2 = GoogleTranslator(source='auto', target=target_lang).translate(text=pass1)
                pass3 = GoogleTranslator(source='auto', target=temp_lang2).translate(text=pass2)
                string = GoogleTranslator(source='auto', target=target_lang).translate(text=pass3)
            except deep_translator.exceptions.NotValidPayload:
                return string
        return string
    else:
        locale = GoogleTranslator(source='auto', target="ru").translate(text=string)
        try:
            encoded_text = locale.encode("utf-8").decode(charset)
        except UnicodeDecodeError:
            print("[ERROR] ({}) UnicodeDecodeError => Skipping encoding".format(key))
            encoded_text = locale
        except AttributeError:
            print("[ERROR] ({}) Failed to encode text (AttributeError) => Skipping translate".format(key))
            return string
        string = GoogleTranslator(source='auto', target=target_lang).translate(text=encoded_text)
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
    start_time = datetime.now()
    print("[INFO] Starting...")

    result = {}
    data = read_lang_file()
    print("[INFO] Started. The process can take a long time!")
    try:
        for key_name in data:
            value = data[key_name]
            result[key_name] = translate(key_name, value)
            print(
                '[INFO] Progress: {}% ({}/{}) ({})'.format((len(result) * 100) // len(data), len(result), len(data),
                                                           key_name))
    except KeyboardInterrupt:
        print("[INFO] Stopped by user!")
    ram_used = round(memory_usage()[0])

    print("[INFO] Saving to file...")
    create_json()
    result_file = open(file_name, 'w')
    json.dump(result, result_file, indent=4)
    result_file.close()

    print("[INFO] Finalizing...")
    finalize()
    print("[INFO] Done! ({}) (RAM - {}MB)".format(datetime.now() - start_time, ram_used))
