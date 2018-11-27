RESPONSE_OK = 200 
RESPONSE_CREATED = 201
RESPONSE_BAD_REQUEST = 400
RESPONSE_UNAUTHORIZED = 401
RESPONSE_NOT_FOUND = 404
RESPONSE_METHOD_NOT_ALLOWED = 405
RESPONSE_CONFLICT = 409
RESPONSE_INTERNAL_SERVER_ERROR = 500


USER_ADDED     = "User with ID {} has been added"
USER_REMOVED   = "User with ID {} has been removed"
USER_MODIFIED  = "User with ID {} has been modified"
COURSE_ADDED   = "Course with ID {} has been added"
COURSE_REMOVED = "Course with ID {} has been removed"
COURSE_MODIFIED= "Course with ID {} has been modified"

REGISTERED     = "Registered"

USER_EXISTS    = "User with ID {} already exists"
COURSE_EXISTS  = "Course with ID {} already exists"
USER_REGISTER_COURSE = "User with ID {} already registered this course"

BAD            = "Bad request!"
NO_ID          = "An ID is expected"
NO_NAME_NOR_PH = "A name or a phone number is expected"
INVALID_ID     = "Invalid ID"
INVALID_USER_ID   = "Invalid user ID"
INVALID_COURSE_ID = "Invalid course ID"
INVALID_NAME   = "Invalid name"
INVALID_PHONE  = "Invalid phone"
INVALID_BIRTH  = "Invalid birthdate"
INVALID_CAPACITY = "Invalid course capacity"
INVALID_DATE = "Invalid date"
ONE_REQUIRED   = "One parameter is required"
NOT_ENOUGH_3   = "3 parameters are expected"

USER_NOT_FOUND = "User with ID {} not found"
COURSE_NOT_FOUND = "Course with ID {} not found"

COURSE_FULL    = "Course with ID {} is full"

REGEX_USER_ID   = r"^[0-9]+$"
REGEX_NAME      = r"^([A-Z][a-z]+)+(([',. -][A-Z][a-z]+)?)*$"
REGEX_COURSE_ID = r"^[A-Z]{2,3}[0-9]{3}$"
REGEX_COURSE_NAME = r"^([A-Z][a-z]+)+(([',. -][A-Z][a-z]+)?)*(\s[A-Z0-9]*)?$"
REGEX_DATE      = r"([12]\d{3}([-\/])(0[1-9]|1[0-2])\2(0[1-9]|[12]\d|3[01]))"
REGEX_PHONE     = r"^\(?(0[1-9]{2})\)?([ .-]?)([0-9]{3})\2([0-9]{4})$"

TYPECODE_STRING = "str"
TYPECODE_DATE   = "date"
TYPECODE_PHONE  = "phone"
TYPECODE_INT    = "int"
TYPECODE_FLOAT  = "float"
