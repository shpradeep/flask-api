import mysql.connector
import json
from datetime import date
from flask import make_response

class user_model():
    def __init__(self):
        try:
            self.con = mysql.connector.connect(host="localhost", username="root", password="", database="flask_db")
            self.con.autocommit=True
            self.cur = self.con.cursor(dictionary=True)
            print("connection successfull")
        except:
            print('some errors')
    def user_getall_model(self):
            self.cur.execute(f"SELECT c.*, p.plan_name, DATE_FORMAT(c.registration_date, '%d-%m-%Y') AS date, DATE_FORMAT(c.birthdate, '%d-%m-%Y') AS bdate, DATE_FORMAT(c.plan_renewal_date, '%d-%m-%Y') AS rdate FROM customer c LEFT JOIN plan p ON p.id = c.plan_id")
            result = self.cur.fetchall()
            if (len(result)):
                res = make_response({"payload": result}, 200)
                res.headers['Access-Control-Allow-Origin'] = '*'
                return res
            return make_response({"payload": []}, 204)
    
    def user_getplan_model(self, user_id):
            self.cur.execute(f"SELECT p.id, p.plan_name FROM customer c LEFT JOIN plan p ON p.id = c.plan_id WHERE c.id = {user_id} LIMIT 1")
            result = self.cur.fetchall()
            if (len(result)):
                res = make_response({"payload": result}, 200)
                res.headers['Access-Control-Allow-Origin'] = '*'
                return res
            return make_response({"payload": []}, 204)

    def user_addone_model(self, data):
            try:
                today = date.today()
                self.cur.execute(f"INSERT INTO customer(name, birthdate, email, adhar_number, registration_date, mobile, plan_id, plan_renewal_date, plan_status) VALUES('{data['username']}', '{data['dob']}', '{data['email']}', '{data['adhar']}', '{data['date']}', '{data['mobile']}', '{data['plan_id']}', '{today}', '{data['plan_status']}')")
                if (self.cur.rowcount > 0):
                    res = make_response({"message": "Customer added successfully"}, 201)
                    res.headers['Access-Control-Allow-Origin'] = '*'
                    return res
            except KeyError as e:
                res = make_response({"error": 'Something went wrong' + e}, 500)
                res.headers['Access-Control-Allow-Origin'] = '*'

    def user_update_model(self, data):
            if 'plan_id' in data:
                self.cur.execute(f"UPDATE customer SET plan_renewal_date = '{data['date']}', plan_id = '{data['plan_id']}', plan_status = '{data['plan_status']}' where id = {data['user_id']}")
            else:
                self.cur.execute(f"UPDATE customer SET plan_renewal_date = '{data['date']}', plan_status = '{data['plan_status']}' where id = {data['user_id']}")
            if (self.cur.rowcount > 0):
                res = make_response({"message": "User updated successfully"}, 200)
                res.headers['Access-Control-Allow-Origin'] = '*'
                return res
                # return make_response({"message": "User updated successfully"}, 200)
            return make_response({"message": "Nothing to update"}, 202)