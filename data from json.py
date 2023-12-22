import requests
import json

with open('Group_GA14.json','r') as ofile:
 json_res=json.load(ofile)

flights = json_res.get('data',[])


selected_info = []
for flight in flights:
   if flight['flight']['iata'] =="PR3502" :
        selected_info.append({
            'IATA code': flight['flight']['iata'],
            'departure airport': flight['departure']['airport'],
            'original departure time': flight['departure']['scheduled'],
            'status': flight['flight_status']
        })
with open('Group_GAFlight.json', 'w') as file:
        json.dump(selected_info, file,indent=4) 

print("===")