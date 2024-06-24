from flask import Flask, jsonify, make_response, request, render_template
from pony import orm
from datetime import datetime

DB = orm.Database()

app = Flask(__name__, static_folder='static')

class Desert(DB.Entity):
    id = orm.PrimaryKey(int, auto=True)
    naziv = orm.Required(str)
    vrsta = orm.Required(str)
    sastojci = orm.Required(str)
    dostupno = orm.Required(int)
    prodano = orm.Required(int)
    fotografija = orm.Required(str)
    bezglutena = orm.Required(bool)
    vegan = orm.Required(bool)
    cijena = orm.Required(float)
    dodano = orm.Required(str)

DB.bind(provider="sqlite", filename="database.sqlite", create_db=True)
DB.generate_mapping(create_tables=True)


def dohvati_deserte_iz_baze():
    try:
        with orm.db_session:
            db_querry = orm.select(desert for desert in Desert)[:]
            deserti = []
            for item in db_querry:
                deserti.append(item.to_dict())
            return deserti
    except Exception as e:
        return {"poruka": "Greška", "error": str(e)}

def dodaj_desert_u_bazu(json_request):
    try:
        naziv = json_request["naziv"]
        vrsta = json_request["vrsta"]
        sastojci = json_request["sastojci"]
        dostupno = json_request["dostupno"]
        prodano = json_request["prodano"]
        fotografija = json_request["fotografija"]
        bezglutena = json_request["bezglutena"]
        vegan = json_request["vegan"]
        cijena = json_request["cijena"]
        dodano = json_request["dodano"]
        try:
            datetime.strptime(dodano, "%Y-%m-%d")
        except ValueError:
            return make_response(jsonify({"poruka": "Neispravan format datuma."}), 400)

        with orm.db_session:
            Desert(naziv=naziv, vrsta=vrsta, sastojci=sastojci, dostupno=dostupno, prodano=prodano, fotografija=fotografija, bezglutena=bezglutena, vegan=vegan, cijena=cijena, dodano=dodano)
        orm.commit()
        response = {"poruka": "Proizvod je dodan."}
        return response
    except Exception as e:
        return {"poruka": "Greška", "error": str(e)}

    
def dohvati_pojedini_desert(id):
    try:
        with orm.db_session:
            desert = Desert[id].to_dict()
            return desert
    except Exception as e:
        return {"poruka": "Greška", "error": str(e)}
    

def izmijeni_desert(id, json_request):
    try:
        with orm.db_session:
            desert = Desert[id]
            if 'naziv' in json_request:
                desert.naziv = json_request['naziv']
            if 'vrsta' in json_request:
                desert.vrsta = json_request['vrsta']
            if 'sastojci' in json_request:
                desert.sastojci = json_request['sastojci']
            if 'dostupno' in json_request:
                desert.dostupno = json_request['dostupno']
            if 'prodano' in json_request:
                desert.prodano = json_request['prodano']
            if 'fotografija' in json_request:
                desert.fotografija = json_request['fotografija']
            if 'bezglutena' in json_request:
                desert.bezglutena = json_request['bezglutena']
            if 'vegan' in json_request:
                desert.vegan = json_request['vegan']
            if 'cijena' in json_request:
                desert.cijena = json_request['cijena']
            if 'dodano' in json_request:
                desert.dodano = json_request['dodano']

            response = {"poruka": "Desert je izmijenjen."}
            return response
    except Exception as e:
        return {"poruka": "Greška", "error": str(e)}
    
    
def kupi_desert_db(id):
    try:
        with orm.db_session:
            desert = Desert[id]
            if desert.dostupno > 0:
                desert.prodano += 1
                desert.dostupno -= 1
                response = {"poruka": "Desert je kupljen.", "data": desert.to_dict()}
                return response
            else:
                return {"poruka": "Desert nije dostupan."}
    except Exception as e:
        return {"poruka": "Greška", "error": str(e)}
    

def izbrisi_desert_db(id):
    try:
        with orm.db_session:
            desert = Desert[id]
            desert.delete()
            response = {"poruka": "Desert je izbrisan."}
            return response
    except Exception as e:
        return {"poruka": "Greška", "error": str(e)}
    

@app.route("/deserti/<filtriranje>/<sortiranje>", methods=["GET"])
def dohvati_filtrirano(filtriranje="sve", sortiranje="najpopularnije"):
    try:
        desserts = dohvati_deserte_iz_baze()
        if filtriranje == "suhi":
            temp_deserti = [desert for desert in desserts if desert.get("vrsta")=="suhi kolači"]
        elif filtriranje == "torte":
            temp_deserti = [desert for desert in desserts if desert.get("vrsta")=="torte"]
        elif filtriranje == "cokolada":
            temp_deserti = [desert for desert in desserts if "čokolada" in desert.get("sastojci").lower()]
        elif filtriranje == "bezglutena":
            temp_deserti = [desert for desert in desserts if desert.get("bezglutena")==True]
        elif filtriranje == "bezsecera":
            temp_deserti = [desert for desert in desserts if not "šećer" in desert.get("sastojci").lower()]
        elif filtriranje == "vegansko":
            temp_deserti = [desert for desert in desserts if desert.get("vegan")==True]
        else:
            temp_deserti = desserts

        if sortiranje == "najjeftinije":
            temp_deserti.sort(key=lambda desert: desert.get("cijena"))
        elif sortiranje == "najskuplje":
            temp_deserti.sort(key=lambda desert: desert.get("cijena"), reverse=True)
        elif sortiranje == "najnovije":
            temp_deserti.sort(key=lambda desert: desert.get("dodano"), reverse=True)
        elif sortiranje == "nazivuzlazno":
            temp_deserti.sort(key=lambda desert: desert.get("naziv"))
        elif sortiranje == "nazivsilazno":
            temp_deserti.sort(key=lambda desert: desert.get("naziv"), reverse=True)
        else:
            temp_deserti.sort(key=lambda desert: desert.get("prodano"), reverse=True)
        #return make_response(jsonify(temp_deserti), 200)
        #print(temp_deserti)
        return render_template("index.html", desserts=temp_deserti, sortiranje=sortiranje, filtriranje =filtriranje)
    except Exception as e:
        return make_response(jsonify({"poruka": "Greška prilikom dohvaćanja podataka.", "error": str(e)}), 500)


@app.route("/deserti", methods=["POST"])
def dodaj_desert():
    data = request.json
    try:
        datetime.strptime(data["dodano"], "%Y-%m-%d")
    except ValueError:
        return make_response(jsonify({"poruka": "Neispravan format datuma."}), 400)
    if ("fotografija" not in data.keys()) or ("fotografija" in data.keys() and data["fotografija"]==""):
        data["fotografija"] = "../static/no_photo_photo.png"
    for key, value in data.items():
        if (key == "naziv" or key == "sastojci") and value == "":
            return make_response(jsonify({"poruka":"Ime i sastojci ne smiju biti prazni."}), 200)
        elif (key == "prodano" or key == "dostupno" or key=="cijena") and value < 0:
            return make_response(jsonify({"poruka":"Cijena i broj dostupnih i prodanih proizvoda moraju biti veći od 0."}), 200)
    try:
        dodavanje_deserta = dodaj_desert_u_bazu(data)
        return make_response(jsonify(dodavanje_deserta), 200)
    except Exception as e:
        return make_response(jsonify({"poruka": "Greška.", "error": str(e)}), 500)


@app.route("/deserti/<int:id>", methods=["GET"])
def dohvati_jedan_desert(id):
    try:
        desert = dohvati_pojedini_desert(id)
        if "error" in desert:
            return make_response(jsonify(desert), 500)
        return render_template("detalji.html", dessert=desert)
    except Exception as e:
        return make_response(jsonify({"poruka": "Greška prilikom dohvaćanja deserta.", "error": str(e)}), 500)



@app.route("/deserti/<int:id>", methods=["DELETE"])
def izbrisi_desert(id):
    try:
        desert = dohvati_pojedini_desert(id)
        if desert:
            response = izbrisi_desert_db(id)
            return make_response(jsonify(response), 200)
        else:
            return make_response(jsonify({"poruka": "Desert nije pronađen."}), 404)
    except Exception as e:
        return make_response(jsonify({"poruka": "Greška.", "error": str(e)}), 500)


@app.route("/deserti/<int:id>", methods=["PUT"])
def uredi_desert(id):
    data = request.json
    try:
        if "dodano" in data:
            datetime.strptime(data["dodano"], "%Y-%m-%d")
    except ValueError:
        return make_response(jsonify({"poruka": "Neispravan format datuma."}), 400)
    if "fotografija" in data.keys() and data["fotografija"]=="":
        data["fotografija"] = "../static/no_photo_photo.png"
    try:
        desert = dohvati_pojedini_desert(id)
        if desert:
            for key, value in data.items():
                if (key == "naziv" or key == "sastojci") and value == "":
                    return make_response(jsonify({"poruka":"Ime i sastojci ne smiju biti prazni."}), 200)
                elif (key == "prodano" or key == "dostupno" or key == "cijena") and value < 0:
                    return make_response(jsonify({"poruka":"Cijena i broj dostupnih i prodanih proizvoda moraju biti veći od 0."}), 200)
            izmijeni_desert(id, data)
            return make_response(jsonify(dohvati_pojedini_desert(id)), 200)
        else:
            return make_response(jsonify({"poruka": "Desert nije pronađen."}), 404)
    except Exception as e:
        return make_response(jsonify({"poruka": "Greška.", "error": str(e)}), 500)


@app.route("/deserti/<int:id>/kupi", methods=["PATCH"])
def kupi_desert(id):
    try:
        result = kupi_desert_db(id)
        if "data" in result:
            return make_response(jsonify(result), 200)
        else:
            return make_response(jsonify(result), 400)
    except Exception as e:
        return make_response(jsonify({"poruka": "Greška prilikom kupovine.", "error": str(e)}), 500)

    
@app.route("/novi-desert", methods=["GET"])
def novi_desert():
    return render_template("dodavanjeProizvoda.html")

if __name__ == "__main__":
    app.run(port=3001, host='0.0.0.0', debug=True)
