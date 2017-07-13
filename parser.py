""" This file contains parser classes
"""

import re
import json

class ParserBase(object):
    """ Base parser class
    """
    TITLE_ONLY = 'title'
    AUTHOR_ONLY = 'author'
    CONTENT_ONLY = 'content'
    ALL = 'title,author,content'


    def __init__(self, documents, mode):
        self.documents = documents
        self.mode = mode


    def add_parsed_result(self, current_map):
        """ Extend current_map with parse results.
        """
        if not current_map:
            current_map = {}
        for doc in self.documents:
            with open(doc) as json_file:
                data = json.load(json_file)
                current_map.update(self.parse(data))
        return current_map


    def parse(self, data):
        """ Parse data, create all categories specified in mode.
        """
        categories = self.mode.split(',')
        result = {}
        for category in categories:
            result.update(self.get_word_to_category_dict(
                category, data[category]))
        return result


    @staticmethod
    def get_word_to_category_dict(category, words):
        """ Given a category and text belongs to the category,
            return a word to category dictionary
            for example {'fox': 'content', 'jump': 'content'}.
        """
        words = words.lower()
        word_list = re.split(r'\s+', words)
        word_to_category_dict = {key:category for key in word_list}
        return word_to_category_dict


    @staticmethod
    def dict_to_inverted_tuples(word_to_category_dict):
        """ Given a word to category dictionary,
            return a list of (category, word) tuples
        """
        return [(category, word) for (word, category) in word_to_category_dict]


    @staticmethod
    def dict_to_inverted_index(word_to_category_dict):
        """ Given a word to category dictionary,
            return a string of "category:word" separated by commas
        """
        inverted_index_list = []
        for (word, category) in word_to_category_dict.items():
            inverted_index_list.append("{}:{}".format(category, word))
        return ",".join(inverted_index_list)
      