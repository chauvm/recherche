""" This file contains parser classes
"""

import re

class ParserBase(object):
    """ Base parser class
    """
    # parse modes
    TITLE_ONLY = 'title'
    AUTHOR_ONLY = 'author'
    CONTENT_ONLY = 'content'
    ALL = 'title,author,content'

    # list of stop words
    STOP_WORDS = ["a", "about", "above", "above", "across", "after", "afterwards", "again", "against", "all", "almost", "alone", "along", "already", "also","although","always","am","among", "amongst", "amoungst", "amount",  "an", "and", "another", "any","anyhow","anyone","anything","anyway", "anywhere", "are", "around", "as",  "at", "back","be","became", "because","become","becomes", "becoming", "been", "before", "beforehand", "behind", "being", "below", "beside", "besides", "between", "beyond", "bill", "both", "bottom","but", "by", "call", "can", "cannot", "cant", "co", "con", "could", "couldnt", "cry", "de", "describe", "detail", "do", "done", "down", "due", "during", "each", "eg", "eight", "either", "eleven","else", "elsewhere", "empty", "enough", "etc", "even", "ever", "every", "everyone", "everything", "everywhere", "except", "few", "fifteen", "fify", "fill", "find", "fire", "first", "five", "for", "former", "formerly", "forty", "found", "four", "from", "front", "full", "further", "get", "give", "go", "had", "has", "hasnt", "have", "he", "hence", "her", "here", "hereafter", "hereby", "herein", "hereupon", "hers", "herself", "him", "himself", "his", "how", "however", "hundred", "ie", "if", "in", "inc", "indeed", "interest", "into", "is", "it", "its", "itself", "keep", "last", "latter", "latterly", "least", "less", "ltd", "made", "many", "may", "me", "meanwhile", "might", "mill", "mine", "more", "moreover", "most", "mostly", "move", "much", "must", "my", "myself", "name", "namely", "neither", "never", "nevertheless", "next", "nine", "no", "nobody", "none", "noone", "nor", "not", "nothing", "now", "nowhere", "of", "off", "often", "on", "once", "one", "only", "onto", "or", "other", "others", "otherwise", "our", "ours", "ourselves", "out", "over", "own","part", "per", "perhaps", "please", "put", "rather", "re", "same", "see", "seem", "seemed", "seeming", "seems", "serious", "several", "she", "should", "show", "side", "since", "sincere", "six", "sixty", "so", "some", "somehow", "someone", "something", "sometime", "sometimes", "somewhere", "still", "such", "system", "take", "ten", "than", "that", "the", "their", "them", "themselves", "then", "thence", "there", "thereafter", "thereby", "therefore", "therein", "thereupon", "these", "they", "thickv", "thin", "third", "this", "those", "though", "three", "through", "throughout", "thru", "thus", "to", "together", "too", "top", "toward", "towards", "twelve", "twenty", "two", "un", "under", "until", "up", "upon", "us", "very", "via", "was", "we", "well", "were", "what", "whatever", "when", "whence", "whenever", "where", "whereafter", "whereas", "whereby", "wherein", "whereupon", "wherever", "whether", "which", "while", "whither", "who", "whoever", "whole", "whom", "whose", "why", "will", "with", "within", "without", "would", "yet", "you", "your", "yours", "yourself", "yourselves", "the"]

    def __init__(self, documents, mode):
        self.documents = documents
        self.mode = mode


    @staticmethod
    def is_stop_word(word):
        """ Given a word, return True if it is in STOP_WORDS list
        """
        return word in ParserBase.STOP_WORDS


    def add_parsed_result(self, current_map):
        """ Extend current_map with parse results.
        """
        if not current_map:
            current_map = {}
        for doc in self.documents:
            #with open(doc) as json_file:
            #    data = json.load(json_file)
            #    current_map.update(self.parse_categories(data))
            current_map.update(self.parse_categories(doc.data))
        return current_map


    def parse_categories(self, data):
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



    def add_parsed_word_count_result(self, current_map):
        """ Extend current_map with parse results.
        """
        if not current_map:
            current_map = {}
        for doc in self.documents:
            #with open(doc) as json_file:
            #    data = json.load(json_file)
            #    current_map.update(self.get_word_to_count_dict(data['content']))
            current_map.update(self.get_word_to_count_dict(doc.data['content']))
        return current_map


    @staticmethod
    def get_word_to_count_dict(words, skip_stop_words=True):
        """ Given the text return a word to count dictionary,
            skip stop words such as "a", "the" unless specify otherwise
            for example {'fox': 2, 'jump': 1}.
        """
        words = words.lower()
        word_list = re.split(r'\s+', words)
        word_to_count_dict = {}
        for word in word_list:
            if not skip_stop_words or not ParserBase.is_stop_word(word):
                word_to_count_dict[word] = word_to_count_dict.get(word, 0) + 1
        return word_to_count_dict


if __name__ == "__main__":
    import document
    document = document.JSONDocument(1, 'D:\search\data\sherlock\lstb.json', ['literature', 'thriller', 'detective'])
    parser = ParserBase([document], ','.join([
        ParserBase.TITLE_ONLY, ParserBase.AUTHOR_ONLY]))
    word_to_count = parser.add_parsed_word_count_result({})
    print(word_to_count)