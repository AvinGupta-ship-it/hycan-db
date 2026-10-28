# HyCAN-DB v1.0 registration record

The v1.0 protocol was registered by publishing a standalone Zenodo record that
archives the files the protocol names (`docs/v1_protocol.md`, Registration).

| Item | Value |
|---|---|
| Zenodo record | https://zenodo.org/records/23719010 |
| DOI | [10.5281/zenodo.23719010](https://doi.org/10.5281/zenodo.23719010) |
| Concept DOI | [10.5281/zenodo.23719009](https://doi.org/10.5281/zenodo.23719009) |
| Publication (registration) date | 2026-10-28 |
| Published at | 2026-10-28T03:26:46Z (Zenodo record `created` timestamp) |
| Registration commit | `0190009f414488812c84d7f3bee8753cdc54f6a4` |

## Archived files

Each file in the record is byte-identical to the same path at the registration
commit. Zenodo reports MD5; the SHA-256 values are also stated in the record's
description.

| File (path at the commit) | Bytes | SHA-256 | MD5 (as reported by Zenodo) |
|---|---|---|---|
| `docs/v1_protocol.md` | 46641 | `5e77195d4215f7013847ea314f13165e3c2df87d107568b8ba46426326079498` | `6bb763d0d1029c928390b8f4455d781a` |
| `src/hycan/schema.py` | 32892 | `40224df6a1804d80e9a00336279b8a2f9a7159e894fc53de9d1945ba6d448219` | `6db832a13c4f9c3973ae713f211d8002` |
| `docs/data_dictionary.md` | 53418 | `91a102fda438eccb5c29c1c15d6d7d537175280fcfbf2e50920b13763dcd7176` | `b33b039ca4fa700b000582bb036202c8` |
| `requirements-v1.lock` | 1050 | `4b4ca40e4e4873a78f558822a9c32fee4e100c7de105f5d7774909435de359a6` | `e665bfcd4d142e441694c6ad57bc11ff` |

To check a file against the commit:

```bash
git show 0190009f414488812c84d7f3bee8753cdc54f6a4:docs/v1_protocol.md | sha256sum
```

## State at registration

At the publication time above, no v1.0 search request had been sent, and no
frame record, sampled paper or new data value had been seen. The protocol's §1
states what the author had seen: the v0.1 rows and the referee's re-analyses of
them.

The commit before the registration commit, `d75061d`, carries an earlier state
of the same files. It was pushed before the computed-field code showed that the
data dictionary needed a definition of a coded row; `0190009` added that
definition and is the registered state.

## After registration

`docs/v1_protocol.md`, `src/hycan/schema.py`, `docs/data_dictionary.md` and
`requirements-v1.lock` are changed only through dated amendments appended to
protocol §15 (`docs/v1_protocol.md`, §9 and §15). Their state at any later
commit can be compared with the registered state with `git diff 0190009 --`.
