from flask_restful import Resource, reqparse
from db import query
from flask_jwt_extended import create_access_token, jwt_required
from werkzeug.security import safe_str_cmp

class Student():
    def __init__(self,roll,pword):
        self.roll=roll
        self.pword=pword

    @classmethod
    def getStudentByRoll(cls,roll):
        result=query(f"""SELECT roll,pword FROM Student WHERE roll='{roll}'""",return_json=False)
        if len(result)>0: return Student(result[0]['roll'],result[0]['pword'])
        return None


class StudentLogin(Resource):
    
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('roll', type=str, help="roll cannot be left blank!")
        parser.add_argument('pword', type=str, help="pword cannot be left blank!")
        
        data = parser.parse_args()

        #create query string
        qstr = f""" 
        select * from Student
        WHERE roll='{data['roll']}';
        """
        try:
            return query(qstr)
        except Exception as e:
            return {
                "message" : "There was an error connecting to the database while retrieving." + str(e)
            }, 500

class StudentLogin(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('roll', type=str, required=True,
                            help="roll cannot be left blank!")
        parser.add_argument('pword', type=str, required=True,
                            help="pword cannot be left blank!")
        data=parser.parse_args()
        student=Student.getStudentByRoll(data['roll'])
        if student and safe_str_cmp(student.pword,data['pword']):
            access_token=create_access_token(identity=student.roll,expires_delta=False)
            return {'roll': data['roll'] , 'access_token':access_token, 'admin': 0},200
        return {"message":"Invalid Credentials!"}, 401
