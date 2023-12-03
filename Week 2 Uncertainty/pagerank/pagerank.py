import collections
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

    # {'4.html': {'2.html'}, '3.html': {'2.html', '4.html'}, '2.html': {'1.html', '3.html'}, '1.html': {'2.html'}}
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
    # The corpus is a Python dictionary mapping a page name to a set of all pages linked to by that page.
    # The page is a string representing which page the random surfer is currently on.
    # The damping_factor is a floating point number representing the damping factor to be used when generating the probabilities.

    # The return value of the function should be a Python dictionary with one key for each page in the corpus.
    # Each key should be mapped to a value representing the probability that a random surfer would choose that page next.
    # The values in this returned probability distribution should sum to 1.
    # With probability damping_factor, the random surfer should randomly choose one of the links from page with equal probability.
    # With probability 1 - damping_factor, the random surfer should randomly choose one of all pages in the corpus with equal probability.

    # For example, if the corpus were {"1.html": {"2.html", "3.html"}, "2.html": {"3.html"}, "3.html": {"2.html"}}, the page was "1.html",
    # and the damping_factor was 0.85, then the output of transition_model should be {"1.html": 0.05, "2.html": 0.475, "3.html": 0.475}.
    # This is because with probability 0.85,
    # we choose randomly to go from page 1 to either page 2 or page 3 (so each of page 2 or page 3 has probability 0.425 to start),
    # but every page gets an additional 0.05 because with probability 0.15 we choose randomly among all three of the pages.

    linked_pages_in_page = corpus[page]
    number_linked_pages_in_page = len(linked_pages_in_page)

    probability_distribution = {}

    if not number_linked_pages_in_page:
        pages_in_corpus = list(corpus.keys())
        for page in pages_in_corpus:
            probability_distribution[page] = 1 / len(pages_in_corpus)
        return probability_distribution

    average_random_damping_factor = round((1 - damping_factor) / (number_linked_pages_in_page + 1), 3)
    probability_distribution[page] = average_random_damping_factor
    for linked_page in linked_pages_in_page:
        probability_distribution[linked_page] = round((damping_factor / number_linked_pages_in_page)
                                                      + average_random_damping_factor, 3)

    return probability_distribution


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    # The function accepts three arguments: corpus, a damping_factor, and n.
    # The corpus is a Python dictionary mapping a page name to a set of all pages linked to by that page.
    # The damping_factor is a floating point number representing the damping factor to be used by the transition model.
    # n is an integer representing the number of samples that should be generated to estimate PageRank values.

    # The return value of the function should be a Python dictionary with one key for each page in the corpus. Each key should be mapped to a value representing that page’s estimated PageRank (i.e., the proportion of all the samples that corresponded to that page). The values in this dictionary should sum to 1.
    # The first sample should be generated by choosing from a page at random.
    # For each of the remaining samples, the next sample should be generated from the previous sample based on the previous sample’s transition model.
    # You will likely want to pass the previous sample into your transition_model function, along with the corpus and the damping_factor, to get the probabilities for the next sample.
    # For example, if the transition probabilities are {"1.html": 0.05, "2.html": 0.475, "3.html": 0.475}, then 5% of the time the next sample generated should be "1.html", 47.5% of the time the next sample generated should be "2.html", and 47.5% of the time the next sample generated should be "3.html".
    # You may assume that n will be at least 1.

    page = random.choice(list(corpus.keys()))
    page_rank = collections.defaultdict(int)
    for i in range(n):
        probability_distribution = transition_model(corpus, page, damping_factor)
        # Choose a random element from the list with the specified probabilities
        new_page = random.choices(list(probability_distribution.keys()),
                                  weights=list(probability_distribution.values()), k=1)
        page_rank[new_page[0]] += 1 / n
        page = new_page[0]

    return page_rank


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    # start by assuming the PageRank of every page is 1 / N

    page_rank = collections.defaultdict(int)
    # start by assuming the PageRank of every page is 1 / N
    init_page_rank_value = 1 / len(corpus)
    reach_min_changes_value = False

    for page in list(corpus.keys()):
        page_rank[page] = init_page_rank_value

    while not reach_min_changes_value:
        # new PageRank values for each page, based on the previous PageRank values.
        # {'4.html': {'2.html'}, '3.html': {'2.html', '4.html'}, '2.html': {'1.html', '3.html'}, '1.html': {'2.html'}}
        current_page_rank = page_rank.copy()
        for page in list(corpus.keys()):
            # PageRank formula
            # 1 - d divided by N, where N is the total number of pages across the entire corpus.
            new_page_rank_value = (1 - damping_factor) / len(corpus)
            for i in list(corpus.keys()):
                # consider each possible page i that links to page p
                if page in corpus[i]:
                    # PR(i), representing the probability that we are on page i at any given time.
                    # NumLinks(i) be the number of links on page i
                    new_page_rank_value += damping_factor * (page_rank[i] / len(corpus[i]))
                elif len(corpus[i]) == 0:
                    new_page_rank_value += damping_factor * (page_rank[i] / len(corpus))
                # A page that has no links at all should be interpreted as having one link for every page in the corpus (including itself).
            current_page_rank[page] = round(new_page_rank_value, 5)

        # Repeat until no PageRank value changes by more than 0.001 between the current rank values and the new rank values.
        diff_list = []
        for page in list(corpus.keys()):
            diff_list.append(abs(current_page_rank[page] - page_rank[page]))
            page_rank[page] = current_page_rank[page]
        if check_all_value_is_less_than_value(diff_list, 0.0001):
            reach_min_changes_value = True

    return page_rank


def check_all_value_is_less_than_value(diff_list, min_value):
    for diff in diff_list:
        if diff > min_value:
            return False
    return True


if __name__ == "__main__":
    main()
