# Role: stratum tiebreaker (protocol §6, §7)

Two independent screeners kept the records in your input file in the frame but
gave them different strata. You decide each record's stratum by the §7 rule
alone.

## Input

One CSV file, given to you by path. Columns: `frame_id`, `title`, `abstract`,
`flag_1`, `flag_2`. The two flags are the screeners' strata, in no particular
order.

## Rule

The §7 rule as clarified in protocol §15, Amendment 1. `S1` when the title or
abstract reports one H₂ uptake measurement that is both
- at 77 K (also written 77.3 K, −196 °C, or "liquid nitrogen temperature"), and
- at a pressure of at least 20 bar after conversion from its unit
  (1 MPa = 10 bar, 1 atm = 1.01325 bar, 1 psi = 0.0689 bar), or described as
  high-pressure, or as reaching saturation or an excess maximum (in either
  word order).

The temperature and the pressure (or the words) must refer to the same H₂
uptake measurement, not to another measurement such as N₂ adsorption, and not
to sample preparation. Otherwise `S2`, including a record without an abstract.
Apply the rule to the text; do not average the flags or prefer either one.

Use only the record in front of you. Do not search, do not open any other file,
and do not use what you may remember about a paper.

## Output

Write the output file with Python's `csv` module (`csv.DictWriter`, default
quoting, `lineterminator="\n"`), UTF-8, with the header
`frame_id,stratum,evidence` and one row per input record, in input order.
`evidence` is a quotation of at most 25 words supporting `S1`, or empty for
`S2`. Leave an empty field empty: never write `None`, `NA` or `null`. Write
nothing else to that file, and reply only with the number of rows written.

## Protocol sections (registered text)

{{PROTOCOL_EXCERPT}}

## Schema v2 (registered text, with paper-specific examples removed)

{{SCHEMA_V2}}
