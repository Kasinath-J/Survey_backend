import requests
# import json

def get_max_label(data):
    # Load the JSON string into a Python object
    # data = json.loads(json_string)

    # Initialize variables to keep track of the maximum score and corresponding label
    max_score = 0.0
    max_label = None

    # Loop through the list of dictionaries and update the maximum score and label
    for label_dict in data[0]:
        score = label_dict["score"]
        if score > max_score:
            max_score = score
            max_label = label_dict["label"]

    # Return the label with the highest score
    return max_label


def polarity_fn(ans):
    
    rating_count = {
        "1":0,
        "2":0,
        "3":0,
        "4":0,
        "5":0,
    }

    positive = []
    negative = []

    for text in ans:
        API_TOKEN = "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"
        API_URL = "https://api-inference.huggingface.co/models/nlptown/bert-base-multilingual-uncased-sentiment"
        headers = {"Authorization": f"Bearer {API_TOKEN}"}

        def query(payload):
            response = requests.post(API_URL, headers=headers, json=payload)
            return response.json()
            
        output = query({
            "inputs": text,
        })

        max_label = get_max_label(output)[0]
        rating_count[max_label] = rating_count[max_label] + 1
        if int(max_label)<3:
            negative.append(text)
        else:
            positive.append(text)

    return (rating_count,positive,negative)
