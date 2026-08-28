import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
sys.stdout.reconfigure(encoding='utf-8')

from services.funtime_api import fetch_funtime_events
from services.seed_db import init_csv, load_all_seeds, find_similar_anarchies
from handlers.events import build_events_page_text, build_events_keyboard, filter_event_list

async def run_tests():
    print("=== TEST 1: CSV Seed DB ===")
    seeds = load_all_seeds()
    print(f"Loaded {len(seeds)} seeds successfully.")
    
    res101 = find_similar_anarchies("101")
    print(f"Query 101: found={res101['found']}, seed={res101['seed']}, matching={res101['matching']}")
    assert res101["found"] == True
    assert "202" in res101["matching"]
    print("[OK] CSV matching test passed!")

    print("\n=== TEST 2: FunTime Events API ===")
    events = await fetch_funtime_events()
    print(f"Fetched {len(events)} events from funtime.me API.")
    if events:
        sample = events[0]
        print(f"Sample Event: {sample['icon']} {sample['name']} on {sample['server_name']} (phase: {sample['phase_name']}, time: {sample['time_str']}, coords: {sample['coords']})")
        
        filtered = filter_event_list(events, "all")
        page_text = build_events_page_text(filtered, 0, 5, "all")
        print("\nFormatted page preview:")
        print(page_text[:400] + "...\n")
        print("[OK] Events parsing and formatting test passed!")

    print("\n=== ALL UNIT TESTS PASSED SUCCESSFULLY! ===")

if __name__ == "__main__":
    asyncio.run(run_tests())
