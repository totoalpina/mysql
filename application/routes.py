from flask import Flask, render_template, request, redirect, flash, url_for, session
from application import app, mysql
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import MySQLdb.cursors



# FOLOSESC BAZE DE DATE SEPARATE PENTRU UTILIZATORI SI PENTRU DATE

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

def iesire_user():
    session.pop('utilizator', None)



@app.route('/')
@app.route('/home', methods=['GET', 'POST'])
def home():
    return render_template('home.html')


@app.route('/logare', methods=['GET', 'POST'])
def logare():
    if request.method == 'POST' and 'utilizator' in request.form and 'parola' in request.form:
        f_utilizator = request.form['utilizator']
        f_parola = request.form['parola']
        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute("SELECT * FROM user.login WHERE utilizator=%s", (f_utilizator,))
        cont=cur.fetchone()                                                 # selectrez utilizatorul
        if cont:
            if check_password_hash(cont['parola'], f_parola):
                flash('Bine ai venit ' + cont['utilizator'])
                session['utilizator'] = cont['utilizator']                    # stabilesc informatiile din sesiune, ma ajuta mai tarziu sa controlez accesul in paginile site-ului
                session['activ'] = cont['activ']
                session['id'] = cont['id']
                session.permanent = True
                return redirect(url_for('index'))
            # elif check_password_hash(cont['parola'], f_parola) and cont['activ'] == 2:
            #     flash('Bine ai venit COSMIN')
            #     session['utilizator'] = cont['utilizator']  # stabilesc informatiile din sesiune, ma ajuta mai tarziu sa controlez accesul in paginile site-ului
            #     session['id'] = cont['id']
            #     session['activ'] = cont['activ']
            #     print('hgsf -' + str(session))
            #     return redirect(url_for('administrare'))
        else:
             flash("Utilizator si parola incorecte . Incercati din nou")
    return render_template('logare.html')


@app.route('/cont_nou', methods=['POST'])
def cont_nou():
    if request.method == "POST":
        nume = request.form['nume']
        prenume = request.form['prenume']
        utilizator = request.form['utilizator']
        # print('hhhh - ' + utilizator)                      #verific ce informatii imi aduce
        parola = request.form['parola']
        confirma_parola = request.form['confirma_parola']
        email = request.form['email']
        secure_parola = generate_password_hash(request.form['parola'], method='sha256') # criptez parola pentru a o introduce in baza de date
        # print(secure_parola)                                      # verific daca a encriptat parola
        activ = 1                                          # ar fi ideal sa gasesc o metoda de activare automata a contului(pe viitor)
        data_modificare = datetime.now()
        data_adaugare = datetime.now()
        sql = "INSERT INTO user.login (utilizator, parola, email, nume, prenume, data_modificare, data_adaugare, activ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        args = [utilizator, secure_parola, email, nume, prenume, data_modificare, data_adaugare, activ]
        if parola == confirma_parola:                       # daca parola este corecta in ambele campuri
            cur = mysql.connection.cursor()
            cur.execute(sql, args)
            # mysql.connection.commit()
            # cur.close()
            # cur = mysql.connection.cursor()
            #
            # cur.execute("CREATE DATABASE %s", utilizator)
            # mysql.connection.commit()
            # cur = mysql.connection.cursor()
            # cur.execute("""CREATE TABLE %s.parole (
            #                       id int(20) NOT NULL AUTO_INCREMENT,
            #                       nume_domeniu varchar(255) COLLATE utf8_romanian_ci DEFAULT NULL,
            #                       utilizator varchar(255) COLLATE utf8_romanian_ci DEFAULT NULL,
            #                       parola varchar(255) COLLATE utf8_romanian_ci DEFAULT NULL,
            #                       descriere varchar(500) COLLATE utf8_romanian_ci DEFAULT NULL,
            #                       data_modificare datetime DEFAULT NULL,
            #                       data_inserare datetime DEFAULT NULL,
            #                       PRIMARY KEY (id)) ENGINE=InnoDB AUTO_INCREMENT=38 DEFAULT CHARSET=utf8 COLLATE=utf8_romanian_ci")""",
            #             utilizator
            #             )

            mysql.connection.commit()
            cur.close()
            flash("Operatorul a fost adaugat cu succes !")
        else:
            flash('Datele din formularul de adaugare cont nu au fost conforme cu cerintele. PAROLA nu a putut fi confirmata. Reintroduceti datele in formularul de "Creaza cont nou" !')
        return redirect(url_for('logare'))
        # return redirect(url_for('cont_nou'))

@app.route('/index', methods=['GET', 'POST'])
def index():
    logare = False
    if 'utilizator' in session:                             # verific daca in sesiune a fost salvat utilizatorul la logare
        logare = True
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM cosmin.parole ORDER BY id")
        data = cur.fetchall()
        cur.close()
        # print(data)                                       # VERIFIC DATELE AFISATE DUPA INTEROGARE
        return render_template('index.html', parole=data)               # parole=data arunca in formularul din html informatiile din query
    else:
        return redirect(url_for('logare'))

@app.route('/linkuri', methods=['GET', 'POST'])      # routina pentru linkuri
def linkuri():
    logare = False
    if 'utilizator' in session:                             # verific daca in sesiune a fost salvat utilizatorul la logare
        logare = True
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM cosmin.linkuri ORDER BY id")
        linkuri = cur.fetchall()
        cur.close()
        # print(data)                                       # VERIFIC DATELE AFISATE DUPA INTEROGARE
        return render_template('linkuri.html', linkuri=linkuri)               # parole=data arunca in formularul din html informatiile din query
    else:
        return redirect(url_for('logare'))


@app.route('/administrare', methods=['GET', 'POST'])
def administrare():
    logare = False
    if 'utilizator' in session and session['utilizator'] == 'totoalpina':                             # verific daca in sesiune a fost salvat utilizatorul la logare
        logare = True
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM user.login ORDER BY id")
        data = cur.fetchall()
        cur.close()
        # print(data)                                       # VERIFIC DATELE AFISATE DUPA INTEROGARE
        return render_template('administrare.html', data=data)               # parole=data arunca in formularul din html informatiile din query
    else:
        flash('Aceasta sectiune este dedicata strict administratorilor !!!')
        return redirect(url_for('logare'))

@app.route('/tarife/<int:id_data>', methods=['GET', 'POST'])
def tarife(id_data):
    logare = False
    if 'utilizator' in session:  # verific daca utilizatoru este logat, in caz ca nu il redirectionez la pagina principala - ma folosesc de sesiune pentru a nu putea fi accesata decat daca userul este logat
        logare = True
        sql = """SELECT * FROM 
                        cosmin.tarife
                    WHERE 
                            id_client = %s
                  """
        args = (id_data,)
        cur = mysql.connection.cursor()
        cur.execute(sql, args)
        tarife = cur.fetchone()
        # print('id =' + str(id_data))
        print(tarife)
        # mysql.connection.commit()
        cur.close()
        cur_2 = mysql.connection.cursor()
        cur_2.execute("SELECT nume_domeniu FROM cosmin.parole WHERE id=%s", (id_data,))
        nume_client  = cur_2.fetchone()
        cur_2.close()
        print(nume_client)
        if tarife == None :
            id_client = id_data
            adaugare_fisa(id_client)
            flash("Fisa a fost creata! Accesati butonul < Fisa > din nou pentru a vizualiza fisa ")
            return redirect(url_for('index'))
        else:
            return render_template("tarife.html", tarife=tarife, nume_client=nume_client)

@app.route('/adauga_suma_initiala', methods=['GET','POST'])
def adauga_suma_initiala():
    try:
        if request.method == 'POST':
            id = request.form['id']
            id_data = request.form['id_data']
            suma_incasata = request.form['suma_incasata']
            tarif_initial = request.form['tarif_initial']
            ramas_de_incasat = float(tarif_initial) - float(suma_incasata)
            cur = mysql.connection.cursor()
            # cur.execute("'UPDATE cosmin.tarife SET tarif_initial =' + tarif_initial + 'ramas_de_incasat =' + ramas_de_incasat + 'WHERE id=' + id ")
            cur.execute("""
                           UPDATE
                           cosmin.tarife
                           SET
                                tarif_initial=%s,
                                ramas_de_incasat=%s

                           WHERE
                                id=%s
                        """,
                        (
                            tarif_initial,
                            ramas_de_incasat,
                            id,
                        )
                        )
            mysql.connection.commit()
            cur.close()

            flash("Tarif inregistrat cu succes")
            return redirect(url_for('tarife', id_data=id_data))
    except :
        flash("Datele introduse sunt incorecte ! Reintroduceti datele ! Formularul accepta doar cifre !")
        return redirect(url_for('tarife'))

@app.route('/incaseaza', methods=['GET','POST'])
def incaseaza():
    try:
        if request.method == 'POST':
            id_data = request.form['id_data']
            suma_incasata = request.form['suma_incasata']
            id_update = request.form['id']
            tarif_initial = request.form['tarif']
            initial = request.form['suma_incasata_ianinte_de_plata']
            v_ramas_de_plata = request.form['ramas_de_incasat']
            update_incasat_totala = float(initial) + float(suma_incasata)      # ce se va duce in final la suma incasat dupa efectuarea noii plati
            dp_ramas_de_plata = float(tarif_initial) - (float(suma_incasata) + float(initial))
            print(dp_ramas_de_plata)
            print(update_incasat_totala)
            cur = mysql.connection.cursor()
            cur.execute(""" 
                           UPDATE 
                           cosmin.tarife
                           SET 
                                incasare=%s, 
                                ramas_de_incasat=%s
                           WHERE 
                                id=%s 
                        """,
                        (
                            update_incasat_totala,
                            dp_ramas_de_plata,
                            id_update,
                        )
                        )
            mysql.connection.commit()
            cur.close()
            flash("Plata a fost inregistrata")
            return redirect(url_for('tarife', id_data=id_data))
    except :
        flash("Datele introduse sunt incorecte ! Reintroduceti datele ! Formularul accepta doar cifre !")
        return redirect(url_for('tarife', id_data=id_data))




@app.route('/cautare', methods=['GET', 'POST'])                         # functia de CAUTARE si randare pagina -  tabel PAROLE
def cautare():
    logare = False
    if 'utilizator' in session:                             # verific daca utilizatoru este logat, in caz ca nu il redirectionez la pagina principala - ma folosesc de sesiune pentru a nu putea fi accesata decat daca userul este logat
        logare = True
        v_cauta = '%' + request.form.get('cauta') + '%'
        # print('vpmc 11 - ' + v_cauta)                     # verific daca datele din camp sunt in forma corect
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM cosmin.parole WHERE nume_domeniu LIKE %s OR utilizator LIKE %s OR parola LIKE %s OR descriere LIKE %s ORDER BY id", (v_cauta, v_cauta, v_cauta, v_cauta,))
        mysql.connection.commit()
        data = cur.fetchall()
        # print('vpmc 12 - ' + str(data))               #   verific datele afisate in urma filtrului
        return render_template("cautare.html", data=data)
    else:
        return redirect(url_for('logare'))

@app.route('/cautare_linkuri', methods=['GET', 'POST'])                         # functia de CAUTARE si randare pagina -  tabel LINKURI
def cautare_linkuri():
    logare = False
    if 'utilizator' in session:                             # verific daca utilizatoru este logat, in caz ca nu il redirectionez la pagina principala - ma folosesc de sesiune pentru a nu putea fi accesata decat daca userul este logat
        logare = True
        v_cauta = '%' + request.form.get('cauta') + '%'
        # print('vpmc 11 - ' + v_cauta)                     # verific daca datele din camp sunt in forma corect
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM cosmin.linkuri WHERE topic LIKE %s OR link LIKE %s OR descriere LIKE %s ORDER BY id", (v_cauta, v_cauta, v_cauta,))
        mysql.connection.commit()
        search_links = cur.fetchall()
        # print('vpmc 12 - ' + str(data))               #   verific datele afisate in urma filtrului
        return render_template("cautare_linkuri.html", data=search_links)
    else:
        return redirect(url_for('logare'))

@app.route('/adauga', methods = ['POST'])                   # functia de adaugare de date noi in baza de date
def adauga():                                               # nu am nevoie de verificarea de logare pentru ca folosesc modal si randarea paginii se face in alt mod
    if request.method == "POST":
        nume_domeniu = request.form['nume_domeniu']
        utilizator = request.form['utilizator']
        parola = request.form['parola']
        descriere = request.form['descriere']
        data_modificare = datetime.now()
        data_inserare = datetime.now()
        sql = "INSERT INTO cosmin.parole (nume_domeniu, utilizator, parola, descriere, data_modificare, data_inserare) VALUES (%s, %s, %s, %s,%s,%s)"
        args = [nume_domeniu, utilizator, parola, descriere, data_modificare, data_inserare]
        cur = mysql.connection.cursor()
        cur.execute(sql, args)
        mysql.connection.commit()
        cur.close()
        flash("Inregistrare reusita. Datele au fost adaugate !")
        return redirect(url_for('index'))

@app.route('/adaugalink', methods = ['POST'])                   # functia de adaugare de date noi in baza de date
def adaugalink():                                               # nu am nevoie de verificarea de logare pentru ca folosesc modal si randarea paginii se face in alt mod
    if request.method == "POST":
        topic = request.form['topic']
        link = request.form['link']
        descriere = request.form['descriere']
        data_modificare = datetime.now()
        data_adaugare = datetime.now()
        sql = "INSERT INTO cosmin.linkuri (topic, link, descriere, data_modificare, data_adaugare) VALUES (%s, %s, %s, %s,%s)"
        args = [topic, link, descriere, data_modificare, data_adaugare]
        cur = mysql.connection.cursor()
        cur.execute(sql, args)
        mysql.connection.commit()
        cur.close()
        flash("Inregistrare reusita. Datele au fost adaugate !")
        return redirect(url_for('linkuri'))

@app.route('/adminedit', methods=['GET','POST'])                 # functia pentru editarea datelor
def adminedit():                                                 # nu am nevoie de verificarea de logare pentru ca folosesc modal si randarea paginii se face in alt mod
    if request.method == 'POST' and session['utilizator'] == 'totoalpina':
        id_data = request.form['id']
        utilizator = request.form['utilizator']
        # parola = request.form['parola']
        # edit_secure_parola = generate_password_hash(request.form['parola'], method='sha256')
        email = request.form['email']
        nume = request.form['nume']
        prenume = request.form['prenume']
        activ = request.form['activ']
        mod_data = datetime.now()                               # stabilesc data si ora pentru a introduce in baza de date cand a fost modificata informatia
        cur = mysql.connection.cursor()
        cur.execute("""
                       UPDATE 
                       user.login
                       SET 
                            utilizator=%s,  
                            email=%s, 
                            nume=%s,
                            prenume=%s,                        
                            data_modificare=%s,
                            activ=%s
                       WHERE 
                            id=%s
                    """,
                    (
                     utilizator,
                     email,
                     nume,
                     prenume,
                     mod_data,
                     activ,
                     id_data,
                     )
                    )
        flash("Inregistrare editata cu succes")
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('administrare'))

@app.route('/editeaza', methods=['GET','POST'])                 # functia pentru editarea datelor
def editeaza():                                                  # nu am nevoie de verificarea de logare pentru ca folosesc modal si randarea paginii se face in alt mod
    if request.method == 'POST':
        id_data = request.form['id']
        nume_domeniu = request.form['nume_domeniu']
        utilizator = request.form['utilizator']
        parola = request.form['parola']
        descriere = request.form['descriere']
        mod_data = datetime.now()                               # stabilesc data si ora pentru a introduce in baza de date cand a fost modificata informatia
        cur = mysql.connection.cursor()
        cur.execute("""
                       UPDATE 
                       cosmin.parole
                       SET 
                            nume_domeniu=%s, 
                            utilizator=%s, 
                            parola=%s, 
                            descriere=%s,
                            data_modificare=%s
                       WHERE 
                            id=%s
                    """,
                    (
                     nume_domeniu,
                     utilizator,
                     parola,
                     descriere,
                     mod_data,
                     id_data,
                     )
                    )
        flash("Inregistrare editata cu succes")
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('index'))

@app.route('/editeazalink', methods=['GET','POST'])                 # functia pentru editarea datelor
def editeazalink():                                                  # nu am nevoie de verificarea de logare pentru ca folosesc modal si randarea paginii se face in alt mod
    if request.method == 'POST':
        id_link = request.form['id']
        topic = request.form['topic']
        link = request.form['link']
        descriere = request.form['descriere']
        mod_data = datetime.now()                               # stabilesc data si ora pentru a introduce in baza de date cand a fost modificata informatia
        cur = mysql.connection.cursor()
        cur.execute("""
                       UPDATE 
                       cosmin.linkuri
                       SET 
                            topic=%s, 
                            link=%s, 
                            descriere=%s,
                            data_modificare=%s
                       WHERE 
                            id=%s
                    """,
                    (
                     topic,
                     link,
                     descriere,
                     mod_data,
                     id_link,
                     )
                    )
        flash("Inregistrare editata cu succes")
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('linkuri'))

@app.route('/delete/<int:id_data>', methods=['GET', 'POST'])   # functia de stergere a datelor din baza de date
def delete(id_data):                                            # nu am nevoie de verificarea de logare pentru ca folosesc modal si randarea paginii se face in alt mod
    flash("Stergerea a fost realizata cu succes !")
    sql = """DELETE FROM 
                    cosmin.parole 
             WHERE 
                    id=%s
          """
    args = [id_data]
    cur = mysql.connection.cursor()
    cur.execute(sql, args)
    mysql.connection.commit()
    cur.close()
    return redirect(url_for('index'))

@app.route('/userdelete/<int:id_data>', methods=['GET', 'POST'])   # functia de stergere a datelor din baza de date
def userdelete(id_data):                                            # nu am nevoie de verificarea de logare pentru ca folosesc modal si randarea paginii se face in alt mod
    if session['utilizator'] == 'totoalpina' and session['activ'] == 2:
        flash("Stergerea a fost realizata cu succes !")
        sql = """DELETE FROM 
                        user.login 
                 WHERE 
                        id=%s
              """
        args = [id_data]
        cur = mysql.connection.cursor()
        cur.execute(sql, args)
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('administrare'))

@app.route('/deletelink/<int:id_data>', methods=['GET', 'POST'])   # functia de stergere a datelor din baza de date
def deletelink(id_data):                                            # nu am nevoie de verificarea de logare pentru ca folosesc modal si randarea paginii se face in alt mod
    flash("Stergerea a fost realizata cu succes !")
    sterge_linkuri(id_data)
    return redirect(url_for('linkuri'))


@app.route('/logout')
def logout():
    iesire_user()                        # inchid sesiunea si sterg datele de cookie legate de aceasta
    flash("Sesiune inchisa cu succes")
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run()