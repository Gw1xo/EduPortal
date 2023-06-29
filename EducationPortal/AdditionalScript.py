import hashlib
import string
from functools import wraps
import random
from flask import session, abort
from init_db import OperatorDB


def check_access(userrole):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            with OperatorDB() as op:
                op.cur.execute(f"select school.shcoolid from school where uniq_code = '{session.get('uniqcode')}'")
                school_id = op.cur.fetchone()
                if not school_id or school_id[0] != session.get("schoolid"):
                    abort(404)
            if session.get("userrole") != userrole:
                abort(404)
            return func(*args, **kwargs)
        return wrapper
    return decorator


def generate_unique_key():
    # Генеруємо випадкову послідовність символів
    random_string = ''.join(random.choices(string.ascii_letters + string.digits, k=10))

    # Використовуємо хеш-функцію для створення скороченого хешу
    hashed_string = hashlib.sha256(random_string.encode()).hexdigest()

    # Повертаємо перші 5 символів хешу
    unique_key = hashed_string[:5]

    return unique_key


def get_user(userid):
    with OperatorDB() as op:
        op.cur.execute(f"select * from users where userid = {userid}")
        return op.cur.fetchone()
