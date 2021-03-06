# /usr/bin/python2.7
import psycopg2
from configparser import ConfigParser
from flask import Flask, request, render_template, g, abort
import time
import redis

def config(filename='config/database.ini', section='postgresql'):
    # create a parser
    parser = ConfigParser()
    # read config file
    parser.read(filename)

    # get section, default to postgresql
    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception('Section {0} not found in the {1} file'.format(section, filename))

    return db

def fetch(sql):
    ttl = 20
    try:
       params = config(section='redis')
       cache = redis.Redis.from_url(params['redis_url'])
       results = cache.get(sql) 
    	
       if results:
          return results
       else:
          # connect to database listed in datbase.ini
          conn = connect()
          cur = conn.cursor()
          cur.execute(sql)
          # fetch one row
          results = cur.fetchone()
          print('Closing connection to database...')
          cur.close()
          conn.close()
         
          # cache results
          cache.setex(sql, ttl, ''.join(results))
          return results
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

    # connect to database listed in database.ini
    #conn = connect()
    #if(conn != None):
     #   cur = conn.cursor()
     #   cur.execute(sql)
        
        # fetch one row
      #  retval = cur.fetchone()
        
        # close db connection
       # cur.close() 
        #conn.close()
        #print("PostgreSQL connection is now closed")

       # return retval
    #else:
     #   return None    

def connect():
    """ Connect to the PostgreSQL database server and return a cursor """
    conn = None
    try:
        # read connection parameters
        params = config()

        # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params)
        
                
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error:", error)
        conn = None
    
    else:
        # return a conn
        return conn

app = Flask(__name__) 

@app.before_request
def before_request():
   g.request_start_time = time.time()
   g.request_time = lambda: "%.5fs" % (time.time() - g.request_start_time)

@app.route("/")     
def index():
    sql = 'SELECT slow_version();'
    db_result = fetch(sql)

    if(db_result):
       print(type(db_result) is tuple ) 
       db_version = ''.join(db_result) if type(db_result) is tuple  else db_result
      #db_version = ''.join(db_result)
      # db_version = ','.join([str(i) for i in db_result])    
    else:
        abort(500)
    params = config()
    return render_template('index.html', db_version = db_version, db_host = params['host'])

if __name__ == "__main__":        # on running python app.py
    app.run()                     # run the flask app