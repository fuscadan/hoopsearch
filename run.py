"""
    Created on Tue October  08 2019

    @author danie

    Launches the HoopSearch app on a local server that can be accessed via a 
    web browser by navigating to http://127.0.0.1:5000/.  Enter a query in the 
    search bar, and the search engine returns up to ten games relevant to the 
    query, including their headlines, dates, and a summary description.

    Example:

    Search Query:

    thrilling overtime close game buzzer beater

    First Result:

    Ellis (42), Warriors nip Martin (50), Kings in OT
    2009-04-02
    Although the Kings and the Warriors don't have a fierce rivalry, they've 
    got a knack for entertainment when they get together -- and Monta Ellis 
    shot Golden State to victory in the latest meeting.
"""

# A model used in the search engine is pickled, but a custom class the model
# uses was not pickled along with it. That class, 'LemmaTokenizer', therefore
# needs to be imported at the highest level so the unpickled model can use it.
from hoopsearch.models.LSA_model import LemmaTokenizer
from hoopsearch.views import app

app.run(debug = True)

