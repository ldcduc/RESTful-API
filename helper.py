from flask_restful import reqparse, abort, Api, Resource
from flaskext.mysql import MySQL
from flask import jsonify, make_response
from const import *
import pymysql
import json
import re

# mysql = MySQL()
# MySQL configurations
# app.config['MYSQL_DATABASE_USER'] = 'ducle'
# app.config['MYSQL_DATABASE_PASSWORD'] = '123465@B'
# app.config['MYSQL_DATABASE_DB'] = 'testDB'
# app.config['MYSQL_DATABASE_HOST'] = 'localhost'
# mysql.init_app(app)

# class Type Description
class TypeDescription():
    def __init__(self, null_=True, type_='str', min_value_= None, max_value_= None, min_length_= -1, max_length_= -1, regex_= None):
        self.allow_null = null_
        self.data_type = type_

        self.min_value = min_value_
        self.max_value = max_value_

        self.min_length = min_length_
        self.max_length = max_length_
        self.regex_to_check = regex_

class Validator():
    def __init__(self):
        Validator.thisdict = {TYPECODE_STRING: self.Validate_string, TYPECODE_DATE: self.Validate_date,
                              TYPECODE_PHONE: self.Validate_phone, TYPECODE_INT: self.Validate_number, }

    def Validate(self, value, description : TypeDescription):
        if value == None:
            return description.allow_null == True
        validate = self.Poly_validate(Validator.thisdict[description.data_type], value, description)
        return validate

    def Poly_validate(self, func, value, description : TypeDescription):
        return func(value, description)

    def Validate_date(self, value, description : TypeDescription):
        if description.regex_to_check != None:
            return False
        if description.min_value != None or description.max_value != None:
            return False
        if description.min_length != -1 or description.max_length != -1:
            return False
        #
        if self.Validate_string(value, description) == False:
            return False
        if re.match(REGEX_DATE, value) == None:
            return False
        return True

    def Validate_number(self, value, description : TypeDescription):
        if description.regex_to_check != None:
            return False
        if description.min_length != -1 or description.max_length != -1:
            return False
        #
        if (isinstance(value, int) or isinstance(value, float)) == False:
            return False
        if (description.min_value != None and description.min_value > value) or (description.max_value != None and description.max_value < value):
            return False
        return True

    def Validate_phone(self, value, description : TypeDescription):
        if description.regex_to_check != None:
            return False
        if description.min_length != -1 or description.max_length != -1:
            return False
        #
        if self.Validate_string(value, description) == False:
            return False
        if re.match(REGEX_PHONE, value) == None:
            return False
        return True

    def Validate_string(self, value, description : TypeDescription):
        if description.min_value != None or description.max_value != None:
            return False
        #
        if isinstance(value, str) == False:
            return False
        if (description.min_length != -1 and description.min_length > len(value)) or (description.max_length != -1 and description.max_length < len(value)):
            return False
        if description.regex_to_check != None and re.match(description.regex_to_check, value) == None:
            return False

        return True



# class Helper
class Helper():
    db_user = 'ducle'
    db_password = '123465@B'
    db_db = 'testDB'
    db_host = 'localhost'

    # data parser
    def Get_data(*arguments):
        parser = reqparse.RequestParser()
        res_list = []
        for argument in arguments:
            parser.add_argument(str(argument))

        args = parser.parse_args()
        for argument in arguments:
            value = args[str(argument)]
            res_list.append(value)
        return res_list

    def Return_result(self, result_number, result_string, *args):
        if args:
            result_string = result_string.format(args[0])
        if result_number < 300:
            return make_response(jsonify(successful=result_string), result_number)
        else:
            return make_response(jsonify(error=result_string), result_number)

    def Connect_to_database(self):
        connection = pymysql.connect(Helper.db_host, Helper.db_user, Helper.db_password, Helper.db_db)
        cursor = connection.cursor()

        return connection, cursor



# class Helper for User
class Helper_user(Helper):

    # get an user
    def Get_an_user(self, id_):
        # Directly create a connection to Database
        conn, cursor = self.Connect_to_database()

        # Execute a query
        query = "SELECT * FROM Users WHERE ID = (%s)"
        cursor.execute(query, (id_, ))
        db_res = cursor.fetchall()
            
        # Return result
        if len(db_res) > 0:
            return True, id_, db_res[0][1], db_res[0][2], db_res[0][3]
        return False, id_, None, None, None

    # validate user name
    def Validate_user_name(self, name):
        reg = re.search("^([A-Z][a-z]+)+(([',. -][A-Z][a-z]+)?)*$", name)
        # First letter of each word is uppercase, only one space between two words, no digit
        if reg != None and reg.group(0) == name:
                return True
        return False

    # validate user phone
    def Validate_phone(self, phone):
        if re.match("^[0-9]{10}$", phone):
            return True
        return False

    # Validate user ID format 
    def Validate_user_ID(self, id_):
        # Wrong ID format
        if re.match("^[0-9]{4}$", id_):
            return True
        return False

    # Validate date
    def Validate_date(self, date):
        if re.match("([12]\d{3}[-/](0[1-9]|1[0-2])[-/](0[1-9]|[12]\d|3[01]))", date):
            return True
        return False

    # Check if an user exists
    def Validate_user_exists(self, id_):
        # Directly create a connection to Database
        conn, cursor = self.Connect_to_database()

        # Execute a query
        query = "SELECT * FROM Users WHERE ID = (%s)"
        cursor.execute(query, (id_, ))
        db_res = cursor.fetchone()

        if db_res == None:
            return False
        else:
            return True

    # Insert an user
    def Add_an_user(self, id_, name, phone, birthdate):
        # Directly create a connection to Database
        conn, cursor = self.Connect_to_database()

        # Validate
            # User exists
        if self.Validate_user_exists(id_) == True:
            return RESPONSE_CONFLICT, USER_EXISTS

        ## Execute a query
        query = "INSERT INTO Users (ID, Name, Phone, Birthdate) VALUES (%s, %s, %s, %s)"
        cursor.execute(query, (id_, name, phone, birthdate, ))
        conn.commit()

        return RESPONSE_CREATED, USER_ADDED

    # Edit an user
    def Modify_an_user(self, id_, name=None, phone=None, birthdate=None):
        # Directly create a connection to Database
        conn, cursor = self.Connect_to_database()

        # Validate
            # User does not exist
        if self.Validate_user_exists(id_) == False:
            return RESPONSE_NOT_FOUND, USER_NOT_FOUND

        # Execute a query
        if phone != None:
            query = "UPDATE Users SET Phone = (%s) WHERE ID = (%s)"
            cursor.execute(query, (phone, id_, ))
        if name != None:
            query = "UPDATE Users SET Name = (%s) WHERE ID = (%s)"
            cursor.execute(query, (name, id_, ))
        if birthdate != None:
            query = "UPDATE Users SET Birthdate = (%s) WHERE ID = (%s)"
            cursor.execute(query, (birthdate, id_, ))
        conn.commit()

        return RESPONSE_CREATED, USER_MODIFIED

    # Remove an user
    def Delete_an_user(self, id_):
        # Directly create a connection to Database
        conn, cursor = self.Connect_to_database()

        # Validate
            # User does not exist
        if self.Validate_user_exists(id_) == False:
            return RESPONSE_NOT_FOUND, USER_NOT_FOUND

        # Execute a query
        sql = "DELETE FROM Users WHERE ID = (%s)"
        cursor.execute(sql, (id_, ))
        conn.commit()

        return RESPONSE_OK, USER_REMOVED

    def Return_an_user_in_json(self, id_, name, phone, birthday):
        return jsonify(id=id_, name=name, phone=phone, birthday=birthday)


# class Helper for Course
class Helper_course(Helper):
    def Get_a_course(self, id_):
        # Directly create a connection to Database
        conn, cursor = self.Connect_to_database()

        # Execute a query
        query = "SELECT * FROM Courses WHERE ID = (%s)"
        cursor.execute(query, (id_, ))
        db_res = cursor.fetchall()
            
        # Return result
        if len(db_res) > 0:
            return True, id_, db_res[0][1], db_res[0][2]
        return False, id_, None, None

    def Validate_name(self, name):
        reg = re.search("^([A-Z][a-z]+)+(([',. -][A-Z][a-z]+)?)*(\s[A-Z0-9]*)?$", name)
        if reg != None and reg.group(0) == name:
                return True
        return False

    def Validate_course_ID(self, id_):
        # Wrong course ID format
        if re.match("^[A-Z0-9]{5,6}$", id_):
            return True
        return False

    def Validate_course_exists(self, id_):
        # Directly create a connection to Database
        conn, cursor = self.Connect_to_database()

        # Execute a query
        query = "SELECT * FROM Courses WHERE ID = (%s)"
        cursor.execute(query, (id_, ))
        db_res = cursor.fetchone()

        if db_res == None:
            return False
        else:
            return True

    def Validate_capacity(self, capacity):
        if re.match('^[0-9]+$', capacity):
            return True
        return False

    def Add_a_course(self, id_, name, capacity):
        # Directly create a connection to Database
        conn, cursor = self.Connect_to_database()

        # Validate
            # Course exists
        if self.Validate_course_exists(id_):
            return RESPONSE_CONFLICT, COURSE_EXISTS

        # Execute a query
        query = "INSERT INTO Courses (ID, Name, Capacity) VALUES (%s, %s, %s)"
        cursor.execute(query, (id_, name, capacity, ))
        conn.commit()

        return RESPONSE_CREATED, COURSE_ADDED

    def Modify_a_course(self, id_, name=None, capacity=None):
        # Directly create a connection to Database
        conn, cursor = self.Connect_to_database()

        # Validate
            # Course does not exist
        if self.Validate_course_exists(id_) == False:
            return RESPONSE_NOT_FOUND, COURSE_NOT_FOUND

        # Execute a query
        if name != None:
            query = "UPDATE Courses SET Name = (%s) WHERE ID = (%s)"
            cursor.execute(query, (name, id_))
        if capacity != None:
            query = "UPDATE Courses SET Capacity = (%s) WHERE ID = (%s)"
            cursor.execute(query, (capacity, id_))

        conn.commit()

        return RESPONSE_OK, COURSE_MODIFIED

    def Delete_a_course(self, id_):
        # Directly create a connection to Database
        conn, cursor = self.Connect_to_database()

        # Validate
            # Course exists
        if self.Validate_course_exists(id_) == False:
            return RESPONSE_NOT_FOUND, COURSE_NOT_FOUND

        # Execute a query
        sql = "DELETE FROM Courses WHERE ID = (%s)"
        cursor.execute(sql, (id_, ))
        conn.commit()

        return RESPONSE_OK, COURSE_REMOVED
        
    

    def Return_a_course_in_json(self, id_, name, capacity):
        return jsonify(id=id_, name=name, capacity=capacity)

class Helper_user_course(Helper_user, Helper_course):
    def Validate_course_full(self, course_id):
        # Directly create a connection to Database
        conn, cursor = self.Connect_to_database()

        # Execute a query
        query = "SELECT * FROM Courses WHERE ID = (%s) AND Capacity > (SELECT COUNT(*) FROM Course_reg WHERE Course_id = (%s))"
        cursor.execute(query, (course_id, course_id, ) )
        db_res = cursor.fetchone()

        if db_res == None:
            return True
        else:
            return False

    def Validate_registered(self, user_id, course_id):
        # Directly create a connection to Database
        conn, cursor = self.Connect_to_database()

        # Execute a query
        query = "SELECT * FROM Course_reg WHERE User_id = (%s) AND Course_id = (%s)"
        cursor.execute(query, (user_id, course_id, ))
        db_res = cursor.fetchone()

        if db_res == None:
            return False
        else:
            return True

    def Get_registered_courses(self, user_id):
        # Directly create a connection to Database
        conn, cursor = self.Connect_to_database()

        # Validate
            # User exists
        if self.Validate_user_exists(user_id) == False:
            return RESPONSE_CONFLICT, USER_NOT_FOUND

        # Execute a query
        query = "SELECT C.ID, C.Name FROM Course_reg CR JOIN Courses C ON CR.Course_id = C.ID WHERE User_id = (%s)"
        cursor.execute(query, (user_id, ))
        db_res = cursor.fetchall()

        # Return a json list
        s = []
        for row in db_res:
            s.append(json.loads(json.dumps({"id":row[0], "name":row[1]})))
        return RESPONSE_OK, make_response(jsonify(result=s), RESPONSE_OK)


    def Register_a_course(self, user_id, course_id):
        # Directly create a connection to Database
        conn, cursor = self.Connect_to_database()

        # Validate
            # User exists
        if self.Validate_user_exists(user_id) == False:
            return RESPONSE_CONFLICT, USER_NOT_FOUND, user_id

            # Course exists
        if self.Validate_course_exists(course_id) == False:
            return RESPONSE_NOT_FOUND, COURSE_NOT_FOUND, course_id

            # User registered to this course
        if self.Validate_registered(user_id, course_id):
            return RESPONSE_CONFLICT, USER_REGISTER_COURSE, user_id

            # Course full
        if self.Validate_course_full(course_id) == True:
            return RESPONSE_CONFLICT, COURSE_FULL, course_id

        # Execute a query
        sql = "INSERT INTO Course_reg (User_id, Course_id) VALUES (%s, %s)"
        cursor.execute(sql, (user_id, course_id))
        conn.commit()

        return RESPONSE_CREATED, REGISTERED, None
