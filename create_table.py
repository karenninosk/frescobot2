import sqlite3

conn = sqlite3.connect('Restaurant.db')
c = conn.cursor()
c.execute('''
PRAGMA foreign_keys = ON;
''')
conn.commit()

c.execute('''
CREATE TABLE IF NOT EXISTS Orders(
    order INTEGER PRIMARY KEY AUTOINCREMENT,
    table INTEGER NOT NULL,
    date DATETIME NOT NULL,
    FOREIGN KEY(table) REFERENCES Tables(table)
); 
''')
conn.commit()

c.execute( '''
CREATE TABLE IF NOT EXISTS Order_ Dish(
order INTEGER NOT NULL,
dish INTEGER NOT NULL,
FOREIGN KEY( order) REFERENCES Orders(Order),
FOREIGN KEY( dish) REFERENCES Dishes(Dish)
);
''')
conn.commit()

c.execute( '''
CREATE TABLE IF NOT EXISTS Dishes (
Dish INTEGER PRIMARY KEY AUTOINCREMENT,
name TEXT UNIQUE NOT NULL,
type TEXT NOT NULL CHECK (type IN ('Tradicional', 'Sopa', 'Bebidas', 'Postre')),
ingredients TEXT,
price INTEGER NOT NULL,
availability BOOLEAN NOT NULL,
discount INTEGER,
vegetarian BOOLEAN NOT NULL
);
''')
conn.commit()

c.execute( '''
CREATE INDEX IF NOT EXISTS my_index ON Dishes( availability, type, vegetarian);
''')
conn.commit()
c.execute( '''
CREATE TABLE IF NOT EXISTS Tables (
table INTEGER PRIMARY KEY AUTOINCREMENT,
type TEXT NOT NULL CHECK (Type IN ('VIP', 'Vista calle', 'Salon')),
places INTEGER NOT NULL,
price INTEGER NOT NULL
);
''')
conn.commit()

c.execute( '''
CREATE TABLE IF NOT EXISTS Reservations (
table INTEGER NOT NULL,
date DATETIME NOT NULL,
FOREIGN KEY( table) REFERENCES Tables( table),
CONSTRAINT booking UNIQUE (table, date)
);
''')
conn.commit()

c.execute( '''
CREATE TABLE IF NOT EXISTS Income (
date DATETIME NOT NULL,
income INTEGER NOT NULL,
account_status INTEGER NOT NULL
);
''')
conn.commit()

c.close()
conn.close()
