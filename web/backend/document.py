""" This file contains document class
"""

import json

class Document(object):
    """ Represents a document
    """

    def __init__(self, document_id, path, tags):
        """ document_id: unique ID of a document
            path: file path to read the document data file
            tags: a list of topics of length at least 1
        """
        self.document_id = document_id
        self.path = path
        self.tags = tags
        self.data = self.get_data()


    def get_data(self):
        """ Implemented by subclass
        """
        raise NotImplementedError


    def has_topic(self, topic):
        """ Given a topic, return True if topic is in document tags
        """
        return topic.lower() in self.tags


class JSONDocument(Document):
    """ A document whose content is created from a json file
    """

    def __init__(self, document_id, path, tags):
        super(JSONDocument, self).__init__(document_id, path, tags)


    def get_data(self):
        data = {}
        with open(self.path) as json_file:
            data = json.load(json_file)
        return data


