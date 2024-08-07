from user.Midllvary import rate_limit, ThrottlingMiddleware 
from create_bot import bot, dp
from config import ignore, chat_ignore, moderator, db_item, db_item_two, VIP, db_item_ignore
from database.start import base, cur

from aiogram import types, executor, Dispatcher
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message
from math import floor
import time
import asyncio
import datetime
import random

'''*******************************************Func*****************************************************************'''

#create
@rate_limit(2, 'create')
async def create(message: types.Message):

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
		
			if givint <= 0:
				await message.reply("Ставка від'ємного або нульового числа предметів - неможливий!")
				return

			if givint > 1000:
				await message.reply('Завелике число, малий шанс гри!\nМакс число == 1000;')
				return
	
			try:
				sid = cur.execute('SELECT user_id FROM games WHERE user_id == ?', (user_id,)).fetchone()
				sid = str(sid[0])
		
				if sid == user_id:
					await message.reply('Ви уже створили гру!')
					return
			except:pass
	
		except:
			await message.reply('Неправильно написано!\nПриклад:\n/create 1 🥚')
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

		comment = f'Ви <b>успішно</b> почали гру, із ставкою <b>{givint}{givtype}</b>.\nУчасників: 1.'
	
		awalisty = []
		chat_list = cur.execute('SELECT * FROM chatlist').fetchmany(10000)
	
		item_id = random.randint(1111,2000)
	
		if len(awalisty) > 0:
			for x in chat_list:
				chat_id_bd = x[1]
				awalisty.append(chat_id_bd)
		
			itmlist = []
		
			for x in awalisty:
				item_id = random.randint(1001,9999)
		
				if item_id != x:
					itmlist.append(item_id)
		
			item_id = itmlist[0]
	
		try:
			cur.execute('INSERT INTO games VALUES(?, ?, ?, ?, ?, ?)', (user_id, "-", "-", "-", givint, givtype, int(time.time())))
			base.commit()
		except:
			await message.answer(f"<b>Error!</b>",  parse_mode='html')
			return
	
		markup = InlineKeyboardMarkup()
		button = InlineKeyboardButton(text="Увійти", callback_data=f'btn1:{user_id}')
		button1 = InlineKeyboardButton(text="Вийти", callback_data=f'btn2:{user_id}')
		button2 = InlineKeyboardButton(text="Старт", callback_data=f'btn3:{user_id}')
		markup.add(button, button1).add(button2)

		await message.answer(f"{comment}",  parse_mode='html', reply_markup=markup)
	
	except:
		await message.answer(f"<b>У вас немає цього предмета!</b>\nСпробуйте: '/dickup'",  parse_mode='html')

#Button1
@dp.callback_query_handler(lambda c: c.data.startswith('btn1:'))
@rate_limit(3, 'btn1')
async def but1(callback_query: types.CallbackQuery):
	mather_id = callback_query.data.split(':')[1]
	chat_id = str(callback_query.message.chat.id)
	user_id = str(callback_query.from_user.id)
	first_name = str(callback_query.from_user.first_name)
	callback_query_id = callback_query.message.message_id

	num_user = []
	try:
		if str(user_id) in ignore:
			return
		
		try:
			sid = cur.execute('SELECT * FROM games WHERE user_id == ?', (mather_id,)).fetchone()
			userlist = [sid[0], sid[1], sid[2], sid[3]]
	
			if user_id in userlist:
				await callback_query.message.reply('Ви уже учасник гри!')
				return

			for x in userlist:
				if x != "-":
					num_user.append(x)

		except:pass

		usern = user+str(len(num_user))
			await callback_query.message.reply('Лобі уже заповнено!')
			return

		kind_item_name = db_item[sid[5]]

		kind_item = cur.execute(f'SELECT {kind_item_name} FROM inventory WHERE user_id == ?', (user_id,)).fetchone()
		
		if int(kind_item[0]) < int(sid[4]):
			await callback_query.message.reply(f"У вас замало <b>{givtype}</b>.",  parse_mode='html')
			return
		
		kind_item = int(kind_item[0]) - int(sid[4])
		
		cur.execute(f'UPDATE inventory SET {kind_item_name} == ? WHERE user_id == ?', (kind_item, user_id))
		base.commit()

		comment = f'Ви <b>успішно</b> почали гру, із ставкою <b>{givint}{givtype}</b>.\nУчасників: {len(num_user)+1}.'
	
		try:
			cur.execute(f'UPDATE games SET {usern} == ? WHERE user_id == ?', (user_id, mather_id))
			base.commit()
		except:
			await callback_query.message.answer(f"<b>Error!</b>",  parse_mode='html')
			return
		await bot.edit_message_text(comment, chat_id=chat_id, message_id=callback_query_id, parse_mode='html')	
	except:pass

#Button2
@dp.callback_query_handler(lambda c: c.data.startswith('btn2:'))
@rate_limit(3, 'btn2')
async def but2(callback_query: types.CallbackQuery):
	mather_id = callback_query.data.split(':')[1]
	chat_id = str(callback_query.message.chat.id)
	user_id = str(callback_query.from_user.id)
	first_name = str(callback_query.from_user.first_name)
	callback_query_id = callback_query.message.message_id

	num_user = []
	try:
		if str(user_id) in ignore:
			return
		
		try:
			sid = cur.execute('SELECT * FROM games WHERE user_id == ?', (mather_id,)).fetchone()
			userlist = [sid[0], sid[1], sid[2], sid[3]]
	
			if user_id not in userlist:
				await callback_query.message.reply('Ви не берете участь в грі!')
				return

		comment = f'Ви <b>успішно</b> почали гру, із ставкою <b>{givint}{givtype}</b>.\nУчасників: {len(num_user)-1}.'
	
		try:
			cur.execute(f'UPDATE games SET {usern} == ? WHERE user_id == ?', (user_id, mather_id))
			base.commit()
		except:
			await callback_query.message.answer(f"<b>Error!</b>",  parse_mode='html')
			return
		await bot.edit_message_text(comment, chat_id=chat_id, message_id=callback_query_id, parse_mode='html')	
	except:pass
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


'''*******************************************start*****************************************************************'''

def register_handlers_casino(dp : Dispatcher):

	#Code
	dp.register_message_handler(comand_start, commands=["start"])