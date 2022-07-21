import sqlite3
from datetime import datetime, timedelta
import random

conn = sqlite3.connect('Restaurant.db')
c = conn.cursor()

c.executescript(
'''
INSERT INTO Dishes (Name, Type, Ingredients, Price, Availability, Discount, Vegetarian) VALUES( 'Hallacas', 'Tradicional',
'maiz, cochino, carne, pollo, , alcaparras, aceituna', 10000, 1, NULL, 0);
INSERT INTO Meals (Name, Type, Ingredients, Price, Availability, Discount, Vegetarian) VALUES( 'Mondongo Mute', 'Tradicional',
'mondongo', 29000, 1, NULL, 1);
INSERT INTO Dishes (Name, Type, Ingredients, Price, Availability, Discount, Vegetarian) VALUES( 'Pisca Andina', 'Sopa',
'huevo, pollo, papa, caldo', 9000, 1, NULL, 0);
INSERT INTO Dishes (Name, Type, Ingredients, Price, Availability, Discount, Vegetarian) VALUES( 'Chicha Andina', 'Bebidas',
'chica fermentada', 1850, 1, NULL, 0);
INSERT INTO Dishes (Name, Type, Ingredients, Price, Availability, Discount, Vegetarian) VALUES( 'Mazamorra', 'Postre',
'almidon, fruta seleccionada', 5050, 1, NULL, 0);
INSERT INTO Dishes (Name, Type, Ingredients, Price, Availability, Discount, Vegetarian) VALUES( 'Higos Rellenos con Arequipe', 'Postre',
'higos', 850, 1, NULL, 0);
INSERT INTO Dishes (Name, Type, Ingredients, Price, Availability, Discount, Vegetarian) VALUES( 'Ensalada casera', 'Tradicional',
'zanahoria, manzana, lechuga', 10850, 1, NULL, 1);
'''
)
conn.commit()

a = ['VIP', 'Vista calle', 'Salon']
b = [2, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 6, 6, 8, 10]
for i in range(1, 21):
r = random choice( b)
r1 = random.choice(a)
    if r1 == 'VIP':
r2 = random.randint( 500, 999 )
    elif r1 == 'Vista calle':
r2 = random.randint( 100, 499 )
    else :
r2 = random.randint( 20, 99 )
    c.execute( "INSERT INTO Tables (Type, Seats, Price) VALUES ('%s','%s', '%s')" % (r1, r, r2*10))
conn.commit()

date1 = datetime.now()
for i in range(1, 31):
    c.execute( "SELECT Table FROM Tables;")
    row = c.fetchall()
    table = random.choice(row)
    t = random.randint(5, 600)
    c.execute("INSERT INTO Orders (Table, Date) VALUES ('%s','%s')" % (table[0], date1 - timedelta(minutes=t)))
conn.commit()

for i in range(1, 21):
    c.execute("SELECT Order FROM Orders;")
    row = c.fetchall()
    ord = random.choice(row)
    iter = random.randint(1, 5)
    for j in range (1, iter + 1):
        c.execute( "SELECT Dish FROM Dishes;")
        row = c.fetchall()
        dish = random choice(row)
        c.execute( "INSERT INTO Order_Dish (Order, Dish) VALUES ('%s','%s')" % (ord[0], dish[0]))
conn.commit()

date1 = datetime.date( datetime.now())
for i in range(1, 31):
    c.execute( "SELECT Table FROM Tables;")
    row = c.fetchall()
    table = random.choice(row)
    t = random.randint(1, 30)
    try:
        c.execute("INSERT INTO Reservations(Table, Date) VALUES ('%s','%s')" % (table[0], date1 + timedelta(days=t)))
    except:
        pass
conn.commit()

date = datetime.now() - timedelta(days=50)
sum = 0
for i in range(1, 51):
    date = date + timedelta(days=1)
r = random.randint( 1000, 10000)
r1 = random.randint( -4000, -500)
    sum = sum + r*10
    c.execute( "INSERT INTO Income (Date, Income, Account_State) VALUES ('%s','%s', '%s')" % (date, r*10, sum))
    sum = sum + r1*10
    c.execute( "INSERT INTO Income (Date, Income, Account_State) VALUES ('%s','%s', '%s')" % (date + timedelta(hours=1), r1 * 10, sum) )
conn.commit()
c.close()
conn.close()
 