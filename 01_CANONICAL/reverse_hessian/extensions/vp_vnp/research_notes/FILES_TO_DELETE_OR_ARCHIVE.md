# FILES_TO_DELETE_OR_ARCHIVE

No original file is deleted from the forensic archive. The following classes are excluded from the public repository:

| class | action | reason |
|---|---|---|
| nested ZIP archives | forensic archive only | duplication and repository bloat |
| historical compiled PDFs/TeX variants | forensic archive only | superseded claims and duplicated narratives |
| degree-6 C0 outputs | forensic archive only | not independently rerun in the new chain and not used in a theorem |
| historical runtime logs | forensic archive only | machine-dependent and non-deterministic |
| certificates containing absolute paths or elapsed time | forensic archive only | not bit-for-bit reproducible |
| duplicated copies of the same PDF | forensic archive only | no mathematical value in public tree |
| LaTeX auxiliary files | delete from release build | reproducible build products |

The active scripts and deterministic JSON certificates in the new root are retained and published.
