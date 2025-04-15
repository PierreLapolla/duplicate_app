import questionary
from pathlib import Path
from utils.try_except import try_except


@try_except
def get_user_configuration():
    # Option 1: Drives
    drives = [f"{chr(d)}:\\" for d in range(65, 91) if Path(f"{chr(d)}:\\").exists()]
    if not drives:
        raise Exception("Aucun disque trouvé!")

    selected_drives = questionary.checkbox(
        "Sélectionnez les disques à scanner:",
        choices=drives,
    ).ask()

    if not selected_drives:
        raise Exception("Aucun disque sélectionné!")

    # Option 2: File extensions
    file_extensions = questionary.checkbox(
        "Sélectionnez les extensions à scanner:",
        choices=["txt", "jpg", "png", "mp3", "mp4", "pdf", "docx"],
    ).ask()

    # Option 3: Fast search
    fast_search = questionary.select(
        "Utiliser la recherche rapide?",
        choices=[
            "Oui - Recherche rapide, mais peut avoir des faux positifs",
            "Non - Recherche plus lente mais sûre",
        ],
    ).ask()

    return {
        "selected_drives": selected_drives,
        "fast_search": fast_search.startswith("Oui"),
        "file_extensions": file_extensions,
    }
