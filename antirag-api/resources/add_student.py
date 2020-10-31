from flask_restful import Resource, reqparse
from db import connectToHost, query
import base64
import pymysql
from flask_jwt_extended import jwt_required


userdb = 'Hackathonproject'

class AddStudent(Resource):
    @jwt_required
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('sname', type=str, required=True, help="sname cannot be left blank!")
        parser.add_argument('aid', type=str, required=True, help="aid cannot be left blank!")
        parser.add_argument('pword', type=str, required=True, help="pword cannot be left blank!")
        parser.add_argument('roll', type=str, required=True, help="roll cannot be left blank!")
        parser.add_argument('branch', type=str, required=True, help="branch cannot be left blank!")
        parser.add_argument('email', type=str, required=True, help="email cannot be left blank!")
        data = parser.parse_args()
        
        try:
            qstr = f""" 
            SELECT roll from Student where roll = "{ data['roll'] }";
            """
            usersWithRoll = query(qstr, return_json=False, connect_db=userdb)
        
        except Exception as e:
            return {
                "message" : "There was an error connecting to the Users table while checking for an existing user."  + str(e)
            }, 500

        if len(usersWithRoll)>0:
            return {
                "message" : "A student with the same roll number exists."
            }, 400


        qstr = f""" INSERT into Student (sname, aid, pword, branch, roll, email)
                values ('{data['sname']}', 
                '{data['aid']}', 
                '{data['pword']}', 
                '{data['branch']}', 
                '{data['roll']}', 
                '{data['email']}' ); """

        try:
            query(qstr, connect_db=userdb)
        except Exception as e:
            return {
                "message" : "Cannot add the student." + str(e)
            }, 500
        
        return {
            "message" : "Succesfully added student."
        }, 200