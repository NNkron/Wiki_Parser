import requests
import progressbar
from bs4 import BeautifulSoup
import sys


class FileManager:

    @staticmethod
    def get_file_data(file_name, param):
        try:
            f = open(file_name, param)
        except FileNotFoundError:
            print("File {} is not found".format(file_name))
            print("Press any key to exit...")
            print(quit)
        data = [line.strip() for line in f if line != '']
        f.close()
        return data

    @staticmethod
    def put_data_in_file(data):
        f = open('answer.csv', 'w')
        for object in data:
            f.write('{0},"{1}"\n'.format(object[0], object[1]))
        f.close()


class WikiParser:

    def open_url(self, link):
        """Method gets a page via given URL."""
        page = requests.get(link)
        return page

    def find_company_url(self, page):
        """Method gets a page as an input, processes it and gives back URL."""
        soup = BeautifulSoup(page.text, 'lxml')  # transforming page in XML
        table = str(soup.find('table', {'class': 'infobox'}))  # selecting needed XML-node
        index = table.index('Website')  # we are looking for a Website row in our table
        table = table[index:index+200]  # 200 is kind of a magic number. It ensures, that needed URL will fit
                                        # in search area
        for element in table.split('"'):
            if element.startswith('http') or element.startswith('//www'):  # retrieving URL
                return element


if __name__ == '__main__':

    print('Program started.')

    resource_file_name = sys.argv       # retrieving arguments from input
    resource_file_name = str(resource_file_name[1])   # selecting right argument

    WikiParserInstance = WikiParser()

    print('Retrieving links from the file...')
    list_of_links = FileManager.get_file_data(resource_file_name, 'r')
    print('Done')
    print('Processing links...')

    result = []
    i = 0  # this line and two lines below are progress bar implementation
    max_bar = len(list_of_links)
    bar = progressbar.ProgressBar(max_value=max_bar).start()

    for element in list_of_links:
        i += 1
        bar.update(i)
        page = WikiParserInstance.open_url(element.strip('"'))
        url = WikiParserInstance.find_company_url(page)
        result.append([element.strip('"'), url])

    bar.finish()

    print('Done')
    print("Writing results in file...")
    FileManager.put_data_in_file(result)
    print("Done.")

    print("Press any key to exit")
    if input():
        exit(0)
