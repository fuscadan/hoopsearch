# A model used in the search engine is pickled, but a custom class the model
# uses was not pickled along with it. That class, 'LemmaTokenizer', therefore
# needs to be imported at the highest level so the unpickled model can use it.
from hoopsearch.models.LSA_model import LemmaTokenizer
from hoopsearch.views import app

app.run(debug = True)

