# Kryeit Datapack Monorepo

Welcome to the **Kryeit Datapack Monorepo** for Minecraft 1.21.1 (NeoForge).

This repository organizes the server's custom mechanics, recipes, fluid conventions, and world protection tags into standalone, modular datapacks. Each sub-pack operates independently, logs diagnostic loading messages on `/reload`, and can be loaded or updated without side-effects on other server features.

---

## 📦 Packs Overview

All packs reside under the [`packs/`](./packs/) directory:

| Pack Directory | Description | Load Announcement |
|---|---|---|
| [`kryeit_world_guards`](./packs/kryeit_world_guards/) | Anti-exploit tags: prevents Create from moving Vaults/Trial Spawners/Heavy Cores, blocks infinite Hose Pulley pools on culinary liquids, and makes End structures dragon-immune. | `[kryeit_world_guards] Loaded: Non-movable blocks, dragon immunity & bottomless deny tags active.` |
| [`kryeit_fluid_compat`](./packs/kryeit_fluid_compat/) | Standardized `c:tags/fluid` and culinary item tags uniting Farmer's Delight and Create fluids (soups, stews, ciders, sauces). | `[kryeit_fluid_compat] Loaded: Standardized fluid and culinary tags for Create & Farmer's Delight.` |
| [`kryeit_custom_recipes`](./packs/kryeit_custom_recipes/) | Catalytic superheated mixing (iron, copper, zinc), casing application, rich soil, crying obsidian, and wild crop crafting recipes. | `[kryeit_custom_recipes] Loaded: Catalytic metallurgy, casing transformations & custom crafting recipes.` |
| [`kryeit_delightful_creators`](./packs/kryeit_delightful_creators/) | Custom automation recipes overriding Delightful Creators (pie crust, mechanical cutter, cabbage rolls, etc.). | `[kryeit_delightful_creators] Loaded: Mechanical kitchen recipes & automation overrides.` |
| [`kryeit_train_fuels`](./packs/kryeit_train_fuels/) | Custom Steam 'n Rails locomotive liquid fuel definitions (Bioethanol). | `[kryeit_train_fuels] Loaded: Locomotive bioethanol fuel registry.` |

---

## 🛠️ Validation & Build Tool

A python build tool is provided in [`tools/build_packs.py`](./tools/build_packs.py) to validate all JSON files and package the packs for deployment.

### Validate JSON Syntax
```bash
python3 tools/build_packs.py --validate-only
```

### Build Distribution ZIPs
```bash
python3 tools/build_packs.py
```
This builds ready-to-deploy `.zip` files into `dist/`:
- `dist/kryeit_world_guards.zip`
- `dist/kryeit_fluid_compat.zip`
- `dist/kryeit_custom_recipes.zip`
- `dist/kryeit_delightful_creators.zip`
- `dist/kryeit_train_fuels.zip`

---

## 🚀 Adding a New Pack

To add a new feature pack:
1. Create a new directory under `packs/your_pack_name`.
2. Add a `pack.mcmeta` with `pack_format: 48`.
3. Add a diagnostic function hook under `data/minecraft/tags/function/load.json` pointing to `your_pack_name:load`.
4. Run `python3 tools/build_packs.py` to verify JSON syntax.
