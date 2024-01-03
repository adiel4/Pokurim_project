from database import postgres_database

database = postgres_database.Database('pokurim_bot', 'postgres', 'adilet321')
database.connect()

da