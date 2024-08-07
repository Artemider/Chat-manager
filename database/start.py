from config import base

import sqlite3

base = sqlite3.connect(base)
cur = base.cursor()
#Список чатів
base.execute('CREATE TABLE IF NOT EXISTS chatlist(number_chat integer, chat_name, chat_id, data)')
base.commit()

#Список dickup
base.execute('CREATE TABLE IF NOT EXISTS size_table_dickup(first_name, user_id, lvl, size integer, chat_id, time_dickup integer)')
base.commit()

#Список effect
base.execute('CREATE TABLE IF NOT EXISTS effect(user_id, grease, rabot)')
base.commit()

#Список inventory
base.execute('CREATE TABLE IF NOT EXISTS inventory(user_id, coin, frihand, pump, grease, rabot, item_case, magnifier, machine, libra, time_coin)')
base.commit()

#Список market
base.execute('CREATE TABLE IF NOT EXISTS market(user_id, item_id, price, numb, item, dt)')
base.commit()

#Список Бонускодів
base.execute('CREATE TABLE IF NOT EXISTS bonuscode(user_id, b1, b2, b3, b4, b5)')
base.commit()

#Список ігор
base.execute('CREATE TABLE IF NOT EXISTS games(user_id, user2, user3, user4, numb, item, dt)')
base.commit()
