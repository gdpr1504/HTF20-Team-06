from flask_restful import Resource, reqparse
from db import query, connectToHost, encode
import base64
import pymysql
from flask_jwt_extended import jwt_required

class ViewMessages(Resource):
    
    @jwt_required

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('roll', type=str, required=True, help="roll cannot be left blank!")
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

   

            qstr = f"""
            select Message.roll, message, Message.cid, place, time_c
            from Message join Complaints
            on Message.cid = Complaints.cid
            where Message.roll = '{data['roll']}'
            order by cid desc;
            """

            cursor.execute(qstr) 
            result = encode(cursor.fetchall())

            qstr = f"""
            delete from Unopened
            where roll = '{data['roll']}';
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
                "message" : "There was an error connecting." + str(e)
            }, 500
        
        return result, 200