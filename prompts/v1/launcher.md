Read the file {PROMPT_PATH} completely before you do anything else. It is long,
so read it in parts with offset and limit until you reach its end. It is your
complete instruction. Then carry out its task with these run parameters:

- Tools directory (run commands from here): {TOOLS}
- Input: {INPUT}
- Output: {OUTPUT}
- Work directory: {WORK}

You may open only these paths: the instruction file; the input and, if it is a
directory, the files inside it; the output and, if it is a directory, the files
inside it; the work directory and the files inside it; and any file in which
your own tool environment saves your own command output. In the tools directory
you may run `scripts/digitize_figure.py` and `scripts/validate_row_detail.py`;
do not open, list or search anything else there or anywhere else. Put every
file you create, other than the output itself, in your work directory. Do not
use any shared scratch or temporary folder: other agents may be working there
at the same time. If you open a path outside this list by mistake, add one line
saying which after the reply your instruction asks for.
