from application import mysql


def adaugare_fisa(id_client):
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO cosmin.tarife SET id_client=%s", (id_client,))
    mysql.connection.commit()
    cur.close()

def sterge_linkuri(id_data):
    sql = """DELETE FROM 
                        cosmin.linkuri 
                 WHERE 
                        id=%s
              """
    args = [id_data]
    cur = mysql.connection.cursor()
    cur.execute(sql, args)
    mysql.connection.commit()
    cur.close()