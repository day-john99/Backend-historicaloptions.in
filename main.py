
# jiggy jiggy




from flask import Flask ,request, jsonify
import mysql.connector
from collections import OrderedDict

from flask_cors import CORS

app = Flask(__name__)

CORS(app)

str=0
temp_right = []       # list/array of dictionary
temp_key = {}         # dictionary
res=0



# Database connection
def get_db_connection():


   try:
    db_socket = "/cloudsql"
    instance_connection_name = "hardy-antonym-424411-h8:asia-south1:demooptions1"
    unix_socket_path = f"{db_socket}/{instance_connection_name}"

    connection = mysql.connector.connect(
        user='root',
        password='*********',
        database='stock',
        unix_socket= unix_socket_path
    )
    return connection

   except mysql.connector.Error as e:

     return {"error": e}  # Return a dictionary with the error message



# ITS HOME PAGE WHERE MESSAGE IS SEEN WHEN BASIC URL IS ACCESSED
@app.route('/', methods=['GET'])
def get_home_page():

    return "WELCOME TO HOME PAGE"


# once user selects a scrip this api transfers him list of expiry dates
@app.route('/api/expiries', methods=['GET'])
def get_expiry_data():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute('SELECT expiry_dates FROM expiry;')
    result = cursor.fetchall()
    cursor.close()
    connection.close()
    return jsonify(result)




# once user selects an expiry date ,and then selects call/put ; this api transfers him list of strikes
# for ,output of this api = strikes data , input req = primary keys of both (expiry date, call/put)
# so expiry date and call/put ,input is taken by user then their primary keys is found via some logic
@app.route('/api/strikes', methods=['GET'])
def get_strikes_list_data():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)


    val= request.args.get('expiry')              # accepts expiry date in string type via 'expiry' dictionary id
    right= request.args.get('right0')             # accepts whether call/put, in string type via 'right0' dictionary id

    # if else to check val is not empty
    if val :

        #  query1 fetches temp_key or eid or primary key of expiry dates
        query1 = 'SELECT eid FROM expiry WHERE expiry_dates=%s '
        cursor.execute(query1,(val,))
        temp_key = cursor.fetchone()
        print("\n*****************",temp_key)

        # query2 ,based on temp_key value ,fetches primary keys of both call/put of that specific expiry date
        query2 = 'SELECT oid FROM options_type WHERE f_eid=%s '
        cursor.execute(query2, (temp_key['eid'],))
        temp_right = cursor.fetchall()
        print("\n*****************", temp_right)

        # query1 and query2 outputs (temp_key , temp_right) are used here to get strikes ,call or put
        if (right=="call"):

            # query3 ,based on temp_key value, temp_right value ,fetches call strikes of that expiry date
            query3 = 'SELECT strikes FROM strikes_list WHERE ff_eid=%s AND f_oid=%s'
            cursor.execute(query3, (temp_key['eid'],temp_right[0]['oid']))
            str1 = cursor.fetchall()

        else:

            # query4 ,based on temp_key value, temp_right value ,fetches put strikes of that expiry date
            query4 = 'SELECT strikes FROM strikes_list WHERE ff_eid=%s AND f_oid=%s'
            cursor.execute(query4, (temp_key['eid'], temp_right[1]['oid']))
            str1 = cursor.fetchall()

    else:
        print('\n ERROR 2: EMPTY DATA, EXPIRY DATE')


    cursor.close()
    connection.close()
    return jsonify(str1)


# once user selects a strike, this api outputs him the price table
# for ,output of this api = price data , input req = primary keys of both (expiry date , call/put) , strike as it is
'''  expiry date and call/put ,input is taken by user then their primary keys is found via some logic ,also strike
 is input by user as it is'''

@app.route('/api/price', methods=['GET'])
def get_price_data():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    val = request.args.get('expiry')  # accepts expiry date in string type via 'expiry' dictionary id
    right = request.args.get('right1')  # accepts whether call/put, in string type via 'right1' dictionary id
    user_strike = request.args.get('strike')  # accepts strike in int type via 'strike' dictionary id

    # date and right type primary key to be found via below logic ,and stored in temp_key , temp_right

    #  query1 fetches temp_key or eid or primary key of expiry dates
    query1 = 'SELECT eid FROM expiry WHERE expiry_dates=%s '
    cursor.execute(query1, (val,))
    temp_key = cursor.fetchone()  # temp_key is dictionary like {'eid' : 102}
    print("\n*****************", temp_key)

    # query2 ,based on temp_key value ,fetches primary keys of both call/put of that specific expiry date
    query2 = 'SELECT oid FROM options_type WHERE f_eid=%s '
    cursor.execute(query2, (temp_key['eid'],))
    temp_right = cursor.fetchall()  # temp_right is a list of dict. like [ {'oid' : 1001} , {'oid' : 1002} ]
    print("\n*****************", temp_right)

    if right == "call":
        res = temp_right[0]['oid']
    elif right == "put":
        res = temp_right[1]['oid']          # res contains primary key of call/put


    # now primary key of expiry date and call/put, strike itself, is used to find primary key of strike table (sid)


    query10 = 'SELECT sid FROM strikes_list WHERE ff_eid=%s AND f_oid=%s AND strikes=%s '
    cursor.execute(query10 , (temp_key['eid'], res, user_strike) )
    temp_strike = cursor.fetchone()
    print('\n************** sid of strike: ', temp_strike)

    query11 = 'SELECT table_name FROM table_unique_fsid WHERE f_sid=%s '
    cursor.execute(query11 , (temp_strike['sid'],) )
    tab_nam = cursor.fetchone()
    print('\n *********** table is : ',tab_nam)

    table_name = tab_nam['table_name']
    query12 = f'SELECT * FROM {table_name}'
    cursor.execute(query12)
    results = cursor.fetchall()

    cursor.close()
    connection.close()

    # Reformatting the result
    reformatted_result = OrderedDict([
        ("stock_code", results[0]["d_stockcode"]),
        ("exchange_code", results[0]["d_exchange"]),
        ("product_type", results[0]["d_products"]),
        ("expiry_date", results[0]["d_expirydate"].strftime("%d-%b-%y")),
        ("strike_price", results[0]["d_strikeprice"]),
        ("right", results[0]["d_right"]),
        ("ohlc_data", [])
    ])

    for result in results:
        ohlc_entry = {
            "datetime": result["d_datetime"].strftime("%Y-%m-%d %H:%M:%S"),
            "open": result["d_open"],
            "high": result["d_high"],
            "low": result["d_low"],
            "close": result["d_close"],
            "volume": result["d_volume"],
            "open_interest": result["d_openinterest"],
            "count": result["d_count"]
        }
        reformatted_result["ohlc_data"].append(ohlc_entry)

    return jsonify(reformatted_result)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)

