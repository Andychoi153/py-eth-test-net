addr = [1,2]
cnnOut = 2
import requests
import json


# TODO: use this function & make another lib
def get_account(data):
    response = requests.post('http://127.0.0.1:5000/get_account', json=data)
    print(data['account'])
    print(response.text)
    return response.text


def test_demo_scenario():
    data = {'account': 'MES'}
    response = requests.post('http://127.0.0.1:5000/get_account', json=data)
    print('MES')
    print(response.text)

    data = {'account': 'REQUESTER1'}

    response = requests.post('http://127.0.0.1:5000/get_account', json=data)
    print('REQUESTER1')
    print(response.text)


    response = requests.post('http://127.0.0.1:5000/get_account', json=data)
    print('REQUESTER1')
    print(response.text)
    assert result is not None

    data = {'req_addr': 'REQUESTER1',
            'data': {'hash': hash(str(cnnOut)),
                     'sol': {'name': 'hello',
                             'age': 1}
                     },
            'time_stamp': '201821199'
            }

    response = requests.post('http://127.0.0.1:5000/create_transaction_by_contract', json=data)
    print(response.text)

    data = {'account': 'MES'}

    response = requests.post('http://127.0.0.1:5000/get_account', json=data)
    print('MES')
    print(response.text)

    data = {'account': 'REQUESTER1'}

    response = requests.post('http://127.0.0.1:5000/get_account', json=data)
    print('REQUESTER1')
    print(response.text)