# Portfolio preparation review — 2026-09-05

## Changes

- Replaced the incomplete README with project scope, screenshot, local startup commands, model restoration instructions and explicit evaluation limitations.
- Converted requirements.txt from UTF-16 to UTF-8 without changing version pins. Dependency installation and compatibility remain unverified.
- Added .gitignore for common credentials, environments and model weights.
- Excluded only the large model weight file from the source deliverable. Restore it from the original submission to run inference. The original upload is preserved.
- Application code, datasets, reports and historical thesis documentation were not modified.

## Verification

All eight Python files passed AST syntax parsing. This is not a runtime test. PyTorch, Transformers and Streamlit are unavailable in the review environment, so no inference or UI execution was performed. Data counts and overlap were computed from the uploaded CSVs; the original sklearn split was reproduced to check overlap.

## Findings

599/1215 held-out rows share normalized text with training; 3/54 separate test rows also occur in training. Whole-dataset evaluation includes training data. Historical metrics must not be presented as proof of independent real-world accuracy. Removing duplicates from the files alone would not repair the already trained model or its metrics; retraining and a clean evaluation are required.

The submitted baseline results exceed DistilBERT on the original held-out split and tie it on the small separate test set. The reports do not substantiate a transformer superiority claim.

The original README had an unclosed code fence and no installation/run instructions. Inference loads weights immediately at import and fails when weights or dependencies are missing. Priority is determined by substring keywords and a confidence threshold. Very long input is truncated to 128 tokens. Training lacks comprehensive RNG seeding. Running baseline training replaces the comparison CSV and removes any existing transformer result until transformer training is rerun.

## Security review scope

The archive filenames contain no .env, private key, signing key or Git history files. Text scans across Python, Markdown, CSV, TXT and JSON found no matches for the checked credential formats, private-key headers, email patterns or quoted sensitive assignments. Manual review of the separate test CSV found generic example requests. This is a limited static review, not a guarantee that every asset is free of personal data or that dependencies are secure. Images and model tensor contents were not audited for privacy; dependency vulnerabilities were not checked. No repository was created and nothing was published.
