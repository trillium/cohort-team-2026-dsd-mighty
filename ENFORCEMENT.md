# Enforcement

Every binding rule names the mechanism that enforces it. `node scripts/check-enforcement.mjs` (pre-commit and CI) verifies that every named file exists and that no rule rests on `convention`, `review` or `audit` alone - those are defects, allowed only as dated exceptions that expire.

Kinds: `structure` (the mistake cannot be written), `lint`, `hook`, `ci`, `test` - then, as defects, `convention`, `review`, `audit`. The ladder runs from `structure` (strongest) to `audit` (weakest); when a rule is broken, build the enforcer at the highest rung that works and add or update its row.

The checker runs by `node` from the repo root because the root has no `package.json`; enforcer cells therefore name file paths rather than `pnpm run` scripts. Git hooks live in `frontend/.husky` (installed by `pnpm install` in `frontend/`, which runs `prepare`).

| Rule | Kind | Enforcer | Exception |
|------|------|----------|-----------|
| Backend tests pass before merge | ci | `.github/workflows/ci.yml` | - |
| Backend is ruff-clean and ruff-formatted | ci | `backend/pyproject.toml`, `.github/workflows/ci.yml` | - |
| Frontend tests (Vitest) pass before merge | ci | `frontend/vitest.config.ts`, `.github/workflows/ci.yml` | - |
| TypeScript strict; frontend types check before merge | ci | `frontend/tsconfig.json`, `.github/workflows/ci.yml` | - |
| Frontend builds before merge | ci | `.github/workflows/ci.yml` | - |
| Every rule above has an enforcer that exists; no exception has expired | ci | `scripts/check-enforcement.mjs`, `.github/workflows/ci.yml` | - |
| Commit messages follow `type(scope): description` | hook | `frontend/.husky/commit-msg` | - |
| No direct pushes to `main` or `master` | hook | `frontend/.husky/pre-push` | - |
| pnpm is the only package manager; no foreign lock files | hook | `frontend/.husky/pre-commit` | - |
| Next.js 16: `proxy.ts`, never `middleware.ts` | hook | `frontend/.husky/pre-commit` | - |
| Staged frontend files are Biome-fixed and type-checked on commit | hook | `frontend/package.json`, `frontend/scripts/tsc-staged.sh` | - |
| No raw emoji in frontend source; use lucide-react | hook | `frontend/scripts/check-no-emoji.mjs` | - |
| `ENFORCEMENT.md` and `CLAUDE.md` are checked on commit | hook | `.lintstagedrc.json`, `scripts/check-enforcement.mjs` | - |
| Biome is the only linter and formatter (no ESLint, no Prettier); lint passes before merge | ci | `frontend/biome.json`, `.github/workflows/ci.yml` | - |
| No literal user-visible text in components | convention | - | 2026-12-31 Biome `noJsxLiterals` runs at warn, not error: literals not yet extracted (14 in 3 files) |
| Required status checks and squash-only merges on `main` | audit | - | 2026-12-31 repository admin settings, not changeable from a PR |
