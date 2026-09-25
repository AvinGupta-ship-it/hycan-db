#!/usr/bin/env python3
"""
Source-backed backfills for schema v1.1 (manual §8.5 gaps 3-4, §8.6).

These are the three changes docs/migration_v1.1_plan.md §3 deferred because
they needed the source papers. Every value below was extracted from the PDF
and then independently re-derived by a second agent that had the papers and
the candidate values only, with no access to the first agent's reasoning
(§3.2). All 40 verified cells agreed.

1. HYC-0021 (Sethia & Sayari 2016) ultra-micropore volumes, Table 2, the
   column footnoted "Volume of pores with less than 0.7 nm width". CP-400 and
   CP-600 are "NA" in the table and stay empty.

2. HYC-0005 (Texier-Mandoki 2004) pore volume below 0.7 nm, Table 1, the
   V_DR(CO2) column. The paper defines it: "the adsorption of CO2 at 273 K
   allows us to assess the narrowest micropores (i.e., pores size smaller
   than 0.7 nm)". Same physical quantity as HYC-0021's ultra-micropore
   column, determined by a different method, which the row note records.

   Also for HYC-0005: surface_area_method BET -> unspecified. §8.6 asked
   whether a total surface area had been entered into the BET field. It had.
   Table 1's column is headed "TSA" and footnoted "TSA, total surface area";
   the strings "BET" and "Brunauer" do not occur anywhere in the paper. The
   only method sentence names instruments, not a model: "The total surface
   area and micropore volume were determined by physical adsorption of N2 at
   77 K and CO2 at 273 K using, respectively, an automatic adsorption system
   (ASAP2000-micromeritics) and a manual adsorption system." The values stay
   in bet_surface_area_m2_g because the schema has no generic surface-area
   field; surface_area_method is what now carries the truth. §8.6 also asked
   whether this warrants extraction_confidence 4 rather than 5. It does: the
   rows previously asserted a method the authors never claimed.

3. HYC-0018 (Singh & De 2020) two characterization-only rows recovered, which
   schema v1.0 could not represent because temperature_k and pressure_bar
   were unconditionally required (§8.5 gap 3). Table 2, corroborated in body
   text. Neither sample has a numeric hydrogen uptake anywhere in the text or
   tables; EGR (400)'s uptake exists only as plotted points in Fig. 9, so
   under §3.4 it cannot be recorded without digitization, and the row says so.

Run with --dry-run first. Refuses to run twice.
"""

from __future__ import annotations

import argparse
import csv
import os
import shutil
import sys
from datetime import datetime

DATASET = "data/raw/measurements_v0.1.csv"

# --- 1. HYC-0021, Table 2, "Ultra-micropores" (< 0.7 nm) --------------------
SETHIA_ULTRAMICROPORE = {
    "HYC-0021-S3": "0.12",   # NAC-1.5-550
    "HYC-0021-S4": "0.27",   # NAC-1.5-600
    "HYC-0021-S5": "0.21",   # NAC-1.5-650
    "HYC-0021-S6": "0.0",    # NAC-1.5-700
}
SETHIA_NOTE = (
    "Ultra-micropore volume from Table 2, DFT cumulative pore volume, "
    "pores below 0.7 nm width (Table 2 footnote c). Micropore column is "
    "pores below 2 nm (footnote d)."
)

# --- 2. HYC-0005, Table 1, V_DR(CO2) (< 0.7 nm) -----------------------------
TEXIER_ULTRAMICROPORE = {
    "S1": "0.39",   # Carbon C
    "S2": "0.31",   # JM1
    "S3": "0.33",   # Norit R0,8
    "S4": "0.37",   # PICACTIF SC
    "S5": "0.52",   # Carbon A
    "S6": "0.56",   # AX21
    "S7": "0.60",   # Carbon B
}
TEXIER_NOTE = (
    "Pore volume below 0.7 nm is V_DR(CO2) from Table 1, Dubinin-Radushkevitch "
    "applied to CO2 adsorption at 273 K, P/P0 < 0.03. Surface area is the "
    "paper's TSA column, footnoted 'total surface area'; the paper never "
    "states a BET determination, so surface_area_method is unspecified and "
    "extraction_confidence is 4 rather than 5."
)

# --- 3. HYC-0018, Table 2, the two samples with no uptake measurement -------
SINGH_NEW_ROWS = [
    {
        "sample_id": "HYC-0018-S4", "measurement_id": "HYC-0018-M5",
        "material_class": "graphene_oxide",
        "material_description": "Graphene oxide, unexfoliated starting material (GO)",
        "bet_surface_area_m2_g": "41", "total_pore_volume_cm3_g": "0.14",
        "average_pore_diameter_nm": "1.8",
        "notes": (
            "Characterization-only row: this paper reports no numeric hydrogen "
            "uptake for the unexfoliated GO sample in any text or table, and GO "
            "appears in none of the hydrogen panels of Fig. 9. Recoverable only "
            "under schema v1.1, which makes temperature and pressure "
            "conditional. Caution for later extractors: this paper uses 'GO "
            "exfoliated at 300 C' in prose to mean the sample Table 2 calls EGR "
            "(300), so the 3.12 wt% figure belongs to EGR (300), not to GO."
        ),
    },
    {
        "sample_id": "HYC-0018-S5", "measurement_id": "HYC-0018-M6",
        "material_class": "reduced_graphene_oxide",
        "material_description": (
            "Graphene oxide thermally exfoliated at 400 C in hydrogen flow "
            "(EGR 400)"
        ),
        "bet_surface_area_m2_g": "218", "total_pore_volume_cm3_g": "1.40",
        "average_pore_diameter_nm": "3.9",
        "notes": (
            "Characterization-only row: EGR (400)'s hydrogen uptake appears "
            "nowhere in the text or tables, only as plotted points in Fig. 9, "
            "so under §3.4 it cannot be recorded without programmatic "
            "digitization. Structural values from Table 2, corroborated at "
            "p. 9: 'At 400 C, the values decreased slightly to 218 m2/g and "
            "1.4 cm3/g respectively'. Tier inherited from this paper's "
            "uptake-bearing rows; the §13.3 rubric scores the reporting of an "
            "uptake measurement and this row has none."
        ),
    },
]


def load(path):
    with open(path, "r", encoding="utf-8", newline="") as handle:
        rows = list(csv.reader(handle))
    return rows[0], rows[1:]


def save(path, header, rows):
    with open(path, "w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle, lineterminator="\n")
        writer.writerow(header)
        writer.writerows(rows)


def append_note(existing: str, addition: str) -> str:
    existing = (existing or "").strip()
    if addition in existing:
        return existing
    return f"{existing} {addition}".strip()


def backfill(header, rows):
    index = {name: position for position, name in enumerate(header)}
    if "ultramicropore_volume_cm3_g" not in index:
        raise SystemExit(
            "run scripts/migrate_v1_1.py first; the v1.1 columns are absent"
        )

    changes = []
    new_rows = []
    template = None

    for row in rows:
        row = list(row)
        paper = row[index["paper_id"]]
        sample = row[index["sample_id"]]

        if paper == "HYC-0018" and template is None:
            template = list(row)

        if paper == "HYC-0021" and sample in SETHIA_ULTRAMICROPORE:
            if row[index["ultramicropore_volume_cm3_g"]].strip():
                raise SystemExit(f"{sample} already has an ultramicropore value")
            row[index["ultramicropore_volume_cm3_g"]] = SETHIA_ULTRAMICROPORE[sample]
            row[index["notes"]] = append_note(row[index["notes"]], SETHIA_NOTE)
            changes.append((sample, "ultramicropore_volume_cm3_g"))

        if paper == "HYC-0005":
            key = sample.split("-")[-1]
            if key in TEXIER_ULTRAMICROPORE:
                row[index["ultramicropore_volume_cm3_g"]] = TEXIER_ULTRAMICROPORE[key]
                row[index["surface_area_method"]] = "unspecified"
                row[index["extraction_confidence"]] = "4"
                row[index["notes"]] = append_note(row[index["notes"]], TEXIER_NOTE)
                changes.append((sample, "ultramicropore + method + confidence"))

        new_rows.append(row)

    if template is None:
        raise SystemExit("no HYC-0018 row to use as a template")

    for spec in SINGH_NEW_ROWS:
        row = list(template)
        # everything not named below is inherited from the paper's other rows:
        # paper_id, doi, first_author, year, journal, title, synthesis_method,
        # extractor, extraction_date, reproducibility_tier.
        for field in ("purification_method", "activation_method", "dopant_element",
                      "dopant_concentration_at_pct", "functional_groups",
                      "langmuir_surface_area_m2_g", "micropore_volume_cm3_g",
                      "ultramicropore_volume_cm3_g", "temperature_k",
                      "pressure_bar", "uptake_wt_pct", "uptake_mmol_g",
                      "uptake_ml_stp_g", "uncertainty_wt_pct", "verified_by",
                      "verification_date"):
            row[index[field]] = ""
        row[index["uptake_type"]] = "unspecified"
        row[index["measurement_method"]] = "unknown"
        row[index["extraction_method"]] = "table_direct"
        row[index["extraction_confidence"]] = "5"
        row[index["source_location"]] = "Table 2"
        row[index["surface_area_method"]] = "BET"
        for field, value in spec.items():
            row[index[field]] = value
        new_rows.append(row)
        changes.append((spec["sample_id"], "new characterization-only row"))

    return header, new_rows, changes


def main(argv):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dataset", default=DATASET)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--backup-dir", default="/tmp")
    args = parser.parse_args(argv[1:])

    if not os.path.exists(args.dataset):
        print(f"Error: dataset not found: {args.dataset}")
        return 2

    header, rows = load(args.dataset)
    header, new_rows, changes = backfill(header, rows)

    print(f"{len(changes)} change(s):")
    for sample, what in changes:
        print(f"  {sample}: {what}")
    print(f"rows {len(rows)} -> {len(new_rows)}")

    target = (os.path.join(args.backup_dir, "backfill_dryrun.csv")
              if args.dry_run else args.dataset)
    if not args.dry_run:
        os.makedirs(args.backup_dir, exist_ok=True)
        stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        backup = os.path.join(
            args.backup_dir, f"measurements_v0.1.prebackfill.{stamp}.csv"
        )
        shutil.copy2(args.dataset, backup)
        print(f"Backup: {backup}")

    save(target, header, new_rows)
    print(f"Written: {target}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
