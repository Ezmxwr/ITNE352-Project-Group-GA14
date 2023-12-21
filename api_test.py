import requests
import json


params = {
  'access_key': 'fcd54fda53bc3908921d2821cca1cbb7',
  'flight_iata': 'mh1037',
  'limit':100
  # Arrival airport ICAO code for Bahrain International Airport 
}

api_result = requests.get('http://api.aviationstack.com/v1/flights', params)
"""  api_response = api_result.json()
print(api_response)  """
if api_result.status_code == 200:
    #api_response = api_result.json()
    json_res=api_result.json()
    flights = json_res.get('data',[]) #get the value associated with the key 'data' in the json_res dictionary
                                      #[] to return empty list if there is no match with the key( your code will not break)
    print(json_res)



selected_info = []
for flight in flights:

        selected_info.append({
            'IATA code': flight['flight']['iata'],
            'departure airport': flight['departure']['airport'],
            'original departure time': flight['departure']['scheduled'],
            'status': flight['flight_status']
        })
with open('Group_GAFlight.json', 'w') as file:
        json.dump(selected_info, file,indent=4) 








   
        """ if 'data' in api_response and 'flights' in api_response['data']:
            # Iterate over each flight in the data
            for flight in api_response['data']['flights']:
                print(flight)
                # Extract specific information
                airline_name = flight['airline']['name']
                flight_iata = flight['flight']['iata']
                departure_airport = flight['departure']['airport']
                departure_iata = flight['departure']['iata']
                arrival_airport = flight['arrival']['airport']
                arrival_iata = flight['arrival']['iata']

                # Print or use the extracted information as needed
                print(f'{airline_name} flight {flight_iata} from {departure_airport} ({departure_iata}) to {arrival_airport} ({arrival_iata})') """