#!/usr/bin/env python3
"""DaCapo Engine - Architekt 3.0"""

import os, sys, re, shutil
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple, Optional
import time
from os import getenv
from dotenv import load_dotenv

load_dotenv()

INPUT_CHAR_LIMIT = 7500
BASE_DIR = Path(__file__).parent
AGENTS_DIR = BASE_DIR / "agents"
DOCS_DIR = BASE_DIR / "docs"
CODE_MAP_DIR = BASE_DIR / "code_map"
INPUT_DIR = BASE_DIR / "input"
HISTORY_DIR = BASE_DIR / "history"

STAGE_PROMPTS = {
    "analyst": AGENTS_DIR / "analyst.txt",
    "constructor": AGENTS_DIR / "constructor.txt",
    "critic": AGENTS_DIR / "critic.txt"
}


class LLMProvider:
    def __init__(self):
        self.provider = getenv("LLM_PROVIDER", "openai").lower()
        self.max_retries = int(getenv("MAX_RETRIES", "3"))
        self.retry_delay = int(getenv("RETRY_DELAY", "2"))
        
        if self.provider == "openai":
            self._init_openai()
        elif self.provider == "perplexity":
            self._init_perplexity()
        else:
            raise ValueError(f"Unknown provider: {self.provider}")
    
    def _init_openai(self):
        try:
            from openai import OpenAI
            api_key = getenv("OPENAI_API_KEY")
            if not api_key:
                raise ValueError("OPENAI_API_KEY not set")
            self.client = OpenAI(api_key=api_key)
            self.model = getenv("OPENAI_MODEL", "gpt-4o-mini")
            self.max_tokens = int(getenv("OPENAI_MAX_TOKENS", "8000"))
            self.temperature = float(getenv("OPENAI_TEMPERATURE", "0.2"))
            print(f"   Provider: OpenAI ({self.model})")
        except ImportError:
            print("ERROR: pip install openai")
            sys.exit(1)
    
    def _init_perplexity(self):
        try:
            from openai import OpenAI
            api_key = getenv("PERPLEXITY_API_KEY")
            if not api_key:
                raise ValueError("PERPLEXITY_API_KEY not set")
            self.client = OpenAI(api_key=api_key, base_url="https://api.perplexity.ai")
            self.model = getenv("PERPLEXITY_MODEL", "sonar")
            self.max_tokens = 8000
            self.temperature = 0.2
            print(f"   Provider: Perplexity ({self.model})")
        except ImportError:
            print("ERROR: pip install openai")
            sys.exit(1)
    
    def call(self, prompt: str) -> str:
        for attempt in range(self.max_retries):
            try:
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": "You are a code architecture assistant."},
                        {"role": "user", "content": prompt}
                    ],
                    max_tokens=self.max_tokens,
                    temperature=self.temperature
                )
                return response.choices[0].message.content
            except Exception as e:
                print(f"   Attempt {attempt + 1} failed: {e}")
                if attempt < self.max_retries - 1:
                    time.sleep(self.retry_delay)
                else:
                    raise
        return ""


class Architect:
    def __init__(self):
        self.iteration_counter = 0
        self.llm = LLMProvider()
    
    def validate_input(self, text: str) -> Tuple[bool, str]:
        length = len(text)
        if length > INPUT_CHAR_LIMIT:
            return False, f"Za długi: {length}/{INPUT_CHAR_LIMIT}"
        if length < 100:
            return False, "Za krótki (min 100)"
        return True, f"OK: {length}/{INPUT_CHAR_LIMIT}"
    
    def create_backup(self, iteration: int):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_dir = HISTORY_DIR / f"{timestamp}_iter{iteration}"
        backup_dir.mkdir(parents=True, exist_ok=True)
        for src_dir in [DOCS_DIR, CODE_MAP_DIR]:
            if src_dir.exists():
                dst_dir = backup_dir / src_dir.name
                shutil.copytree(src_dir, dst_dir, dirs_exist_ok=True)
        return backup_dir
    
    def load_structure(self) -> Dict[str, str]:
        structure = {}
        for base_dir in [DOCS_DIR, CODE_MAP_DIR]:
            if not base_dir.exists():
                continue
            for ext in ["*.py", "*.md"]:
                for file_path in base_dir.rglob(ext):
                    relative_path = file_path.relative_to(BASE_DIR)
                    try:
                        structure[str(relative_path)] = file_path.read_text(encoding='utf-8')
                    except Exception as e:
                        print(f"Error {relative_path}: {e}")
        return structure
    
    def load_agent_prompt(self, stage: str) -> str:
        prompt_file = STAGE_PROMPTS.get(stage)
        if not prompt_file or not prompt_file.exists():
            raise FileNotFoundError(f"Brak: {stage}")
        return prompt_file.read_text(encoding='utf-8')
    
    def run_stage(self, stage: str, input_content: str, context: Dict[str, str]) -> str:
        prompt = self.load_agent_prompt(stage)
        full_prompt = f"{prompt}\n\n=== STRUKTURA ===\n"
        for path, content in context.items():
            full_prompt += f"\n<file path='{path}'>\n{content}\n</file>\n"
        full_prompt += f"\n=== PRAD ===\n{input_content}"
        print(f"\nAgent '{stage}' ({len(full_prompt)} chars)...")
        response = self.llm.call(full_prompt)
        print(f"   {len(response)} chars")
        return response
    
    def parse_file_blocks(self, response: str) -> Dict[str, str]:
        files = {}
        pattern = r'<file\s+path=["\']([^"\']+ )["\']\s*>(.*?)</file>'
        for path, content in re.findall(pattern, response, re.DOTALL):
            files[path] = content.strip()
        return files
    
    def apply_changes(self, files: Dict[str, str]):
        for relative_path, content in files.items():
            file_path = BASE_DIR / relative_path
            file_path.parent.mkdir(parents=True, exist_ok=True)
            file_path.write_text(content, encoding='utf-8')
            print(f"   Updated: {relative_path}")
    
    def save_report(self, report: str, iteration: int):
        report_path = HISTORY_DIR / f"critic_report_iter{iteration}.md"
        report_path.write_text(report, encoding='utf-8')

    
    def run_iteration(self, input_file: Path):
        self.iteration_counter += 1
        iteration = self.iteration_counter
        print("\n" + "="*70)
        print(f"ARCHITEKT 3.0 - ITERACJA {iteration}")
        print("="*70)
        input_content = input_file.read_text(encoding='utf-8')
        valid, msg = self.validate_input(input_content)
        print(f"\n{msg}")
        if not valid:
            return
        print(f"\nBackup...")
        backup_dir = self.create_backup(iteration)
        structure = self.load_structure()
        print(f"   {len(structure)} files")
        print(f"\nANALIZA")
        analyst_response = self.run_stage('analyst', input_content, structure)
        print(f"\nKONSTRUKTOR")
        constructor_response = self.run_stage('constructor', input_content, structure)
        updated_files = self.parse_file_blocks(constructor_response)
        print(f"   {len(updated_files)} files")
        if updated_files:
            self.apply_changes(updated_files)
        print(f"\nWERYFIKACJA")
        updated_structure = self.load_structure()
        critic_response = self.run_stage('critic', input_content, updated_structure)
        self.save_report(critic_response, iteration)
        print("\n" + "="*70)
        print(f"ITERACJA {iteration} OK")
        print("="*70)
        print(f"Pliki: {', '.join(updated_files.keys()) or 'brak'}")
        print(f"critic_report_iter{iteration}.md")


if __name__ == "__main__":
    print("DaCapo Architect 3.0")
    input_file = INPUT_DIR / "raw_chunk.txt"
    if not input_file.exists():
        print(f"\nStwórz: {input_file}")
        sys.exit(0)
    architect = Architect()
    architect.run_iteration(input_file)
