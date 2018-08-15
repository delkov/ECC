# import psycopg2


# try:
# 	connect = psycopg2.connect(database='eco_db', user='postgres', host='localhost', password='z5UHwrg8', port=5432)
# 	cursor = connect.cursor()
# except Exception as err:
# 	print('SQL  connect problem')


# table_name="eco.tracks";

# SQL='''
# SELECT *
#   FROM table_name LIMIT 1;
# '''

# # print('SQL QUERY', sql_query)
# # data = (sql_query[0],sql_query[0])
# cursor.execute(SQL, )
# answer= cursor.fetchall()


# print(answer)



aString = "hello world"
# print(aString[1:3])
print(aString.startswith(aString[0:3]))
