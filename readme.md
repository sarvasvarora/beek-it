# beek-it
Beek it is a very basic search engine that builds upon the graph data structure. It uses depth-first traversal to crawl and index the webpages, which are stored in an XML format DB and serve as a proxy for actual webpages for this project. 

For querying, I implemented standard keyword search as well as exact-phrase search (ignores punctuation). The query method returns the relevant webpages in descending order of their page ranks.

I wrote a blog post which goes in depth of fundamentals of how search engines work, and also explains this project in more detail. The post can be accessed [here](https://sarvasvarora.me/article/The-hitchhiker's-guide-to-search-engines/)
<hr>

The name of this search engine is a portmanteau of "seek" — which has the obvious meaning to search for something, exactly what a search engine does – and "bee" – which is due to the fact that this search engine is inspired by the final project of COMP 250 course and our first assignment was to create a bee vs hornet tower defence game!

