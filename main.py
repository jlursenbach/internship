# author: Jacob Ursenbach
# date: 20210725
# project: Wikipedia Scraper for internship

# !interpreter [Python 3.8]
# -*- coding: utf-8 -*-

"""
This wikipedia scraper was created for an internship interview.
The prompt was followed:

We will ask for a link to a Python script written by you that takes in a Wikipedia link and for each section,
prints out the title of the section, prints out the most frequent words in the section that are
not considered “stop words”, and lists every hyperlink in the section.
Here we are looking to get a better sense of your programming abilities to see where you would best fit in the project.

The scraper takes a wikipedia page, and uses the headers as delimiters for the task.
First the page HTML is pulled
Headers are than pulled into a list
Headers are iterated through.
All hyperlinks are pulled into a dictionary.
Similarly, all words are pulled out of the paragraphs following each header.
The words are tokenized, cleaned (remove capitalization, punctuation, and stop words), and counted
than the section header names are printed out, with words and hyperlinks following them.

At default only the top 10 words are printed per section header, and all hyperlinks are printed.
You can change these numbers in the
if __name__ == '__main__':
scraper.print_all(#,#)

as of right now, the user interface in main is simple as can be.
You are prompted to input a valid wikipedia URL, and after a valid input, the output is automatic.

I've provided a default list of stop_words in case git_hub is unable to access the .txt files I've provided
however you should be able to specify a file.

{License_info}
personal project for internship, no licenses
"""

# Futures
# NONE

# Built-in/Generic Imports
# NONE

# Libs
# NONE

# Own modules
import scraper_code

# dependent files
# stop word files list:
#     stop_words_files = ["stopWords.txt", "stopWordsExtended.txt", "stopWordsGoogle.txt", "stopWordsFrench.txt",
#                         "stopWordsMySQL.txt", "stopWordsFrench.txt", "stopWordsArabic.txt"]


if __name__ == '__main__':

    program_is_running = True

    # urls for testing (easy copy/paste)
    url_1 = "https://en.wikipedia.org/wiki/Cat"
    url_2 = "https://en.wikipedia.org/wiki/United_States"
    url_3 = "https://en.wikipedia.org/wiki/Running"

    while program_is_running:

        target_page = input("Please provide a valid Wikipedia page url: ")

        wiki_page = scraper_code.WikiScraper(target_page, "stopWordsExtended.txt")

        print(f"{wiki_page.page_title}\n")
        # only words have been limited due to prompt asking for all hyperlinks
        wiki_page.print_all(10)

        user_continue = input("do you want to provide another URL? (Y/N): ")
        if user_continue.lower() != 'y':
            program_is_running = False

    print("Goodbye")
