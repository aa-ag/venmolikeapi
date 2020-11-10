from webapp import app
from flask import jsonify
import requests 
from enum import Enum


## Flask config to have json response not in alphabetical order
app.config['JSON_SORT_KEYS'] = False


## Endpoints
accounts_endpoint = '.../accounts/:id'
users_endpoint = '.../users/:id'
likes_endpoint = '.../likes/'


## Helper code
class Account(Enum):
    ORIGIN = 'originAccount'
    TARGET = 'targetAccount'


def get_user_name(transfer, account):
    '''
    Gets full user name using account_id from the transfer
    and then requesting user information from users endpoint
    '''
    account_id = transfer[account.value]
    account_url = accounts_endpoint.replace(':id', f"{account_id}")
    account_request = requests.get(account_url).json()

    user_account_id = account_request['user']
    user_account_url = users_endpoint.replace(':id', f"{user_account_id}")
    user_account_request = requests.get(user_account_url).json()

    return f"{user_account_request['firstName']} {user_account_request['lastName']}"


def get_count_likes(all_likes, transfer_id):
    '''
    From all likes, lists those likes per transfer_id and counts them
    '''
    transfer_likes = [i for i in all_likes if i['transfer'] == transfer_id]
    return len(transfer_likes)


## Routes
@app.route('/')
def home():
    '''
    Sends response "{'status': 'ok'}" to browser to verify that the server is running
    '''
    return jsonify({'status': 'ok'})


@app.route('/feed')
def feed():
    '''
    Using the API, implements a method to build the data for a "social" transfers feed, 
    combining information from whichever API resources are necessary. 
    Transfers with a "failed" status should be excluded from the feed. 
    Your method should return an Array of Objects with the following information:
    [
        {
            "originUserName": "John Smith",
            "targetUserName": "Sallie Someone",
            "amount": 54.99,
            "description": "For drinks and dinner", 
            "likesCount": 2
        }
    ]
    '''
    # All transfers from transfers endpoint
    transfers = requests.get('.../transfers').json()
    
    # Transfers that have "status" of "completed" only
    completed_transfers = [i for i in transfers if i['status'] == 'complete']

    # All likes from the likes endpoint
    all_likes = requests.get(likes_endpoint).json()

    # Empty list to fill with required information from stories
    feed_data = []

    # Loop through all completed transfers and executes helper code to fill feed_data
    for transfer in completed_transfers:
        feed_item = {}
        feed_item['originUserName'] = get_user_name(transfer, Account.ORIGIN)
        feed_item['targetUserName'] = get_user_name(transfer, Account.TARGET)
        feed_item['amount'] = "{0:.2f}".format(transfer['amount'] / 100)
        feed_item['description'] = transfer['description']
        feed_item['likesCount'] = get_count_likes(all_likes, transfer['id'])
        feed_data.append(feed_item)

    return jsonify(feed_data)