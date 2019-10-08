from hoopsearch.models.LSA_model import LemmaTokenizer
import hoopsearch.common.search_engine as search_engine
import warnings
warnings.filterwarnings("ignore")

query = input('Please enter a search query: ')
results = search_engine.search(query)

print('\n')
for result in results:
    print(result[0] + '\n\n' + result[1] + '\n' + result[2] + '\n')