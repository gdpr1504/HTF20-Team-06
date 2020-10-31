from flask_restful import Resource, reqparse
from db import query
import pymysql
from flask_jwt_extended import jwt_required


class UnreadCount(Resource):
    
    #@jwt_required
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('roll', type=str, help="roll cannot be left blank!")
        data = parser.parse_args()
        #create query string
        qstr = f""" select count(roll) as unread
        from Unopened
        where roll="{data['roll']}"; """
        try:
            return query(qstr)
        except Exception as e:
            return {
                "message" : "There was an error connecting to the Unopened table while retrieving." + str(e)
            }, 500
