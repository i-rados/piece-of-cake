# Piece of cake
Piece of cake je aplikacija za slastičarnicu. Omogućuje prikaz cijele ponude deserta na jednom mjestu 
koju je moguće sortirati i filtrirati. Daje detaljan uvid u svaki proizvod pojedinačno te omogućuje uređivanje informacija
o proizvodima, kao što su dostupnost, cijena, broj prodanih proizvoda i slično. Unos novog deserta se obavlja vrlo
jednostavno i intuitivno. Moguće je i kupiti neki desert te ažurirati stanje dostupne količine, a mogućnost trajnog brisanja 
nekog deserta je također implementirana. Ova aplikacija je korisna jer pojednostavljuje upravljanje stanjem proizvoda,
zaliha, poboljšava korisničko iskustvo pregledavanja ponude i omogućuje uštedu vremena pomoću jednostavne online kupovine.
## Funkcionalnosti
- Pregled svih deserta (uz mogućnost filtriranja i/ili sortiranja)
- Pregled detalja o pojedinom desertu
- Uređivanje informacija o desertu
- Kupovina deserta (ažuriranje dostupne količine i broja prodanih deserta)
- Brisanje deserta
## UseCase dijagram
![image](https://github.com/i-rados/piece-of-cake/assets/166507783/e2faa580-2273-4a13-944d-7c52a56429a0)
## Struktura
Sav poslužiteljski dio se nalazi u datoteci app.py i napisan je u Pythonu uz korištenje razvojnog okvira Flask i  
alata PonyORM, za bazu podataka koristi SQLite, a za klijentski dio su izrađene 3 HTML datoteke u 
direktoriju templates. HTML kod koristi JavaScript za funkcionalnost web stranice te CSS za oblikovanje dizajna.
Za upravljanje kontejnerom je napravljena datoteka Dockerfile, a fotografije koje se koriste na web stranici se
nalaze u direktoriju static.

```plaintext
piece-of-cake/
├── static/
│   ├── cake_cover_photo.jpg
│   ├── logo_best.png
│   ├── no_photo_photo.png
├── templates/
│   ├── index.html
│   ├── detalji.html
│   ├── dodavanjeProizvoda.html
├── app.py
├── database.sqlite
├── Dockerfile
└── requirements.txt
```
## Instalacija
Pozicionirati se u neku mapu (npr Downloads) i preuzeti kod s GitHub-a ili pokrenuti naredbu git clone.
Primjer:
```plaintext
cd ~/Downloads
git clone https://github.com/i-rados/piece-of-cake.git
cd piece-of-cake-main
```

## Pokretanje
```
docker build -t pieceofcake:3.1 .
docker ps
docker run -p 5001:3001 pieceofcake:3.1
```
