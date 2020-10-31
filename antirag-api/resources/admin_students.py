from flask_restful import Resource, reqparse
from db import query
import pymysql
from flask_jwt_extended import jwt_required



class AdminStudents(Resource):
    
    @jwt_required
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('aid', type=str, help="aid cannot be left blank!")

        data = parser.parse_args()
        #create query string
        
        qstr = f""" select sname, Aid, branch, phone, roll, 
        email, pphone, address from Student where Aid = '{data['aid']}'; """
        try:
            return query(qstr)
        except:
            return {
                "message" : "There was an error connecting to the Student table while retrieving."
            }, 500
