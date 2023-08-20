import pandas as pd
import argparse
from modules.book import ContactBook
from modules.interface import Interface

from config import headers

def get_arguments():
    parser = argparse.ArgumentParser()
    
    parser.add_argument('-f', '--file', type=str, default='contacts.json', help='Contacts data file')
    parser.add_argument('-s', '--size', type=int, default=5, help='Size of the page')
    parser.add_argument('-p', '--page', type=int, default=1, help='Start page number')
    
    args = parser.parse_args()
    return args

def main():
    args = get_arguments()
    book = ContactBook(file_name = args.file)
    
    while True:
        interface = Interface(book = book, records_per_page = args.size, current_page = args.page)
        interface.main_poller()
                

        
if __name__ == "__main__":
    main()
    