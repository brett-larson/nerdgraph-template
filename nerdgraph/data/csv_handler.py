"""CSV handler for reading and writing data"""

from typing import List, Dict, Generator
import csv
import os
from pathlib import Path


class CSVHandler:
    """Generic CSV handler for reading and writing data"""

    def __init__(self, base_dir: str = None, chunk_size: int = 1000):
        if base_dir is None:
            # Default to 'files' directory under nerdgraph/data
            base_dir = Path(__file__).parent.parent / 'files'
        self.base_dir = Path(base_dir)
        self.chunk_size = chunk_size
        self.base_dir.mkdir(exist_ok=True)

    def get_file_path(self, filename: str) -> Path:
        """Get full path for a CSV file"""
        return self.base_dir / filename

    def write_data(self, filename: str, data: List[Dict], append: bool = False):
        """Write data to CSV file"""
        if not data:
            return

        mode = 'a' if append else 'w'
        file_path = self.get_file_path(filename)

        with open(file_path, mode, newline='') as f:
            writer = csv.DictWriter(f, fieldnames=data[0].keys())
            if not append or file_path.stat().st_size == 0:
                writer.writeheader()

            for chunk in self._chunk_data(data):
                writer.writerows(chunk)

    def read_data(self, filename: str) -> Generator[Dict, None, None]:
        """Read data from CSV file"""
        file_path = self.get_file_path(filename)

        with open(file_path, 'r', newline='') as f:
            reader = csv.DictReader(f)
            for row in reader:
                yield row

    def _chunk_data(self, data: List[Dict]) -> Generator[List[Dict], None, None]:
        """Break data into chunks"""
        for i in range(0, len(data), self.chunk_size):
            yield data[i:i + self.chunk_size]