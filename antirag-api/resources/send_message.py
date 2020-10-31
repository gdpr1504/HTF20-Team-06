from flask_restful import Resource, reqparse
from db import query, connectToHost
import base64
import pymysql
from flask_jwt_extended import jwt_required

class SendMessage(Resource):
    
    @jwt_required
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('roll', type=str, required=True, help="roll cannot be left blank!")
        parser.add_argument('message', type=str, required=True, help="message cannot be left blank!")
        parser.add_argument('cid', type=str, required=True, help="cid cannot be left blank!")
        data = parser.parse_args()
        


        # a transaction is made, so not using query function from db module
        # we use connectToHost function from db module and commit explicitly
        # the query function from db module commits for each query which is not desirable in 
        # a transaction sequence as follows.
        # here we execute several queries then commit.
        try:
            connection = connectToHost()
            #start connection, create cursor and execute query from cursor
            connection.begin()
            cursor = connection.cursor()


            #creating a tuple of values to be inserted because a formatted string is used
            #here its useful to avoid SQL syntax errors while inserting BLOB value into table
            vals_tuple = (data['roll'], data['message'], data['cid'])
            #convertToBlob is used to convert base64 string to BLOB data

            qstr = f""" INSERT INTO Message (roll, message, cid)
                    values ("{data['roll']}", "{data['message']}", "{data['cid']}"); """
            
            cursor.execute(qstr)


            qstr = f"""
            update Complaints
            set resolved = 1
            where cid = '{data['cid']}';
            """

            cursor.execute(qstr) 
            
            
            connection.commit() #commit the changes made
    
            #close the cursor and connection
            cursor.close()
            connection.close()       

        except (pymysql.err.InternalError, pymysql.err.ProgrammingError, pymysql.err.IntegrityError) as e:
            return {
                "message" : "MySQL error: " + str(e)
            }, 500
        except Exception as e:
            return {
                "message" : "There was an error connecting to the requests table while inserting." + str(e)
            }, 500
        
        return {
            "message" : "Succesfully inserted"
        }, 200