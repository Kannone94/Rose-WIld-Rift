# Rose Wild Rift Farm Automator

Bot automatico per la gestione dell'orto (farm) in League of Legends Wild Rift tramite API.

## ⚠️ Disclaimer

Questo script interagisce con API ufficiali di Riot Games. 

L'uso di questo tool potrebbe violare i Termini di Servizio di League of Legends. 

Usalo a tuo rischio e pericolo.

## Prerequisiti

- Python 3.8+
- pip (gestore pacchetti Python)
- Un proxy HTTP/HTTPS (se necessario per il testing locale con mitmproxy)

## Installazione

### 1. Clone il repository
```bash
git clone <repository-url>
cd Rose-WIld-Rift
```

### 2. Crea un ambiente virtuale
```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# Linux/macOS
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Installa le dipendenze
```bash
pip install -r requirements.txt
```

## Configurazione

### 1. Crea il file `.env`
Copia i tuoi token sessione dal browser (DevTools > Application > Cookies):

```env
# Session Cookies e Tokens
SESSION_STATE=<your_session_state>
ACCESS_TOKEN=<your_access_token>
SESSION_EXPIRY=<your_session_expiry>
REFRESH_TOKEN=<your_refresh_token>
ID_TOKEN=<your_id_token>
ID_HINT=<your_id_hint>

# Configurazione
SEED_ID=2000005
proxy=False
PROXY_HOST=127.0.0.1
PROXY_PORT=8080
```

### Come ottenere i token:

1. Apri https://crystalrosegame.wildrift.leagueoflegends.com/ nel browser
2. Accedi al tuo account
3. Apri **DevTools** (F12)
4. Vai a **Application** → **Cookies**
5. Filtra i cookie con nome `__Secure-`
6. Copia i valori dei cookie richiesti nel file `.env`

### Note importanti:

⚠️ **NON condividere il file `.env`** - contiene credenziali sensibili!

I token hanno una durata limitata e scadono regolarmente. Se lo script smette di funzionare, potrebbe essere necessario aggiornare i token.

## Lancio

Attiva l'ambiente virtuale e esegui lo script:

```bash
# Windows
.venv\Scripts\activate
python main.py

# Linux/macOS
source .venv/bin/activate
python main.py
```

Quando richiesto, inserisci il **Seed ID** (o premi Enter per il default 2000005).

Lo script farà il loop ogni minut0 (60 secondi) per:
1. Controllare quali piante sono pronte per la raccolta
2. Raccogliere le piante mature
3. Piantare nuovi semi nei terreni liberi (assicurarsi di avere il seme necessario)
4. Innaffiare tutti i terreni

## Utilizzo del Proxy (opzionale)

Se usi mitmproxy o burpsuite per debuggare le richieste modifica l'opzione in "proxy=True" nel .env

Lo script è già configurato per usare il proxy su `127.0.0.1:8080`.

## Struttura del codice

- `main.py` - Script principale con tutte le funzioni
  - `prepare_session()` - Inizializza la sessione con i cookie
  - `plant_seed()` - Pianta un nuovo seed
  - `harvest_crop()` - Raccoglie una pianta
  - `water_plants()` - Innaffia tutti i terreni
  - `is_plantable()` - Controlla se un terreno è libero
  - `is_harvestable()` - Controlla se una pianta è pronta
  - `refresh_session()` - Rinnova i token di sessione
  - `check_session_time()` - Verifica se la sessione sta per scadere

## Risoluzione Problemi

### "InsecureRequestWarning"
Lo script disabilita gli avvisi di certificato SSL per il proxy locale. È normale e innocuo.

### Lo script non fa nulla
Verifica che:
- Il file `.env` sia nella stessa cartella di `main.py`
- Tutti i token siano completi e corretti
- Hai almeno una pianta nel tuo orto

## Contatti & Supporto

Per bug o domande, apri un issue su GitHub.

## Licenza

Questo progetto è fornito così com'è. Non c'è alcuna garanzia.

---

**Divertiti a coltivare il tuo orto in Wild Rift!** 🌾
