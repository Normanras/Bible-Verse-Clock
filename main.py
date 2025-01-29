import time
import re
import random
import sched
import sqlite3
import datetime

DBCON = sqlite3.connect("./acv.db")
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


def get_time():
    gettime = datetime.datetime.now()
    time = gettime.strftime("%H:%M")
    return time


def choose_book():
    rand_book = random.choice(BIBLE_BOOKS)
    book_index = BIBLE_BOOKS.index(rand_book)
    return (book_index, rand_book)


def get_verse():
    curr_time = get_time()
    extract = ""
    verse = int(curr_time.split(":")[1])
    chap = int(curr_time.split(":")[0])
    data = []
    while not data:
        if chap > 12:
            hour = [chap, chap-12]
            chap = random.choice(hour)
        book_tuple = choose_book()
        # book_tuple = (5, 'Deuteronomy')
        book_index = book_tuple[0]+1
        book = book_tuple[1]
        data = CURSOR.execute(
            f"select text from acv_verses where book_id == {book_index} and chapter == {chap} and verse == {verse}"
        ).fetchall()
        if data:
            break
    DBCON.commit()
    verse_text = data[0][0]
    print(f"""
        Book: {book}
        Chapter: {chap}
        Verse: {verse}
        Text: {verse_text}
          """)


# if __name__ == "__main__":
    # get_verse()

my_scheduler = sched.scheduler(time.time, time.sleep)
my_scheduler.enter(60, 1, get_verse)
my_scheduler.run()
