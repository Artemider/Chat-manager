from user.Midllvary import rate_limit, ThrottlingMiddleware 
from create_bot import bot, dp
from config import ignore, chat_ignore, bonuscode_dict, bonuscode_items_dict, db_item, db_item_two, db_item_ignore
from database.start import base, cur

from aiogram import types, executor, Dispatcher
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message
from math import floor
import time
import asyncio
import datetime
import random

'''*******************************************shop*****************************************************************'''

async def get_key(d, value, args):
	for k, v in d.items():
		if k == value:
			return v

async def balance_coin(coin, user_id):

	lvl = cur.execute('SELECT lvl FROM size_table_dickup WHERE user_id == ?', (user_id,)).fetchone()
	lvl = lvl[0]
	if int(lvl) <= 0: lvl = 1

	a = int(lvl) * 15
	random_du = random.randint(0,a)
	coin_up = int(coin) + random_du

	coin_list = [coin_up, random_du]

	return coin_list

async def items(random_items, user_id):

	if random_items > 80:
		comment = "💪"
		type_item = "frihand"
		number_item = 1

	elif random_items <= 59 and random_items >= 55:
		comment = "⚖️"
		type_item = "libra"
		number_item = 1

	elif random_items <= 80 and random_items >= 73:
		comment = "⛽"
		type_item = "pump"
		number_item = 1

	elif random_items < 73 and random_items >= 70:
		comment = "🧼"
		type_item = "grease"
		number_item = 1

	elif random_items == 1:
		comment = "🐰"
		type_item = "rabot"
		number_item = 1

	elif random_items < 70 and random_items >= 60:
		type_item = "coin"
		number_item = int(random.randint(20,140))
		comment = "💶"

	elif random_items == 5:
		random_ = random.randint(1,10)
		if random_ == 1:
			comment = "🔍"
			type_item = "magnifier"
			number_item = 1
		else:
			type_item = "coin"
			number_item = int(random.randint(90,180))
			comment = "💶"

	else:
		type_item = "coin"
		number_item = int(random.randint(1,40))
		comment = "💶"

	return [comment, number_item, type_item]

'''*******************************************shop*****************************************************************'''

#shop
@rate_limit(2, 'shop')
async def shop(message: types.Message):

	user_id = str(message.from_user.id)
	username = message.from_user.username
	first_name = str(message.from_user.first_name)
	chat_id = str(message.chat.id)
	chat_name = message.chat.title

	if str(user_id) in ignore:
		return

	if str(chat_id) in chat_ignore:
		await message.reply(f'Дякую за запуск <i><b><a href="tg://user?id={user_id}">{first_name}</a></b></i>.\n!!!<i>Бот перейшов в @pipup_comm</i>!!!!',  parse_mode='html')
		return

	try:
		coin = cur.execute('SELECT coin FROM inventory WHERE user_id == ?', (user_id,)).fetchone()
		coin = coin[0]

		sorted_db_item = dict(sorted(db_item.items(), key=lambda x: int(x[1][1]), reverse=False))

		linv = []
		for k, v in sorted_db_item.items():
			if k not in db_item_ignore.keys() and k not in ["💶", "💼", "🏅"]:
				linv.append(f"   <i>{v[0]} {k}</i> == <b>{v[1]}💶</b>\n")

		shop_item = ''.join(linv)
	
		title = f'\
		Coin: <b>{coin}💶</b>\n\
		--------------------------------------\n{shop_item}\
		--------------------------------------\n\
		====<b>/buy n item</b>====\n\
		--------------------------------------\n\
		  <i>/case</i> $✓`•~ <b>35💶</b>\n\
		--------------------------------------\n\
		'
	except:
		await message.answer(f"Спробуйте: '/dickup'",  parse_mode='html')
		return

	await message.answer(f'{title}',  parse_mode='html')

#market
@rate_limit(2, 'market')
async def market(message: types.Message):

	user_id = str(message.from_user.id)
	username = message.from_user.username
	first_name = str(message.from_user.first_name)
	chat_id = str(message.chat.id)
	chat_name = message.chat.title

	if str(user_id) in ignore:
		return

	if str(chat_id) in chat_ignore:
		await message.reply(f'Дякую за запуск <i><b><a href="tg://user?id={user_id}">{first_name}</a></b></i>.\n!!!<i>Бот перейшов в @pipup_comm</i>!!!!',  parse_mode='html')
		return

	try:
		sell_list = cur.execute('SELECT * FROM market').fetchall()
	except: pass

	awalist = []
	n = 0

	if sell_list == []:
		await message.answer(f"<b>None</b>\n",  parse_mode='html')
		return

	for x in sell_list:
		n += 1
		lc1 = x[1]#item_id
		lc2 = x[2]#price
		lc3 = x[3]#numb
		lc4 = x[4]#item
		lc5 = x[5]#dt

		if lc1 != None:
			awalist.append((f"<b>{n}){lc3}{lc4} $✓ {lc2}💶 [id == <i>{lc1}</i>]</b>"))

	awatitle = ';\n'.join(map(''.join,awalist))
	await message.answer(f"<b>Auction:</b>\n" + awatitle,  parse_mode='html')

#sell
@rate_limit(2, 'sell')
async def sell(message: types.Message):

	user_id = str(message.from_user.id)
	args = message.get_args()
	username = message.from_user.username
	first_name = str(message.from_user.first_name)
	chat_id = str(message.chat.id)
	chat_name = message.chat.title

	try:
		if str(user_id) in ignore:
			return

		if str(chat_id) in chat_ignore:
			await message.reply(f'Дякую за запуск <i><b><a href="tg://user?id={user_id}">{first_name}</a></b></i>.\n!!!<i>Бот перейшов в @pipup_comm</i>!!!!',  parse_mode='html')
			return
	
		if not args:
			await message.reply("Команда не має бути пуста!")
			return
		
		try:
			givint = int(message.text.split()[1])
			givtype = message.text.split()[2]
			givprice = int(message.text.split()[3])
		
			if givint <= 0 or givprice < 0:
				await message.reply("Продаж від'ємного або нульового числа предметів - неможливий!")
				return

			if givint > 50 or givprice > 1000:
				await message.reply('Завелике число, малий шанс покупкки!\nМакс число == 50;\nМакс ціна == 1000;')
				return
	
			try:
				sid = cur.execute('SELECT user_id FROM market WHERE user_id == ?', (user_id,)).fetchone()
				sid = str(sid[0])
		
				if sid == user_id:
					await message.reply('Ви уже продаєте товари!')
					return
			except:pass
	
		except:
			await message.reply('Неправильно написано!\nПриклад:\n/sell 1 🥚 150')
			return

		if givtype not in db_item.keys() and givtype not in db_item_two:
			await message.answer(f"<b>Цього знаку, немає у Базі Даних!</b>",  parse_mode='html')
			return

		if givtype in db_item.keys():
			kind_item_name = db_item[givtype][0]
		if givtype in db_item_two.keys():
			db_ite = await get_key(db_item, db_item_two[givtype], givtype)
			kind_item_name = db_ite[0]
			givtype = db_item_two[givtype]
		if givtype in db_item_ignore.keys():
			givtype = db_item_ignore[givtype]

		kind_item = cur.execute(f'SELECT {kind_item_name} FROM inventory WHERE user_id == ?', (user_id,)).fetchone()
		
		if int(kind_item[0]) < givint:
			await message.answer(f"У вас замало <b>{givtype}</b>.",  parse_mode='html')
			return
		
		kind_item = int(kind_item[0]) - givint
		
		cur.execute(f'UPDATE inventory SET {kind_item_name} == ? WHERE user_id == ?', (kind_item, user_id))
		base.commit()

		comment = f'Ви <b>успішно</b> виставили <b>{givint}{givtype}</b>, за {givprice}💶.'
	
		awalisty = []
		chat_list = cur.execute('SELECT * FROM market').fetchmany(10000)
	
		item_id = random.randint(1111,2000)
	
		if len(awalisty) > 0:
			for x in chat_list:
				chat_id_bd = x[1]
				awalisty.append(chat_id_bd)
		
			itmlist = []
		
			for x in awalisty:
				item_id = random.randint(1111,2000)
		
				if item_id != x:
					itmlist.append(item_id)
		
			item_id = itmlist[0]
	
		try:
			cur.execute('INSERT INTO market VALUES(?, ?, ?, ?, ?, ?)', (user_id, item_id, givprice, givint, givtype, 1))
			base.commit()
		except:
			await message.answer(f"<b>Error!</b>",  parse_mode='html')
			return
	
		await message.answer(f"{comment}",  parse_mode='html')
	
	except:
		await message.answer(f"<b>У вас немає цього предмета!</b>\nСпробуйте: '/dickup'",  parse_mode='html')

#kauf
@rate_limit(2, 'kauf')
async def kauf(message: types.Message):

	user_id = str(message.from_user.id)
	args = message.get_args()
	username = message.from_user.username
	first_name = str(message.from_user.first_name)
	chat_id = str(message.chat.id)
	chat_name = message.chat.title

	if str(user_id) in ignore:
		return

	if str(chat_id) in chat_ignore:
		await message.reply(f'Дякую за запуск <i><b><a href="tg://user?id={user_id}">{first_name}</a></b></i>.\n!!!<i>Бот перейшов в @pipup_comm</i>!!!!',  parse_mode='html')
		return

	if not args:
		await message.reply("Команда не має бути пуста!")
		return

	try:
		args = int(args)
	except:
		await message.answer(f"<i>Вкажіть, будь ласка, </i><b>id товару!</b>",  parse_mode='html')
		return

	try:
		sell_list = cur.execute('SELECT * FROM market WHERE item_id == ?', (args,)).fetchone()
		if sell_list == None:
			await message.answer(f"<i>Лота з таким</i> <b>id - немає!</b>",  parse_mode='html')
			return
		
		lc1 = sell_list[0]#user_id
		lc2 = int(sell_list[2])#price
		lc3 = int(sell_list[3])#numb
		lc4 = sell_list[4]#item
		
		prcoin = cur.execute('SELECT coin FROM inventory WHERE user_id == ?', (lc1,)).fetchone()
		prcoin = int(prcoin[0])
		
		coin = cur.execute('SELECT coin FROM inventory WHERE user_id == ?', (user_id,)).fetchone()
		coin = int(coin[0])
		
		if coin < (lc2):
			await message.answer(f"У вас замало <b>💶</b>, потрібно <b>{lc2}</b>.",  parse_mode='html')
			return
		coin_def = coin

		coin = coin - lc2
		prcoin = prcoin + lc2

		if user_id == lc1:
			coin = coin_def
			prcoin = coin_def
		
		cur.execute('UPDATE inventory SET coin == ? WHERE user_id == ?', (coin, user_id))
		base.commit()
		cur.execute('UPDATE inventory SET coin == ? WHERE user_id == ?', (prcoin, lc1))
		base.commit()

		if lc4 in db_item.keys() or givtype in db_item_two:
			kind_item_name = db_item[lc4][0]

			item_nm1 = cur.execute(f'SELECT {kind_item_name} FROM inventory WHERE user_id == ?', (user_id,)).fetchone()
			item_nm1 = int(item_nm1[0])
		
			itemsum = item_nm1 +lc3
		
			cur.execute(f'UPDATE inventory SET {kind_item_name} == ? WHERE user_id == ?', (itemsum, user_id))
			base.commit()

		cur.execute('DELETE FROM market WHERE item_id  == ?', (args,))
		base.commit()
	
		comment = f'Ви <b>успішно</b> купили <b>{lc3}{lc4}</b>.'
		
		await message.answer(f"{comment}",  parse_mode='html')
	except:
		await message.answer("Спробуйте: '/dickup'",  parse_mode='html')

#cancel
@rate_limit(2, 'cancel')
async def cancel(message: types.Message):

	user_id = str(message.from_user.id)
	args = message.get_args()
	username = message.from_user.username
	first_name = str(message.from_user.first_name)
	chat_id = str(message.chat.id)
	chat_name = message.chat.title

	if str(user_id) in ignore:
		return

	if str(chat_id) in chat_ignore:
		await message.reply(f'Дякую за запуск <i><b><a href="tg://user?id={user_id}">{first_name}</a></b></i>.\n!!!<i>Бот перейшов в @pipup_comm</i>!!!!',  parse_mode='html')
		return

	if not args:
		await message.reply("Команда не має бути пуста!")
		return

	try:
		args = int(args)
	except:
		await message.answer(f"<i>Вкажіть, будь ласка, </i><b>id товару!</b>",  parse_mode='html')
		return

	try:
		sell_list = cur.execute('SELECT * FROM market WHERE item_id == ?', (args,)).fetchone()
		if sell_list == None:
			await message.answer(f"<i>Лота з таким</i> <b>id - немає!</b>",  parse_mode='html')
			return
		
		lc1 = sell_list[0]#user_id
		lc3 = int(sell_list[3])#numb
		lc4 = sell_list[4]#item
		
		if lc1 != user_id:
			await message.answer(f"<b>Це не ваш лот!</b>",  parse_mode='html')
			return

		if lc4 in db_item.keys() or givtype in db_item_two:
			kind_item_name = db_item[lc4][0]

			item_nm1 = cur.execute(f'SELECT {kind_item_name} FROM inventory WHERE user_id == ?', (user_id,)).fetchone()
			item_nm1 = int(item_nm1[0])
		
			itemsum = item_nm1 + lc3
		
			cur.execute(f'UPDATE inventory SET {kind_item_name} == ? WHERE user_id == ?', (itemsum, user_id))
			base.commit()

		cur.execute('DELETE FROM market WHERE item_id  == ?', (args,))
		base.commit()
	
		comment = f'Ви <b>успішно</b> скасували <b>{lc3}{lc4}</b>.'
		
		await message.answer(f"{comment}",  parse_mode='html')
	except:
		await message.answer("Спробуйте: '/dickup'",  parse_mode='html')

#buy
@rate_limit(2, 'buy')
async def buy(message: types.Message):

	user_id = str(message.from_user.id)
	args = message.get_args()
	username = message.from_user.username
	first_name = str(message.from_user.first_name)
	chat_id = str(message.chat.id)
	chat_name = message.chat.title

	if str(user_id) in ignore:
		return

	if str(chat_id) in chat_ignore:
		await message.reply(f'Дякую за запуск <i><b><a href="tg://user?id={user_id}">{first_name}</a></b></i>.\n!!!<i>Бот перейшов в @pipup_comm</i>!!!!',  parse_mode='html')
		return

	if not args:
		await message.reply("Команда не має бути пуста!")
		return

	try:
	
		try:
			givint = int(message.text.split()[1])
			givtype = message.text.split()[2]
		except:
			await message.reply('Неправильно написано!\nПриклад:\n/buy 1 🥚')
			return
	
		if givint < 0:
			await message.reply("Покупка від'ємного числа предметів - неможлива!")
			return

		if givtype not in db_item.keys() and givtype not in db_item_two:
			await message.answer(f"<b>Цього знаку, немає у Базі Даних!</b>",  parse_mode='html')
			return
	
		if givtype in db_item.keys():
			kind_item_name = db_item[givtype][0]
			db_ite = db_item[givtype]
		if givtype in db_item_two.keys():
			db_ite = await get_key(db_item, db_item_two[givtype], givtype)
			kind_item_name = db_ite[0]
			givtype = db_item_two[givtype]
		
		if givtype == "💶":
			await message.answer(f"Ви <b>успішно</b> купили <b>{givint}{givtype}</b>.",  parse_mode='html')
			return

		coin = cur.execute('SELECT coin FROM inventory WHERE user_id == ?', (user_id,)).fetchone()
		kind_item = cur.execute(f'SELECT {kind_item_name} FROM inventory WHERE user_id == ?', (user_id,)).fetchone()
		coin = int(coin[0])
	
		if coin < (givint*int(db_ite[1])):
			givint15 = givint*int(db_ite[1])
			await message.answer(f"У вас замало <b>💶</b>, потрібно <b>{givint15}</b>.",  parse_mode='html')
			return
	
		kind_item = int(kind_item[0]) + givint
		coin = coin - givint*int(db_ite[1])
	
		cur.execute(f'UPDATE inventory SET {kind_item_name} == ? WHERE user_id == ?', (kind_item, user_id))
		base.commit()
		cur.execute('UPDATE inventory SET coin == ? WHERE user_id == ?', (coin, user_id))
		base.commit()
	
		comment = f'Ви <b>успішно</b> купили <b>{givint}{givtype}</b>.'
	
		await message.answer(f"{comment}",  parse_mode='html')
	except:
		await message.answer("Спробуйте: '/dickup'",  parse_mode='html')

#mine
@rate_limit(2, 'mine')
async def mine(message: types.Message):

	user_id = str(message.from_user.id)
	username = message.from_user.username
	first_name = str(message.from_user.first_name)
	chat_id = str(message.chat.id)
	chat_name = message.chat.title

	lucky = 1
	print_lk = " "

	if str(user_id) in ignore:
		return

	if str(chat_id) in chat_ignore:
		await message.reply(f'Дякую за запуск <i><b><a href="tg://user?id={user_id}">{first_name}</a></b></i>.\n!!!<i>Бот перейшов в @pipup_comm</i>!!!!',  parse_mode='html')
		return

	try:
		coin = cur.execute('SELECT coin FROM inventory WHERE user_id == ?', (user_id,)).fetchone()
		coin = coin[0]
	
		try:
			time_coin = cur.execute('SELECT time_coin FROM inventory WHERE user_id == ?', (user_id,)).fetchone()
			time_coin = time_coin[0]
		
			if int(time_coin) > int(time.time()):
				raise SyntaxError(x)
	
		except:
			abc_time = int(time_coin) - int(time.time())
			h = floor(int(abc_time)/3600) 
			m = floor((int(abc_time) - int(h*3600))/60)
			s = int(abc_time) - int(h*3600 + m*60)
	
			if len(str(h)) < 2:
				h = str(0) + str(h)
		
			if len(str(m)) < 2:
				m = str(0) + str(m)
		
			if len(str(s)) < 2:
				s = str(0) + str(s)
		
			await message.reply(f'Ви уже <b>отримали <i>coin</i></b>,\nнаступний раз буде\nчерез: <b>{h}:{m}:{s}</b>.',  parse_mode='html')
			return
		
		treasury = cur.execute('SELECT treasury FROM inventory WHERE user_id == ?', (user_id,)).fetchone()
		treasury = int(treasury[0])

		coin_list = await balance_coin(coin, user_id)
		coin = coin_list[0]
		random_du = coin_list[1]
		time_coin_bd = int(time.time()) + int(14400)

		if treasury > 0:
			time_coin_bd = int(time.time()) + int(7200)
		
		cur.execute('UPDATE inventory SET coin == ? WHERE user_id == ?', (coin, user_id))
		base.commit()
		cur.execute('UPDATE inventory SET time_coin == ? WHERE user_id == ?', (time_coin_bd, user_id))
		base.commit()
	
		text = f"<i><b>{first_name}</b></i>, ви збільшили свій рахунок на <b>{random_du}</b> 💶.\nВаш новий рахунок: <b>{coin}</b> 💶."
	
		try:
			await message.reply(f'{text}',  parse_mode='html')
		except:
			first_name = username
			if first_name == None:
				first_name = "Fredd"
			await message.reply(f'{text}',  parse_mode='html')
	except:
		await message.answer("Спробуйте: '/dickup'",  parse_mode='html')

#case
@rate_limit(1, 'case')
async def case(message: types.Message):

	user_id = str(message.from_user.id)
	username = message.from_user.username
	first_name = str(message.from_user.first_name)
	chat_id = str(message.chat.id)
	chat_name = message.chat.title
	args = message.get_args()
	num = 1

	if str(user_id) in ignore:
		return

	if str(chat_id) in chat_ignore:
		await message.reply(f'Дякую за запуск <i><b><a href="tg://user?id={user_id}">{first_name}</a></b></i>.\n!!!<i>Бот перейшов в @pipup_comm</i>!!!!',  parse_mode='html')
		return
	try:
		if isinstance(int(args), int) == True:
			num = int(args)

		if isinstance(int(args), int) == False or args == 0:
			await message.answer(f"<b>{args}</b> - не натуральне число!",  parse_mode='html')
	except: pass

	try:
		comment0 = {"💪":0, "⛽":0, "🧼":0, "🐰":0, "💶":0, "⚖️":0, "🔍":0}

		item_case = cur.execute('SELECT item_case FROM inventory WHERE user_id == ?', (user_id,)).fetchone()
		item_case = int(item_case[0])

		if item_case == 0 and num == 1:
			coin = cur.execute('SELECT coin FROM inventory WHERE user_id == ?', (user_id,)).fetchone()
			coin = int(coin[0])
			
			if coin < 35*num:
				await message.answer(f"У вас замало <b>💶</b>, потрібно <b>{35*num}</b>.",  parse_mode='html')
				return
			
			coin = coin - 35*num
	
			cur.execute('UPDATE inventory SET coin == ? WHERE user_id == ?', (coin, user_id))
			base.commit()

			comm1 = "Ви <b>купили</b> 💼:"

			random_items = random.randint(0,100)
			comment = await items(random_items, user_id)

			item_rand = cur.execute(f'SELECT {comment[2]} FROM inventory WHERE user_id == ?', (user_id,)).fetchone()
			item_rand = item_rand[0]
			item_rand = int(item_rand) + 1

			cur.execute(f'UPDATE inventory SET {comment[2]} == ? WHERE user_id == ?', (item_rand, user_id))
			base.commit()

			comment = f"   <i>Ви отримали:</i> <b>{comment[0]}{comment[1]}</b>"

		elif item_case >= num and item_case != 0:
			item_case = item_case - 1*num

			cur.execute('UPDATE inventory SET item_case == ? WHERE user_id == ?', (item_case, user_id))
			base.commit()

			comm1 = "Ви використали 💼:"

			while num != 0:
				num -= 1
				random_items = random.randint(0,100)
				icl = await items(random_items, user_id)
				comment0[icl[0]] = comment0[icl[0]] + icl[1]

			comment = []

			for k, v in comment0.items():
				if int(v) != 0:
					item_rand = cur.execute(f'SELECT {db_item[k][0]} FROM inventory WHERE user_id == ?', (user_id,)).fetchone()
					item_rand = item_rand[0]
					item_rand = int(item_rand) + int(v)

					cur.execute(f'UPDATE inventory SET {db_item[k][0]} == ? WHERE user_id == ?', (item_rand, user_id))
					base.commit()

					comment.append(f"   <i>Ви отримали:</i> <b>{v}{k}</b>\n")

			comment = ''.join(comment)

		else:
			await message.answer(f"<b>Завелике число</b>.",  parse_mode='html')
			return

		comm = f"{comm1}\n{comment}"
	except:
		await message.answer("Спробуйте: '/dickup'",  parse_mode='html')
		return

	await message.answer(f"{comm}",  parse_mode='html')

'''*******************************************bonuscode*****************************************************************'''

#bonuscode
@rate_limit(3, 'bonuscode')
async def bonuscode(message: types.Message):

	user_id = str(message.from_user.id)
	args = str(message.get_args())
	username = message.from_user.username
	first_name = str(message.from_user.first_name)
	chat_id = str(message.chat.id)
	chat_name = message.chat.title

	if str(user_id) in ignore:
		return

	if str(chat_id) in chat_ignore:
		await message.reply(f'Дякую за запуск <i><b><a href="tg://user?id={user_id}">{first_name}</a></b></i>.\n!!!<i>Бот перейшов в @pipup_comm</i>!!!!',  parse_mode='html')
		return

	if not args:
		await message.reply("<b>Команда не має бути пуста!</b>", parse_mode='html')
		return
	
	try:
		if str(args) not in bonuscode_dict.keys():
			await message.reply("<b>Даний бонускод відсутній в базі!</b>\nКоманда записується:\n/bonuscode КОД", parse_mode='html')
			return
	
		bnda = bonuscode_dict[str(args)]
	
		bn = cur.execute(f'SELECT {bnda} FROM bonuscode WHERE user_id == ?', (user_id,)).fetchone()
		bn = int(bn[0])
		
		if bn < 1:
			await message.answer(f"Ви уже активували <b>бонускод</b>!",  parse_mode='html')
			return
	
		bn = bn - 1
		
		cur.execute(f'UPDATE bonuscode SET {bnda} == ? WHERE user_id == ?', (bn, user_id))
		base.commit()
	
		text_list = []
		c = f = p = g = r = ""
	
		#coin
		item = cur.execute('SELECT coin FROM inventory WHERE user_id == ?', (user_id,)).fetchone()
		item = int(item[0]) + bonuscode_items_dict[args][0]
		if bonuscode_items_dict[args][0] != 0:
			c = f"\n<i>Coin 💶</i> '*&#×- <b>{bonuscode_items_dict[args][0]}</b>"
		cur.execute('UPDATE inventory SET coin == ? WHERE user_id == ?', (item, user_id))
		base.commit()
	
		#frihand
		item = cur.execute('SELECT frihand FROM inventory WHERE user_id == ?', (user_id,)).fetchone()
		item = int(item[0]) + bonuscode_items_dict[args][1]
		if bonuscode_items_dict[args][1] != 0:
			f = f"\n<i>Frihand 💪</i> '*&#×- <b>{bonuscode_items_dict[args][1]}</b>"
		cur.execute('UPDATE inventory SET frihand == ? WHERE user_id == ?', (item, user_id))
		base.commit()
	
		#pump
		item = cur.execute('SELECT pump FROM inventory WHERE user_id == ?', (user_id,)).fetchone()
		item = int(item[0]) + bonuscode_items_dict[args][2]
		if bonuscode_items_dict[args][2] != 0:
			p = f"\n<i>Pump ⛽</i> '*&#×- <b>{bonuscode_items_dict[args][2]}</b>"
		cur.execute('UPDATE inventory SET pump == ? WHERE user_id == ?', (item, user_id))
		base.commit()
	
		#grease
		item = cur.execute('SELECT grease FROM inventory WHERE user_id == ?', (user_id,)).fetchone()
		item = int(item[0]) + bonuscode_items_dict[args][3]
		if bonuscode_items_dict[args][3] != 0:
			g = f"\n<i>Grease 🧼</i> '*&#×- <b>{bonuscode_items_dict[args][3]}</b>"
		cur.execute('UPDATE inventory SET grease == ? WHERE user_id == ?', (item, user_id))
		base.commit()
	
		#rabot
		item = cur.execute('SELECT rabot FROM inventory WHERE user_id == ?', (user_id,)).fetchone()
		item = int(item[0]) + bonuscode_items_dict[args][4]
		if bonuscode_items_dict[args][4] != 0:
			g = f"\n<i>Rabot 🐰</i> '*&#×- <b>{bonuscode_items_dict[args][4]}</b>"
		cur.execute('UPDATE inventory SET rabot == ? WHERE user_id == ?', (item, user_id))
		base.commit()
	
		#case
		item = cur.execute('SELECT item_case FROM inventory WHERE user_id == ?', (user_id,)).fetchone()
		item = int(item[0]) + bonuscode_items_dict[args][5]
		if bonuscode_items_dict[args][5] != 0:
			g = f"\n<i>Case 💼</i> '*&#×- <b>{bonuscode_items_dict[args][5]}</b>"
		cur.execute('UPDATE inventory SET item_case == ? WHERE user_id == ?', (item, user_id))
		base.commit()
	
		#machine
		item = cur.execute('SELECT machine FROM inventory WHERE user_id == ?', (user_id,)).fetchone()
		item = int(item[0]) + bonuscode_items_dict[args][6]
		if bonuscode_items_dict[args][6] != 0:
			g = f"\n<i>Machine 🎛️</i> '*&#×- <b>{bonuscode_items_dict[args][6]}</b>"
		cur.execute('UPDATE inventory SET machine == ? WHERE user_id == ?', (item, user_id))
		base.commit()
	
		#magnifier
		item = cur.execute('SELECT magnifier FROM inventory WHERE user_id == ?', (user_id,)).fetchone()
		item = int(item[0]) + bonuscode_items_dict[args][7]
		if bonuscode_items_dict[args][7] != 0:
			g = f"\n<i>Magnifier 🔍</i> '*&#×- <b>{bonuscode_items_dict[args][7]}</b>"
		cur.execute('UPDATE inventory SET magnifier == ? WHERE user_id == ?', (item, user_id))
		base.commit()

		#libra
		item = cur.execute('SELECT libra FROM inventory WHERE user_id == ?', (user_id,)).fetchone()
		item = int(item[0]) + bonuscode_items_dict[args][8]
		if bonuscode_items_dict[args][8] != 0:
			g = f"\n<i>Libra ⚖️</i> '*&#×- <b>{bonuscode_items_dict[args][8]}</b>"
		cur.execute('UPDATE inventory SET libra == ? WHERE user_id == ?', (item, user_id))
		base.commit()

		#ironhand
		item = cur.execute('SELECT ironhand FROM inventory WHERE user_id == ?', (user_id,)).fetchone()
		item = int(item[0]) + bonuscode_items_dict[args][9]
		if bonuscode_items_dict[args][9] != 0:
			g = f"\n<i>Ironhand 🦾</i> '*&#×- <b>{bonuscode_items_dict[args][9]}</b>"
		cur.execute('UPDATE inventory SET ironhand == ? WHERE user_id == ?', (item, user_id))
		base.commit()
	
		#autofiller
		item = cur.execute('SELECT autofiller FROM inventory WHERE user_id == ?', (user_id,)).fetchone()
		item = int(item[0]) + bonuscode_items_dict[args][10]
		if bonuscode_items_dict[args][10] != 0:
			g = f"\n<i>Autofiller 🧴</i> '*&#×- <b>{bonuscode_items_dict[args][10]}</b>"
		cur.execute('UPDATE inventory SET autofiller == ? WHERE user_id == ?', (item, user_id))
		base.commit()

		#treasury
		item = cur.execute('SELECT treasury FROM inventory WHERE user_id == ?', (user_id,)).fetchone()
		item = int(item[0]) + bonuscode_items_dict[args][11]
		if bonuscode_items_dict[args][11] != 0:
			g = f"\n<i>Treasury 🪙</i> '*&#×- <b>{bonuscode_items_dict[args][11]}</b>"
		cur.execute('UPDATE inventory SET treasury == ? WHERE user_id == ?', (item, user_id))
		base.commit()	

		await message.answer(f"Ви отримали:\n--------------------------------------{c}{f}{p}{g}{r}\n--------------------------------------",  parse_mode='html')
	except:
		await message.answer(f"<b>Error!</b>",  parse_mode='html')

'''*******************************************start*****************************************************************'''

def register_handlers_shop(dp : Dispatcher):

	#shop
	dp.register_message_handler(shop, commands=["shop"])
	dp.register_message_handler(buy, commands=["buy"])
	dp.register_message_handler(mine, commands=["mine"])

	#market
	dp.register_message_handler(market, commands=["market"])
	dp.register_message_handler(sell, commands=["sell"])
	dp.register_message_handler(kauf, commands=["kauf"])
	dp.register_message_handler(cancel, commands=["cancel"])

	#case
	dp.register_message_handler(case, commands=["case"])
	dp.register_message_handler(case, lambda message: message.text.startswith("Кейс"))

	#bonuscode
	dp.register_message_handler(bonuscode, commands=["bonuscode"])