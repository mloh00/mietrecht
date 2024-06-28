import requests

import json

import os

# url = "https://classix.ai/api/v1/"
url = "http://localhost:5000/"

endpoints = [
    
    # "Klio/chat",
    # "nlp/QLoRA/chat",
    "nlp/LLM/chat",
    # "nlp/RAG/chat",

    # "nlp/RAG/setup"

    # "Klio/status",
    # "nlp/RAG/status"
]

querylist = ["Who is Donald Trump?", "Mein Lebenspartner, der Mieter war, ist verstorben. Wir hatten einen gemeinsamen Haushalt geführt. Was passiert nun mit dem Mietverhältnis?", "Wann kann mein Vermieter den Mietvertrag kündigen?", "Darf ich meine Wohnung untervermieten?", "Darf ich meine Haustiere in der Wohnung halten?"]

with open("Mietrecht_chunks.json", "r", encoding="utf-8") as f:
    request_data = json.load(f)

json_QnA = []

for query in querylist:
    y_responses = []
    y_endpoints = []
    y_chunks = []
    answers = []
    for endpoint in endpoints:
        streaming = False

        if "setup" in endpoint:
            y = requests.post(url + endpoint + f"?apiKey={os.environ.get('API_KEY')}", json=request_data)
        elif "chat" in endpoint:
            y = requests.get(url + endpoint + f"?text={query}&lang=de&maxChunks=3&apiKey={os.environ.get('API_KEY')}&threshold=0.18&defaultAnswer=No%20relevant%20documents%20found.", stream=streaming)
        elif "query" in endpoint:
            y = requests.get(url + endpoint + f"?text={query}&lang=de&apiKey={os.environ.get('API_KEY')}")
        else:
            y = requests.get(url + endpoint + f"?apiKey={os.environ.get('API_KEY')}")

        y_json = json.dumps(y.json(), indent=4)
    
        y_responses.append(y.json()["response"])

        y_chunks.append(y.json()["chunks"])

        y_endpoints.append(endpoint)

    for response, endpoint in zip(y_responses, y_endpoints):
        y_chunks_sliced = y_chunks[y_endpoints.index(endpoint)]
        answers.append({endpoint: response, "chunks": y_chunks_sliced})

    json_QnA.append({"question": query, "answers": answers})

with open("Mietrecht_QnA_LLM.json", "w", encoding="utf-8") as f:
    json.dump(json_QnA, f, indent=4, ensure_ascii=False)

