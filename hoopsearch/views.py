from flask import Flask
from flask import render_template
from flask import request 
from nltk import word_tokenize
import hoopsearch.common.search_engine as backend
from hoopsearch.models.LSA_model import LemmaTokenizer

app = Flask(__name__)

@app.route('/',methods=["GET","POST"])
@app.route('/index')
def index():
    return render_template("index.html")

@app.route('/output')
def recommendation_output():     
        # Pull input
        query =request.args.get('user_input')            
       
        # Case if empty
        if query =='':
            return render_template("index.html",
                                   my_input = query,
                                   my_form_result="Empty")
        else:
            # if query is non-empty, return the results of the search
            # TODO dates = ...
            results = backend.search(query)
 
            headlines = ['','','']
            for i in range(0,len(results)):
                headlines[i] = results[i][0]
            summaries = ['','','']
            for i in range(0,len(results)):
                summaries[i] = results[i][2]
            dates = ['','','']
            for i in range(0,len(results)):
                dates[i] = results[i][1]

            return render_template("index.html",
                                my_input=query,
                                headline_1 = headlines[0],
                                headline_2 = headlines[1],
                                headline_3 = headlines[2],
                                summary_1 = summaries[0],
                                summary_2 = summaries[1],
                                summary_3 = summaries[2],
                                date_1 = dates[0],
                                date_2 = dates[1],
                                date_3 = dates[2],  
                                my_form_result="NotEmpty")

# start the server with the 'run()' method
if __name__ == "__main__":
    app.run(debug=True) #will run locally http://127.0.0.1:5000/

