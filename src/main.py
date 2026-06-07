import sys, platform
from downloader import (
    clear_screen,
    ask_user_input,
    select_from_list,
    get_download_path,
    get_episode_range,
    AnimeUnityAPIClient,
    stream_with_mpv,
    download_videos
)

def main():
    # Pulisce lo schermo e mostra l'intestazione
    clear_screen()
    print("="*60)
    print("ANIMEUNITY DOWNLOADER/STREAMER")
    print("="*60)
    print(f"Piattaforma: {platform.system()} {platform.release()}")
    print(f"Python: {sys.version.split()[0]}")
    print("="*60)
    
    # Chiede il percorso di download
    download_path = get_download_path()
    
    # Seleziona la modalita
    print(f"\n{'='*60}")
    print("SELEZIONA MODALITA")
    print(f"{'='*60}")
    mode_options = {
        '1': ('stream', 'Stream con mpv (guarda ora)'),
        '2': ('download', 'Download su disco (salva per dopo)')
    }
    
    print("\n  1. Stream con mpv (guarda ora)")
    print("  2. Download su disco (salva per dopo)")
    
    while True:
        choice = ask_user_input("\nSeleziona modalita", default="1")
        if choice in mode_options:
            mode, _ = mode_options[choice]
            break
        print("Scelta non valida. Seleziona 1 o 2")
    
    # Cerca l'anime
    print(f"\n{'='*60}")
    print("CERCA ANIME")
    print(f"{'='*60}")
    query = ask_user_input("Inserisci il titolo dell'anime da cercare")
    
    # Inizializza il client API
    client = AnimeUnityAPIClient()
    
    try:
        # Verifica che l'API sia in esecuzione
        print("\nControllo connessione API...")
        if not client.check_api_health():
            print("L'API di AnimeUnity non e in esecuzione!")
            print("\nAvviala con:")
            print("  cd Animeunity-API")
            print("  uvicorn main:app --reload --host 0.0.0.0 --port 8000")
            sys.exit(1)
        
        print("API raggiungibile")
        
        # Esegue la ricerca
        print(f"\nRicerca di '{query}' in corso...")
        results = client.search_anime(query)
        
        if not results:
            print("Nessun risultato trovato")
            return
        
        # Lascia selezionare l'anime
        selected = select_from_list(
            results, 
            title_key='title', 
            id_key='anime_id',
            prompt="Seleziona l'anime (numero)"
        )
        
        anime_id = selected.get('anime_id')
        anime_title = selected.get('title', query)
        
        print(f"\nSelezionato: {anime_title}")
        
        # Recupera gli episodi
        print("\nRecupero episodi in corso...")
        episodes = client.get_episodes(anime_id)
        
        if not episodes:
            print("Nessun episodio trovato")
            return
        
        total_episodes = len(episodes)
        print(f"Trovati {total_episodes} episodi")
        
        # Ottiene l'intervallo di episodi
        start_ep, end_ep = get_episode_range(total_episodes)
        
        selected_episodes = episodes[start_ep-1:end_ep]
        print(f"\nSelezionati {len(selected_episodes)} episodi")
        
        # Recupera gli URL degli stream
        print("\nRecupero URL dello stream...")
        video_urls = []
        
        for ep in selected_episodes:
            episode_id = ep.get('episode_id')
            episode_num = ep.get('number', '?')
            
            if episode_id:
                print(f"  Recupero URL per episodio {episode_num}...")
                url = client.get_stream_url(episode_id)
                if url:
                    video_urls.append(url)
                    print(f"    URL ottenuto")
                else:
                    print(f"    Nessun URL restituito (potrebbe essere premium/non disponibile)")
            else:
                print(f"  Episodio {episode_num} non ha episode_id")
        
        # Verifica che ci siano URL validi
        if not video_urls:
            print("\nNessun URL stream valido trovato!")
            print("Questo potrebbe essere dovuto a:")
            print("  Limiti di velocita dell'API")
            print("  Episodio richiede premium")
            print("  Stream temporaneamente non disponibile (errore 503)")
            return
        
        print(f"\nRecuperati con successo {len(video_urls)} URL stream")
        
        # Esegue la modalita scelta
        if mode == "stream":
            stream_with_mpv(video_urls, anime_title)
        else:
            download_videos(video_urls, anime_title, anime_id, download_path, start_ep)
        
        print("\nFatto!")
        
        # Chiede se continuare con un altro anime
        if ask_user_input("\nVuoi scaricare/riprodurre un altro anime?", is_yes_no=True):
            print("\n" + "="*60)
            main()  # Ricorsione per un altro download
        else:
            print("\nGrazie per aver usato AnimeUnity Downloader!")
            
    except KeyboardInterrupt:
        print("\n\nOperazione interrotta dall'utente")
        sys.exit(1)
    except Exception as e:
        print(f"\nErrore inaspettato: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
    finally:
        client.close()  # Chiude la connessione

if __name__ == "__main__":
    main()