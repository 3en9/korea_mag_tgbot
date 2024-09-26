import sqlite3



def new_row(user):
    conn = sqlite3.connect('bot.db')
    cursor = conn.cursor()
    cursor.execute(f'INSERT INTO baskets(id, basket) VALUES ({user}, "NULL")')
    conn.commit()
    conn.close()

def get_basket(user):
    conn = sqlite3.connect('bot.db')
    cursor = conn.cursor()
    cursor.execute(f'SELECT * FROM baskets WHERE id={user}')
    res = cursor.fetchone()
    conn.close()
    return res

def add_basket(user, note):
    prev_basket = get_basket(user)[1]
    if not prev_basket:
        return
    if prev_basket == 'NULL':
        basket = note
    else:
        basket = prev_basket + '\n' + note
    conn = sqlite3.connect('bot.db')
    cursor = conn.cursor()
    cursor.execute(f'UPDATE baskets SET basket="{basket}" WHERE id={user}')
    conn.commit()
    conn.close()

def del_position(user, position):
    prev_basket = get_basket(user)[1]
    positions = prev_basket.split('\n')
    if len(positions) == 1:
        clear_basket(user)
    else:
        positions.pop(position)
        basket = '\n'.join(positions)
        conn = sqlite3.connect('bot.db')
        cursor = conn.cursor()
        cursor.execute(f'UPDATE baskets SET basket="{basket}" WHERE id={user}')
        conn.commit()
        conn.close()


def clear_basket(user):
    conn = sqlite3.connect('bot.db')
    cursor = conn.cursor()
    cursor.execute('UPDATE baskets SET basket=? WHERE id=?', ("NULL",user))
    conn.commit()
    conn.close()


def new_order(user, order):
    conn = sqlite3.connect('bot.db')
    cursor = conn.cursor()
    cursor.execute(f'INSERT INTO orders(id, structure) VALUES ({user}, "{order}")')
    conn.commit()


conn = sqlite3.connect('bot.db')
cursor = conn.cursor()
cursor.execute('SELECT * FROM baskets')
conn.commit()
res = cursor.fetchall()
conn.close()
print(res)


