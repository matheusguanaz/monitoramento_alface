import psycopg2

def executarSelect(query):
    conn = psycopg2.connect(host="",database="",user="",password="")
    cursor = conn.cursor()
    cursor.execute(query)
    result = cursor.fetchall()
    conn.close()
    return result

def execUpdateOuInsert(query):
    conn = psycopg2.connect(host="",database="",user="",password="")
    cursor = conn.cursor()
    cursor.execute(query)
    conn.commit()
    conn.close()