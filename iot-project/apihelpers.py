from flask import request, jsonify
from app import app
import db
from flask import send_from_directory

# endpoint not found 
@app.errorhandler(404)
def not_found(error=None):
    message = {
        'status': 404,
        'message': 'Not Found: ' + request.url,
    }
    resp = jsonify(message)
    resp.status_code = 404    
    return resp

@app.route('/api/dump', methods=['GET'])
def dump_smart():
    try:
        
        conn = db.createConnection()
        cursor = conn.cursor()
        # get all signal names

        sql = """
            SELECT DISTINCT jsonb_object_keys(data) AS name 
            FROM smart
            ORDER BY name
        """
        cursor.execute(sql)
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        #generate signal colums
        #data ->> 'A3-16 dB level' as "A3-16 dB level",
        #data ->> 'A3_16_Vais_CO2' as " A3_16_Vais_CO2"
        names = ''
        name = ''
        for r in rows:
            name = name.join(r) # tuple to string,remove '()'
            names += (f"""data->>'{name}' as "{name}",""")
        names = names.rstrip(names[-1]) #remove the last comma
        
        sql2 = """
            SELECT id, device_id, date_time, data
            FROM smart
            ORDER BY id
        """.format(names)
        conn = db.createConnection()
        cursor = conn.cursor()
        cvs_output = "COPY (" + sql2 + ") TO STDOUT WITH CSV HEADER QUOTE '\b'"
        filename ='data.csv'
        with open(filename, 'w') as f_output:
             cursor.copy_expert(cvs_output, f_output)
        cursor.close()
        conn.close()
        return send_from_directory('', filename, as_attachment=False)

    except Exception as e:
        message = {
            'status': 500,
            'message': str(e)
        }
        resp = jsonify(message)
        resp.status_code = 500
        return resp