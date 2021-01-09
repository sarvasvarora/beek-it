from search_engine.search import SearchEngine

s = SearchEngine('test.xml')

s.crawl_and_index('www.ea.com')
print('CRAWLING DONE')
print(s)
print()
s.assign_page_ranks(0.01)
print('RANKS ASSIGNED')
print(s)
print()
print('GETTING RESULTS')
print(s.query('mcgill university  is one of the', phrase_query=True))


