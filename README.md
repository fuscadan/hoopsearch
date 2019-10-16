# HoopSearch - Find the NBA games you want to watch

A concept-searchable database of NBA games.  Find a game to watch by entering descriptive words of the kind of game you are interested in.


## Usage

Run the file run.py and navigate to http://127.0.0.1:5000/ in a web browser.  You should see a page that looks like this:

![Main search page](https://github.com/fuscadan/hoopsearch/blob/master/hoopsearch/static/img/readme/HoopSearch_main.png)

When you enter a search, for example

> thrilling overtime close game buzzer beater

the search engine returns up to ten games relevant to the search query, including their headlines, dates, and a summary description.

![Search results](https://github.com/fuscadan/hoopsearch/blob/master/hoopsearch/static/img/readme/results.png)


## Concept-searchability and Underlying Theory

The dataset that we work with is the collection of long-form game recap articles found on espn.com, comprising every regular season game played between 2003 and 2009.  A given query is compared to each article in order to find the most relevant games.  The search engine returns results based on more than just keyword-matching, however; the underlying concept of the search is matched with relevant articles as well.  This is achieved by "Latent Semantic Analysis", or LSA.  The idea is as follows.

For each article, a bag-of-words representation is constructed (weighted using tf-idf).  Latent semantic analysis is the process of finding the k-dimensional subspace (I used k = 100) that fits best the cloud of data points, and then projecting each data point onto this subspace.  The projected vector is termed the "concept vector" of the document. 

!["Concept vectors" of Latent Semantic Analysis](https://github.com/fuscadan/hoopsearch/blob/master/hoopsearch/static/img/readme/lsa.png)

A concept vector for the given query is also constructed by projecting its bag-of-words representation.  The concept vector for the query is then compared (using cosine similarity) to the concept vectors of each article, and the games with the most similar articles to the query are surfaced.


## Intuition behind the success of Latent Semantic Analysis

When validating the results of the search engine (see below), I found that the search engine with LSA performs better than a less sophisticated weighted keyword search.  To understand why this might be, consider the subspace of the bag-of-words vector space spanned by the axes for the words "Kobe" and "Lakers".  On this space we plot, for each document, the number of instances of these words.  We might find that on average, "Lakers" appears twice as often as "Kobe", as illustrated by the line of best fit through the data points.  

![Idea of why LSA performs better than keyword search](https://github.com/fuscadan/hoopsearch/blob/master/hoopsearch/static/img/readme/lsa_idea.png)

LSA finds this line of best fit and projects the data onto it.  In addition to a reduction in dimension, this projection has another beneficial effect; since we also project any query vector onto the subspace, any query with the word "Kobe" is treated exactly the same as a query with the words "Kobe Lakers Lakers".  The search query "Kobe" is therefore matched with articles containing the word "Lakers", even though the user didn't specify that explicitly.  In this way, a search engine using LSA can perform better than a simple keyword search.


## Validation

One measure of the success of a search engine is its "Mean Average Precision".  Here is a description of how MAP is computed.

Suppose a query is given and each document in the corpus is labelled as being either relevant or non-relevant to that query.  The "Precision at k", denoted P(k), is the fraction of relevant documents that are returned in the first k results.

![Computing Average Precision for a single query](https://github.com/fuscadan/hoopsearch/blob/master/hoopsearch/static/img/readme/AP.png)

The "Average Precision" AP is computed by taking the average of the values of P(k) for k ranging between 1 and the total number of relevant documents in the corpus.

So each query has its own relevant/non-relevant labelling of the documents in the corpus, and its own sorted list of search results, which lead to its own Average Precision.  The Mean Average Precision is found by taking the mean of the AP's computed for some set of queries, which is hopefully representative of possible interests a user may have.

Due to the large amount of labelling involved, I was only able to compute the Average Precision for a single query.  I computed the Average Precision for the query

> thrilling overtime close buzzer beater

for two search engines.  One search engine compared the bag-of-words embedding (weighted by tf-idf) of the query to those of the game articles.  This is essentially keyword search.  The other engine, used by HoopSearch, compares the LSA-generated "concept vector" of a query to those of the game articles.  Here we see that the LSA-powered search engine performs better, with an AP of 87% compared to 71%.

![Comparison of Average Precision for a keyword search and an LSA-powered search](https://github.com/fuscadan/hoopsearch/blob/master/hoopsearch/static/img/readme/validation.png)


## Structure of the Repository

**run.py**

Launches the HoopSearch app on a local server that can be accessed via a web browser.

**hoopsearch_program.py**

A version of HoopSearch with no GUI.  Run the file via command line and enter a search query when prompted to do so.  Results are printed in the terminal.

**folder 'hoopsearch'**

The folders 'static' and 'templates' hold the front-end content of the web app. These files are modified from a template from bootstrap.com.  The script 'views.py' connects the front-end content to the python back-end using flask.

**folder 'common'**

Contains the central python programs that define objects and functions used in multiple other places.  The main programs 'search_engine.py' and 'summarizer.py' are found here.

**folder 'data'**

Contains the raw data and processed databases used for the search and summarization tasks.

**folder 'models'**

Contains trained model files and the scripts that trained them.  The model 'lsa_model.joblib' handles the extraction of concept vectors from search queries and game articles.  The model 'tree_model_balanced.joblib' predicts which sentence in a game article is most descriptive (so that it can be presented as a summary of the game).

**folder 'scripts'**

Contains scripts that scrape data from espn.com and process it.  There is also a file 'validation.py' containing the functions used to validate the results of the search engine.

