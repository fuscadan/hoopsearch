"""
    Created on Tue October  08 2019

    @author danie

    A version of HoopSearch with no GUI.  Run the file via command line and 
    enter a search query when prompted to do so.  Results are printed in the 
    terminal.
"""

from hoopsearch.models.LSA_model import LemmaTokenizer
import hoopsearch.common.search_engine as search_engine

query = input('Please enter a search query: ')
results = search_engine.search(query)

print('\n')
for result in results:
    print(result[0] + '\n\n' + result[1] + '\n' + result[2] + '\n')