from flask import Flask, jsonify, make_response, render_template
from flask_restful import reqparse, abort, Api, Resource
from helper import *
from const import *

app = Flask(__name__)
app.config.from_pyfile('config.cfg')
api = Api(app)


class User(Resource):
    def get(self):
        helper = Helper_user()
        # Parse arguments
        [dummy, id_] = helper.Get_data("id")

        ## VALIDATION
        validator = Validator()

            # Validate ID
        if validator.Validate(id_, TypeDescription(False, TYPECODE_STRING, min_length_=4, max_length_=6, regex_=REGEX_USER_ID)) == False:
            return helper.Return_result(RESPONSE_BAD_REQUEST, INVALID_ID)

        ## EXECUTION
        result, id_, name, phone, birthdate = helper.Get_an_user(id_)

        ## Return result
        if result == True:
            return helper.Return_an_user_in_json(id_, name, phone, birthdate)
        else:
            return helper.Return_result(RESPONSE_NOT_FOUND, USER_NOT_FOUND, id_)

    def post(self):
        helper = Helper_user();

        ## Parse arguments
        [dummy, id_, name, phone, birthdate] = helper.Get_data("id", "name", "phone", "birthdate")

        ## VALIDATION
        validator = Validator()

            # Validate ID
        if validator.Validate(id_, TypeDescription(False, TYPECODE_STRING, min_length_=4, max_length_=6, regex_=REGEX_USER_ID)) == False:
            return helper.Return_result(RESPONSE_BAD_REQUEST, INVALID_ID)

            # Validate name
        if validator.Validate(name, TypeDescription(False, TYPECODE_STRING, min_length_=2, max_length_=30, regex_=REGEX_NAME)) == False:
            return helper.Return_result(RESPONSE_BAD_REQUEST, INVALID_NAME)

            # Validate phone
        if validator.Validate(phone, TypeDescription(False, TYPECODE_PHONE)) == False:
            return helper.Return_result(RESPONSE_BAD_REQUEST, INVALID_PHONE)

            # Validate date
        if validator.Validate(birthdate, TypeDescription(False, TYPECODE_DATE)) == False:
            return helper.Return_result(RESPONSE_BAD_REQUEST, INVALID_DATE)

        ## EXECUTION
        response_code, response_mess = helper.Add_an_user(id_, name, phone, birthdate)

        ## RESULT
            # 2 cases:
            # user exists
            # successful
        return helper.Return_result(response_code, response_mess, id_)

    def put(self):
        helper = Helper_user()

        ## Parse arguments
        [dummy, id_, name, phone, birthdate] = helper.Get_data("id", "name", "phone", "birthdate")
        if name == "":
            name = None
        if phone == "":
            phone = None
        if birthdate == "":
            birthdate = None

        ## VALIDATION
        validator = Validator()

            # Validate ID
        if validator.Validate(id_, TypeDescription(False, TYPECODE_STRING, min_length_=4, max_length_=6, regex_=REGEX_USER_ID)) == False:
            return helper.Return_result(RESPONSE_BAD_REQUEST, INVALID_ID)

            # Validate name if exists
        if validator.Validate(name, TypeDescription(True, TYPECODE_STRING, min_length_=2, max_length_=30, regex_=REGEX_NAME)) == False:
            return helper.Return_result(RESPONSE_BAD_REQUEST, INVALID_NAME)

            # Validate phone if exists
        if validator.Validate(phone, TypeDescription(True, TYPECODE_PHONE)) == False:
            return helper.Return_result(RESPONSE_BAD_REQUEST, INVALID_PHONE)

            # Validate date if exists
        if validator.Validate(birthdate, TypeDescription(True, TYPECODE_DATE)) == False:
            return helper.Return_result(RESPONSE_BAD_REQUEST, INVALID_DATE)

            # Make sure at least one field is supplied
        if name == None and phone == None and birthdate == None:
            return helper.Return_result(RESPONSE_NOT_FOUND, ONE_REQUIRED)

        ## EXECUTION
        response_code, response_mess = helper.Modify_an_user(id_, name, phone, birthdate)

        ## RESULT
            # 2 cases:
            # User does not exist
            # Sucessful
        return helper.Return_result(response_code, response_mess, id_)

    def delete(self):
        helper = Helper_user()

        ## Parse arguments
        [dummy, id_] = helper.Get_data("id")

        ## VALIDATION
        validator = Validator()

        # Validate ID
        if validator.Validate(id_, TypeDescription(False, TYPECODE_STRING, min_length_=4, max_length_=6, regex_=REGEX_USER_ID)) == False:
            return helper.Return_result(RESPONSE_BAD_REQUEST, INVALID_ID)

        ## EXECUTION
        response_code, response_mess = helper.Delete_an_user(id_)

        ## RESULT
            # 2 cases:
            # User does not exist
            # Successfully remove
        return helper.Return_result(response_code, response_mess, id_)


class Course(Resource):
    def get(self):
        helper = Helper_course()
        # Parse arguments
        [dummy, id_] = helper.Get_data("id")

        ## VALIDATION
        validator = Validator()

            # Validate ID
        if validator.Validate(id_, TypeDescription(False, TYPECODE_STRING, min_length_=5, max_length_=6, regex_=REGEX_COURSE_ID)) == False:
            return helper.Return_result(RESPONSE_BAD_REQUEST, INVALID_ID)

        ## EXECUTION
        result, id_, name, capacity = helper.Get_a_course(id_)

        ## Return result
        if result == True:
            return helper.Return_a_course_in_json(id_, name, capacity)
        else:
            return helper.Return_result(RESPONSE_NOT_FOUND, COURSE_NOT_FOUND, id_)

    def post(self):
        helper = Helper_course();

        ## Parse arguments
        [dummy, id_, name, capacity] = helper.Get_data("id", "name", "capacity")
        if capacity != None:
            capacity = int(capacity)

        ## VALIDATION
        validator = Validator()

            # Validate course ID
        if validator.Validate(id_, TypeDescription(False, TYPECODE_STRING, min_length_=5, max_length_=6, regex_=REGEX_COURSE_ID)) == False:
            return helper.Return_result(RESPONSE_BAD_REQUEST, INVALID_ID)

            # Validate name
        if validator.Validate(name, TypeDescription(False, TYPECODE_STRING, min_length_=1, max_length_=40, regex_=REGEX_COURSE_NAME)) == False:
            return helper.Return_result(RESPONSE_BAD_REQUEST, INVALID_NAME)

            # Validate capacity
        if validator.Validate(capacity, TypeDescription(False, TYPECODE_INT, min_value_=1, max_value_=100)) == False:
            return helper.Return_result(RESPONSE_BAD_REQUEST, INVALID_CAPACITY)

        ## EXECUTION
        response_code, response_mess = helper.Add_a_course(id_, name, capacity)

        ## RESULT
            # 2 Cases:
            # Course exists
            # Successfully added
        return helper.Return_result(response_code, response_mess, id_)

    def put(self):
        helper = Helper_course()

        ## Parse arguments
        [dummy, id_, name, capacity] = helper.Get_data("id", "name", "capacity")
        if name == "":
            name = None
        if capacity == "":
            capacity = None
        elif capacity != None:
            capacity = int(capacity)

        ## VALIDATION
        validator = Validator()
            # Validate course ID
        if validator.Validate(id_, TypeDescription(False, TYPECODE_STRING, min_length_=5, max_length_=6, regex_=REGEX_COURSE_ID)) == False:
            return helper.Return_result(RESPONSE_BAD_REQUEST, INVALID_ID)

            # Validate name
        if validator.Validate(name, TypeDescription(True, TYPECODE_STRING, min_length_=1, max_length_=40, regex_=REGEX_COURSE_NAME)) == False:
            return helper.Return_result(RESPONSE_BAD_REQUEST, INVALID_NAME)

            # Validate capacity
        if validator.Validate(capacity, TypeDescription(True, TYPECODE_INT, min_value_=1, max_value_=100)) == False:
            return helper.Return_result(RESPONSE_BAD_REQUEST, INVALID_CAPACITY)

        if name == None and capacity == None:
            return helper.Return_result(RESPONSE_BAD_REQUEST, ONE_REQUIRED)

        ## EXECUTION
        response_code, response_mess = helper.Modify_a_course(id_, name, capacity)

        ## RESULT
            # 2 Cases:
            # Course does not exist
            # Successfully modified
        return helper.Return_result(response_code, response_mess, id_)

    def delete(self):
        helper = Helper_course()

        ## Parse arguments
        [dummy, id_] = helper.Get_data("id")

        ## VALIDATION
        validator = Validator()

            # Validate ID
        if validator.Validate(id_, TypeDescription(False, TYPECODE_STRING, min_length_=5, max_length_=6, regex_=REGEX_COURSE_ID)) == False:
            return helper.Return_result(RESPONSE_BAD_REQUEST, INVALID_ID)

        ## EXECUTION
        response_code, response_mess = helper.Delete_a_course(id_)

        ## RESULT
            # 2 cases:
            # Course does not exist
            # Successfully removed
        return helper.Return_result(response_code, response_mess, id_)


class Registration(Resource):
    def get(selfs):
        helper = Helper_user_course()
        # Parse arguments
        [dummy, user_id] = helper.Get_data("id")

        ## VALIDATION
        validator = Validator()

            # Validate ID
        if validator.Validate(user_id, TypeDescription(False, TYPECODE_STRING, min_length_=4, max_length_=6, regex_=REGEX_USER_ID)) == False:
            return helper.Return_result(RESPONSE_BAD_REQUEST, INVALID_ID)

        ## EXECUTION
        response_code, response_mess = helper.Get_registered_courses(user_id)

        ## Return result
        if response_code == RESPONSE_CONFLICT:
            return helper.Return_result(response_code, response_mess, user_id)

        return response_mess

    def post(self):
        helper = Helper_user_course()

        ## PARSE ARGUMENTS
        [dummy, user_id, course_id] = helper.Get_data("user id", "course id")

        ## VALIDATION
        validator = Validator()

            # Validate user ID
        if validator.Validate(user_id, TypeDescription(False, TYPECODE_STRING, min_length_=4, max_length_=6, regex_=REGEX_USER_ID)) == False:
            return helper.Return_result(RESPONSE_BAD_REQUEST, INVALID_USER_ID)

            # Validate course ID
        if validator.Validate(course_id, TypeDescription(False, TYPECODE_STRING, min_length_=5, max_length_=6, regex_=REGEX_COURSE_ID)) == False:
            return helper.Return_result(RESPONSE_BAD_REQUEST, INVALID_COURSE_ID)

        ## EXECUTION
        response_code, response_mess, parameter = helper.Register_a_course(user_id, course_id)

        ## RESULT
        return helper.Return_result(response_code, response_mess, parameter)


api.add_resource(User, "/users")
api.add_resource(Course, "/courses")
api.add_resource(Registration, "/register")

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/users/')
def users_page():
    return render_template('users.html')

@app.route('/courses/')
def courses_page():
    return render_template('courses.html')

@app.route('/register/')
def register_page():
    return render_template('register.html')

if __name__ == '__main__':
    app.run()
