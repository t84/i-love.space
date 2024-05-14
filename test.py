import requests
while True:
    response = requests.get('http://localhost:5000/api/update_iss')
    
    # Check if the response is successful
    if response.status_code == 200:
        # Check the X-Cache header to see if the response is from cache
        cache_status = response.headers.get('X-Cache')
        if cache_status:
            print(f'Response served from cache: {cache_status}')
        else:
            print('Response not served from cache')
    
        # Print the response data
        print(response.json())
    else:
        print(f'Error: {response.status_code}')
