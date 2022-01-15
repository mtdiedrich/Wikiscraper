from bs4 import BeautifulSoup
from tqdm import tqdm
import urllib.request
# IGNORE BELOW
import ssl

try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context
# IGNORE ABOVE

def main():
    # IDEAS
    # - Some form of intelligent path traversal
    # - Reverse traversal from the page using (Links here)
    # - Using categories
    start_url = "https://en.wikipedia.org/wiki/Lemon_Sky"
    end_url = "https://en.wikipedia.org/wiki/Avant-garde"

    degree = 0
    links = [start_url]

    found = False
    while not found:
        degree += 1
        new_links = []
        for link in tqdm(links):
            sublinks = get_links(link)
            if end_url in sublinks:
                found = True
                break
            new_links += sublinks
        links = list(set(new_links))
        if not found:
            print("Not found", degree)
    print("Success", degree)

def get_links(url):
    base_url = "https://en.wikipedia.org"
    # Read URL
    html_page = urllib.request.urlopen(url)
    # Convert to HTML
    soup = BeautifulSoup(html_page, features="html.parser")

    drops = ['Wikipedia:', 'Special:', 'Portal:', 'Help:', 'Talk:', 'Category:', 'File:', '/wiki/Main_Page']
    # Get list of links
    links = []
    for link in soup.findAll('a'):
        shortened_link = link.get('href')
        # If shortened is null, continue
        if not shortened_link:
            continue
        # If shortened does not start with /wiki/, continue
        if '/wiki/' not in shortened_link[:6]:
            continue
        # Flag the link to not be used if it has a drop prefix
        use = True
        for prefix in drops:
            if prefix in shortened_link:
                use = False
        if use:
            links += [base_url + shortened_link]
    links = list(set(links))
    return links

if __name__ == "__main__":
    main()