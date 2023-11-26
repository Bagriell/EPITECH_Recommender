# Recommender

![gift photo](/assets/cadeau.jpg)


This programm takes a client id and:
1. get statistical description of the client
2. get client profile analysis
3. recommended gift product

Dataset is only available for Epitech school students and represents supermarkets transactions.
## Commands

The software requires python > 3.9.

create env:    
`python -m venv dataenv`

activate env(windows):    
`dataenv\Scripts\activate`

activate env(linux):    
`source dataenv/bin/activate`

install dependencies:  
`pip install -r requirements.txt`

run project:  
`python user_recommendation.py <client_id>`

## Recommendation strategy

We try to find similarities among customers using the kmeans clusterization algorithm.  
Each customer is linked to a cluster of similar customers based on the nature of their transactions.  
Finally, we recommend a product based on popularity among this cluster.

## Architecture

* __user_recommendation.py__: entrypoint
* __/clustering__: build clustering model
* __/data__: different data
* __/transaction_items__: product analysis
* __customer_segmentation.py__: profile customer
* __recommender.py__: recommend product to customer
* __stats.py__: get statistics of customer