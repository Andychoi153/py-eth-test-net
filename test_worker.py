addr = [1,2]
cnnOut = 2
import requests
import time
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
    assert response.text is not None

    data = {'account': 'REQUESTER1'}

    response = requests.post('http://127.0.0.1:5000/get_account', json=data)
    print('REQUESTER1')
    print(response.text)
    assert response.text is not None



    response = requests.post('http://127.0.0.1:5000/get_account', json=data)
    print('REQUESTER1')
    print(response.text)
    assert response.text is not None

    data = {'req_addr': 'REQUESTER1',
            'data': {'hash': hash(str(cnnOut)),
                     'sol': {'name': 'hello',
                             'age': 1}
                     },
            'time_stamp': '201821199'
            }

    response = requests.post('http://127.0.0.1:5000/send_detect_data', json=data)
    assert response.text is not None

    data = {'account': 'MES'}

    time.sleep(5)
    response = requests.post('http://127.0.0.1:5000/send_block_info')
    assert response.text is not None

    response = requests.post('http://127.0.0.1:5000/get_account', json=data)
    print('MES')
    assert response.text is not None

    response = requests.post('http://127.0.0.1:5000/get_account', json=data)
    print('MES')
    assert response.text is not None

    data = {'account': 'REQUESTER1'}

    response = requests.post('http://127.0.0.1:5000/get_account', json=data)
    print('REQUESTER1')
    assert response.text is not None

    response = requests.post('http://127.0.0.1:5000/get_account', json=data)
    print('REQUESTER1')
    assert response.text is not None
