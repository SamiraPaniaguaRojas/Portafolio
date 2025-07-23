import pymysql

def obtener_conexion():
    return pymysql.connect(
        host='localhost',
        user='root',
        password='123456789',
        db='escuela',
        port=3307,
        cursorclass=pymysql.cursors.DictCursor
    )
