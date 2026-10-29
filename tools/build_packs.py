#!/usr/bin/env python3
"""
Kryeit Datapack Monorepo Build & Validation Tool
"""

import os
import sys
import json
import zipfile
import argparse

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PACKS_DIR = os.path.join(REPO_ROOT, 'packs')
DIST_DIR = os.path.join(REPO_ROOT, 'dist')

def validate_json_files():
    """Validates that all .json and .mcmeta files in packs/ contain valid JSON."""
    errors = 0
    checked = 0
    for root, _, files in os.walk(PACKS_DIR):
        for f in files:
            if f.endswith('.json') or f.endswith('.mcmeta'):
                full_path = os.path.join(root, f)
                rel_path = os.path.relpath(full_path, REPO_ROOT)
                checked += 1
                try:
                    with open(full_path, 'r', encoding='utf-8') as fh:
                        json.load(fh)
                except Exception as e:
                    print(f"❌ JSON ERROR in {rel_path}: {e}", file=sys.stderr)
                    errors += 1
    if errors == 0:
        print(f"✅ All {checked} JSON/mcmeta files validated successfully.")
        return True
    else:
        print(f"❌ Validation failed with {errors} errors.", file=sys.stderr)
        return False

def build_packs(output_dir=DIST_DIR):
    """Packages each directory in packs/ into a standalone .zip file."""
    os.makedirs(output_dir, exist_ok=True)
    built = []
    
    for pack_name in sorted(os.listdir(PACKS_DIR)):
        pack_path = os.path.join(PACKS_DIR, pack_name)
        if not os.path.isdir(pack_path):
            continue
        
        mcmeta = os.path.join(pack_path, 'pack.mcmeta')
        if not os.path.exists(mcmeta):
            print(f"⚠️  Skipping {pack_name}: no pack.mcmeta found.")
            continue
        
        zip_name = f"{pack_name}.zip"
        zip_path = os.path.join(output_dir, zip_name)
        
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zf:
            for root, _, files in os.walk(pack_path):
                for f in files:
                    if f.endswith('.disabled'):
                        continue
                    full = os.path.join(root, f)
                    arcname = os.path.relpath(full, pack_path)
                    zf.write(full, arcname)
        
        size_kb = os.path.getsize(zip_path) / 1024
        print(f"📦 Built {zip_name:<30} ({size_kb:6.1f} KB)")
        built.append(zip_path)
    
    return built

def main():
    parser = argparse.ArgumentParser(description="Kryeit Datapack Tool")
    parser.add_argument('--validate-only', action='store_true', help="Only validate JSON files")
    parser.add_argument('--output', default=DIST_DIR, help="Output directory for zip archives")
    args = parser.parse_args()

    print(f"🔍 Validating datapack JSON files in {PACKS_DIR}...")
    if not validate_json_files():
        sys.exit(1)
        
    if args.validate_only:
        sys.exit(0)
        
    print(f"\n🔨 Building datapack archives in {args.output}...")
    build_packs(args.output)
    print("\n🎉 Build complete!")

if __name__ == '__main__':
    main()
