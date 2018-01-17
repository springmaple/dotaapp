import sqlite3

db_conn = sqlite3.connect("dotaapp.db", check_same_thread=False, detect_types=sqlite3.PARSE_DECLTYPES)
db_conn.row_factory = sqlite3.Row
sqlite3.register_converter("BOOL", lambda data: True if data == b'1' else False)
sqlite3.register_adapter(bool, lambda data: 1 if data else 0)


def set_db_version(version:int):
    db_conn.execute("PRAGMA user_version=" + str(version))
    db_conn.commit()


def get_db_version():
    return int(db_conn.execute("PRAGMA user_version").fetchone()[0])


def init():
    if get_db_version() == 0:
        note = ("CREATE TABLE IF NOT EXISTS note("
                "name TEXT PRIMARY KEY,"
                "text TEXT)")
        db_conn.execute(note)
        set_db_version(1)
        db_conn.commit()


def update_item(id, name, cost, localized_name:"label", secret_shop, side_shop, recipe):
    for _ in db_conn.execute("SELECT id FROM item WHERE id=?", (id,)):
        sql = ("UPDATE item "
               "SET name=?, cost=?, label=?, secret_shop=?, side_shop=?, recipe=? "
               "WHERE id=?")
        db_conn.execute(sql, (name, cost, localized_name, secret_shop, side_shop, recipe, id))
        break
    else:
        values = (id, name, cost, localized_name, secret_shop, side_shop, recipe)
        db_conn.execute("INSERT INTO item VALUES (" + ", ".join(["?"] * len(values)) + ")", values)
    db_conn.commit()