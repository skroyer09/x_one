from bottle import request, response
from icecream import ic
import re
import requests
import random

##############################
def disable_cache():
    response.add_header("Cache-Control", "no-cache, no-store, must-revalidate")
    response.add_header("Pragma", "no-cache")
    response.add_header("Expires", 0)   


##############################
def generate_random_color():
    """
    Generate a random color in hexadecimal format.
    """
    r = lambda: random.randint(0,255)
    return '#{:02x}{:02x}{:02x}'.format(r(),r(),r())


##############################

def db(query):
    try:
        url = "http://arangodb:8529/_api/cursor"
        res = requests.post( url, json = query )
        ic(res)
        ic(res.text)
        return res.json()
    except Exception as ex:
        print("#"*50)
        print(ex)
    finally:
        pass


##############################
USER_NAME_MIN = 2
USER_NAME_MAX = 20
USER_NAME_REGEX = "^.{2,20}$" 

def validate_user_name():
    error = f"user_name {USER_NAME_MIN} to {USER_NAME_MAX} characters"
    user_name = request.forms.get("user_name", "")
    user_name = user_name.strip()
    if not re.match(USER_NAME_REGEX, user_name): raise Exception(400, error)
    return user_name


##############################
USER_LAST_NAME_MIN = 2
USER_LAST_NAME_MAX = 20
USER_LAST_NAME_REGEX = "^.{2,20}$"

def validate_user_last_name():
    error = f"user_last_name {USER_LAST_NAME_MIN} to {USER_LAST_NAME_MAX} characters"
    user_last_name = request.forms.get("user_last_name", "")
    user_last_name = user_last_name.strip()
    if not re.match(USER_LAST_NAME_REGEX, user_last_name): raise Exception(400, error)
    return user_last_name


##############################
USER_NICK_NAME_MIN = 2
USER_NICK_NAME_MAX = 20
USER_NICK_NAME_REGEX = "^.{2,20}$"

def validate_nick_name():
    error = f"nick_name {USER_NICK_NAME_MIN} to {USER_NICK_NAME_MAX} characters"
    nick_name = request.forms.get("nick_name", "")
    nick_name = nick_name.strip()
    if not re.match(USER_NICK_NAME_REGEX, nick_name): raise Exception(400, error)
    return nick_name


##############################

def validate_user_gender():
    error = "Invalid gender selection"
    user_gender = request.forms.get("user_gender", "").strip()
    if user_gender not in ["male", "female", "other"]: raise Exception(400, error)
    return user_gender

