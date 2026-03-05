from pathlib import Path 
from datetime import datetime 

class FileMetadata:
    def __init__(self, path: str):
        self.path: Path = Path(path) 

    def add_metadata(self) -> dict:
        name = self.path.name 
        stat = self.path.stat()
        size = stat.st_size 
        try:
            birth_time = stat.st_birthtime 
        except AttributeError:
            birth_time = stat.st_mtime 
        date_created = datetime.fromtimestamp(birth_time) 
        date_modified = datetime.fromtimestamp(stat.st_mtime)
        
        
        return {
            "name": name, 
            "size": size, 
            "date_created": str(date_created), 
            "date_modified": str(date_modified) 
        }