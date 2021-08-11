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
import string
from typing import Dict, Any

# Libs
from bs4 import BeautifulSoup
import requests

# import pandas as pd # Or any other
# import string
# import re

# Own modules
# NONE

# dependent files
# stop word files list:
#     stop_words_files = ["stopWords.txt", "stopWordsExtended.txt", "stopWordsGoogle.txt", "stopWordsFrench.txt",
#                         "stopWordsMySQL.txt", "stopWordsFrench.txt", "stopWordsArabic.txt"]

__author__ = 'Jacob Ursenbach'
__creation_date__ = '20210721'
__copyright__ = 'Copyright NONE'
__credits__ = ['Jacob Ursenbach'
               'Leonard Richardson - Beautiful Soup library'
               'Apache2 - requests library']
__license__ = 'None'
__version__ = '1.0.0'
__maintainer__ = 'Jacob Ursenbach'
__email__ = 'jacob.ursenbach@gmail.com'
__status__ = 'in-process'


class WikiScraper:
    target_page = ""
    page_title = ""
    soup = None
    headers = []
    stop_word_file = ''
    stop_words = []
    default_stop_words = ['a', 'about', 'above', 'after', 'again', 'against', 'all', 'am', 'an', 'and', 'any', 'are',
                          "aren't", 'as', 'at', 'be', 'because', 'been', 'before', 'being', 'below', 'between', 'both',
                          'but', 'by', "can't", 'cannot', 'could', "couldn't", 'did', "didn't", 'do', 'does', "doesn't",
                          'doing', "don't", 'down', 'during', 'each', 'few', 'for', 'from', 'further', 'had', "hadn't",
                          'has', "hasn't", 'have', "haven't", 'having', 'he', "he'd", "he'll", "he's", 'her', 'here',
                          "here's", 'hers', 'herself', 'him', 'himself', 'his', 'how', "how's", 'i', "i'd", "i'll",
                          "i'm", "i've", 'if', 'in', 'into', 'is', "isn't", 'it', "it's", 'its', 'itself', "let's",
                          'me', 'more', 'most', "mustn't", 'my', 'myself', 'no', 'nor', 'not', 'of', 'off', 'on',
                          'once', 'only', 'or', 'other', 'ought', 'our', 'ours', 'ourselves', 'out', 'over',
                          'own', 'same', "shan't", 'she', "she'd", "she'll", "she's", 'should', "shouldn't",
                          'so', 'some', 'such', 'than', 'that', "that's", 'the', 'their', 'theirs', 'them',
                          'themselves', 'then', 'there', "there's", 'these', 'they', "they'd", "they'll",
                          "they're", "they've", 'this', 'those', 'through', 'to', 'too', 'under', 'until',
                          'up', 'very', 'was', "wasn't", 'we', "we'd", "we'll", "we're", "we've", 'were',
                          "weren't", 'what', "what's", 'when', "when's", 'where', "where's", 'which',
                          'while', 'who', "who's", 'whom', 'why', "why's", 'with', "won't", 'would',
                          "wouldn't", 'you', "you'd", "you'll", "you're", "you've", 'your', 'yours',
                          'yourself', 'yourselves']
    list_of_single_letters = list(string.ascii_lowercase)

    def __init__(self, webpage: str, stop_word_file_input='stopWords.txt'):
        """
        Initializes scraper class. Scrapes page, creates a list of all headers, sets stop words
        :param webpage: A valid Wikipedia webpage
        :param stop_word_file_input: Optional: choose a text file containing stopwords.
        If none is chosen, generic stopwords will be used.
        """
        self.scrape_page(webpage)
        self.set_headers()
        self.set_page_title()
        self.set_stop_word_file(stop_word_file_input)
        self.set_stop_words(self.stop_word_file)

    def scrape_page(self, webpage: str) -> None:
        """
        Attempts to pull a page request from provided URL. Throws generic exceptions for obvious errors.
        :param webpage: A valid Wikipedia URL
        :return: None
        """
        try:
            page_request = requests.get(webpage)
            page_source = page_request.text
            self.soup = BeautifulSoup(page_source, 'html.parser')
        except requests.HTTPError:
            print("Unable to ")
        except requests.ConnectionError:
            print("Connection Error. Check network connectivity")
        except requests.Timeout:
            print("Server timeout, try a different URL")
        except requests.exceptions.MissingSchema:
            print("Invalid URL")

    def set_headers(self) -> None:
        """
        uses grab_headers to pull all page headers and place them in headers variable
        :return: None
        """
        self.headers = self.grab_headers(self.soup)

    def set_page_title(self):
        """
        Sets page_title variable to the title of scraped page
        :return:
        """
        self.page_title = self.soup.title.text

    def set_stop_word_file(self, file_name: str) -> None:
        """
        Sets the file that the stop_words list pulls from
        :param file_name: .txt file of a list of stopwords. A few have been provided.
        :return: None
        """
        self.stop_word_file = file_name

    def set_stop_words(self, stop_word_file='stopWords.txt'):
        """
        Pulls from inputs stop_words list. If non is input, uses generic file.
        If no file is available, warns user and uses default stop_words list
        :param stop_word_file: a valid .txt
        :return:
        """
        try:
            f = open(stop_word_file, "r")
            self.stop_words = f.read().split()
        except IOError:
            print(f"Error opening {stop_word_file}: used default list")
            self.stop_words = self.default_stop_words

    @staticmethod
    def grab_headers(soup_object) -> list:
        """
        iterates through soup object and pulls all header objects into a list of headers
        :param soup_object: BeautifulSoup object
        :return: a list of all headers (raw)
        """

        all_headers = []
        for header_object in soup_object.find_all([f'h{i}' for i in range(1, 9)]):
            if header_object.text == "Navigation menu":
                break
            else:
                all_headers.append(header_object)

        return all_headers

    @staticmethod
    def pull_word_list(header_input) -> list:
        """
        Pulls all strings from wikipedia headers. Does not separate words. Must tokenize_paragraph for separate words
        :param header_input: a header from a wikipedia website
        :return: a list holding all strings under the header paragraph
        """
        text_table = []

        for sib in header_input.find_next_siblings():
            if any(sib.name == word for word in [f'h{i}' for i in range(1, 9)]):
                break
            else:
                text_table.append(sib.text)

        return text_table

    @staticmethod
    def tokenize_paragraph(string_list: list) -> list:
        """
        Takes a list of strings, and separates every word int individual tokens.
        After using this, run the results through clean_word_list
        :param string_list: a list of raw strings from website
        :return: an unedited list of individual words
        """
        word_list = []
        for item in string_list:
            word_list.append(item.split())

        return word_list

    def clean_word_list(self, word_list) -> list:
        """
        Scrubs a tokenized word list. Removes all punctuation, makes the entire list lower case.
        Checks list for stop words and removes them.
        :param word_list: a tokenized list of words
        :return: same list of words with capitalization, stop words, and punctuation removed
        """
        translated = ""
        cleaned = []
        for sublist in word_list:
            for item in sublist:
                for char in item:
                    if char.isalpha():
                        translated += char.lower()
                if translated not in self.stop_words:
                    cleaned.append(translated)
                translated = ''

        return cleaned

    def word_counter(self, word_list: list) -> dict:
        """
        Iterates through a list of words, counting them and putting them in a dict paired with num of reps
        case sensitive. List should be tokenized and cleaned before using word_counter
        :param word_list: a tokenized, cleaned list of words
        :return: dict holding pairs of unique words with their counts
        """
        word_count = {'': 0}

        for word in word_list:
            if word in self.stop_words:
                pass
            elif word in word_count:
                word_count[word] += 1
            else:
                word_count[word] = 1

        word_count.pop('')

        return word_count

    @staticmethod
    def sort_word_dict(words: dict) -> dict:
        """
        Takes a dictionary of counted words, and sorts them from most frequent to least frequent
        :param words: dictionary of counted words
        :return: a sorted dictionary of words (most to least frequent)
        """
        sorted_list = sorted(words.items(), key=lambda x: x[1], reverse=True)
        sorted_dict: Dict[Any, Any] = {}

        for item in sorted_list:
            name, number = item
            sorted_dict.update({name: number})

        return sorted_dict

    def print_dict(self, dict_input: dict) -> None:
        """
        Calls print_partial_dict without providing a print number value.
        This automatically prints the entire dictionary.
        :param dict_input: dictionary to be printed
        :return: None
        """
        self.print_partial_dict(dict_input)

    def print_partial_dict(self, sorted_dict: dict, print_number: int = None) -> None:
        """
        Iterates through and prints a dictionary, a new line for each item.
        If a number is provided in print_number, will only print the first few dict objects,
        depending on the number provided.
        :param sorted_dict: a sorted dicitonary
        :param print_number: provides a limiter, to only print the first few objects
        :return: None
        """
        # creates a list of the items to be printed. print_number limits amount printed
        print_list = list(sorted_dict.items())[:print_number]

        # prints: ex: apple - 1
        for item in print_list:
            print(f"{item[0]} - {item[1]}")

    @staticmethod
    def parse_hyperlinks(link) -> dict:
        """
        Takes a hyperlink and returns a dict object containing the hyperlink name and text
        If a hyperlink has no text, has a count for "unnamed links"
        :param link: a hyperlink for parsing
        :return: a dict {link_text: hyperlink}
        """
        unnamed_link_count = 0
        hyperlink = ''

        if link.get('href') is not None:
            if 'https://' in link.get('href'):
                hyperlink = link.get('href')
            else:
                hyperlink = ('https://en.wikipedia.org' + link.get('href'))
        if link.get_text() == '':
            unnamed_link_count += 1
            link_name = f'unnamed_link_{unnamed_link_count}'
        else:
            link_name = link.get_text()

        return {link_name: hyperlink}

    def pull_paragraph_hyperlinks(self, header_object) -> dict:
        """
        Takes a header object and creates a dict, containing all links that appear before the next header object
        uses parse_hyperlinks to create a dict object for each link
        Breaks once another header is found
        :param header_object: a wikipedia html header
        :return: a dict containing all hyperlinks, and their accompanying text ex: {Google: www.google.com}
        """
        # unfinished: grab all hyperlinks in section
        # puts all hyperlinks in dictionary with hyperlink text as key

        hyperlinks = {}
        for link in header_object.find_all_next([f'h{i}' for i in range(1, 9)] + ['a']):
            if any(link.name == word for word in [f'h{i}' for i in range(1, 9)]):
                break
            else:
                hyperlinks.update(self.parse_hyperlinks(link))

        return hyperlinks

    def create_word_list(self, header_object) -> dict:
        """
        Calls all helper functions to parse a paragraph into an ordered counted dictionary of words
        Removes capitalization, punctuation, and stop words
        :param header_object: a header object to specify the section to be parsed
        :return: a dictionary with ordered counted words
        """
        basic_text = self.pull_word_list(header_object)
        text_intermediate = self.tokenize_paragraph(basic_text)
        text = self.clean_word_list(text_intermediate)
        word_dictionary = self.sort_word_dict(self.word_counter(text))
        return word_dictionary

    def print_all(self, num_words_to_print=None, num_links_to_print=None) -> None:
        """
        iterates through every header on a wikipedia page.
        Prints words in order from most frequent to least
        Prints all hyperlinks
        Number of words and hyperlinks can be separately controlled through optional parameters
        :param num_words_to_print: how many words should be printed in each section. If no input, prints them all
        :param num_links_to_print: how many links should be printed in each section. If no input prints them all
        :return:
        """
        for header in self.headers:
            print(f"--------{header.text}")

            word_list = self.create_word_list(header)
            link_table = self.pull_paragraph_hyperlinks(header)

            self.print_partial_dict(word_list, num_words_to_print)
            self.print_partial_dict(link_table, num_links_to_print)

            print("\n")

    def create_full_page_dict(self) -> dict:
        """
        Creates a dictionary containing all headers, counted words and links for each header.
        Can be used to export data into CSV or to do data visualization
        :return: a dict containing data from entire wikipedia page
        """
        page_dict = {"page_name": self.page_title,
                     "page_hyperlink": self.target_page}

        for header in self.headers:

            basic_text = self.pull_word_list(header)
            link_table = self.pull_paragraph_hyperlinks(header)
            text_intermediate = self.tokenize_paragraph(basic_text)
            text = self.clean_word_list(text_intermediate)

            page_dict.update({header.text: ({"words": self.sort_word_dict(self.word_counter(text))},
                                            {"hyperlinks": link_table})})

        return page_dict


if __name__ == '__main__':

    target_page = "https://en.wikipedia.org/wiki/Cat"
    scraper = WikiScraper(target_page)

    print(scraper.page_title)
    scraper.print_all(10)
