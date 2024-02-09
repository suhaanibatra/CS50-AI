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
    probability_distribution = {}

    dict_len = len(corpus.keys())
    no_of_outgoing_pages = len(corpus[page])

    if len(corpus[page]) == 0:
        # no outgoing links
        probability_distribution[page] = 1 / dict_len

    else:
        outgoing_factor = damping_factor / no_of_outgoing_pages
        incoming_factor = (1 - damping_factor) / dict_len

        for p in corpus.keys():
            if p in corpus[page]:
                probability_distribution[p] = outgoing_factor + incoming_factor
            
            else:
                probability_distribution[p] = incoming_factor
    
    return probability_distribution


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    sample_dict = corpus.copy()
    for i in sample_dict:
        sample_dict[i] = 0

    sample = None

    # generating n samples
    for i in range(n):
        if sample:
            #not the first sample
            #use previous sample 
            distribution = transition_model(corpus, sample, damping_factor)
            # randomly choosing the next sample using the current sample
            distribution_list = list(distribution.keys())
            weights = [distribution[i] for i in distribution]
            sample = random.choices(distribution_list, weights, k=1)[0]
        
        
        else:
            #the first sample will be random
            sample = random.choice(list(sample_dict.keys()))
        
        sample_dict[sample] += 1
    
    for item in sample_dict:
        sample_dict[item] /= n
    

    return sample_dict


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    no_of_pages = len(corpus)
    prev = {}
    curr = {}

    # initial condition
    for page in corpus:
        prev[page] = 1 / no_of_pages
    
    # repeatedly updating page ranks and checking their differences

    while True:
        for page in corpus:
            temp = 0
            for link in corpus:
                if page in corpus[link]:
                    temp += prev[link]/len(corpus[link])
                
                if len(corpus[link]) == 0:
                    temp += prev[link]/len(corpus)
            
            temp *= damping_factor
            temp += (1 - damping_factor)/ no_of_pages
            curr[page] = temp

        diff = max([abs(curr[x] - prev[x]) for x in prev])
        if diff < 0.001:
            break
        else:
            prev = curr.copy()
    
    return prev

if __name__ == "__main__":
    main()
