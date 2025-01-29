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
import pprint

TWELVE_HOURS = list(range(1, 12))
TWOFOUR_HOURS = list(range(1, 25))
MINUTES = list(range(1, 61))
VERSION = "en-lsv"
APIKEY = apikey.APIBIBLEKEY
HEADERS = {"api-key": APIKEY}
DBCON = sqlite3.connect("./time_verse.db")
CURSOR = DBCON.cursor()
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
BIBLEID = "65eec8e0b60e656b-01"


def get_bibles():
    url = f"https://api.scripture.api.bible/v1/bibles/{BIBLEID}/books"  # /search?query=Jude 2:24"
    response = requests.get(url, headers=HEADERS)
    data = response.json()
    pprint.pp(data)


def test_call():
    url = (
        f"https://api.scripture.api.bible/v1/bibles/{BIBLEID}/search?query=Exodus 13:13"
    )
    response = requests.get(url, headers=HEADERS)
    pprint.pp(response.json())
    query = response.json()["data"]["passages"][0]["content"]
    parsed = query.split("/span>")[1][:-4]
    print(parsed)

    # pass_extract = re.split(r"\[\d{1,3}\]", str(passage[0]))
    # simplified = re.sub(r"(^\s|\s{2,}|\s\(ESV\)$)", "", pass_extract[1])
    # if "Footnotes" in simplified:
    #     new_list = re.sub(r"Footnotes.*$", "", simplified)
    #     new_list = new_list.replace("(1)", "")
    #     print(new_list)
    # else:
    #     new_list = simplified
    # simplified2 = re.sub(r"(\\n|,$)", " ", new_list)


# {"detail": "Request was throttled. Try again in 700 seconds."}


def iterate_over_books():
    count = 0
    for book in BIBLE_BOOKS:
        print(f"Searching for {book}")
        for hour in TWOFOUR_HOURS:
            for min in MINUTES:
                time.sleep(1)
                count += 1
                url = f"https://api.scripture.api.bible/v1/bibles/{BIBLEID}/search?query={book} {hour}:{min}"
                response = requests.get(url, headers=HEADERS)
                if response.status_code == 400:
                    print(
                        "Status Code 400 - End of Chapter. Moving onto the next one."
                    )
                    if count > 4500:
                        print(
                            f"Getting close to the end of the 5k daily limit. Cutting it off now, at the end of a book. Current location is {book} {hour}:{min}"
                    )
                        return
                    break
                print(f"Count: {count} and Passage: {book} {hour}:{min}")
                query = response.json()["data"]["passages"][0]["content"]
                simplified2 = query.split("/span>")[1][:-4]

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
                replace_apos = simplified2.replace("'", "’")
                print(replace_apos)

                CURSOR.execute(
                f"""
                    insert or replace into verses(book, chap_num, verse_num, verse_text)
                    values ('{book}','{hour}','{min}', '{replace_apos}')
                """)
                DBCON.commit()


if __name__ == "__main__":
    # get_bibles()
    test_call()
    # iterate_over_books()
