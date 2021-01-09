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
print(s.get_results('a'))

