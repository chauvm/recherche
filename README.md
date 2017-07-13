"# recherche" 
    parser = ParserBase(['path_to_json'], ','.join([ParserBase.TITLE_ONLY, ParserBase.AUTHOR_ONLY]))
    current_map = parser.add_parsed_result({})
    inverted_index = ParserBase.dict_to_inverted_index(current_map)
    inverted_index
    'author:Arthur,title:HIS,author:Conan,title:LAST,title:BOW,author:Doyle'