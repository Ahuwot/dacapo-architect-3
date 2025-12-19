#!/usr/bin/env python3
"""Setup script - tworzy pozostałe pliki Architektury 3.0"""

from pathlib import Path

BASE = Path(__file__).parent

# Remaining agent prompts
(BASE / "agents" / "constructor.txt").write_text("""Jesteś Konstruktorem w DaCapo Engine Architect 3.0.

TWOJE ZADANIE:
Na podstawie raportu Analityka oraz AKTUALNEGO STANU STRUKTURY (pliki docs/, code_map/), wygeneruj PEŁNE, ZAKTUALIZOWANE wersje plików, w których WPLATASZ nowe elementy wgłąb istniejących sekcji – nie na końcu.

ZASADY PRACY WGŁĄB:
1. Jeśli plik już istnieje, ZMODYFIKUJ go w odpowiednim miejscu
2. Jeśli klasa istnieje, DODAJ/ZAKTUALIZUJ metody wewnątrz niej
3. Jeśli sekcja dokumentacji istnieje, WSTAW nowy akapit w logicznym miejscu
4. Oznacz każdą zmianę: # [ITERACJA: N] [ŹRÓDŁO: raw_chunk.txt]
5. Jeśli brak szczegółów: [PUSTE MIEJSCE: opis]

FORMAT WYJŚCIA: Generuj bloki <file path="...">...</file>

PAMIĘTAJ: Generuj KOMPLETNE pliki, nie fragmenty.""", encoding='utf-8')

(BASE / "agents" / "critic.txt").write_text("""Jesteś Krytykiem w DaCapo Engine Architect 3.0.

TWOJE ZADANIE:
Przeanalizuj AKTUALNY STAN STRUKTURY i wykryj:
1. Niespójności między dokumentacją a kodem
2. Luki (miejsca [PUSTE MIEJSCE])
3. Sprzeczności w nazwach, typach
4. Brakujące zależności

FORMAT WYJŚCIA:
=== RAPORT KRYTYKA ===

🔴 KRYTYCZNE LUKI:
...

🟡 WAŻNE NIESPÓJNOŚCI:
...

=== PRIORYTET NAPRAWY ===
...""", encoding='utf-8')

# Docs
(BASE / "docs").mkdir(exist_ok=True)
(BASE / "docs" / "01_vision.md").write_text("""# DaCapo Engine - Vision

[UTWORZONO: Iteracja 0]

## Cel Projektu
DaCapo Engine to local-first PKM dla śpiewaków operowych i studentów języków.

[PUSTE MIEJSCE: szczegółowy opis user persona]

## Core Philosophy
- Local-first: Wszystkie dane w SQLite
- Text-centric: Libreta, arie jako materiał edukacyjny
- Iterative design: Architektura hermeneutyczna

## Technical Stack
- Backend: Python 3.10+, SQLite
- AI: LLM agents
- UI: [PUSTE MIEJSCE]
""", encoding='utf-8')

(BASE / "docs" / "02_data_structure.md").write_text("""# Data Structure

## Database Schema

### Tabela: documents
[PUSTE MIEJSCE: schemat]

### Tabela: sentences
[PUSTE MIEJSCE]

### Tabela: vocabulary
[PUSTE MIEJSCE]

### Tabela: srs_cards
[PUSTE MIEJSCE]
""", encoding='utf-8')

(BASE / "docs" / "03_ui_ux.md").write_text("""# UI/UX Design

## User Journey
[PUSTE MIEJSCE]

## Main Views
### 1. Library View
[PUSTE MIEJSCE]

### 2. Reading View
[PUSTE MIEJSCE]

### 3. Study Session
[PUSTE MIEJSCE]
""", encoding='utf-8')

# Code map
(BASE / "code_map").mkdir(exist_ok=True)
(BASE / "code_map" / "ingestion.py").write_text("""# DaCapo Engine - Ingestion Pipeline
# [UTWORZONO: Iteracja 0]

from pathlib import Path
from typing import Dict, List

class IngestionPipeline:
    def __init__(self, db_path: str):
        self.db_path = db_path
        # [PUSTE MIEJSCE: inicjalizacja DB]
    
    def parse_markdown(self, content: str) -> Dict:
        # [PUSTE MIEJSCE: implementacja]
        return {"sections": []}
    
    def extract_sentences(self, text: str) -> List[str]:
        # [PUSTE MIEJSCE: tokenizer]
        return []
""", encoding='utf-8')

(BASE / "code_map" / "learning.py").write_text("""# DaCapo Engine - Learning Module
# [UTWORZONO: Iteracja 0]

from typing import List, Dict
from datetime import datetime, timedelta

class SRSScheduler:
    def __init__(self, algorithm: str = "SM2"):
        self.algorithm = algorithm
    
    def calculate_next_review(self, card: Dict, grade: int) -> datetime:
        # [PUSTE MIEJSCE: algorytm SM-2]
        return datetime.now() + timedelta(days=1)
    
    def get_due_cards(self, limit: int = 20) -> List[Dict]:
        # [PUSTE MIEJSCE: query DB]
        return []

class VocabularyExtractor:
    def __init__(self, db_path: str):
        self.db_path = db_path
    
    def extract_from_sentence(self, sentence: str, language: str) -> List[Dict]:
        # [PUSTE MIEJSCE: tokenizacja]
        return []
""", encoding='utf-8')

(BASE / "code_map" / "database.py").write_text("""# DaCapo Engine - Database Layer
# [UTWORZONO: Iteracja 0]

import sqlite3
from pathlib import Path
from typing import Optional, Dict, List

def create_schema(db_path: str) -> None:
    # [PUSTE MIEJSCE: SQL dla tabel]
    pass

class DatabaseConnection:
    def __init__(self, db_path: str):
        self.db_path = db_path
        self.conn = None
        # [PUSTE MIEJSCE: połączenie]
    
    def execute_query(self, query: str, params: tuple = ()) -> List[Dict]:
        # [PUSTE MIEJSCE: transakcje]
        return []
    
    def execute_write(self, query: str, params: tuple = ()) -> int:
        # [PUSTE MIEJSCE: commit]
        return -1
""", encoding='utf-8')

# Input folder with example
(BASE / "input").mkdir(exist_ok=True)
(BASE / "input" / "raw_chunk.txt").write_text("""[PRZYKŁADOWY PRĄD - USUŃ I WKLEJ SWÓJ]

Tutaj wklejaj surowe fragmenty rozmów, notatek, kodu do przetworzenia przez Architekta.

Format opcjonalny:
[ITERATION: 1]
[SOURCE: conversation_with_gemini.txt]

... treść prądu ...
""", encoding='utf-8')

# .gitignore
(BASE / ".gitignore").write_text("""__pycache__/
*.py[cod]
*$py.class
*.so
.Python
history/
critic_report_*.md
.DS_Store
.vscode/
.idea/
*.db
*.sqlite
""", encoding='utf-8')

print("✅ Struktura Architektury 3.0 utworzona!")
print(f"📁 Lokalizacja: {BASE}")
print("\n📂 Struktura:")
print("├── architect.py")
print("├── agents/")
print("│   ├── analyst.txt")
print("│   ├── constructor.txt")
print("│   └── critic.txt")
print("├── docs/")
print("│   ├── 01_vision.md")
print("│   ├── 02_data_structure.md")
print("│   └── 03_ui_ux.md")
print("├── code_map/")
print("│   ├── ingestion.py")
print("│   ├── learning.py")
print("│   └── database.py")
print("├── input/")
print("│   └── raw_chunk.txt")
print("└── history/ (pusty)")
print("\n🚀 Następne kroki:")
print("1. git add .")
print("2. git commit -m 'Complete Architecture 3.0 structure'")
print("3. git push")
