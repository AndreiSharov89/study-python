import db
import util
from datetime import datetime

connection=db.connection_DB("farmers_markets123")
connection.autocommit = True
cursor = connection.cursor()

def all_markets_full():
    sql1 = """select markets.market_id, markets.market_name, markets.street, cities.city, states.state_full,
    markets.zip, markets.lat, markets.lon
    from markets
    inner join cities on markets.city=cities.city_id
    inner join states on markets.state=states.state_id
    ORDER BY market_id ASC;"""

    dict1 = {}
    cursor.execute(sql1)
    res = cursor.fetchall()
    for rec in res:
        dict1.setdefault(rec[0], []).append(rec[1:])

    sql2 = """SELECT markets.market_id, markets_categories.market_id, categories.category
    FROM markets
    FULL join markets_categories on markets.market_id = markets_categories.market_id
    FULL join categories on markets_categories.category_id = categories.category_id
    ORDER BY markets_categories.market_id, categories.category_id"""

    dict2 = {}
    cursor.execute(sql2)
    res = cursor.fetchall()
    for rec in res:
        dict2.setdefault(rec[0], []).append(rec[2])

    sql3 = """SELECT markets.market_id, reviews.date_time, users.username, reviews.score, coalesce(reviews.review,'Нет рецензий')
    FROM markets
    FULL join reviews on reviews.market_id = markets.market_id
    FULL join users on reviews.user_id = users.user_id
    ORDER BY markets.market_id, reviews.review_id"""

    dict3 = {}
    cursor.execute(sql3)
    res = cursor.fetchall()
    for rec in res:
        dict3.setdefault(rec[0], []).append(rec[1:])

    dict = dict1.copy()

    for key,val in dict2.items():
        if key in dict:
            dict[key] = [dict[key],val]

    for key,val in dict3.items():
        if key in dict:
            dict[key] = [dict[key],val]

    return dict

def all_markets():
    sql1 = """select markets.market_id, markets.market_name, markets.street, cities.city, states.state_full,
    markets.zip, markets.lat, markets.lon
    from markets
    inner join cities on markets.city=cities.city_id
    inner join states on markets.state=states.state_id
    ORDER BY market_id ASC;"""

    dict1 = {}
    cursor.execute(sql1)
    res = cursor.fetchall()
    for rec in res:
        dict1.setdefault(rec[0], []).append(rec[1:])

    sql2 = """SELECT markets.market_id, markets_categories.market_id, categories.category
        FROM markets
        FULL join markets_categories on markets.market_id = markets_categories.market_id
        FULL join categories on markets_categories.category_id = categories.category_id
        ORDER BY markets_categories.market_id, categories.category_id"""

    dict2 = {}
    cursor.execute(sql2)
    res = cursor.fetchall()

    for rec in res:
        dict2.setdefault(rec[0], []).append(rec[2])
    dict = dict1.copy()

    for key,val in dict2.items():
        if key in dict:
            dict[key] = [dict[key],val]

    return dict

def market_by_id(id):
    dict = all_markets()
    return dict.get(id)
def market_by_id_full(id):
    dict = all_markets_full()
    return dict.get(id)


def id_by_location(city, state):
    ids = []
    cursor.execute("""select markets.market_id, markets.market_name, markets.street, cities.city, states.state_full, markets.zip, markets.lat, markets.lon
    from markets
    inner join cities on markets.city=cities.city_id
    inner join states on markets.state=states.state_id
    where lower(cities.city) = %s and lower(states.state_full) = %s;""", (city.lower(), state.lower()))
    res = cursor.fetchall()
    for record in res:
        ids.append(record[0])
    return ids

def id_by_zip(zip):
    ids = []
    cursor.execute("""select markets.market_id, markets.market_name, markets.street, cities.city, states.state_full, markets.zip, markets.lat, markets.lon
    from markets
    inner join cities on markets.city=cities.city_id
    inner join states on markets.state=states.state_id
    where markets.zip = %s;""", (zip, ))
    res = cursor.fetchall()
    for record in res:
        ids.append(record[0])
    return ids

def id_by_zip_and_distance(zip, distance):
    ids = []
    id = id_by_zip(zip)
    market_zip = market_by_id_full(id[0])
    markets = all_markets_full()
    location1 = [market_zip[0][0][0][5], market_zip[0][0][0][6]]
    for key, val in markets.items():
        if (val[0][0][0][5] != None and val[0][0][0][6] != None):
            location2 = [val[0][0][0][5], val[0][0][0][6]]
            if util.calculate_distance(location1, location2) <= distance:
                ids.append(key)
    return ids

def new_user(fname, lname, username, password):
    cursor.execute("""SELECT user_id FROM users
    ORDER BY user_id DESC  LIMIT 1;""")
    last = cursor.fetchone()[0]+1
    user = [last, fname, lname, username, password]
    cursor.execute("""INSERT INTO users VALUES (%s, %s, %s, %s, %s);""", user)

def find_user_id(username, password):
    cursor.execute(f"""SELECT user_id FROM users
        WHERE username = '{username}' and password_hash = '{password}' LIMIT 1;""")
    id = cursor.fetchone()
    if id != None: return id;
    else: return 0;

def new_review(user_id, market_id, score, review):
    cursor.execute("""SELECT review_id FROM reviews
    ORDER BY review_id DESC  LIMIT 1;""")
    last = cursor.fetchone()[0]+1
    date = datetime.today().strftime('%Y-%m-%d')
    review = [last, user_id, market_id, date, score, review]
    cursor.execute("""INSERT INTO reviews VALUES (%s, %s, %s, %s, %s, %s);""", review)

def get_review(market_id):
    cursor.execute(f"""SELECT market_id, score, review FROM reviews
    WHERE market_id = '{market_id}';""")
    list = cursor.fetchall()
    return list

def get_reviews(username, password):
    user_id = find_user_id(username, password)[0]
    cursor.execute(f"""SELECT * FROM reviews
            WHERE user_id = '{user_id}';""")
    list = cursor.fetchall()
    return list

def delete_review(id):
    cursor.execute("""DELETE from reviews
    where review_id = %s;""", (id, ))

def sort_by_state_city(sort):
    dict = all_markets_full()
    sort_desc = True
    if sort is False:
        sort_desc = False
    sorted_state_and_city = sorted(dict.items(), key=lambda item: (item[1][0][0][0][3], item[1][0][0][0][2]), reverse=sort_desc)
    return sorted_state_and_city

