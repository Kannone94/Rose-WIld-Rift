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
git clone https://github.com/Kannone94/Rose-WIld-Rift/
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

# Gold Target for Cheat Loop
GOLD_TARGET=30000
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

### Menu Principale

All'avvio dello script, ti verrà presentato un menu con due modalità:

```
=== Wild Rift Crystal Rose Main Menu ===
1. Farm Bot
2. Cheat Gold Bot
3. exit
```

#### 1. **Farm Bot** - Modalità Automazione Orto

Questa modalità gestisce automaticamente il tuo orto nel gioco:
- Raccoglie le piante mature
- Pianta nuovi semi nei terreni liberi
- Innaffia le piante che ne hanno bisogno
- Il loop si ripete ogni **60 secondi**

Quando selezioni questa modalità, ti verrà chiesto quale seme piantare:

```
=== Wild Rift Crystal Rose Farm Bot ===
1. Input the flower corresponding number to plant:
    1) Skyglow Tulip
    2) Battle Rose
    3) Spirit Lotus
    4) Emerald Vine
    5) Fire Iris
    6) Desert Rose
    7) Voidbloom
    8) Thunder Iris
    9) Crystal Rose
    10) Aurora Icebloom
    11) Moonlight Lotus
    12) Starlight Lily
2. Ctrl+C to stop the bot.
```

Inserisci il numero del fiore che vuoi piantare (1-12) o premi Enter per usare il `SEED_ID` dal file `.env`.

#### 2. **Cheat Gold Bot** - Modalità Raccolta Veloce Oro

⚠️ **Uso a scopo dimostrativo/testing**

Questa modalità automatizza la raccolta di oro piantando e raccogliendo rapidamente i semi:
- Pianta il Skyglow Tulip (seed_ID 2000001) in tutti i terreni
- Rimuove i semi immediatamente senza attendere la crescita
- Completa ripetutamente le quest per raccogliere oro
- Continua fino al raggiungimento del `GOLD_TARGET` definito nel `.env` (default: 30000)



## Utilizzo del Proxy (opzionale)

Se usi mitmproxy o burpsuite per debuggare le richieste modifica l'opzione in "proxy=True" nel .env

Lo script è già configurato per usare il proxy su `127.0.0.1:8080`.

## Struttura del codice

- `main.py` - Script principale e punto di ingresso
- `api.py` - Modulo API con funzioni per interagire con Wild Rift Farm
  - `plant_seed()` - Pianta un nuovo seed
  - `harvest_crop()` - Raccoglie una pianta
  - `water_plants()` - Innaffia tutti i terreni
  - `is_plantable()` - Controlla se un terreno è libero
  - `is_harvestable()` - Controlla se una pianta è pronta
  - `refresh_session()` - Rinnova i token di sessione
  - `check_session_time()` - Verifica se la sessione sta per scadere
- `prepare_session()` - Inizializza la sessione con i cookie da `.env`

## Risoluzione Problemi

### "InsecureRequestWarning"
Lo script disabilita gli avvisi di certificato SSL per il proxy locale. È normale e innocuo.

### "CookieConflictError"
I token sono scaduti o non validi. Aggiorna il file `.env` con nuovi token dal browser.

### Lo script non fa nulla o da errori
Verifica che:
- Il file `.env` sia nella stessa cartella di `main.py`
- Tutti i token siano completi e corretti
- Hai almeno una pianta nel tuo orto
- Dipendenze installate correttamente: `pip install -r requirements.txt`

## Contatti & Supporto

Per bug o domande, apri un issue su GitHub.

## Licenza

Questo progetto è fornito così com'è. Non c'è alcuna garanzia.

---

**Divertiti a coltivare il tuo orto in Wild Rift!** 🌾
