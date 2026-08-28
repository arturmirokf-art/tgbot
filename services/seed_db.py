import csv
import os
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from config import CSV_PATH, SYSTEMDLC_CSV_PATH

def init_csv():
    """Ensure CSV file exists with headers."""
    CSV_PATH.parent.mkdir(parents=True, exist_ok=True)
    if not CSV_PATH.exists():
        with open(CSV_PATH, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["anarchy", "seed", "updated_at"])
            # Add some sample starter seeds for popular FunTime anarchies
            writer.writerow(["101", "GEN-9A4F2B", "2026-08-29 00:00"])
            writer.writerow(["105", "GEN-9A4F2B", "2026-08-29 00:00"])
            writer.writerow(["118", "GEN-9A4F2B", "2026-08-29 00:00"])
            writer.writerow(["102", "GEN-3E8C1D", "2026-08-29 00:00"])
            writer.writerow(["204", "GEN-3E8C1D", "2026-08-29 00:00"])
            writer.writerow(["201", "GEN-F5109A", "2026-08-29 00:00"])
            writer.writerow(["203", "GEN-F5109A", "2026-08-29 00:00"])
            writer.writerow(["501", "GEN-F5109A", "2026-08-29 00:00"])

def sync_mod_csv():
    """Sync data from Minecraft mod CSV if it exists."""
    for mod_path in [SYSTEMDLC_CSV_PATH, SYSTEMDLC_CSV_PATH.parent.parent / "anarchy_seeds.csv"]:
        if mod_path.exists():
            try:
                records = load_all_seeds(mod_path)
                for anarchy, (seed, updated_at) in records.items():
                    save_seed(anarchy, seed, updated_at)
            except Exception:
                pass

def load_all_seeds(file_path: Optional[Path] = None) -> Dict[str, Tuple[str, str]]:
    """Loads all anarchy -> (seed, updated_at) mappings."""
    path = file_path or CSV_PATH
    if not path.exists():
        init_csv()
    
    seeds: Dict[str, Tuple[str, str]] = {}
    try:
        with open(path, "r", encoding="utf-8") as f:
            reader = csv.reader(f)
            header = next(reader, None)
            for row in reader:
                if len(row) >= 2:
                    anarchy = str(row[0]).strip().lower().replace("anarchy", "").replace("анка", "").replace("анархия", "")
                    seed = str(row[1]).strip()
                    updated_at = str(row[2]).strip() if len(row) > 2 else ""
                    if anarchy and seed:
                        seeds[anarchy] = (seed, updated_at)
    except Exception as e:
        print(f"[SeedDB] Error loading CSV {path}: {e}")
    return seeds

def save_seed(anarchy: str, seed: str, updated_at: str = "") -> bool:
    """Saves or updates a seed record in CSV."""
    init_csv()
    anarchy_clean = str(anarchy).strip().lower().replace("anarchy", "").replace("анка", "").replace("анархия", "")
    seed_clean = str(seed).strip()
    
    seeds = load_all_seeds()
    seeds[anarchy_clean] = (seed_clean, updated_at)
    
    try:
        with open(CSV_PATH, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["anarchy", "seed", "updated_at"])
            for ank, (s, up) in sorted(seeds.items(), key=lambda x: (int(x[0]) if x[0].isdigit() else 9999, x[0])):
                writer.writerow([ank, s, up])
        return True
    except Exception as e:
        print(f"[SeedDB] Error writing CSV: {e}")
        return False

def find_similar_anarchies(anarchy_query: str) -> Dict:
    """
    Finds seed of given anarchy and all other anarchies sharing the same seed.
    """
    sync_mod_csv()
    anarchy_clean = str(anarchy_query).strip().lower().replace("anarchy", "").replace("анка", "").replace("анархия", "").strip()
    seeds = load_all_seeds()
    
    if anarchy_clean not in seeds:
        return {
            "found": False,
            "query": anarchy_clean,
            "seed": None,
            "matching": [],
            "all_recorded_count": len(seeds)
        }
    
    target_seed, updated_at = seeds[anarchy_clean]
    
    # Find all other anarchies with the identical seed
    matching = [
        ank for ank, (s, _) in seeds.items()
        if s.lower() == target_seed.lower() and ank != anarchy_clean
    ]
    
    # Sort matching numerically if possible
    matching.sort(key=lambda x: int(x) if x.isdigit() else 9999)
    
    return {
        "found": True,
        "query": anarchy_clean,
        "seed": target_seed,
        "updated_at": updated_at,
        "matching": matching,
        "all_recorded_count": len(seeds)
    }
