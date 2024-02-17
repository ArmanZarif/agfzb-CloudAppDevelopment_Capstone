import requests
import json
# import related models here
from requests.auth import HTTPBasicAuth
from django.http import HttpResponse


# Create a `get_request` to make HTTP GET requests
# e.g., response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
#                                     auth=HTTPBasicAuth('apikey', api_key))
from .models import CarDealer , DealerReview


def get_request(url,api_key=None, **kwargs):
    print(kwargs)
    print("GET from {} ".format(url))    
    try:
        if api_key:
            response = requests.get(url, headers={'Content-Type': 'application/json'},
                                    params=kwargs,auth=HTTPBasicAuth('apikey', api_key)) 
        else:            
        # Call get method of requests library with URL and parameters
            response = requests.get(url, headers={'Content-Type': 'application/json'},
                                    params=kwargs)
    except:
        # If any error occurs
        print("Network exception occurred")
    status_code = response.status_code
    print("With status {} ".format(status_code))
    json_data = json.loads(response.text)
    return json_data


# Create a `post_request` to make HTTP POST requests
# e.g., response = requests.post(url, params=kwargs, json=payload)
def post_request(url, json_payload, **kwargs):
    try:
        # response = 'hi'
        response = requests.post(url, params=kwargs, json=json_payload)        
        # return HttpResponse('hi there!')
    except:
        print('network error')
    status_code = response.status_code
    print(f"status code is = {status_code}")
    response_to_return = response.json()   
    return response_to_return


# Create a get_dealers_from_cf method to get dealers from a cloud function
def get_dealers_from_cf(url, **kwargs):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url)
    if json_result:
        # Get the row list in JSON as dealers
        dealers = json_result
        
        # For each dealer object
        for dealer in dealers:
            # Get its content in `doc` object
            dealer_doc = dealer
            print("DEaler",dealer_doc)
            # Create a CarDealer object with values in `doc` object
            dealer_obj = CarDealer(address=dealer_doc["address"], city=dealer_doc["city"], full_name=dealer_doc["full_name"],
                                   id=dealer_doc["id"], lat=dealer_doc["lat"], long=dealer_doc["long"],
                                   short_name=dealer_doc["short_name"],state=dealer_doc['state'],
                                   st=dealer_doc["st"], zip=dealer_doc["zip"])
            results.append(dealer_obj)

    return results


# Create a get_dealer_reviews_from_cf method to get reviews by dealer id from a cloud function
def get_dealer_reviews_from_cf(url, dealer_id):
    json_result = get_request(url, id=dealer_id)
    results = []
    if json_result:
        reviews = json_result
        for review in reviews:
            review_obj = DealerReview(
                id=review.get('id'),
                name=review.get('name'),
                dealership=review.get('dealership'),
                review=review.get('review'),
                purchase=review.get('purchase'),
                purchase_date=review.get('purchase_date'),
                car_make=review.get('car_make'),
                car_model=review.get('car_model'),
                car_year=review.get('car_year')
            )
            results.append(review_obj)
    return results



# - Parse JSON results into a DealerView object list


# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
# def analyze_review_sentiments(text):

def analyze_review_sentiments(review):   
    api_key = 'BBW0NdFyhn6TRLQtDg8h-ZDmyX54KamAJoSHGLeNPCWw'
    url = 'https://api.us-south.natural-language-understanding.watson.cloud.ibm.com/instances/077adcb3-6e83-4ca3-998d-993821be0ae7/v1/analyze'
    kwargs = {
    "text": "Thank you and have a nice day!",
    "version": "2022-04-07",
    "features": {
        "sentiment": {
            "document": True
        }
    },
    "return_analyzed_text": True    
    }    
    result = analyze_text(review)
    sentiment_label = result.get('sentiment', {}).get('document', {}).get('label')
    if sentiment_label:
        print(sentiment_label)
        response = sentiment_label
    else:
        print(None)
        response = 'none'


    # response = 'positive'
    # response = get_request(url, api_key=api_key, **params)
    return response  # Assuming response contains sentiment analysis result


# - Call get_request() with specified arguments
# - Get the returned sentiment label such as Positive or Negative

def get_test_dealers():    
    results = []    
    path_to_dealerships = './dealerships.json'
    with open(path_to_dealerships) as f:
        data = json.load(f)    
         
    json_result = data['dealerships']
    if json_result:
        # Get the row list in JSON as dealers
        dealers = json_result
        
        # For each dealer object
        for dealer in dealers:
            # Get its content in `doc` object
            dealer_doc = dealer
            print("DEaler",dealer_doc)
            # Create a CarDealer object with values in `doc` object
            dealer_obj = CarDealer(address=dealer_doc["address"], city=dealer_doc["city"], full_name=dealer_doc["full_name"],
                                   id=dealer_doc["id"], lat=dealer_doc["lat"], long=dealer_doc["long"],
                                   short_name=dealer_doc["short_name"],state=dealer_doc['state'],
                                   st=dealer_doc["st"], zip=dealer_doc["zip"])
            results.append(dealer_obj)

    return results



def analyze_text(text):
    api_key = 'BBW0NdFyhn6TRLQtDg8h-ZDmyX54KamAJoSHGLeNPCWw'
    url = 'https://api.us-south.natural-language-understanding.watson.cloud.ibm.com/instances/077adcb3-6e83-4ca3-998d-993821be0ae7/v1/analyze'

    params = {
    "text": text,
    "version": "2022-04-07",
    "features": {
        "sentiment": {
            "document": True
        }
    },
    "return_analyzed_text": True
}
    headers = {'Content-Type': 'application/json'}
    response = requests.get(url, params=params, headers=headers, auth=HTTPBasicAuth('apikey', api_key))
    return response.json()


# print(result['sentiment']['document']['label'])



