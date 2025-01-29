"""
This is a one time script to pull all possible time stamped verses into a local db.
I am not sure if an ESP device would have the appropriate storage for the db, so this
branch is just for testing. As of writing this, the main file hasn't been updated to not
make API calls.
"""

import requests
import apikey
import re
import time
import sqlite3

TWELVE_HOURS = list(range(1, 12))
TWOFOUR_HOURS = list(range(1, 25))
MINUTES = list(range(1, 61))
VERSION = "en-lsv"
APIKEY = apikey.KEY
HEADERS = {"Authorization": APIKEY}
DBCON = sqlite3.connect('./time_verse.db')
CURSOR = DBCON.cursor()
BIBLE_BOOKS = [
    # "Genesis",
    # "Exodus",
    # "Leviticus",
    # "Numbers",
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
    "2 Peter",p
    "1 John",
    "2 John",
    "3 John",
    "Jude",
    "Revelation",
]

def test_call():
    url = "https://api.esv.org/v3/passage/text/?q=Exodus 9:29"
    response = requests.get(url, headers=HEADERS)
    print(response.text)
    query = response.json()["query"]
    passage = response.json()["passages"]
    verse = response.json()["query"]
    pass_extract = re.split(r"\[\d{1,3}\]", str(passage[0]))
    simplified = re.sub(r"(^\s|\s{2,}|\s\(ESV\)$)", "", pass_extract[1])
    if "Footnotes" in simplified:
        new_list = re.sub(r"Footnotes.*$", "", simplified)
        new_list = new_list.replace("(1)", "")
        print(new_list)
    else:
        new_list = simplified
    simplified2 = re.sub(r"(\\n|,$)", " ", new_list)


# {"detail": "Request was throttled. Try again in 700 seconds."}

def iterate_over_books():
    for book in BIBLE_BOOKS:
        print(f"Searching for {book}")
        for hour in TWOFOUR_HOURS:
            for min in MINUTES:
                time.sleep(1)
                while True:
                    url = f"https://api.esv.org/v3/passage/text/?q={book} {hour}:{min}"
                    response = requests.get(url, headers=HEADERS)
                    if response.status_code == 429:
                        time_to_wait = int(re.search(r'\d+', response.text).group())
                        seconds_to_wait = int(time_to_wait)+200
                        print("...ZzZzZz....")
                        print(f"Waiting {seconds_to_wait} seconds because of rate limiting.")
                        print("...ZzZzZz....")
                        time.sleep(seconds_to_wait)
                        continue
                    break
                query = response.json()["query"]
                if query != f"{book} {hour}:{min}":
                    break
                else:
                    print(f"{query} successfully found. Parsing and writing to file.")
                    passage = response.json()["passages"]
                    verse = response.json()["query"]
                    pass_extract = re.split(r"\[\d{1,3}\]", str(passage[0]))
                    simplified = re.sub(r"(^\s|\s{2,}|\s\(ESV\)$)", "", pass_extract[1])
                    if "Footnotes" in simplified:
                        new_list = re.sub(r"Footnotes.*$", "", simplified)
                        new_list = new_list.replace("(1)", "")
                    else:
                        new_list = simplified
                    simplified2 = re.sub(r"(,$)", ".", new_list)

                    double_close = simplified2.count("”")
                    double_open = simplified2.count("“")
                    single_open = simplified2.count("'")
                    single_open = simplified2.count("‘")
                    single_closed = simplified2.count("’")
                    char_tuple = (double_open, double_close, single_open, single_closed)
                    if char_tuple == (1, 0, 0, 0):
                        simplified2 += "”"
                    elif char_tuple == (1, 1, 1, 0):
                        simplified2 += "’"
                    elif char_tuple == (1, 0, 1, 0):
                        simplified2 += "”’"
                    print(simplified2)
                    CURSOR.execute(
                        f"insert into verses(book, chap_num, verse_num, verse_text) values ('{book}','{hour}','{min}', '{new_list}')"
                    )
                    DBCON.commit()


if __name__ == "__main__":
    iterate_over_books()
    # test_call()
