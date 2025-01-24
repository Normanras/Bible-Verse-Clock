import requests
from Levenshtein import distance as lev
import time
import re
import random
import timeit
from timeout import timeout
import datetime

VERSION = "en-lsv"
APIKEY = "Token f562cf2d890151d682065696dacdc0f86938a18e"
HEADERS = {"Authorization": APIKEY}
BIBLE_BOOKS = [
    "Genesis",
    "Exodus",
    "Leviticus",
    "Numbers",
    "Deuteronomy",
    "Joshua",
    "Judges",
    "Ruth",
    "1 Samuel",
    "2 Samuel",
    "1 Kings",
    "2 Kings",
    "1 Chronicles",
    "2 Chronicles",
    "Ezra",
    "Nehemiah",
    "Esther",
    "Job",
    "Psalm",
    "Proverbs",
    "Ecclesiastes",
    "Song of Solomon",
    "Isaiah",
    "Jeremiah",
    "Lamentations",
    "Ezekiel",
    "Daniel",
    "Hosea",
    "Joel",
    "Amos",
    "Obadiah",
    "Jonah",
    "Micah",
    "Nahum",
    "Habakkuk",
    "Zephaniah",
    "Haggai",
    "Zechariah",
    "Malachi",
    "Matthew",
    "Mark",
    "Luke",
    "John",
    "Acts",
    "Romans",
    "1 Corinthians",
    "2 Corinthians",
    "Galatians",
    "Ephesians",
    "Philippians",
    "Colossians",
    "1 Thessalonians",
    "2 Thessalonians",
    "1 Timothy",
    "2 Timothy",
    "Titus",
    "Philemon",
    "Hebrews",
    "James",
    "1 Peter",
    "2 Peter",
    "1 John",
    "2 John",
    "3 John",
    "Jude",
    "Revelation",
]


def get_time():
    gettime = datetime.datetime.now()
    time = gettime.strftime("%H:%M")
    return time


def choose_book():
    rand_book = random.choice(BIBLE_BOOKS)
    return rand_book


# @timeout(15)
def get_verse():
    curr_time = get_time()
    extract = ""
    distance = lev(extract, curr_time)
    while True:
        book = choose_book()
        time.sleep(2)
        url = f"https://api.esv.org/v3/passage/text/?q={book} {curr_time}"
        response = requests.get(url, headers=HEADERS)
        query = response.json()["query"]
        print(query)
        chap_verse = re.search(r"(\d{1,3}:\d{1,3})", query)
        try:
            extract = chap_verse.group(0)
        except AttributeError as a:
            print(a)

        distance = lev(extract, curr_time)
        if "0" in curr_time and not curr_time.endswith("0"):
            curr_time = curr_time.replace("0", "")
            print(curr_time)

        if distance < 1:
            print(f"{extract} is equal to {curr_time}!")
            break
    return response


def parse_verse():
    response = get_verse()
    passage = response.json()["passages"]
    verse = response.json()["query"]
    pass_extract = re.split(r"\[\d{1,3}\]", str(passage[0]))
    simplified = re.sub(r"(^\s|\s{2,}|\s\(ESV\)$)", "", pass_extract[1])
    simplified2 = re.sub(r"(\\n|,[a-zA-Z])", " ", simplified)
    if "(1)Footnotes" in simplified2:
        new_list = simplified2.split("(1)Footnotes")[0]
        print(new_list)
    else:
        new_list = simplified2

    double_close = new_list.count('”')
    double_open = new_list.count('“')
    single_open = new_list.count("'")
    single_open = new_list.count("‘")
    single_closed = new_list.count('’')
    char_tuple = (double_open, double_close, single_open, single_closed)
    if char_tuple == (1, 0, 0, 0):
        new_list += '”'
    elif char_tuple == (1, 1, 1, 0):
        new_list += '’'
    elif char_tuple == (1, 0, 1, 0):
        new_list += '”’'
    print(new_list)
    print(verse)


if __name__ == "__main__":
    parse_verse()
