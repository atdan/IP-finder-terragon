import redis
from flask import Flask, jsonify, make_response, request
import logging, requests, json, sys



app = Flask(__name__)

api = 'http://api.ipstack.com'
access_key = '37647849bacaa2dbc454ff7650896106'



index_name = 'id'
redis_server = '127.0.0.1'
redis_port = '5000'
r = redis.Redis(
    host=redis_server,
port=redis_port)






@app.route('/get-ip-details', methods=['GET'])
def checkIP():
    try:
        content = request.get_json(force = True)
        ip = content['ip']
        results = requests.get(api + '/' + str(ip) + '?access_key=' + 
                               access_key)

        result = json.loads(results.text)
        if(r.hexists(index_name, ip)):
            return r.hget(index_name, ip)


        else:
            
            result_value = {
                    'continent code': result['continent_code'],
                    'continent name': result['continent_name'],
                    'country code': result['country_code'],
                    'country name': result['country_name'],
                    'state code': result['region_code'],
                    'state name': result['region_name'],
                    'city': result['city'],
                    'longitude': result['longitude'],
                    'latitude': result['latitude']

                }
            r.hset(index_name,ip,result_value)
            return jsonify(result_value)
        pass
    except:
        return jsonify("An error occured")
        
if __name__ == '__main__'    :
    app.run(debug=True)
    
