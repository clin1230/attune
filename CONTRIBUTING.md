# Collaboration workflow

- `main`: shared baseline. Merge reviewed pull requests here.
- `feat/mvp-workspace`: application development.
- `docs/product-updates`: PM requirements and documentation updates.

## PM document updates

1. Select `docs/product-updates` on GitHub.
2. Add or edit documents under `docs/`. Keep the product requirements in `docs/PRD.md`.
3. Commit the changes to that branch.
4. Open a pull request into `main`, explaining what changed and whether it affects implementation or acceptance criteria.
5. Merge after review. Update the branch from `main` before the next change.

Use Markdown for requirements where practical. Do not commit confidential credentials, local configuration, generated scenes, render archives, or dependencies.

## Code updates

Work on the feature branch, run `npm run build` and `.venv/bin/python -m unittest discover -s backend -p 'test_*.py'`, then open a pull request into `main`. Reference any related requirements update.

Branch protection and collaborator access are GitHub settings; creating these branches does not configure either automatically.
