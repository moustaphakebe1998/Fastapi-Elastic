import os
import json
import ssl
import time
import urllib3
import requests
#from langchain_elasticsearch import ElasticsearchRetriever
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
#from langchain.prompts import PromptTemplate, ChatPromptTemplate
#from langchain.chains import LLMChain, RetrievalQA
#from langchain.chains.elasticsearch_database import ElasticsearchDatabaseChain
from fastapi import FastAPI, HTTPException, Query, Depends, Request
from pydantic import BaseModel, Field

app = FastAPI()

os.environ['no_proxy'] = "10.185.33.1" 

os.environ['http_proxy'] = "http://DMZ"

os.environ['htpps_proxy'] = "http://DMZ"



@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response
    
#Création d'un contexte SSL personnalisé
#ca_cert_path = '/opt/val/kebeMousFiles/adresses/app/http_ca.crt'
#ssl_context = ssl.create_default_context(cafile=ca_cert_path)
#ssl_context.check_hostname = False
#ssl_context.verify_mode = ssl.CERT_NONE

# Instanciation du client Elasticsearch avec le contexte SSL personnalisé
es = Elasticsearch(
    ['https://10.185.33.241:9200'],
    basic_auth=('elastic', 'uKt'),
    verify_certs=False
)

if es.ping():
    print("Connexion réussie à Elasticsearch.")
else:
    print("Impossible de se connecter à Elasticsearch. Vérifiez l'URL et les paramètres SSL.")

class ElasticsearchRetriever:
    def __init__(self, es_client, index_name):
        self.es_client = es_client
        self.index_name = index_name

    def retrieve(self, query_text, top_k=3):
        # Préparer le corps de la requête de recherche en utilisant le query_text fourni
        body = body_func(query_text)
        # Définir la taille des résultats à top_k
        body['size'] = top_k
        
        # Effectuer la requête de recherche
        response = self.es_client.search(index=self.index_name, body=body)
        
        # Analyser la réponse pour renvoyer une liste de tuples (texte, score)
        return [(hit["_source"]["adressetypo"], hit["_score"]) for hit in response['hits']['hits']]

def body_func(text):
    return {
        "query": {
            "bool": {
                "should": [
                    {
                        "match": {
                            "adressetypo": {
                                "query": text,
                                "fuzziness": "AUTO",
                                "boost": 2.0  # Augmenter le poids du fuzzy matching
                            }
                        }
                    },
                    {
                        "match": {
                            "adressetypo.phonetic": {
                                "query": text,
                                "boost": 1.0  # Poids par défaut pour le phonetic matching
                            }
                        }
                    }
                ]
            }
        }
    }
#ou 

index_name = 'adresses' 
retriever = ElasticsearchRetriever(es, index_name)

class SearchParams(BaseModel):
    query: str
    top_k: int = Field(3, ge=1, le=10)


@app.post("/search_addresses/")
def search_addresses(params: SearchParams):
    results = retriever.retrieve(params.query, params.top_k)
    return {"results": [{"adressetypo": text, "score": score} for text, score in results]}
