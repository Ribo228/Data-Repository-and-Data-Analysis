SELECT date_trunc('hour', date_time) + INTERVAL '30 min' * round(date_part('minute', date_time) / 30.0) as time, 
round(avg((data->>'A3_16_Vais_CO2')::numeric), 2)
from smart 
where data->>'A3_16_Vais_CO2' is not null and date_trunc('hour', date_time) between '2021-11-13' and '2021-11-14'
group by time

def home():
    message = {
        'status': 200,
        'message': 'Hello from Smart IoT!' ,
    }
    resp = jsonify(message)
    resp.status_code = 200
    return resp
@app.route('/api/smart')
def get_data():
    try:
        conn = db.createConnection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        sql = """
            SELECT device_id, date_trunc('second', date_time) as date_time, data
            FROM smart
            ORDER BY id DESC
            LIMIT 500
        """
        cursor.execute(sql)
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        resp = jsonify(rows)
        resp.status_code = 200
        return resp
    except Exception as e:
        message = {
            'status': 500,
            'message': str(e)
        }
    resp = jsonify(message)
    resp.status_code = 500
    return resp
@app.route('/api/signal/<signal>/interval/<float:inter>/start/<start>/end/<end>')
def signal_interval(signal, inter, start, end):
    try:
        conn = db.createConnection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        sql = """
            SELECT date_trunc('hour', date_time) + INTERVAL '{} min' * round(date_part('minute', date_time) / {}) as time, 
            round(avg((data->>'{}')::numeric), 2) as "{}"
            from smart 
            where data->>'{}' is not null and date_trunc('hour', date_time) between '{}' and '{}'
            group by time
        """.format(inter, inter, signal, signal, signal, start, end)
        cursor.execute(sql)
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        resp = jsonify(rows)
        resp.status_code = 200
        return resp
    except Exception as e:
        message = {
            'status': 500,
            'mesage': str(e)
        }
        resp = jsonify(message)
        resp.status_code = 500
        return resp

# @app.route('/api/reset', methods=['POST'])
# def reset_smart():  
#     try:
#         conn = db.createConnection()
#         cursor = conn.cursor()
#         sql = """
#             TRUNCATE TABLE smart RESTART IDENTITY;
#         """
#         cursor.execute(sql)
#         conn.commit()
#         cursor.close() 
#         conn.close()
#         message = {
#             'status': 200,
#             'message': 'Reseted!'
#         }
#         resp = jsonify(message)
#         return resp
#     except Exception as e:
#         message = {
#             'status': 500,
#             'message': str(e)
#         }
#         resp = jsonify(message)
#         resp.status_code = 500
#         return resp
