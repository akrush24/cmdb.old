import sqlalchemy
engine = sqlalchemy.create_engine('mysql://cmdb:unix11@localhost/cmdb') # connect to server
engine.execute("CREATE DATABASE dbname") #create db
engine.execute("USE dbname") # select new db
