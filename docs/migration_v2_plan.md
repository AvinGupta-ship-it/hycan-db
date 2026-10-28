# Migration plan: schema v2 columns

**Script:** `scripts/migrate_v2.py`. **Test:** `tests/test_migrate_v2.py`.
**Why:** `docs/v1_protocol.md` (§3, §9, Appendix A) needs 30 fields that schema
v1.3 cannot hold. Schema v2 adds them to `src/hycan/schema.py`, and this
migration adds the matching columns to the dataset.

## 1. Change

The migration appends 30 columns at physical positions 68–97, in the order the
schema declares them, and writes every new cell empty. Empty means "not yet
coded": no existing row gains a claim it did not make before. The v1.0
re-verification fills the cells from the source papers (protocol §9).

No existing cell changes, and no row is added or removed.

## 2. Guarantees, checked by the script and the test

- The header is the old 67 columns followed by the 30 new ones, in schema order.
- Every original cell is unchanged, and every new cell is empty.
- Every original physical line survives byte-for-byte as a prefix of its new
  line, including line endings and the final-newline state.
- The script refuses to run on a file that already has 97 columns, or that has
  any v2 column.
- The migrated dataset validates against schema v2 with no new errors.
