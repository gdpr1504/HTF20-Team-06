from flask_restful import Resource, reqparse
from db import query, connectToHost
import base64
import pymysql
from flask_jwt_extended import jwt_required

def convertToBlob(value):
    return base64.b64decode(value.encode('utf-8'))

class ComplaintPost(Resource):

    @jwt_required
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('roll', type=str, required=True, help="roll cannot be left blank!")
        parser.add_argument('aid', type=str, required=True, help="aid cannot be left blank!")
        parser.add_argument('culprit', type=str, required=True, help="culprit cannot be left blank!")
        parser.add_argument('time_c', type=str, required=True, help="time_c cannot be left blank!")
        parser.add_argument('place', type=str, required=True, help="place cannot be left blank!")
        parser.add_argument('details', type=str, required=True, help="details cannot be left blank!")
        parser.add_argument('level_of_threat', type=str, required=True, help="level_of_threat cannot be left blank!")
        parser.add_argument('image', type=str, required=False, default=None, help="image is null if left blank!")
        parser.add_argument('resolved', type=str, required=False, default=None, help="resolved is null if left blank!")
        data = parser.parse_args()
        
        data['resolved'] = "0"

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
            vals_tuple = (data["roll"], data["aid"], data["culprit"], data["time_c"], data["place"], data["details"], data["level_of_threat"], data["image"], data["resolved"])
            #convertToBlob is used to convert base64 string to BLOB data

            qstr = f""" INSERT INTO Complaints (roll, Aid, culprit, time_c, place, details, level_of_threat, image, resolved)
                    values (%s, %s, %s, %s, %s, %s, %s, %s, %s); """
            cursor.execute(qstr, vals_tuple)

            
            connection.commit() #commit the changes made
    
            #close the cursor and connection
            cursor.close()
            connection.close()

        except IndexError:
            """
            this is to handle tuple index error 
            which is raised if no data could be retrieved and stored
            where data is retrieved in this way
            result = cursor.fetchall()
            req_no = list(result[0].values())[0] 
            """
            return {
                "message" : "Required data not present."
            }, 400

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