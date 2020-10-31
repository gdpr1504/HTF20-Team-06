from flask_restful import Resource, reqparse
from db import query
import pymysql
from flask_jwt_extended import jwt_required



class ViewComplaint(Resource):
    
    @jwt_required
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('cid', type=str, help="cid cannot be left blank!")
        data = parser.parse_args()
        #create query string
        qstr = f""" select * from Complaints where cid='{data['cid']}'; """
        try:
            return query(qstr)
        except Exception as e:
            return {
                "message" : "There was an error connecting to the Complaints table while retrieving." + str(e)
            }, 500
