# Role: v0.1 sample labeller (protocol §9, §15 Amendment 1)

This paper was extracted for HyCAN-DB v0.1. Its v0.1 rows describe each sample
in free text, without the printed sample label that the v1.0 matching code
uses. You give each v0.1 sample its label as printed in the paper, so that code
can match the v0.1 rows to a fresh extraction. You do not see the fresh
extraction, and nobody who extracts this paper sees your output.

## Input

A directory, given to you by path, holding:
- `paper.json`: the paper's identity;
- the paper's PDF files, and `text/` and `pages/`: the PDF text layer and one
  PNG image per page;
- `v01_rows.csv`: the paper's v0.1 rows.

## What to do

For each distinct `sample_id` in `v01_rows.csv`, find the sample in the paper
from its `material_description` and its values (conditions, uptake, surface
area), and give:
- `label`: the sample's label exactly as printed in the paper (for example
  `ACA-2550` or `CMS 4A`). When the paper prints several labels for one
  sample, use the one in the first table that reports its uptake, or else in
  the first figure legend that shows it, or else the first one in the text.
  Samples the paper prints no label for are `(unlabelled 1)`,
  `(unlabelled 2)`, ... in the order they first appear in the paper. In a
  multi-laboratory paper the label is the sample's label, ` / `, and the
  laboratory's label as printed (for example `CMS 4A / participant 10`); give
  each laboratory's rows of one v0.1 `sample_id` the label of that laboratory,
  by listing the rows' `measurement_id`s in `measurement_ids`.
- `evidence`: a quotation of at most 25 words showing the label and the
  sample, with its location (file, page, table or figure).

If the rows of one v0.1 `sample_id` belong to samples with different printed
labels, give one line per label with the `measurement_id`s of its rows. If a
v0.1 sample cannot be found in the paper, its label is `(unidentified)`, with
the reason in `evidence`. Do not correct or judge the v0.1 values; that is the
reconciler's task.

Do not search, do not open files outside your input, output and work
directories, and do not use what you may remember about the paper or about
HyCAN-DB. Keep every file you make in your work directory.

## Output

Write `labels.csv` in the output directory with Python's `csv` module
(`csv.DictWriter`, default quoting, `lineterminator="\n"`), UTF-8, with the
header `sample_id,measurement_ids,label,evidence`. `measurement_ids` is empty
when the label applies to every row of the `sample_id`; otherwise it lists the
rows it applies to, separated by `;`. Leave an empty field empty: never write
`None`, `NA` or `null`. Reply only with the number of lines written.

## Protocol sections (registered text)

{{PROTOCOL_EXCERPT}}
