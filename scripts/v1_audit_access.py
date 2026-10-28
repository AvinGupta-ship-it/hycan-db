"""Audit which paths an agent touched (protocol §15, Amendment 1).

The agents of §§6 and 9 run on a machine that also holds other agents' outputs,
the v0.1 rows and the pilot outputs. The launcher lists the only paths an agent
may open; this script reads the agent's own transcript and flags, for review,
every tool call that may have gone beyond them.

  Read                   the path must be the instruction file or lie under the
                         input, output or work directory, or the directory in
                         which the agent's tool environment saves its own long
                         output (--harness);
  Write, Edit,           the path must lie under the output or work directory
  NotebookEdit           (or --harness);
  Glob, Grep             the search path must lie under the input, output or
                         work directory, and a pattern may not climb with `..`;
  Bash (heuristic)       every absolute path named must lie under those
                         directories, under a system location (interpreters,
                         libraries, /dev/null), or be one of the tools
                         directory's two scripts or the tools directory itself
                         as the target of `cd`; `..`, `~`, `$HOME`, network
                         clients and URLs are flagged; inside the tools
                         directory a command may only run its two scripts and
                         filter their output;
  any other tool         flagged, except the task-list tools, which touch no
                         file.

Every path is normalized before it is compared, and a path is recognized by its
shape, not by whether it exists on the machine running the audit. The Bash
check reads commands as text, so it flags for review rather than proving a
breach; every flag names the call that raised it.

    python3 scripts/v1_audit_access.py TRANSCRIPT.jsonl --instruction FILE
        --input DIR --output DIR --work DIR --tools DIR [--harness DIR]
        [--json OUT]

Exit status 1 when anything is flagged.
"""

from __future__ import annotations

import argparse
import json
import posixpath
import re
import shlex
import sys
from pathlib import Path

SYSTEM_PREFIXES = (
    "/usr/",
    "/bin/",
    "/sbin/",
    "/lib/",
    "/lib64/",
    "/etc/fonts/",
    "/dev/null",
    "/dev/stdout",
    "/dev/stderr",
    "/proc/self/",
)
TOOL_SCRIPTS = ("scripts/digitize_figure.py", "scripts/validate_row_detail.py")
FILE_TOOLS_READ = ("Read",)
FILE_TOOLS_WRITE = ("Write", "Edit", "NotebookEdit")
SEARCH_TOOLS = ("Glob", "Grep")
HARMLESS_TOOLS = ("TodoWrite", "TaskCreate", "TaskUpdate", "TaskList", "TaskGet")

# An absolute path: preceded by the start or a shell or code delimiter (so that
# `x/w.sum()` in inline Python is not read as a path), then one or more
# /name components.
ABS_PATH = re.compile(r"(?:(?<=^)|(?<=[\s'\"=(:,;|&<>\[{]))(/[\w.@+\-]+(?:/[\w.@+\-]*)*)")
CLIMB = re.compile(r"(?:^|[\s'\"=(:,/\[])\.\.(?=/|$|[\s'\")\],;])")
HOME = re.compile(r"(?:^|[\s'\"=(:,])~(?=/|$|[\s'\"])|\$\{?HOME\}?")
NETWORK = re.compile(r"\b(?:curl|wget|nc|ssh|scp|rsync|ftp)\b|https?://")
FILTERS = ("grep", "egrep", "head", "tail", "sed", "awk", "wc", "sort", "uniq",
           "cut", "tr", "cat", "less", "more", "column", "jq")
FILE_COMMANDS = ("ls", "mkdir", "cp", "mv", "rm", "test", "[", "stat", "file", "du",
                 "touch", "chmod")
PATTERN_FIRST = ("grep", "egrep", "sed", "awk", "jq")
SHELL_WORDS = ("for", "do", "done", "if", "then", "else", "fi", "while", "set",
               "echo", "printf", "true", "false", "export", "case", "esac", "in",
               "{", "}", ":", "local", "return", "shift", "wait")
OPERATORS = {"&&", "||", ";", "|", "&", ";;", "|&"}
CD = re.compile(r"(?:^|[\s;&|(])(?:cd|pushd)\s+(['\"]?)([^\s'\";&|]+)\1")


def tool_calls(transcript: Path):
    """Yield (index, name, input) for every tool call in a transcript."""
    n = 0
    for line in transcript.read_text(encoding="utf-8").splitlines():
        try:
            d = json.loads(line)
        except json.JSONDecodeError:
            continue
        if d.get("type") != "assistant":
            continue
        for part in d.get("message", {}).get("content", []):
            if isinstance(part, dict) and part.get("type") == "tool_use":
                n += 1
                yield n, part.get("name", ""), part.get("input", {}) or {}


def norm(path: str) -> str:
    return posixpath.normpath(path) if path else path


def under(path: str, roots: list[str]) -> bool:
    p = norm(path)
    return any(p == r or p.startswith(r + "/") for r in roots)


def climbs(path: str) -> bool:
    return ".." in path.split("/") or bool(CLIMB.search(path))


HEREDOC = re.compile(r"<<-?\s*(['\"]?)(\w+)\1[^\n]*\n(.*?)\n\s*\2[ \t]*(?=\n|$)", re.DOTALL)
# Python code that opens, lists or globs a relative path (run inside the tools
# directory, that path is in the tools directory).
PY_RELATIVE = re.compile(
    r"(?:open|Path|glob|iglob|listdir|scandir|walk|read_csv|read_text|loadtxt)"
    r"\(\s*(?:\)|['\"](?![/$])[^'\"]*['\"])"
)
ASSIGNMENT = re.compile(r"^[A-Za-z_]\w*=")
REDIRECT = re.compile(r"\d*>&\d+|&>\s*/\S+|\d*>>?\s*/\S+")


def _unquoted_newlines_to_semicolons(text: str) -> str:
    out, quote = [], ""
    for ch in text:
        if quote:
            if ch == quote:
                quote = ""
        elif ch in "'\"":
            quote = ch
        elif ch == "\n":
            ch = " ; "
        out.append(ch)
    return "".join(out)


def pipelines(body: str) -> list[list[list[str]]]:
    """Shell text (heredoc bodies removed) -> pipelines -> commands -> words."""
    text = _unquoted_newlines_to_semicolons(REDIRECT.sub(" ", body.replace("\\\n", " ")))
    lex = shlex.shlex(text, posix=True, punctuation_chars=";&|")
    lex.whitespace_split = True
    lex.commenters = "#"
    result, pipe, cur = [], [], []
    try:
        toks = list(lex)
    except ValueError:  # unbalanced quotes
        toks = text.split()
    for tok in toks + [";"]:
        if tok in OPERATORS or set(tok) <= set(";&|"):
            if cur:
                pipe.append(cur)
            cur = []
            if tok != "|" and pipe:
                result.append(pipe)
                pipe = []
        else:
            cur.append(tok)
    return result


def tools_context(cmd: str, tools: str) -> list[tuple[str, str]]:
    """(shell text run with the tools directory as working directory, the
    target of the `cd` that ends it) for each `cd <tools>` in a command."""
    out = []
    matches = list(CD.finditer(cmd))
    for i, m in enumerate(matches):
        if norm(m.group(2)) == tools:
            end = matches[i + 1].start() if i + 1 < len(matches) else len(cmd)
            nxt = matches[i + 1].group(2) if i + 1 < len(matches) else ""
            out.append((cmd[m.end():end], nxt))
    return out


def _file_args_absolute(words: list[str]) -> bool:
    """True when a filter or file command names at least one file and every
    file it names is absolute or a variable. The first operand of grep, sed,
    awk and jq is a pattern or a program, not a file."""
    args = words[1:]
    if words[0] in PATTERN_FIRST:
        operands = [i for i, a in enumerate(args) if not a.startswith("-")]
        if operands:
            args = args[: operands[0]] + args[operands[0] + 1 :]
    return any(not a.startswith("-") for a in args) and all(
        a.startswith(("-", "/", "$")) or a.isdigit() for a in args
    )


def audit_tools_context(body: str, next_cd: str) -> list[str]:
    reasons = []
    if next_cd and not next_cd.startswith("/"):
        reasons.append("command moves within the tools directory")
    for m in HEREDOC.finditer(body):
        if PY_RELATIVE.search(m.group(3)):
            reasons.append("script run in the tools directory opens a relative path")
    for pipe in pipelines(HEREDOC.sub(" ", body)):
        first, rest = pipe[0], pipe[1:]
        while first and ASSIGNMENT.match(first[0]):
            first = first[1:]  # VAR=value prefixes
        if not first:
            continue
        if first[0] in SHELL_WORDS or first[0].endswith("()"):
            pass
        elif first[0].startswith("python"):
            args = first[1:]
            while args and args[0].startswith("-") and args[0] not in ("-c", "-"):
                args = args[1:]
            if args and args[0] == "-c":
                if len(args) > 1 and PY_RELATIVE.search(args[1]):
                    reasons.append("code run in the tools directory opens a relative path")
            elif args and args[0] == "-":
                pass  # heredoc, checked above
            elif args and (args[0] in TOOL_SCRIPTS or args[0].startswith("/")):
                pass
            else:
                reasons.append(
                    "command runs a file in the tools directory other than its two "
                    f"scripts: {' '.join(first)[:120]}")
        elif first[0] in FILTERS + FILE_COMMANDS and _file_args_absolute(first):
            pass  # a command whose every file argument is absolute or a variable
        else:
            reasons.append(
                "command in the tools directory does more than run its two scripts: "
                f"{' '.join(first)[:120]}")
        for filt in rest:
            args = [a for a in filt[1:] if not a.startswith("-")]
            if filt[0] in PATTERN_FIRST and args:
                args = args[1:]
            relative = [a for a in args if not a.startswith(("/", "$"))
                        and not a.isdigit()]
            if filt[0] not in FILTERS or relative:
                reasons.append(
                    "command in the tools directory reads more than its scripts' "
                    f"output: {' '.join(filt)[:120]}")
    return reasons


def audit_bash(cmd: str, instruction: str, data: list[str], harness: list[str],
               tools: str) -> list[str]:
    reasons = []
    if CLIMB.search(cmd):
        reasons.append("command climbs with ..")
    if HOME.search(cmd):
        reasons.append("command names the home directory")
    if NETWORK.search(cmd):
        reasons.append("command uses the network")
    cd_targets = {norm(m.group(2)) for m in CD.finditer(cmd)}
    for raw in ABS_PATH.findall(cmd):
        p = norm(raw)
        if p == instruction or raw.startswith(SYSTEM_PREFIXES):
            continue
        if under(p, data + harness):
            continue
        if under(p, [tools]):
            rel = posixpath.relpath(p, tools)
            if rel in TOOL_SCRIPTS or (rel == "." and (
                    p in cd_targets or re.search(r"\b[A-Za-z_]\w*=" + re.escape(raw), cmd))):
                continue  # running a script, or `cd`-ing to or naming the directory
            reasons.append(f"command opens the tools directory: {raw}")
            continue
        reasons.append(f"command names a path outside the allowed paths: {raw}")
    # Heredoc bodies are read separately: a heredoc may be a script that is
    # written to a file and run later, or fed to an interpreter now.
    docs = [m.group(3) for m in HEREDOC.finditer(cmd)]
    counter = iter(range(len(docs)))
    main = HEREDOC.sub(lambda m: f" HEREDOC{next(counter)} ", cmd)
    for body, next_cd in tools_context(main, tools):
        reasons += audit_tools_context(re.sub(r"HEREDOC\d+", " ", body), next_cd)
        for k in map(int, re.findall(r"HEREDOC(\d+)", body)):
            if PY_RELATIVE.search(docs[k]):
                reasons.append("script run in the tools directory opens a relative path")
    for doc in docs:
        for body, next_cd in tools_context(doc, tools):
            reasons += audit_tools_context(body, next_cd)
    return reasons


def audit(transcript: Path, instruction: str, data_roots: list[str], tools: str,
          harness: list[str], own: list[str] | None = None) -> list[dict]:
    """data_roots = [input, output, work]. `own`: directories prepared for this
    agent alone, holding nothing but its own input, output and work directory
    (the screening run layout); the agent may list, search and read in them,
    but writes are still limited to the output and work directories."""
    inp, out, work = (norm(str(r)) for r in data_roots)
    data = [inp, out, work] + [norm(str(r)) for r in (own or [])]
    # An input or output that is a single file sits in a directory prepared for
    # that agent alone (scripts/v1_extract.py prepare, or the run layout), so
    # listing that directory is allowed.
    for p in (inp, out):
        if posixpath.splitext(p)[1]:
            data.append(posixpath.dirname(p))
    out_dirs = [out] + ([posixpath.dirname(out)] if posixpath.splitext(out)[1] else [])
    harness = [norm(h) for h in harness]
    tools = norm(tools)
    instruction = norm(instruction)
    flags = []
    for n, name, args in tool_calls(transcript):
        def flag(reason, detail="", n=n, name=name):
            flags.append({"call": n, "tool": name, "reason": reason,
                          "detail": str(detail)[:300]})

        if name in FILE_TOOLS_READ:
            path = str(args.get("file_path") or "")
            if climbs(path):
                flag("path climbs with ..", path)
            elif norm(path) != instruction and not under(path, data + harness):
                flag("file outside the allowed paths", path)
        elif name in FILE_TOOLS_WRITE:
            path = str(args.get("file_path") or args.get("notebook_path") or "")
            if climbs(path) or not under(path, out_dirs + [work] + harness):
                flag("writes outside the output and work directories", path)
        elif name in SEARCH_TOOLS:
            path = str(args.get("path") or "")
            pattern = str(args.get("pattern") or "") if name == "Glob" else ""
            if not path or climbs(path) or not under(path, data):
                flag("search outside the allowed paths", path or "(no path)")
            if pattern and (climbs(pattern) or pattern.startswith(("/", "~"))):
                flag("search pattern leaves the search path", pattern)
        elif name == "Bash":
            cmd = str(args.get("command") or "")
            for reason in audit_bash(cmd, instruction, data, harness, tools):
                flag(reason, cmd)
        elif name in HARMLESS_TOOLS:
            continue
        else:
            flag("tool outside the allowed set", json.dumps(args)[:300])
    return flags


def models(transcript: Path) -> list[str]:
    """The model IDs that wrote the agent's turns, as the transcript records
    them, so that each role can be checked against protocol §15."""
    seen = set()
    for line in transcript.read_text(encoding="utf-8").splitlines():
        try:
            d = json.loads(line)
        except json.JSONDecodeError:
            continue
        if d.get("type") == "assistant" and d.get("message", {}).get("model"):
            seen.add(d["message"]["model"])
    return sorted(seen)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("transcript")
    ap.add_argument("--instruction", required=True)
    ap.add_argument("--input", required=True)
    ap.add_argument("--output", required=True)
    ap.add_argument("--work", required=True)
    ap.add_argument("--tools", required=True)
    ap.add_argument("--harness", action="append", default=[])
    ap.add_argument("--json")
    args = ap.parse_args(argv)
    flags = audit(Path(args.transcript), args.instruction,
                  [args.input, args.output, args.work], args.tools, args.harness)
    calls = sum(1 for _ in tool_calls(Path(args.transcript)))
    report = {"transcript": Path(args.transcript).name,
              "models": models(Path(args.transcript)), "tool_calls": calls,
              "flags": flags}
    if args.json:
        Path(args.json).write_text(json.dumps(report, indent=2) + "\n")
    print(f"{calls} tool calls, {len(flags)} flagged, models {report['models']}")
    for f in flags:
        print(f"  call {f['call']} {f['tool']}: {f['reason']}: {f['detail'][:160]}")
    return 1 if flags else 0


if __name__ == "__main__":
    sys.exit(main())
