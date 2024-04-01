from bottle import delete, get, post, put, request, static_file, template
import x, re
from icecream import ic
from x import generate_random_color


# arangoDB = 127.0.0.1:8529 # 
# live side = 127.0.01 # 

##############################
@get("/favicon.ico")
def _():
    return static_file("favicon.ico", ".")

##############################
@get("/app.css")
def _():
    return static_file("app.css", ".")

##############################
@get("/mixhtml.js")
def _():
    return static_file("mixhtml.js", ".")

##############################
@get("/test")
def _():
    try:
        return template("test")
    except Exception as ex:
        pass
    finally:
        pass


##############################
@get("/")
def _():
    try:
        x.disable_cache()
        users = x.db({"query":"FOR user IN users RETURN user"})
        return template("index", users=users["result"])
    except Exception as ex:
        ic(ex)
        return "system under maintainance"         
    finally:
        pass

##############################
@post("/users")
def _():
    try:
        user_name = x.validate_user_name()
        user_last_name = x.validate_user_last_name()
        nick_name = x.validate_nick_name()
        user_gender = x.validate_user_gender()
        ic(user_last_name)
        user = {"name":user_name, "last_name":user_last_name, "nick_name":nick_name, "user_gender":user_gender}
        res = x.db({"query":"INSERT @doc IN users RETURN NEW", "bindVars":{"doc":user}})
        html = template("_user.html", user=res["result"][0])
        form_create_user =  template("_form_create_user.html")
        return f"""
        <template mix-target="#users" mix-top>
            {html}
        </template>
        <template mix-target="#frm_user" mix-replace>
            {form_create_user}
        </template>
        """
    except Exception as ex:
        ic(ex)
        if "user_name" in str(ex):
            return f"""
            <template mix-target="#message">
                {ex.args[1]}
            </template>
            """            
    finally:
        pass


##############################
@delete("/users/<key>")
def _(key):
    try:
        if not re.match(r"[1-9][0-9]*", key):
            return "shit dont work"
        ic(key)
        res = x.db({"query":"""
                    FOR user IN users
                    FILTER user._key == @key
                    REMOVE user IN users RETURN OLD""", 
                    "bindVars":{"key":key}})
        print(res)
        return f"""
        <template mix-target="[id='{key}']" mix-replace>
            <div class="mix-fade-out user_deleted" mix-ttl="2000">User deleted</div>
        </template>
        """
    except Exception as ex: 
        ic(ex)
    finally:
        pass


##############################
@put("/users/<key>")
def _(key):
    try:
        name = x.validate_user_name()
        last_name = x.validate_user_last_name()
        nick_name = x.validate_nick_name()
        user_gender = x.validate_user_gender()
        res = x.db({"query":"""
                        UPDATE { _key: @key, name: @name, last_name:@last_name, nick_name:@nick_name, user_gender:@user_gender } 
                        IN users 
                        RETURN NEW""",
                    "bindVars":{
                        "key": f"{key}",
                        "name":f"{name}",
                        "last_name":f"{last_name}",
                        "nick_name":f"{nick_name}",
                        "user_gender":f"{user_gender}"
                    }})
        return f"""
        <template>            
        </template>
        """
    except Exception as ex:
        ic(ex)
        if "user_name" in str(ex):
            return f"""
            <template mix-target="#message">
                {ex.args[1]}
            </template>
            """            
    finally:
        pass