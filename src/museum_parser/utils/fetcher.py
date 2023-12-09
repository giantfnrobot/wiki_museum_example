from bs4 import BeautifulSoup
import wikipedia


def fetch_wiki_page(wiki_page_name):
    try:
        wiki_page_html = wikipedia.page(title=wiki_page_name, auto_suggest=False).html()
    except:
        print('Error retrieving page: wiki_page_name')
        return None

    soup = BeautifulSoup(wiki_page_html, 'html.parser')

    return soup

def fetch_wiki_table(wiki_page_name, table_identifier):

    soup = fetch_wiki_page(wiki_page_name)

    if soup is None:
        return None

    return soup.find('table', table_identifier)


def fetch_wiki_table_rows(wiki_page_name, row_identifier):
    wiki_table = fetch_wiki_table(wiki_page_name, row_identifier)

    return wiki_table.find_all('tr')[1:]