import os, platform, subprocess, sys, httpx
from pathlib import Path
from typing import List, Optional
from tqdm import tqdm

IS_WINDOWS = platform.system() == "Windows"
IS_LINUX = platform.system() == "Linux"
IS_MAC = platform.system() == "Darwin"

def clear_screen():
    # Pulisce il terminale in base alla piattaforma
    if IS_WINDOWS:
        subprocess.run(['cmd', '/c', 'cls'], shell=True)
    else:
        subprocess.run(['clear'], shell=True)

def sanitize_filename(name: str) -> str:
    # Rimuove i caratteri non validi per i nomi di file
    invalid_chars = '<>:"/\\|?*'
    for char in invalid_chars:
        name = name.replace(char, '_')
    name = name.strip('. ')
    return name

def ask_user_input(prompt: str, default: str = None, is_yes_no: bool = False) -> str:
    # Chiede input all'utente con valore predefinito opzionale
    if default and not is_yes_no:
        prompt = f"{prompt} [{default}]: "
    elif is_yes_no:
        prompt = f"{prompt} (s/n): "
    else:
        prompt = f"{prompt}: "
    
    user_input = input(prompt).strip()
    
    if is_yes_no:
        return user_input.lower() in ['s', 'si', 'y', 'yes']
    
    return user_input if user_input else default

def select_from_list(items: List[dict], title_key: str, id_key: str, prompt: str) -> dict:
    # Mostra una lista numerata e lascia selezionare l'utente
    print(f"\n{'-'*50}")
    for i, item in enumerate(items[:10], 1):
        title = item.get(title_key, 'Sconosciuto')
        print(f"  {i}. {title}")
    
    print(f"{'-'*50}")
    
    while True:
        try:
            choice = ask_user_input(prompt, default="1")
            choice_num = int(choice)
            if 1 <= choice_num <= len(items[:10]):
                return items[choice_num - 1]
            else:
                print(f"Inserisci un numero tra 1 e {len(items[:10])}")
        except ValueError:
            print("Inserisci un numero valido")

def get_download_path() -> Path:
    # Ottiene la directory di download dall'utente
    print(f"\n{'='*60}")
    print("CONFIGURAZIONE DOWNLOAD")
    print(f"{'='*60}")
    
    # Percorso predefinito in base alla piattaforma
    if IS_WINDOWS:
        default_path = str(Path.home() / "Downloads" / "AnimeUnity")
    elif IS_LINUX:
        default_path = str(Path.home() / "Videos" / "AnimeUnity")
    else:
        default_path = str(Path.home() / "Movies" / "AnimeUnity")
    
    print(f"Piattaforma rilevata: {platform.system()}")
    print(f"Percorso download predefinito: {default_path}")
    
    custom_path = ask_user_input(
        "Inserisci il percorso di download (o premi Invio per usare quello predefinito)",
        default=default_path
    )
    
    download_path = Path(custom_path).expanduser().resolve()
    
    print(f"\nI download verranno salvati in: {download_path}")
    if ask_user_input("Corretto?", is_yes_no=True):
        download_path.mkdir(parents=True, exist_ok=True)
        print(f"Cartella pronta: {download_path}")
        return download_path
    else:
        return get_download_path()  # Richiede nuovamente

class AnimeUnityAPIClient:
    # Client per interagire con l'API locale di AnimeUnity
    
    def __init__(self, base_url: str = "http://127.0.0.1:8000"):
        self.base_url = base_url
        self.client = httpx.Client(timeout=30.0)
    
    def check_api_health(self) -> bool:
        # Verifica se il server API è in esecuzione
        try:
            self.client.get(f"{self.base_url}/docs", timeout=5)
            return True
        except httpx.ConnectError:
            return False
    
    def search_anime(self, title: str) -> List[dict]:
        # Cerca anime per titolo usando l'API
        response = self.client.get(
            f"{self.base_url}/search",
            params={"title": title}
        )
        response.raise_for_status()
        return response.json()
    
    def get_episodes(self, anime_id: str) -> List[dict]:
        # Ottiene la lista degli episodi per un anime specifico
        response = self.client.get(
            f"{self.base_url}/episodes",
            params={"anime_id": anime_id}
        )
        response.raise_for_status()
        return response.json()
    
    def get_stream_url(self, episode_id: str) -> Optional[str]:
        # Ottiene l'URL video diretto per un episodio
        try:
            response = self.client.get(
                f"{self.base_url}/stream",
                params={"episode_id": episode_id}
            )
            response.raise_for_status()
            data = response.json()
            return data.get("video_url") or data.get("url")
        except Exception as e:
            print(f"  Errore nel recupero dell'URL: {e}")
            return None
    
    def close(self):
        # Chiude la sessione HTTP
        self.client.close()

def stream_with_mpv(video_urls: List[str], anime_title: str):
    # Riproduce gli URL video direttamente con mpv
    if not video_urls:
        print("Nessun URL video da riprodurre")
        return
    
    print(f"\n{'='*60}")
    print(f"In riproduzione: {anime_title}")
    print(f"Episodi: {len(video_urls)}")
    print(f"{'='*60}")
    print("\nComandi MPV:")
    print("  Spazio/Pausa - Play/Pausa")
    print("  Invio - Schermo intero")
    print("  q - Esci")
    print("  > - Episodio successivo")
    print("  < - Episodio precedente")
    print(f"\n{'='*60}\n")
    
    mpv_cmd = ["mpv"]
    
    # Opzioni utili per mpv
    mpv_cmd.extend([
        "--save-position-on-quit",  # Ricorda dove ci si era fermati
        "--keep-open=always",       # Non chiude dopo l'episodio
        "--volume=100",             # Volume predefinito
        "--cache=yes",              # Abilita cache per riproduzione fluida
        "--cache-secs=300",         # Cache di 5 minuti
    ])
    
    mpv_cmd.extend(video_urls)
    
    try:
        subprocess.run(mpv_cmd, check=False)
    except FileNotFoundError:
        print("\nmpv non trovato! Per favore installa mpv:")
        if IS_WINDOWS:
            print("  Scarica da: https://mpv.io/installation/")
            print("  Oppure usa chocolatey: choco install mpv")
        elif IS_LINUX:
            print("  Ubuntu/Debian: sudo apt install mpv")
            print("  Fedora: sudo dnf install mpv")
            print("  Arch: sudo pacman -S mpv")
        else:
            print("  brew install mpv")
        sys.exit(1)

def download_videos(video_urls: List[str], anime_title: str, anime_id: str, download_dir: Path, start_ep: int):
    # Scarica i video in cartelle organizzate con barre di progresso
    safe_anime_title = sanitize_filename(anime_title)
    anime_folder = download_dir / safe_anime_title
    anime_folder.mkdir(parents=True, exist_ok=True)
    
    print(f"\n{'='*60}")
    print(f"Download in corso: {anime_title}")
    print(f"Percorso: {anime_folder}")
    print(f"Episodi: {len(video_urls)}")
    print(f"{'='*60}\n")
    
    for i, (url, index) in enumerate(zip(video_urls, range(start_ep, start_ep + len(video_urls))), 1):
        # Formatta il nome come anime_nome_epnumero.mp4
        filename = f"{safe_anime_title}_{index:03d}.mp4"
        filepath = anime_folder / filename
        
        # Salta se il file esiste e l'utente non vuole sovrascrivere
        if filepath.exists():
            overwrite = ask_user_input(
                f"\nIl file {filename} esiste gia. Sovrascrivere?",
                is_yes_no=True
            )
            if not overwrite:
                print(f"  Salto {filename}")
                continue
        
        print(f"\nDownload episodio {index}...")
        print(f"   File: {filename}")
        
        try:
            with httpx.stream("GET", url, timeout=120) as response:
                response.raise_for_status()
                total = int(response.headers.get("content-length", 0))
                
                total_mb = total / (1024 * 1024)
                print(f"   Dimensione: {total_mb:.2f} MB")
                
                with open(filepath, "wb") as f:
                    with tqdm(total=total, unit="B", unit_scale=True, 
                             desc=f"Episodio {index}", 
                             bar_format='{l_bar}{bar}| {n_fmt}/{total_fmt} [{rate_fmt}]') as progress:
                        for chunk in response.iter_bytes(chunk_size=8192):
                            f.write(chunk)
                            progress.update(len(chunk))
            
            print(f"  Salvato in: {filepath}")
        except Exception as e:
            print(f"  Download fallito per l'episodio {index}: {e}")
    
    print(f"\n{'='*60}")
    print(f"Download completato!")
    print(f"File salvati in: {anime_folder}")
    print(f"{'='*60}")

def get_episode_range(total_episodes: int) -> tuple:
    # Ottiene l'intervallo di episodi dall'utente
    print(f"\n{'='*60}")
    print("SELEZIONE EPISODI")
    print(f"{'='*60}")
    print(f"Episodi totali disponibili: {total_episodes}")
    
    while True:
        start_ep = ask_user_input(
            "Inserisci l'episodio di partenza",
            default="1"
        )
        
        end_ep = ask_user_input(
            "Inserisci l'episodio di fine",
            default=str(total_episodes)
        )
        
        try:
            start = int(start_ep)
            end = int(end_ep)
            
            if start < 1 or end > total_episodes or start > end:
                print(f"Intervallo non valido. Inserisci numeri tra 1-{total_episodes} con inizio <= fine")
                continue
            
            print(f"\nEpisodi selezionati: {start} a {end} ({end - start + 1} episodi)")
            if ask_user_input("Corretto?", is_yes_no=True):
                return start, end
        except ValueError:
            print("Inserisci numeri validi")