# This program is specifically made for Italian users since it uses italian subs

![sito logo]([https://cdn.corenexis.com/view/4252568720](https://cdn.phototourl.com/free/2026-06-07-ea7aa282-13ce-4572-b0a9-b5c7ac7999b1.png))

## ANIMEUNITY DOWNLOADER/STREAMER

Programma Python per scaricare o riprodurre in streaming anime da AnimeUnity utilizzando l'API locale.

## Indice

- [Requisiti](#requisiti)

- [Installazione](#installazione)

- [Struttura dei file](#struttura-dei-file)

- [Come funziona](#come-funziona)

- [Comandi mpv](#comandi-mpv-durante-la-riproduzione)

- [Struttura dei file scaricati](#struttura-dei-file-scaricati)

- [Dipendenze Python](#dipendenze-python)

- [Note](#note)

- [Risoluzione problemi](#risoluzione-problemi)

- [Credits](#credits)

- [License](#license)

## Requisiti

- Python 3.8 o superiore

- mpv player installato sul sistema

- AnimeUnity-API in esecuzione

## Installazione

### 1. Clona e avvia l'API di AnimeUnity

```bash

git clone https://github.com/Pal-droid/Animeunity-API

cd Animeunity-API

pip install -r requirements.txt

uvicorn main:app --reload --host 0.0.0.0 --port 8000

```

### 2. Installa mpv player

**Windows:**

- Scarica da: https://mpv.io/installation/

- Oppure con chocolatey: `choco install mpv`

**Linux:**

```bash

sudo apt install mpv  # Ubuntu/Debian

sudo dnf install mpv  # Fedora

sudo pacman -S mpv    # Arch

```

**Mac:**

```bash

brew install mpv

```

### 3. Configura il downloader

```bash

pip install -r requirements.txt

python main.py

```

## Struttura dei file

```

.

├── downloader.py       # Funzioni core e client API

├── main.py            # Logica principale del programma

├── requirements.txt   # Dipendenze Python

└── README.md          # Questo file

```

## Come funziona

1. Il programma chiede il percorso dove salvare i download

2. Selezioni la modalita: stream con mpv o download su disco

3. Inserisci il titolo dell'anime da cercare

4. Scegli l'anime dalla lista dei risultati

5. Seleziona l'intervallo di episodi da scaricare/riprodurre

6. Il programma recupera gli URL e avvia lo stream o il download

## Comandi mpv durante la riproduzione

| Tasto | Azione |

|-------|--------|

| Spazio/Pausa | Play/Pausa |

| Invio | Schermo intero |

| q | Esci |

| > | Episodio successivo |

| < | Episodio precedente |

## Struttura dei file scaricati

I video vengono salvati con questa struttura:

```

Downloads/

└── AnimeUnity/

    └── Nome_Anime/

        ├── Nome_Anime_001.mp4

        ├── Nome_Anime_002.mp4

        └── Nome_Anime_003.mp4

```

## Dipendenze Python

- `httpx==0.27.0` - Client HTTP per chiamate API

- `tqdm==4.66.4` - Barre di progresso per i download

## Note

- L'API di AnimeUnity deve essere in esecuzione prima di avviare il programma

- I sottotitoli sono in italiano come da specifica del sito

- Alcuni stream potrebbero restituire errore 503, riprovare piu tardi

- Programma sviluppato per piattaforme Windows, Linux e Mac

- I nomi dei file vengono automaticamente sanitizzati per rimuovere caratteri non validi

- I download mostrano una barra di progresso con dimensione e velocita

## Risoluzione problemi

**Errore: "L'API di AnimeUnity non e in esecuzione"**

Assicurati di aver avviato il server API in un terminale separato:

```bash

cd Animeunity-API

uvicorn main:app --reload --port 8000

```

**Errore: "mpv non trovato"**

Installa mpv seguendo le istruzioni per il tuo sistema operativo.

**Nessun URL stream trovato**

- Verifica che l'episodio sia disponibile

- Alcuni episodi potrebbero richiedere un account premium

- Prova piu tardi se il server restituisce errori 503

**Download lento**

- La velocita dipende dal server di AnimeUnity

- Prova a scaricare meno episodi alla volta

- Verifica la tua connessione internet

**File non viene salvato**

- Controlla i permessi di scrittura nella cartella di destinazione

- Assicurati che il nome del file non contenga caratteri speciali

- Verifica che ci sia spazio sufficiente sul disco

## Credits (Crediti)

This program is built on top of the Anime-UnityAPI developed by **[Pal-droid](https://github.com/Pal-droid)**:

- 🔗 [Animeunity-API](https://github.com/Pal-droid/Animeunity-API/) — Local API to access AnimeUnity content

## License (Licenza)

This program is provided for educational purposes only. Please respect AnimeUnity's terms of service.
