from flask import Flask, request, jsonify
import db
import json
from app import app
# insert
@app.route('/api/smart', methods=['POST'])
def insert_smart():
    content = request.get_json()
    # insert data to db, to-do
    device_id = content['device_id']
    data = json.dumps(content['data']) 
    try:
        conn = db.createConnection() # make connection to postgres db
        cursor = conn.cursor()
        sql = """ 
			INSERT INTO smart (device_id, data) VALUES ('{}', '{}')
        """.format(device_id, data)
        print (f'sql: {sql}', flush=True)
        cursor.execute(sql) # execute the sql
        conn.commit() # data is saved to db
        cursor.close() # close connecion
        conn.close() # close connecion
        message = {
        'status' :200,
        'message' : 'Inserted!'
        }
        resp = jsonify(message)
        return resp
    except Exception as e:
        message = {
            'status': 500,
            'message': str(e)
        }
        resp = jsonify(message)
        resp.status_code = 500
        return resp

	
	

	