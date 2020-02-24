import requests
from bs4 import BeautifulSoup
import pprint as pp


def get_pages():
    num_of_pages = int(input("Enter the number of pages you want to scrape: "))
    url = 'https://news.ycombinator.com/news'
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'html.parser')
    links = soup.select('.storylink')
    subtext = soup.select('.subtext')
    if num_of_pages > 1:
        tmp = 2
        while tmp <= num_of_pages:
            url = f'https://news.ycombinator.com/news?p={tmp}'
            res = requests.get(url)
            soup = BeautifulSoup(res.text, 'html.parser')
            links = concatenate(links, (soup.select('.storylink')))
            subtext = concatenate(subtext, soup.select('.subtext'))
            tmp += 1
    return create_custom_hn(links, subtext)


def concatenate(old_link, new_link):
    return old_link + new_link


def sort_stories_by_votes(hnlist):
    return sorted(hnlist, key=lambda k: k['votes'], reverse=True)


def create_custom_hn(links, subtext):
    hn = []
    for index, item in enumerate(links):
        title = item.getText()
        href = item.get('href', None)
        vote = subtext[index].select('.score')
        if len(vote):
            points = int(vote[0].getText().replace(' points', ''))
            if points > 99:
                hn.append({'title': title, 'link': href, 'votes': points})
    return sort_stories_by_votes(hn)


pp.pprint(get_pages())
