from telegram.ext import Updater, MessageHandler, CallbackContext, CommandHandler, RegexHandler, ConversationHandler, Filters,  PicklePersistence
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
import sqlite3
from datetime import datetime
from emoji import emojize
import re
import requests
import logging

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',level=logging.INFO)

logger = logging.getLogger(__name__)

step = {}
ordername = {}
BOOK_DATE, BOOK_RES, BOOK_CHOICE, MENU_VEG, MENU_SHOW, ORDER, ORDER_INSERT, CHANGE_END = range(8)

def start(bot, update):
    id = update.message.chat_id
    em = emojize(':star:', use_aliases=True)
    bot.sendMessage(chat_id=id, text=em + em + em + '<b>Bienvenido al Restaurante FRESCO!</b> ' + em + em + em + '''
Para hacer un pedido, escriba /order
Para hacer una reserva, escriba /book
Para cambiar su reserva, escriba /change
Para cancelar su reserva, escriba /cancel
Para ver el menu, escriba /menu
Para cancelar la accion actual, escriba /back
Para finalizar, escriba /end

''', parse_mode='HTML')
    
# Booking
def book(bot, update):
    id = update.message.chat_id
    reply_keyboard = [['VIP', 'Vista calle'],['Salon', 'Cualquiera']]
    update.message.reply_text('¿Que mesa le gustaria elegir?',reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
    return BOOK_DATE
    
def book_date(bot, update, user_data):
    user_data['table'] = update.message.text
    update.message.reply_text('¿Para que fecha desea realizar la reserva?\n Ingrese la fecha en formato YYYY-MM-DD', reply_markup=ReplyKeyboardRemove())
    return BOOK_RES

def book_res(bot, update, user_data):
    user_data['date'] = update.message.text
    if user_data['table'] == 'Cualquiera':
        try :
            conn = sqlite3.connect('Restaurant.db')
            c = conn.cursor()
            c.execute('PRAGMA foreign_keys = ON;')
            conn.commit()
            c.execute('''SELECT * FROM Tables NATURAL JOIN
            (SELECT Table FROM Tables
            EXCEPT SELECT Table FROM Reservations
                WHERE Date = '%s') ORDER BY Price ASC ''' % (user_ data['date']))
            result = c.fetchall()
            c.close()
            conn.close()
            update.message.reply_text('Estas son las mesas disponibles' + user_data['date'] + ':')
            user_data['biggest'] = result[0][0]
            max = result[0][2]
            for row in result:
                if row[2] > max:
                    user_data['biggest'] = row[0]
                    max = row[2]
                update.message.reply_text(emojize(":large_blue_circle:", use_aliases=True) + 
                'Table #' + str(row[0]) + ' | ' + str(row[1]) + ' | Places: ' + str(row[2]) + ' | Price: ' + str(row[3]) + ' RUB')
                reply_keyboard = [['Economico','Grande']]
                user_data['cheapest'] = result[0][0]
                update.message.reply_text('Ingrese el numero de mesa o elija una de las opciones sugeridas.', reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
            except :
            update.message.reply_text('Parece que ha ingresado una fecha incorrecta. Intente nuevamente')
        else :
        try :
            conn = sqlite3.connect('Restaurant.db')
            c = conn.cursor()
            c.execute('PRAGMA foreign_keys = ON;')
            conn.commit()
            c.execute('''SELECT * FROM Tables NATURAL JOIN
            (SELECT Table FROM Tables
            EXCEPT SELECT Table FROM Reservations
            WHERE Date = '%s') WHERE Type = '%s' ORDER BY Price ASC ''' % (user_data['date'], str(user_data['table'])))
            result = c.fetchall()
            c.close()
            conn.close()
update.message.reply_text('Estas son las mesas disponibles' + str(user_data['table']).lower() + ' to ' + user_data['date'] + ':')
user_data['biggest'] = result[0][0]
            max = result[0][2]
            for row in result:
                if row[2] > max:
                    user_data['biggest'] = row[0]
                    max = row[2]
                update.message.reply_text(emojize(":large_blue_circle:", use_aliases=True) + 
                'Mesa N°' + str(row[0]) + ' | Ubicacion: ' + str(row[2]) + ' | Precio: S/' + str(row[3]))
reply_keyboard = [['Economico','Grande']]
user_data['cheapest'] = result[0][0]
update.message.reply_text('Ingrese el numero de mesa o elija una de las opciones sugeridas.', reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
        except :
update.message.reply_text('Parece que ha ingresado una fecha incorrecta. Intente nuevamente')
    return BOOK_CHOICE
    
def book_choice(bot,update,user_data):
    try:
        conn = sqlite3.connect('Restaurant.db')
        c = conn.cursor()
        c.execute('PRAGMA foreign_keys = ON;')
        conn.commit()
        c.execute("INSERT INTO Reservations(table, date) VALUES ('%s','%s')" % (update.message.text, user_data['date']))
        conn.commit()
        c.execute( "SELECT Price FROM Tables WHERE Table = '%s' " % (update.message.text))
        price = c.fetchone()
        d = datetime.now()
        c.execute( "SELECT AccountStatus FROM Income ORDER BY Date DESC LIMIT 1")
        summary = c.fetchone()
        c.execute( "INSERT INTO Revenue VALUES ('%s', '%s', '%s')" % (d, price[0], summary[0] + price[0]))
        conn.commit()
update.message.reply_text('Felicidades, ha reservado la mesa N°' + update.message.text + ' para el ' + user_data['date'] + '!'
+ '\n Si desea cancelar su reserva, presione /cancel.' + '\n Para cambiar su reserva, presione /change.', reply_markup= ReplyKeyboardRemove( ))
user_data['book'] = update.message.text
    except :
update.message.reply_text('Lo sentimos, Tuvimos problemas en registrar su reserva. Intentelo nuevamente.', reply_markup= ReplyKeyboardRemove( ))
    c.close()
    conn.close()
    return ConversationHandler.END

def book_button(bot,update,user_data):
    if update.message.text == 'Economico':
        try :
            conn=sqlite3.connect('Restaurant.db')
c = conn.cursor()
            c.execute('PRAGMA foreign_keys = ON;')
            conn.commit()
            c.execute("INSERT INTO Bookings (Table, Date) VALUES ('%s','%s')" % (user_data['cheapest'], user_data['date']))
            conn.commit()
            c.execute("SELECT Price FROM Tables WHERE Table = '%s' " % (user_data['cheapest']))
            price = c.fetchone()
d = datetime.now()
            c.execute("SELECT AccountStatus FROM Income ORDER BY Date DESC LIMIT 1")
            summary = c.fetchone()
            c.execute("INSERT INTO Revenue VALUES ('%s', '%s', '%s')" % (d, price[0], summary[0] + price[0]))
            conn.commit()
            c.close()
            conn.close()
update.message.reply_text('Felicidades, ha reservado la mesa economica N°' + str(user_data['cheapest']) + ' para el ' + user_data['date'] + '!'
+ '\n Si desea cancelar su reserva, presione /cancel.' + '\n Para cambiar su reserva, presione /change.', reply_markup= ReplyKeyboardRemove( ))
user_data['book'] = user_data['cheapest']
        except :
update.message.reply_text( 'Lo sentimos, Tuvimos problemas en registrar su reserva. Intentelo nuevamente.', reply_markup= ReplyKeyboardRemove( ))
    else :
        try :
            conn = sqlite3.connect('Restaurant.db')
            c = conn.cursor()
            c.execute('PRAGMA foreign_keys = ON;')
            conn.commit()
            c.execute("INSERT INTO Bookings (Table, Date) VALUES ('%s','%s')" % (user_data['biggest'], user_data['date']))
            conn.commit()
            c.execute("SELECT Price FROM Table WHERE Table = '%s' " % (user_data['biggest']))
            price = c.fetchone()
d = datetime.now()
            c.execute("SELECT AccountStatus FROM Income ORDER BY Date DESC LIMIT 1")
            summary = c.fetchone()
            c.execute("INSERT INTO Revenue VALUES ('%s', '%s', '%s')" % (d, price[0], summary[0] + price[0]))
            conn.commit()
            c.close()
            conn.close()
update.message.reply_text('Felicidades, ha reservado la mesa grande N°' + str(user_data['biggest']) + ' para el ' + user_data['date'] + '!'
+ '\n Si desea cancelar su reserva, presione /cancel.' + '\n Para cambiar su reserva, presione /change.', reply_markup= ReplyKeyboardRemove( ))
user_data['book'] = user_data['biggest']
        except :
update.message.reply_text('Lo sentimos, Tuvimos problemas en registrar su reserva. Intentelo nuevamente.', reply_markup= ReplyKeyboardRemove( ))
    return ConversationHandler.END
# Booking - end
# Menu
def menu(bot, update):
    id = update.message.chat_id
reply_keyboard = [['Tradicional'], ['Sopa'], ['Postre', 'Bebidas']]
update.message.reply_text('Elija una categoria', reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
    return MENU_VEG
    
def menu_veg(bot, update, user_data):
user_data['type'] = update.message.text
reply_keyboard = [['Yes', 'No']]
update.message.reply_text('¿Es usted vegetariano?', reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
    return MENU_SHOW
    
def menu_show(bot, update, user_data):
    conn = sqlite3.connect('Restaurant.db')
    c = conn.cursor()
    c.execute('PRAGMA foreign_keys = ON;')
    conn.commit()
    if user_data['type'] == 'Todas':
        if update.message.text == 'Si':
            c.execute('''SELECT * FROM Dishes WHERE Vegetarian = 1 AND Availability = 1 ''')
        else:
            c.execute('''SELECT * FROM Dishes WHERE Availability = 1 ''')
        result = c.fetchall()
        for row in result:
update.message.reply_text(emojize(":fork_and_knife:", use_aliases=True) +
'Platillo: ' + str(row[1]) + ' | Tipo: ' + str(row[2]) + '\n Ingredientes: ' + str(row[3]) + '\n Precio:S/ ' + str(row[4]))
    else :
        if update.message.text == 'Si':
            c.execute( '''SELECT * FROM Dish WHERE Vegetarian = 1 AND Availability = 1 AND Type = '%s' ''' % (str(user_data['type'])))
        else :
            c.execute( '''SELECT * FROM Dish WHERE Availability = 1 AND Type = '%s' ''' % (str(user_data['type'])))
        result = c.fetchall()
        if result is None:
update.message.reply_text('Lo siento, no hay platos disponibles, vuelva al menu /menu',reply_markup= ReplyKeyboardRemove( ))
            return ConversationHandler.END
        if user_data['type'] == 'Tradicional':
            s = ' :stew :'
        elif user_data['type'] == 'Bebidas':
            s = ' :milk :'
        elif user_data['type'] == 'Sopa':
            s = ':ramen:'
        elif user_data['type'] == 'Postre':
            s = ':shaved_ice:'
        else:
            s = ':spaghetti:'
        for row in result:
            update.message.reply_text(emojize(s, use_aliases=True) + 
'Platillo: ' + str(row[1]) + '\n Ingredientes: ' + str(row[3]) + '\n Precio:S/ ' + str(row[4]))
reply_keyboard = [[str(row[1])] for row in result]
update.message.reply_text('''Por favor seleccione el plato a ordenar.\n Tambien puede escribirlo.
''', reply_markup= ReplyKeyboardMarkup(reply_keyboard,one_time_keyboard=True))
    c.close()
    conn.close()
    if 'order_table' in user_data:
        return ORDER_INSERT
    return ORDER
# Menu - end
# Order
def order(bot,update,user_data):
    if update.message.text != '/order':
user_data['dish'] = update.message.text
    if 'order_table' not in user_data:
update.message.reply_text('Ingrese su N° de mesa', reply_markup=ReplyKeyboardRemove())
    else:
        update.message.reply_text('Ingrese el platillo a ordenar')
    return ORDER_INSERT
    
def order_insert(bot, update, user_data):
    if 'order_table' not in user_data:
        try:
            user_data['order_table'] = update.message.text
            conn = sqlite3.connect('Restaurant.db')
            c = conn.cursor()
            c.execute('PRAGMA foreign_keys = ON;')
            conn.commit()
            date = str(datetime.now())
            c.execute("INSERT INTO Orders (Table, Date) VALUES ('%s','%s')" % (user_data['order_table'], date))
            conn.commit()
            c.execute("SELECT Order FROM Orders WHERE Table = '%s' AND Date = '%s'" % (user_data['order_table'], date))
            row = c.fetchone()
user_data['ord'] = row[0]
            c.close()
            conn.close()
        except :
update.message.reply_text('Error. N°de mesa no valida.')
            return ORDER_INSERT
    else :
user_data['dish'] = update.message.text
    if 'dish' not in user_data:
update.message.reply_text('Ingrese el platillo a ordenar')
        return ORDER_INSERT
    conn = sqlite3.connect('Restaurant.db')
c = conn.cursor()
    c.execute('PRAGMA foreign_keys = ON;')
    conn.commit()
    c.execute("SELECT Dish, Price FROM Dish WHERE Name ='%s' " % (str(user_data['dish'])))
    row = c.fetchone()
    if row is None:
        c.close()
        conn.close()
update.message.reply_text('Este platillo no existe, por favor intente nuevamente. Puede revisar el menu escribiendo /menu')
        return ORDER_INSERT
    else :
        c.execute("INSERT INTO Order_Dish (Order, Dish) VALUES ('%s','%s')" % (user_data['ord'], row[0]))
        conn.commit()
d = datetime.now()
        c.execute("SELECT AccountStatus FROM Income ORDER BY Date DESC LIMIT 1")
        summary = c.fetchone()
        c.execute("INSERT INTO Income VALUES ('%s', '%s', '%s')" % (d, row[1], summary[0] + row[1]))
        conn.commit()
update.message.reply_text('El platillo fue agregado a su orden!\n' +
'Puede escribir otro platillo para agregarlo o ver nuestro menu /menu.\n' +
'Escriba /back en caso ya no tenga mas ordenes.\n' +
'Para finaliza y salir escriba /end')
    c.close()
    conn.close()
    return ORDER_INSERT
#Order - end
#Removing armor
def cancel(bot,update,user_data):
    if 'book' not in user_data:
update.message.reply_text('No tenemos reserva registrada en esta sesion.')
        return ConversationHandler.END
    conn = sqlite3.connect('Restaurant.db')
    c = conn.cursor()
    c.execute('PRAGMA foreign_keys = ON;')
    conn.commit()
    c.execute("DELETE FROM Reservations WHERE table='%s' AND date='%s' " % (user_data['book'], user_data['date']))
    conn.commit()
    c.close()
    conn.close()
update.message.reply_text('La Mesa N°' + str(user_data['book']) + ' esta nuevamente disponible para ser reservada ' + str(user_data['date']) + '!')
    return ConversationHandler.END
#Removal of armor - the end
#Change armor
def change(bot,update,user_data):
    if 'book' not in user_data:
update.message.reply_text('No tenemos reserva registrada en esta sesion.')
        return ConversationHandler.END
update.message.reply_text('Ingrese el numero de mesa del cual desea cambiar la reserva.')
    return CHANGE_END
    
def change_end(bot,update,user_data):
    conn = sqlite3.connect('Restaurant.db')
c = conn.cursor()
    try :
        c.execute('PRAGMA foreign_keys = ON;')
        conn.commit()
        c.execute("UPDATE Reservations SET Table='%s' WHERE Table='%s' AND Date='%s' " % (update.message.text, user_data['book'], user_data['date'] ))
        conn.commit()
    except :
update.message.reply_text('Error! EL numero de mesa no es valido o esta ya no esta disponible. Para cancelar su reserva anterior escriba /cancel')
    c.close()
    conn.close()
update.message.reply_text('Mesa N°' + str(user_data['book']) + ' fue cambiada por la N°' + str(update.message.text) + ', para la fecha ' + str(user_data['date']) + '!')
user_data['book']=update.message.text
    return ConversationHandler.END
#Change Armor - End
def end(bot,update,user_data):
update.message.reply_text('Hasta luego, ¡que lo disfrute!\n Para ayuda, escriba /start',
reply_markup= ReplyKeyboardRemove( ))
user_data.clear()
    return ConversationHandler.END

def back(bot,update,user_data):
update.message.reply_text( 'Ha anulado su ultima accion.\n Para ayuda, escriba /start',
reply_markup= ReplyKeyboardRemove( ))
    return ConversationHandler.END

def texter(bot,update):
    update.message.reply_text('Lo siento, no te entendi :)')
    return ConversationHandler.END

def main():
    updater = Updater(token='5513146575:AAHngkSzWxCFNHDYPLVvq84At1U2mdvGPT0', use_context=True)
    
    dispatcher = updater.dispatcher
    
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start), 
        CommandHandler("order", order, pass_user_data=True), 
        CommandHandler("end", end, pass_user_data=True), 
        CommandHandler("book", book),
        CommandHandler("menu", menu),
        CommandHandler("cancel", cancel, pass_user_data=True),
        CommandHandler("change", change, pass_user_data=True)],

        states={
            BOOK_DATE: [RegexHandler('^(VIP|Vista calle|Salon|Cualquiera)$', book_date, pass_user_data=True)],
BOOK_RES: [ RegexHandler('^(\d\d\d\d-\d\d-\d\d)$', book_res, pass_user_data=True)],
BOOK_CHOICE: [ RegexHandler('^(Economico|Grande)$', book_button, pass_user_data=True),
                RegexHandler('^(\d+)$', book_choice, pass_user_data=True)],
MENU_VEG: [ RegexHandler('^(Tradicional|Sopa|Postre|Bebida|Todas)$', menu_veg, pass_user_data=True)],
MENU_SHOW: [ RegexHandler('^(Si|No)$', menu_show, pass_user_data=True)],
            ORDER: [MessageHandler(Filters.text, order, pass_user_data=True)],
            ORDER_INSERT: [MessageHandler(Filters.text, order_insert, pass_user_data=True)],
            CHANGE_END: [RegexHandler('^(\d+)$', change_end, pass_user_data=True)]
        },

        fallbacks=[CommandHandler('end',end,pass_user_data=True), CommandHandler('back',back,pass_user_data=True), CommandHandler('menu',menu), MessageHandler(Filters.text,texter,pass_user_data=True)]
    )
     
    dispatcher.add_handler(conv_handler)
       
    updater.start_polling()
    updater.idle()
    
if __name__ == '__main__':
    main()
