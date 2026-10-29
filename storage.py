"""Persistencia en archivos CSV (un CSV por modelo)."""

import csv
import os
from pathlib import Path

DATA_DIR = Path(os.environ.get("DATA_DIR", "data"))


class CsvRepo:

    def __init__(self, filename: str, model):
        self.model = model
        self.fields = list(model.model_fields)
        DATA_DIR.mkdir(parents=True, exist_ok=True)
        self.path = DATA_DIR / filename
        if not self.path.exists():
            self._write([])

    def _write(self, items):
        with open(self.path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=self.fields)
            writer.writeheader()
            for item in items:
                writer.writerow(item.model_dump(mode="json"))

    def all(self):
        with open(self.path, newline="", encoding="utf-8") as f:
            return [self.model.model_validate(row) for row in csv.DictReader(f)]

    def get(self, item_id: int):
        return next((i for i in self.all() if i.id == item_id), None)

    def add(self, data: dict):
        items = self.all()
        new_id = max((i.id for i in items), default=0) + 1
        obj = self.model(id=new_id, **data)
        items.append(obj)
        self._write(items)
        return obj

    def update(self, item_id: int, changes: dict):
        items = self.all()
        for idx, item in enumerate(items):
            if item.id == item_id:
                items[idx] = item.model_copy(update=changes)
                self._write(items)
                return items[idx]
        return None

    def delete(self, item_id: int) -> bool:
        items = self.all()
        remaining = [i for i in items if i.id != item_id]
        if len(remaining) == len(items):
            return False
        self._write(remaining)
        return True
