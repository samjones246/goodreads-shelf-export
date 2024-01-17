import argparse
import requests
from bs4 import BeautifulSoup
import os

BASE_URL = "https://www.goodreads.com/review/list"

def main():
    parser = argparse.ArgumentParser(description='Export titles from a Goodreads shelf to a text file.')
    parser.add_argument('userid', metavar='User ID', type=str,
                        help='id of the Goodreads user')
    parser.add_argument('shelf', metavar='Shelf', type=str,
                        help='name of the shelf')

    args = parser.parse_args()
    url = f"{BASE_URL}/{args.userid}?shelf={args.shelf}&print=true&view=table"

    all_titles = []
    page = 1
    num_pages = None
    print("Reading titles...")
    while True:
        print(f"Page {page}...")
        response = requests.get(url + f"&page={page}")
        document = BeautifulSoup(response.text, 'html.parser')
        if num_pages is None:
            pagination = document.find(id="reviewPagination")
            if pagination is None:
                num_pages = 1
            else:
                num_pages = int(pagination.find_all(["a", "em", "span"])[-2].string)
        titles = document.find_all("td", class_="field title")
        titles = list(map(lambda tag: next(tag.div.a.stripped_strings), titles))
        all_titles += titles
        if page == num_pages:
            break
        page += 1
    print("Done!")
    print("Writing output...")
    if not os.path.exists(args.userid):
        os.mkdir(args.userid)
    with open(f"{args.userid}/{args.shelf}.txt", "w") as f:
        for title in all_titles:
            f.write(title+"\n")
    print(f"Done! Wrote {len(all_titles)} titles.")
    

if __name__ == "__main__":
    main()