from bs4 import BeautifulSoup
import wikipedia

class Fetcher:

    def fetch_wiki_table(self, wiki_page_name, table_identifier):

        try:
            wiki_page_html = wikipedia.page(title=wiki_page_name, auto_suggest=False).html()
        except:
            print('Error retrieving page: wiki_page_name')
            return None
        
        soup = BeautifulSoup(wiki_page_html, 'html.parser')
        
        return soup.find('table', table_identifier)
    

    def fetch_wiki_table_rows(self, wiki_page_name, table_identifier):

        wiki_table = self.fetch_wiki_table(wiki_page_name, table_identifier)

        return wiki_table.find_all('tr')[1:]