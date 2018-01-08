import os
import urllib
import argparse
import httplib2
import validators
from urlparse import urljoin
from bs4 import BeautifulSoup, SoupStrainer


def check_dir(dir_path):
    '''
    check the directory path given,
    if not exist creates one
    '''

    if not os.path.exists(dir_path):
        os.makedirs(dir_path)

def internet_on():
    '''
    check internet connection using google web adddress
    '''
    try:
        urllib.request.urlopen('www.google.com', timeout=3)
        return True
    except urllib.URLError as err: 
        return False


class SniffLinks():

    def __init__(self, link_to_sniff, file_types, folder_to_save=None):

        if not internet_on:
            raise Exception("Check your internet connection...")

        if not validators.url(link_to_sniff):
            raise Exception("The link entered is not valid ...")

        self._link_to_sniff = link_to_sniff
        self._http = httplib2.Http()
        self._file_downloader = urllib.URLopener()

        if folder_to_save is None:
            self._folder_to_save = './'
        else:
            self._folder_to_save = folder_to_save

        self._urls = []
        self._file_names = []

        self._filetypes = file_types

    def download_file(self, file_link, save_file_name):
        try:
            self._file_downloader.retrieve(file_link, self._folder_to_save+save_file_name)
        except Exception, e:
            print "Exception occured while trying to download the link ", file_link
            print "Exception:", e
        finally:
            print "File: ", save_file_name 
            print "Saved in location: ", self._folder_to_save+save_file_name
        
    def sniffer(self):
        status, response = self._http.request(self._link_to_sniff)
        for link in BeautifulSoup(response, parseOnlyThese=SoupStrainer('a')):
            if link.has_attr('href'):
                src_url = link['href']
                src_url_split = src_url.split('/')
                for file_type in self._filetypes:
                    if src_url_split[-1][-len(file_type):] == file_type:
                        self.download_file(urljoin(self._link_to_sniff, link['href']), src_url_split[-1])

    def run(self):
        self.sniffer()


def main(link_to_sniff, save_folder):
    
    #give location in the PC for saving the files
    if save_folder is None:
        save_folder = './downloaded_files/'

    check_dir(save_folder)
    
    file_types=['.pdf']

    snifflinks = SniffLinks(link_to_sniff, file_types, save_folder)
    snifflinks.run()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Url sniffer')
    
    parser.add_argument('-l', '--url', type=str, help='give the url to be sniffed with argument -l')
    parser.add_argument('-d', '--d_folder', type=str, help='enter the download folder with argument -l')

    args   = parser.parse_args()

    main(link_to_sniff=args.url, save_folder=args.d_folder)
