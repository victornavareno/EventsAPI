import psycopg2

# ESTE ARCHIVO ES UN TEST PARA CONECTARSE A LA BASE DE DATOS CON LOS SIGUIENTES CREDENCIALES:
try:
    conn = psycopg2.connect(
        database="Eventos",
        host="localhost",
        user="postgres",
        password="12345",
        port="5433"
    )
    cur = conn.cursor()

    cur = conn.cursor()
    
    # cargo todos las tuplas en el cursor
    cur.execute("SELECT * FROM events;")
    rows = cur.fetchall()
    
    # Imprimo las lineas
    for row in rows:
        print(row)
    cur.close()
    conn.close()

except psycopg2.Error as e:
    print("Error connecting to the database:", e)