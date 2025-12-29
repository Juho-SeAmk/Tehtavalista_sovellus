# Ollama-avusteinen kotitalouden tehtävälista

Tämä Flask-sovellus hyödyntää Ollama-mallia kotitalouden viikkosuunnitelman ja muistutusten luomiseen.

## Käyttöohjeet
1. Asenna riippuvuudet:
2. Käynnistä sovellus:
3. Avaa selain ja mene osoitteeseen `http://127.0.0.1:5000/`
4. Kirjoita kotitalouden tehtäviä ja paina "Luo viikkosuunnitelma".

## Tekniset yksityiskohdat
- Flask hoitaa web-käyttöliittymän.
- Ollama-malli generoi viikkosuunnitelman ja käytännön vinkit.
- Käyttäjän syöte käsitellään LLM:lle promptina.

## Oma panos
- Suunnittelin prompt-rakenteen, joka muuttaa käyttäjän tehtävät selkeäksi viikkosuunnitelmaksi.
- Toteutin interaktiivisen web-käyttöliittymän.
- Testattu ja analysoitu LLM:n ehdotusten käytännön hyödyllisyyttä.
