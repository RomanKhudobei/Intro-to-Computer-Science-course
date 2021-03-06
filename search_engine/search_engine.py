import re

# Example input
cache = {
   'http://udacity.com/cs101x/urank/index.html': 
"""
<html>
<body>
<h1>Dave's Cooking Algorithms</h1>
<p>
Here are my favorite recipies:
<ul>
<li> <a href="http://udacity.com/cs101x/urank/hummus.html">Hummus Recipe</a>
<li> <a href="http://udacity.com/cs101x/urank/arsenic.html">World's Best Hummus</a>
<li> <a href="http://udacity.com/cs101x/urank/kathleen.html">Kathleen's Hummus Recipe</a>
</ul>
For more expert opinions, check out the 
<a href="http://udacity.com/cs101x/urank/nickel.html">Nickel Chef</a> 
and <a href="http://udacity.com/cs101x/urank/zinc.html">Zinc Chef</a>.
</body>
</html>
""",

   'http://udacity.com/cs101x/urank/zinc.html': 
"""
<html>
<body>
<h1>The Zinc Chef</h1>
<p>
I learned everything I know from 
<a href="http://udacity.com/cs101x/urank/nickel.html">the Nickel Chef</a>.
</p>
<p>
For great hummus, try 
<a href="http://udacity.com/cs101x/urank/arsenic.html">this recipe</a>.
</body>
</html>
""", 
   
    'http://udacity.com/cs101x/urank/nickel.html': 
"""
<html>
<body>
<h1>The Nickel Chef</h1>
<p>
This is the
<a href="http://udacity.com/cs101x/urank/kathleen.html">
best Hummus recipe!
</a>
</body>
</html>
""",

   'http://udacity.com/cs101x/urank/kathleen.html': 
"""
<html>
<body>
<h1>
Kathleen's Hummus Recipe
</h1>
<p>
<ol>
<li> Open a can of garbonzo beans.
<li> Crush them in a blender.
<li> Add 3 tablesppons of tahini sauce.
<li> Squeeze in one lemon.
<li> Add salt, pepper, and buttercream frosting to taste.
</ol>
</body>
</html>
""",

   'http://udacity.com/cs101x/urank/arsenic.html': 
"""
<html>
<body>
<h1>
The Arsenic Chef's World Famous Hummus Recipe
</h1>
<p>
<ol>
<li> Kidnap the <a href="http://udacity.com/cs101x/urank/nickel.html">Nickel Chef</a>.
<li> Force her to make hummus for you.
</ol>
</body>
</html>
""",

   'http://udacity.com/cs101x/urank/hummus.html': 
"""
<html>
<body>
<h1>
Hummus Recipe
</h1>
<p>
<ol>
<li> Go to the store and buy a container of hummus.
<li> Open it.
</ol>
</body>
</html>
""" 
}

"""
cache - example input
index - dictionary type {'keyword': ['urls' where it appears]} and needed for respond search requests
graph - dictionary type {'url': [list of pages it links to]} and needed for calculate rank for each url
ranks - dictionary type {'url': rate} needed for prioritize pages on respond request

About reciprocal links:
Pages can collaborate with each other to improve their page ranks.
The link A->B is reciprocal (where A and B are urls) when there is a path (through links) from B to A (B->A)
the lenght of which equal to or below the "collusion" level, k. In other words, k is number of "how far you want to search".
"""

def is_reciprocal(page, node, graph, k):    # k - is a number of 'how far you want to search'
    '''Returns boolean type, depended on whether link is reciprocal.'''
    if page == node:
        return True
    if k > 0:
        if node in graph[page]:
            return True
        if k > 1:
            i = 1   # to keep track of how 'far' we are searching
            to_check = [] + graph[page]
            next_level = []
            while to_check and i < k:
                url = to_check.pop()
                if node in graph[url]:
                    return True
                next_level = next_level + graph[url]
                if not to_check:
                    if i < k:
                        to_check, next_level = next_level, []
                        i = i + 1
        else:
            return False
    else:
        return False

def compute_ranks(graph, k):
    '''Takes as input graph and returns ranks dictionary.'''
    d = 0.8     # damping factor (probability that user might leave a page)
    numloops = 10   # for more accurate value of rating
    ranks = {}
    npages = len(graph)
    for page in graph:
        ranks[page] = 1.0 / npages
    for i in range(0, numloops):
        newranks = {}
        for page in graph:
            newrank = ((1 - d) / npages)    # default rate for each page
            for node in graph:
                if page in graph[node]:
                    if is_reciprocal(page, node, graph, k):     # if link is reciprocal, then don't include it to compute page rate
                        continue
                    else:
                        newrank = newrank + d * (ranks[node]/len(graph[node]))
            newranks[page] = newrank
        ranks = newranks
    return ranks

def crawl_web(seed): # returns index, graph of inlinks
    '''Web crawler. Takes as input string of html-page and returns index, graph.'''
    tocrawl = [seed]
    crawled = []
    graph = {}  # 'url': [list of pages it links to]
    index = {}  # 'keyword': ['urls' where keyword appears]
    while tocrawl: 
        page = tocrawl.pop()
        if page not in crawled:
            content = get_page(page)
            add_page_to_index(index, page, content)
            outlinks = get_all_links(content)
            graph[page] = outlinks
            union(tocrawl, outlinks)
            crawled.append(page)
    return index, graph

def get_page(url):
    '''Returns html-page string from example input.'''
    if url in cache:
        return cache[url]
    else:
        return None
    
def get_next_target(page):
    '''Finds and returns next url from previous.'''
    start_link = page.find('<a href=')
    if start_link == -1: 
        return None, 0
    start_quote = page.find('"', start_link)
    end_quote = page.find('"', start_quote + 1)
    url = page[start_quote + 1:end_quote]
    return url, end_quote

def get_all_links(page):
    '''Returns list of all links in given page.'''
    links = []
    while True:
        url, endpos = get_next_target(page)
        if url:
            links.append(url)
            page = page[endpos:]
        else:
            break
    return links

def union(a, b):
    '''Append all elements of b to a, if they don't exist already.'''
    for e in b:
        if e not in a:
            a.append(e)

def formatize_word(word):
    '''Formats given word. Extract simple lowercase word from bunch of different characters.'''
    formatted_word = word.lower()
    formatted_word = re.sub('<.*?>', '', formatted_word)    # strip html-tags
    formatted_word = re.sub('.*?>', '', formatted_word)     # strip incomplete html-tags
    formatted_word = formatted_word.strip(r'\,.!:;"?*&%$#@()<>/')   # strip listed not necessary characters
    return formatted_word

def add_page_to_index(index, url, content):
    '''Adds all words from content (text from page) to index.'''
    words = content.split()
    for i in range(0, len(words)):
        words[i] = formatize_word(words[i])
        keyword = words[i]
        if keyword in index and keyword != '':    # because if keyword == '', then it was a html-tag
            index[keyword].append(url)
        else:
            if keyword != '':      # to avoid any empty strings ('') in index
                index[keyword] = [url]

def ordered_search(index, ranks, keyword):
    '''Search request. Returns list of urls, sorted by rate, for given keyword.'''
    tosort_list = index.get(keyword, [])
    return sorted(tosort_list, key=lambda url: ranks[url], reverse=True)    # sort by rate of page (from high to low)


index, graph = crawl_web('http://udacity.com/cs101x/urank/index.html')
ranks = compute_ranks(graph, 3)
