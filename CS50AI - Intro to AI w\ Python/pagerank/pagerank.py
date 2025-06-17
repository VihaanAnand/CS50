import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    pages = {}
    for i in corpus:
        pages[i] = 0
    pagesno = len(pages)
    links = list(corpus[page])
    linksno = len(links)
    for i in links:
        pages[i] = damping_factor / linksno
    for i in pages:
        pages[i] += (1 - damping_factor) / pagesno
    return pages


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    pages = {}
    for i in corpus:
        pages[i] = 0
    curpage = random.choice(list(pages.keys()))
    for i in range(n):
        pages[curpage] += 1
        probs = transition_model(corpus, curpage, damping_factor)
        pageslist = list(probs.keys())
        pagesprobs = list(probs.values())
        curpage = random.choices(pageslist, weights=pagesprobs, k=1)[0]
    visits = sum(pages.values())
    for i in pages:
        pages[i] /= visits
    return pages


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    pages = {}
    for i in corpus:
        pages[i] = 0
    pagesno = len(pages)
    for i in pages:
        pages[i] = 1 / pagesno
    for i in corpus:
        links = list(corpus[i])
        linksno = len(links)
        if linksno == 0:
            corpus[i] = set(pages.keys())
    while True:
        greatestchange = 0
        pagescopy = pages.copy()
        for i in pages:
            prp = (1 - damping_factor) / pagesno
            for j in pages:
                if i in corpus[j]:
                    links = list(corpus[j])
                    linksno = len(links)
                    prp += damping_factor * pagescopy[j] / linksno
            pages[i] = prp
        for i in pages:
            difference = pages[i] - pagescopy[i]
            difference = abs(difference)
            if difference > greatestchange:
                greatestchange = difference
        if greatestchange < 0.001:
            return pages


if __name__ == "__main__":
    main()
