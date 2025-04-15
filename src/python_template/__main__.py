import os
from collections import defaultdict
from dataclasses import dataclass
from hashlib import md5
from pathlib import Path
from typing import List

from tqdm import tqdm

from utils.logger import log
from utils.timer import timer


@dataclass
class FileData:
    path: Path
    extension: str
    size: int
    hash: str = None


def scan_system(allowed_extensions: List[str]) -> List[FileData]:
    root = Path("/").expanduser()
    file_data_list = []

    for root, _, files in tqdm(
        os.walk(root, followlinks=False),
        desc="Scanning system (and filtering invalid extensions)",
        mininterval=0.25,
    ):
        for file in files:
            try:
                file_path = Path(root) / file
                file_extension = file_path.suffix.lstrip(".").lower()
                file_size = file_path.stat().st_size
                if file_extension in allowed_extensions:
                    file_data = FileData(
                        path=file_path, extension=file_extension, size=file_size
                    )
                    file_data_list.append(file_data)
            except Exception:
                continue
                # log.warning(f"Error accessing file {file}: {e}")

    return file_data_list


def filter_alone_files(
    files: List[FileData], grouping_attribute: str
) -> List[FileData]:
    groups = defaultdict(list)
    for file in tqdm(
        files, desc=f"Filtering files by {grouping_attribute}", mininterval=0.25
    ):
        groups[getattr(file, grouping_attribute)].append(file)
    for key, group in list(groups.items()):
        if len(group) <= 1:
            del groups[key]
    return [file for group in groups.values() for file in group]


def compute_hashes(files: List[FileData], block_size: int = -1) -> List[FileData]:
    description = (
        "Computing full hashes" if block_size == -1 else "Computing partial hashes"
    )
    for file in tqdm(files, desc=description, mininterval=0.25):
        try:
            with open(file.path, "rb") as f:
                content = f.read(block_size)
                file.hash = md5(content).hexdigest()
        except Exception:
            continue
            # log.warning(f"Error computing partial hash for file {file.path}: {e}")
    return files


@timer
def main() -> None:
    fast_search = True
    allowed_extensions = [
        "txt",
        "pdf",
        "docx",
        "xlsx",
        "pptx",
        "jpg",
        "png",
        "mp4",
        "mp3",
    ]

    files = scan_system(allowed_extensions)
    log.info(f"Found {len(files)} files")

    filter_size_files = filter_alone_files(files, grouping_attribute="size")
    filter_extensions_files = filter_alone_files(
        filter_size_files, grouping_attribute="extension"
    )
    log.info(f"Filtered files: {len(filter_extensions_files)}")

    partial_hashes = compute_hashes(filter_extensions_files, 1024)
    filter_hash_files = filter_alone_files(partial_hashes, grouping_attribute="hash")
    log.info(f"Filtered files: {len(filter_hash_files)}")

    if not fast_search:
        full_hashes = compute_hashes(filter_hash_files)
        filter_full_hash_files = filter_alone_files(
            full_hashes, grouping_attribute="hash"
        )
        log.info(f"Filtered files: {len(filter_full_hash_files)}")


if __name__ == "__main__":
    main()
