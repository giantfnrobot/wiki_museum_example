from bs4 import BeautifulSoup
import wikipedia

class Fetcher:

    def fetch_wiki_table(wiki_page_name, table_identifier):

        try:
            wiki_page_html = wikipedia.page(title=wiki_page_name, auto_suggest=False).html()
        except:
            print('Error retrieving page: wiki_page_name')
            return None
        
        soup = BeautifulSoup(wiki_page_html, 'html.parser')
        
        return soup.find('table', table_identifier)