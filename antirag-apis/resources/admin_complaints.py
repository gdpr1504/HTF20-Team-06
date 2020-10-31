from flask_restful import Resource, reqparse
from db import query, connectToHost
import base64
import pymysql
from flask_jwt_extended import jwt_required

class AdminComplaints(Resource):
    @jwt_required
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('aid', type=str, help="aid cannot be left blank!")

        data = parser.parse_args()

        qstr = f""" select roll, Aid, culprit, time_c, place, 
        details, level_of_threat, cid, resolved from Complaints where Aid = '{data['aid']}'; """
        try:
            return query(qstr)
        except:
            return {
                "message" : "There was an error connecting to the Complaints table while retrieving."
            }, 500