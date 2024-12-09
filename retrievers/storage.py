import os
import os
import ssl
import urllib3
import requests
import time

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import DirectoryLoader, PyPDFLoader
from langchain_community.document_loaders.pdf import PyPDFDirectoryLoader
from langchain_community.vectorstores import ElasticVectorSearch

from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
from langchain_community.vectorstores import ElasticVectorSearch
from langchain_elasticsearch import ElasticsearchStore
from elasticsearch.helpers import bulk
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

os.environ['no_proxy'] = "10."
proxies = {
    "http": "http://DMZ-/",
    "https": "http://",

}
# URL de destination

#https://www.elastic.co/guide/en/elasticsearch/reference/current/docker.html
PATH = "docs"
# Chemin vers le certificat de l'autorité de certification
ca_cert_path = '/opt/val/kebeMousFiles/http_ca.crt'

# Création d'un contexte SSL personnalisé
ssl_context = ssl.create_default_context(cafile=ca_cert_path)
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE

# Instanciation du client Elasticsearch avec le contexte SSL personnalisé
es = Elasticsearch(
    ['https://localhost:9200'],
    basic_auth=('elastic', 'k1j07vY'),
    ssl_context=ssl_context
)

# Vérification de la connexion Elasticsearch
if es.ping():
    print("Connexion réussie à Elasticsearch.")
else:
    print("Impossible de se connecter à Elasticsearch. Vérifiez l'URL et les paramètres SSL.")


PATH="/opt/val/kebeMousFiles/docs_deliberations/docs"

loader = PyPDFLoader("/opt/val/kebeMousFiles/docs_deliberations/docs//BOVP Délibérations - Février 2024.pdf")
documents=loader.load()

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=500,
    separators=["\n", "\n\n", "(?<=\.!-/)","", " "]
)

data = text_splitter.split_documents(documents)


#Generate embeddings


index_name='test'

if not es.indices.exists(index=index_name):
    mapping = {
        "mappings": {
            "properties": {
                "text": {"type": "text"},
                "vector": {"type": "dense_vector", "dims": 1024}  # Ajustez la dimension selon votre modèle
            }
        }
    }
    es.indices.create(index=index_name, body=mapping)
   

"""

def generate_embeddings(texts,index_name):
    url = "https://148.253.76.61/camembert"
    proxies = {
        "http": "http://DMZ-PXSE",
        "https": "http://DMZ-PXSERVE",
    }
    #headers = {'Content-Type': 'application/json'} , headers=headers
    for text in texts:
        #time.sleep(10)
        file = {"texts": [text.page_content]}
        response = requests.post(url, json=file, proxies=proxies, verify=False)
        if response.status_code == 200:
            doc = {
                'text': str(text.page_content),
                'vector': response.json()['embeddings'][0]
            }
            es.index(index=index_name, document=doc)
        else:
            print(f"Erreur lors de la génération de l'embedding pour le texte: {text}")

"""

start_time = time.time()
print(start_time)
def generate_embeddings(texts,index_name):
    url = "https://148.253.76.61/camembert"
    headers = {'Content-Type': 'application/json'}
    actions = []
    proxies = {
        "http": "http://DMZ-PXSERV"",
    }
    for text in texts:
        file = {"texts": [text.page_content]}
        response = requests.post(url, json=file, proxies=proxies, verify=False)  # Changed to verify=True
        if response.status_code == 200:
            action = {
                "_index": index_name,
                "_source": {
                    'text': text.page_content,
                    'vector': response.json()['embeddings'][0]
                }
            }
            actions.append(action)
        else:
            print(f"Erreur lors de la génération de l'embedding pour le texte")

    if actions:
        bulk(es, actions)


db=generate_embeddings(data,index_name)
end_time=time.time()
print(end_time)
print(f"temps min:{end_time-start_time}")
