from datetime import datetime

from aiogram import Bot, types

from aiogram.dispatcher import Dispatcher

from aiogram.utils import executor

from aiogram.types import ReplyKeyboardRemove,  ReplyKeyboardMarkup, KeyboardButton,  InlineKeyboardMarkup, InlineKeyboardButton,InputMediaPhoto

from aiogram.contrib.fsm_storage.memory import MemoryStorage

from random import randint

import os 

from bd_people import people2

from bd_people2 import people

def save():

  global people2

  f=open('bd_people.py','w+')

  f.write('people2='+str(people2))

  f.close()

  

  global people

  #people[2028784660]['class']['people']=[t for t in people2 if t!=0]

  f=open('bd_people2.py','w+')

  f.write('from bd_people import people2\npeople='+str(people))

  f.close()

def new_people(message):

  global people

  

  if message.from_user.id not in people:

    

    

    people.update({message.from_user.id:{'class':False,'name':message.from_user.first_name,'user':message.from_user.username,'action':[None,None]}})

    save()

  

TOKEN = '5887726218:AAGxILdh6jVAdM0UZunTFN91t3qneBgDiws'

bot = Bot(token=TOKEN)

dp = Dispatcher(bot)

@dp.message_handler(content_types=types.ContentTypes.PHOTO)

async def send_to_admin(message: types.Message):

  print('PHOTO',message.from_user.first_name  )

  

  #await bot.send_message(message.chat.id,'<span class="tg-spoiler">spoiler</span>',parse_mode="html")

  #await bot.send_photo(chat_id=2028784660, photo=message.photo[-1].file_id)

  if people[message.from_user.id]['action'][0] != None and people[message.from_user.id]['action'][0][0:10] == 'edit_photo':

    await message.photo[-1].download(destination_file=f'{people[message.from_user.id]["action"][0].split("_")[-1]}.jpg')

    people2[int(people[message.from_user.id]["action"][0].split("_")[-1])][0]=people[message.from_user.id]["action"][0].split("_")[-1]

    people[message.from_user.id]['action'][0]=None

    await bot.send_message(message.from_user.id,'Фото обновлено')

  save()

@dp.message_handler(lambda msg: msg.from_user.id==2028784660 and "/see" in msg.text)

async def see(message):

  global people,people2

  if message.text[0:6]=="/see_3":

    await bot.send_message(int(message.text.split("_")[2]), message.text.split("_")[3])

    await bot.send_message(message.from_user.id,f'send {message.text.split("_")[2]}\ntext {message.text.split("_")[3]}')

  if message.text=="/see 2":

    a=""

    for t in people2:

      if True:

         a+=str(t)+" {"

         try:

             a+=f"\n    Photo: {str(people2[t][0])}\n    BIO: {str(people2[t][1])}\n    Name: {str(people2[t][2])}"

         except: a+=str(people2 [t])

         a+="\n}\n\n"

      else: pass

    await bot.send_message(message.chat.id,a)

  if message.text=='/see':

    a=''

    for t in people:

      a+=str(t)+' {\n'

      try:

       for y in people[t]:

          if type(people[t][y])==dict:

           b='  class {\n'

           for j in people[t][y]:

              b+='    '+j+' : '+str(people[t][y][j])+'\n'

           b+='  }\n'

          else:

           b='  '+y+' : '+str(people[t][y])+'\n'

          a+=b

       

      except Exception as e:

        print(e)

      a+='\n}\n'

    await bot.send_message(message.chat.id,a)

  elif "/see" in message.text:

    if len(message.text.split())==4:

      people[int(message.text.split()[1])][message.text.split()[2]]=message.text.split()[-1]

    elif len(message.text.split())==5:

       people[int(message.text.split()[1])][message.text.split()[2]][message.text.split()[3]]=message.text.split()[-1]

    save()

    await bot.send_message(message.chat.id,'Work')

    

    

@dp.message_handler(commands=['start'])

async def start(message):

  global people 

  

  if message.from_user.id not in people:

    await bot.send_message(-1001760137677,f'Новый человек <a href="tg://user?id={message.from_user.id}">{message.from_user.first_name}</a>',parse_mode="html")

  new_people(message)

  print(message.text)

  if message.text=="/start":

    await bot.send_message(message.chat.id,f'Привет <a href="tg://user?id={message.from_user.id}">{message.from_user.first_name}</a>! Сдесь ты можешь добавить информацию о своем классе или посмотреть другие классы\nНапиши /menu чтобы продолжить',parse_mode="html")

  else:

    markup=InlineKeyboardMarkup(row_width=2)

    if message.from_user.first_name not in people[int(message.text.split(' ')[1])]['class']['views'] and message.from_user.first_name != people[int(message.text.split(' ')[1])]['name']:

      people[int(message.text.split(' ')[1])]['class']['views'].append(message.from_user.first_name)

      await bot.send_message(int(message.text.split(' ')[1]),f'Ваш класс посмотрел(-a) <a href="tg://user?id={message.from_user.id}">{message.from_user.first_name}</a>',parse_mode="html")

      save()

    for t in people[int(message.text.split(' ')[1])]['class']['people']:

      markup.add(InlineKeyboardButton(text=people2[t][2], callback_data=t))

    await bot.send_message(message.from_user.id,text='Класс '+people[int(message.text.split(' ')[1])]['class']['name'], reply_markup=markup)

    

    

@dp.message_handler(commands=['menu'])

async def menu(message):

  new_people(message)

  global people

  markup_menu = InlineKeyboardMarkup(row_width=1)

  markup_menu.add(InlineKeyboardButton(text='👀Смотреть школы', callback_data='see_schools')) 

  if not people[message.from_user.id]['class']:

   markup_menu.add(InlineKeyboardButton(text='➕Добавить свой класс', callback_data='create_class'))

  else:

    markup_menu.add(InlineKeyboardButton(text='✏️Изменить информацию о классе', callback_data='edit_class'))

  markup_menu.add(InlineKeyboardButton(text='❓Помощь', callback_data='help'))

  await bot.send_message(message.chat.id,'Меню',reply_markup=markup_menu)

@dp.message_handler()

async def messag(message):

  global people

  new_people(message)

  

  print('Message',message.from_user.first_name,':',message.text)

  if people[message.from_user.id]['action'][0]=='reg_name':

    people[message.from_user.id]['class']['name']=message.text

    people[message.from_user.id]['action'][0]='reg_school'

    markup=InlineKeyboardMarkup(row_width=1)

    for t in people['schools']:

      markup.add(InlineKeyboardButton(text=t,callback_data='class_school_'+str(people['schools'].index(t))))

    await bot.send_message(message.from_user.id,'Выбирите школу',reply_markup=markup)

  

  if people[message.from_user.id]['action'][0] != None and people[message.from_user.id]['action'][0][0:13] == 'create_school':

    try:

      people[message.from_user.id]['action'][1]=message.text

      markup = InlineKeyboardMarkup(row_width=2)

      markup.add(InlineKeyboardButton(text='Одобрить', callback_data='True_'+str(message.from_user.id)))

      markup.add(InlineKeyboardButton(text='Не одобрить', callback_data='False_'+str(message.from_user.id)))

    

      await bot.send_message(-1001760137677,f' <a href="tg://user?id={message.from_user.id}">{message.from_user.first_name}</a> create school  {message.text}',reply_markup=markup,parse_mode='html')

      people[message.from_user.id]['action'][0]=None

      await bot.send_message(message.from_user.id,'Ваш запрос на создание новой школы в обработке это займет до 2 дней Если название школы одобрят вам прийдет сообщение')

    except Exception as e:

      await bot.send_message(2028784660,e)

    

  if people[message.from_user.id]['action'][0] != None and people[message.from_user.id]['action'][0][0:10] == 'edit_photo':

    if 'https' in message.text:

      people2[int(people[message.from_user.id]["action"][0].split("_")[-1])][0]=message.text

      people[message.from_user.id]['action'][0]=None

      await bot.send_message(message.from_user.id,'Фото обновлено')

    else:

      await bot.send_message(message.from_user.id,'Надо отправить фото или ссылку на фото , а не текст')

  

  if people[message.from_user.id]['action'][0]!=None and people[message.from_user.id]['action'][0][0:8] == 'edit_bio':

    people2[int(people[message.from_user.id]['action'][0].split('_')[-1])][1]=message.text

    people[message.from_user.id]['action'][0]=None

    await bot.send_message(message.from_user.id,'Биография успешно изменена на '+message.text)

  if people[message.from_user.id]['action'][0]!=None and people[message.from_user.id]['action'][0][0:9]  == 'edit_name':

    people2[int(people[message.from_user.id]['action'][0].split('_')[-1])][-1]=message.text

    people[message.from_user.id]['action'][0]=None

    await bot.send_message(message.from_user.id,'Имя успешно изменено на '+message.text)

  if people[message.from_user.id]['action'][0]=='edit_class_name':

    people[message.from_user.id]['class']['name']=message.text

    

    await bot.send_message(message.from_user.id,'Имя класса изменено на '+message.text)

    people[message.from_user.id]['action'][0]=None

    save()

    markup=InlineKeyboardMarkup(row_width=2)

    if not people[message.from_user.id]['class']:

        people[message.from_user.id]['class']={'name':'Нету','type':'Закрытый','people':[]}

        save()

        

    markup.row(InlineKeyboardButton(text='◀️Назад', callback_data=f'back'))

    markup.row(InlineKeyboardButton(text='Тип '+str(people[message.from_user.id]['class']['type']), callback_data=f'class_type_edit'))

      

    markup.row(InlineKeyboardButton(text='Название класса: '+people[message.from_user.id]['class']['name'], callback_data=f'class_edit_name'))

    markup.row(InlineKeyboardButton(text='Школа: '+people[message.from_user.id]['class']['school'], callback_data=f'class_edit_school'))

    markup.row(InlineKeyboardButton(text='Просмотры: '+str(len(people[message.from_user.id]['class']['views'])), callback_data=f'class_views'))

    

    markup_people=[]

    for t in people[message.from_user.id]['class']['people']:

      markup.row(InlineKeyboardButton(text=people2[t][-1], callback_data=f'edit_people_'+str(t)), InlineKeyboardButton(text="🗑️",callback_data=f"delete_people_{t}"))

    markup.row(InlineKeyboardButton(text='➕Добавить человека', callback_data=f'class_append_people'))

    await bot.send_message(message.from_user.id,text='Ваш класс\nСсылка на класс https://t.me/BookClassesBot?start={0}\nПросто отправьте ссылку другу чтобы он увидел ваш класс'.format(message.from_user.id),reply_markup=markup)

  save()

 

    

@dp.callback_query_handler()

async def process_callback_button(call: types.CallbackQuery):

    print('BUTTON',call.from_user.first_name,':',call.data)

    global people,people2

    #await bot.answer_callback_query(

            #call.id,

           # text='Помощь https://rawskeletalperl.agzamikail.repl.co/chat.html',show_alert=True)

    markup_menu = InlineKeyboardMarkup(row_width=1)

    markup_menu.add(InlineKeyboardButton(text='👀Смотреть школы', callback_data='see_schools'))

    

    if call.data=='class_type_edit':

      if people[call.from_user.id]['class']['type']=='Закрытый':

          people[call.from_user.id]['class']['type']='Открытый'

      else:

          people[call.from_user.id]['class']['type']='Закрытый'

      save()

      call.data='edit_class'

  

    if call.data=='class_edit_name':

      people[call.from_user.id]['action'][0]='edit_class_name'

      await bot.send_message(call.from_user.id,'Напишите название класса: ')

   

    if call.data=='see_schools' or call.data=="back2":

      markup=InlineKeyboardMarkup(row_width=1)

      markup.add(InlineKeyboardButton(text="◀️Назад", callback_data=f'back'))

      for t in people['schools']:

         markup.add(InlineKeyboardButton(text=t, callback_data=f'school {people["schools"].index(t)}'))

      await call.message.edit_text(text='Школы', reply_markup=markup)

      

    

    elif call.data[0:6]=='school':

      markup=InlineKeyboardMarkup(row_width=1)

      markup.add(InlineKeyboardButton(text="◀️Назад", callback_data=f'see_schools'))

      

      for t in people:

        try:

          if people[t]['class']['school']==people['schools'][int(call.data.split()[1])] and people [t]['class']["type"]=="Открытый":

              markup.add(InlineKeyboardButton(text=people[t]['class']['name'], callback_data=f'class {t} {call.data.split()[1]}'))

        except:

          pass

          

      await call.answer(cache_time=2)

      await call.message.edit_text(text='Классы школы '+people['schools'][int(call.data.split()[-1])], reply_markup=markup)

    elif call.data=='create_class':

      people[call.from_user.id]['class']={'name':'Нету','type':'Закрытый','people':[],'views':[],'school':'Без школы'}

      people[call.from_user.id]['action'][0]='reg_name'

      save()

      await bot.send_message(call.from_user.id,'Скажите название класса')

    elif call.data=='edit_class':

      markup=InlineKeyboardMarkup(row_width=2)

      

        

        

      markup.row(InlineKeyboardButton(text='◀️Назад', callback_data=f'back'))

      markup.row(InlineKeyboardButton(text='Тип '+str(people[call.from_user.id]['class']['type']), callback_data=f'class_type_edit'))

      

      markup.row(InlineKeyboardButton(text='Название класса: '+people[call.from_user.id]['class']['name'], callback_data=f'class_edit_name'))

      markup.row(InlineKeyboardButton(text='Школа: '+people[call.from_user.id]['class']['school'], callback_data=f'class_edit_school'))

      markup.row(InlineKeyboardButton(text='Просмотры: '+str(len(people[call.from_user.id]['class']['views'])), callback_data=f'class_views'))

    

      

      for t in people[call.from_user.id]['class']['people']:

        

        markup.row(InlineKeyboardButton(text=people2[t][-1], callback_data="edit_people_"+str(t)), InlineKeyboardButton(text="🗑️",callback_data="delete_people_"+str(t)))

      markup.row(InlineKeyboardButton(text='➕Добавить человека', callback_data=f'create_people'))

      await call.message.edit_text(text='Ваш класс\nСсылка на класс https://t.me/BookClassesBot?start={0}\nПросто отправьте ссылку другу чтобы он увидел ваш класс'.format(call.from_user.id),reply_markup=markup)

    elif call.data[0:11]=='edit_people' or call.data=='create_people':

      if call.data=='create_people':

        people2.update({people2[0]+1:['Нет' for t in range(3)]})

        people[call.from_user.id]['class']['people'].append(people2[0]+1)

        people2[0]+=1

        call.data='edit_people_'+str(people2[0])

        save()

      markup=InlineKeyboardMarkup(row_width=0)

      markup.row(InlineKeyboardButton(text='◀️Назад',callback_data='edit_class'))

      markup.row(InlineKeyboardButton(text='Имя '+people2[int(call.data.split('_')[-1])][-1],callback_data='edit_name_'+call.data.split('_')[-1]))

      markup.row(InlineKeyboardButton(text='О человеке: '+people2[int(call.data.split('_')[-1])][1],callback_data='edit_bio_'+call.data.split('_')[-1]))

      markup.row(InlineKeyboardButton(text='Изменить фото',callback_data='edit_photo_'+call.data.split('_')[-1]))

      try:

          photo=open(call.data.split('_')[-1]+".jpg",'rb')

      except Exception as e:

        print(e)

        if 'https' in people2[int(call.data.split('_')[-1])][0]:

          photo=people2[int(call.data.split('_')[-1])][0]

        else:

          photo='https://okeygeek.ru/wp-content/uploads/2016/07/images.png'

      await bot.delete_message(call.message.chat.id, call.message.message_id)

      await bot.send_photo(call.from_user.id,photo)

      await bot.send_message(call.from_user.id,reply_markup=markup,text='Изменение информации о человеке')

      

    elif call.data[0:3]=="yes":

      people [call.from_user.id]["class"]["people"].remove(int(call.data.split("_")[-1]))

      save()

      await bot.delete_message(call.message.chat.id, call.message.message_id)

      await bot.send_message(call.from_user.id,"Человек удален из класса")

    elif call.data=='empty':

      await bot.delete_message(call.message.chat.id, call.message.message_id)

    elif call.data.split("_")[0]=="delete" and call.data.split("_")[1]=="people":

      markup=InlineKeyboardMarkup(row_width=2)

      markup.add(InlineKeyboardButton(text="Да",callback_data="yes_"+call.data.split("_")[-1]), InlineKeyboardButton(text="Нет", callback_data="empty"))

      await bot.send_message(call.from_user.id,"Вы точно хотите удалить человека?",reply_markup=markup)

    elif call.data=="help":

      markup = InlineKeyboardMarkup(row_width=1)

      markup.add(InlineKeyboardButton(text='◀️Назад',callback_data='back'))

      await call.message.edit_text(text="❓ Справка по Book Classes Bot\nhttps://telegra.ph/Pomoshch-v-Book-Classes-Bot-01-15",reply_markup=markup,parse_mode="html")

    elif call.data=='back':

      

      markup_menu = InlineKeyboardMarkup(row_width=1)

      markup_menu.add(InlineKeyboardButton(text='👀Смотреть школы', callback_data='see_schools'))

      if not people[call.from_user.id]['class']:

        markup_menu.add(InlineKeyboardButton(text='➕Добавить свой класс', callback_data='create_class'))

      else:

        markup_menu.add(InlineKeyboardButton(text='✏️Изменить информацию о классе', callback_data='edit_class'))

      markup_menu.add(InlineKeyboardButton(text='❓Помощь', callback_data='help'))

      await call.message.edit_text(text='Меню', reply_markup=markup_menu)

    elif call.data[0:4]=='True':

      people[call.from_user.id]['action'][0]=None

      people['schools'].append(people[call.from_user.id]['action'][1])

      people[int(call.data.split('_')[1])]['class']['school']=people[call.from_user.id]['action'][1]

      await bot.send_message(int(call.data.split('_')[1]),'Название школы одобрено вашу школу добавили')

      await call.message.edit_text(text='Школа добавлена в БД')

      people[call.from_user.id]['action'][1]=None

    elif call.data[0:5]=='False':

      people[call.from_user.id]['action'][0]=None

      await bot.send_message(int(call.data.split('_')[1]),f'Название школы не одобрено {people[call.from_user.id]["action"][1]}')

      await call.message.edit_text(text='Школа НЕ добавлена в БД')

      people[call.from_user.id]['action'][1]=None

    elif call.data == 'create_school':

      people[call.from_user.id]['action'][0]=call.data

      await bot.send_message(call.from_user.id,'Скажите название школы')

    elif call.data[0:12] == 'class_school':

      people[call.from_user.id]['class']['school']=people['schools'][int(call.data.split('_')[-1])]

      print(people[call.from_user.id]['action'])

      if people[call.from_user.id]['action'][0]=='reg_school':

        people[call.from_user.id]['action'][0]=None

        markup=InlineKeyboardMarkup(row_width=1)

        markup.add(InlineKeyboardButton(text='Дальше',callback_data='edit_class'))

        await bot.send_message(call.from_user.id,'Вы выбрали школу '+people['schools'][int(call.data.split('_')[-1])],reply_markup=markup)

      else:

        await bot.send_message(call.from_user.id,'Школа изменена на '+people['schools'][int(call.data.split('_')[-1])])

      

    elif call.data == 'class_edit_school':

      

      markup=InlineKeyboardMarkup(row_width=1)

      markup.add(InlineKeyboardButton(text='◀️Назад',callback_data='edit_class'))

      for t in people['schools']:

        

        markup.add(InlineKeyboardButton(text=t,callback_data='class_school_'+str(people['schools'].index(t))))

        

      markup.add(InlineKeyboardButton(text='➕Добавить свою школу',callback_data='create_school'))

      try:

        await call.message.edit_text("Выберите школу",reply_markup=markup)

      except Exception as e:

        print(e)

    elif call.data=='class_views':

      markup=InlineKeyboardMarkup(row_width=0)

      markup.row(InlineKeyboardButton(text='◀️Назад',callback_data='edit_class'))

      if len(people[call.from_user.id]['class']['views'])==1:

        a='посмотрел(-а)'

      else:

        a='посмотрели'

      if len(people[call.from_user.id]['class']['views'])!=0:

        await call.message.edit_text(text='<b>Статистика:</b>\nВаш класс посмотрелo '+str(len(people[call.from_user.id]['class']['views']))+f' человек\nВаш класс {a} '+' '.join(people[call.from_user.id]['class']['views']),reply_markup=markup,parse_mode='html')

      else:

        await call.message.edit_text(text='Ваш класс еще никто не посмотрел',reply_markup=markup)

    elif call.data[0:9] == 'edit_name':

      await bot.send_message(call.from_user.id,'Скажите имя человека')

      people[call.from_user.id]["action"][0]=call.data

    elif call.data[0:8] == 'edit_bio':

      await bot.send_message(call.from_user.id,'Скажите биографию для человека')

      people[call.from_user.id]["action"][0]=call.data

    elif call.data[0:10] == 'edit_photo':

      await bot.send_message(call.from_user.id,'Отправьте фото или ссылку на фото')

      people[call.from_user.id]["action"][0]=call.data

    elif call.data.split(' ')[0]=='class':

       if call.from_user.first_name not in people[int(call.data.split(' ')[1])]['class']['views'] and call.from_user.first_name != people[int(call.data.split(' ')[1])]['name']:

          people[int(call.data.split(' ')[1])]['class']['views'].append(call.from_user.first_name)

          await bot.send_message(int(call.data.split(' ')[1]),f'Ваш класс посмотрел(-a) <a href="tg://user?id={call.from_user.id}">{call.from_user.first_name}</a>',parse_mode="html")

          save()

      

       markup=InlineKeyboardMarkup(row_width=2)

       markup.add(InlineKeyboardButton(text="◀️Назад", callback_data=f'school {call.data.split()[2]}'))

       

       for t in people[int(call.data.split(' ')[1])]['class']['people']:

         try:

          markup.add(InlineKeyboardButton(text=people2[t][2], callback_data=t))

         except Exception as e:

           print(e)

       

       await call.message.edit_text(text='Класс '+people[int(call.data.split(' ')[1])]['class']['name'], reply_markup=markup)

    else:

      try:

        try:

          photo=open(f'{people2[int(call.data)][0]}.jpg','rb')

        except:

          if 'https' in people2[int(call.data)][0]:

            photo=people2[int(call.data)][0]

          else:

            photo='https://okeygeek.ru/wp-content/uploads/2016/07/images.png'

        markup=InlineKeyboardMarkup(row_width=2)

        markup.add(InlineKeyboardButton(text="◀️Назад", callback_data=f'empty'))

        await bot.send_photo(call.from_user.id,photo , caption=people2[int(call.data)][2]+'\n'+people2[int(call.data)][1],reply_markup=markup)

      except Exception as e:

        print('Error:' + str(e))

    save()

if __name__ == '__main__':

    executor.start_polling(dp)
