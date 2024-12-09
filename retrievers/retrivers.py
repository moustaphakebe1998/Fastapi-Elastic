import os
import ssl
import urllib3
import requests
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import DirectoryLoader, PyPDFLoader
from langchain_community.vectorstores import ElasticVectorSearch
from elasticsearch import Elasticsearch
import requests
import os

os.environ['no_proxy'] = "1"
# Définition des variables d'environnement pour le proxy
proxies = {
    "http": "ht",
    "https": "http://",

}

# Définition des données à envoyer

"""
data = {
    "texts": [
        "J'aime paris.",
        "j'utilise camembert.",
        "Un chatbot pour la ville de paris."
    ]
}"""



data={"texts":['paris la ville']}


# URL de destination
url = "https://148.253.76.61/camembert"

# Envoi de la requête POST
response = requests.post(url, json=data, proxies=proxies, verify=False)


# Affichage de la réponse
print(response.text)


3


user_name = "elastic"
password = 'k1j07vR'
elasticsearch_url = f"https://{user_name}:{password}@localhost:9200"

# Instanciation de ElasticVectorSearch

def generate_embeddings(texts):
    url = "https://148.253.76.61/camembert"
    proxies = {

        "http": "http://DMZ-PXSERVER.",
        "https": "http://DMZ-PXS",
    }
    data= []
    for text in texts:
        file={"texts": [text.page_content]}
        response = requests.post(url, json=file, proxies=proxies, verify=False)
        if response.status_code == 200:
            data.append({
                'text': str(text.page_content),
                'vector': response.json()['embeddings'][0]
            })
        else:
            print(f"Erreur lors de la génération de l'embedding pour le texte: {str(text.page_content)}")
    return data




class ElasticsearchRetriever:
    def __init__(self, es_client, index_name):
        self.es_client = es_client
        self.index_name = index_name

    def retriever(self, query_text, top_k=20):
        query_vector = text_to_vector(query_text)
        query = {
            "size": top_k,
            "query": {
                "script_score": {
                    "query": {"match_all": {}},
                    "script": {
                        "source": "cosineSimilarity(params.query_vector, 'vector') + 1.0",
                        "params": {"query_vector": query_vector}
                    }
                }
            }
        }

        response = self.es_client.search(index=self.index_name, body=query)
        return [{"text": hit["_source"]["text"], "score": hit["_score"]} for hit in response['hits']['hits']]

#[(hit["_source"]["text"], hit["_score"]) for hit in response['hits']['hits']]

def text_to_vector(text):
    url = "https://148.253.76.61/camembert"
    proxies = {
        "http": "http://DMZ-PXS",
        "https": "http://DMZ-PXSERVE",
    }
    response = requests.post(url, json={"texts":[text]}, proxies=proxies, verify=False)
    if response.status_code == 200:
        return response.json()['embeddings'][0]
    else:
        raise Exception(f"Failed to vectorize text due to {response.status_code}: {response.text}")
