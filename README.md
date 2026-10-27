# Property Bill Automation

A full-stack application developed by **DSD Mighty**, a team from the **Dallas Software Developers 2026 Cohort**.

Property management companies handle hundreds of bills across multiple properties, each with different vendors, due dates, payment methods, and approval requirements.

This project aims to simplify that process by building a system for collecting bills, matching them to the correct properties, detecting duplicates, managing approvals, and tracking payment workflows.

The project will start with traditional software engineering approaches, with AI-powered capabilities introduced in later development phases.

## Technology Stack

**Backend** (`backend/`)

- ⚡ [**FastAPI**](https://fastapi.tiangolo.com/) for the Python backend API.
- 🐍 [**Python**](https://www.python.org/) 3.12+ for backend development.
- 📦 [**uv**](https://docs.astral.sh/uv/) for Python dependency management and locking.
- ✅ [**pytest**](https://docs.pytest.org/) for automated backend tests.
- 🧹 [**Ruff**](https://docs.astral.sh/ruff/) for backend linting and formatting.

**Frontend** (`frontend/`)

- 🖥️ [**Next.js**](https://nextjs.org/) 16 (App Router) with [**React**](https://react.dev/) 19 and strict [**TypeScript**](https://www.typescriptlang.org/).
- 📦 [**pnpm**](https://pnpm.io/) for frontend dependency management.
- 🎨 [**Tailwind CSS**](https://tailwindcss.com/) 4 for styling, with light and dark themes via [next-themes](https://github.com/pacocoursey/next-themes).
- 📝 [**React Hook Form**](https://react-hook-form.com/) and [**Zod**](https://zod.dev/) for forms and validation.
- 🧼 [**Biome**](https://biomejs.dev/) for linting and formatting (replaces ESLint and Prettier).
- 🧪 [**Vitest**](https://vitest.dev/) and Testing Library for frontend tests.

**Tooling**

- 🔄 [**GitHub Actions**](https://docs.github.com/en/actions) for continuous integration.
- 🪝 [**husky**](https://typicode.github.io/husky/) and [lint-staged](https://github.com/lint-staged/lint-staged) for git hooks.
- 📋 `ENFORCEMENT.md` lists every project rule and the mechanism that enforces it; `CLAUDE.md` holds the instructions for coding agents.

## Meet the Team

Built collaboratively by members of the Dallas Software Developers 2026 cohort. 
| Team Member | GitHub | LinkedIn | Portfolio |
| :--- | :--- | :--- | :--- |
| **Kervintz Noel** | [@kervcodes](https://github.com/kervcodes) | [LinkedIn](https://www.linkedin.com/in/kervintznoel/) | [Website](https://kervintznoel.com/) |
| **Member Name** | [GitHub](https://github.com/) | — | — |
| **Member Name** | [GitHub](https://github.com/) | — | — |
| **Member Name** | [GitHub](https://github.com/) | — | — |
| **Member Name** | [GitHub](https://github.com/) | — | — |
| **Member Name** | [GitHub](https://github.com/) | — | — |


## Project Structure

```text
cohort-team-2026-dsd-mighty/
├── .github/
│   └── workflows/        # CI configuration
├── backend/
│   ├── src/
│   │   └── backend/      # FastAPI application package (api/ routers, schemas/)
│   ├── tests/            # Backend tests
│   ├── pyproject.toml    # Project, dependency and Ruff configuration
│   └── uv.lock           # Locked Python dependencies
├── frontend/
│   ├── app/              # Next.js routes (/, /dashboard, /invoices/new), components, lib, providers, types
│   ├── .husky/           # Git hooks
│   ├── scripts/          # Hook helper scripts
│   ├── biome.json        # Biome lint and format configuration
│   ├── package.json      # Frontend scripts and dependencies
│   └── vitest.config.ts  # Vitest configuration
├── scripts/
│   └── check-enforcement.mjs  # Checks that ENFORCEMENT.md is honest
├── CLAUDE.md             # Instructions for coding agents
├── ENFORCEMENT.md        # Rule -> enforcer table
├── .lintstagedrc.json    # Pre-commit checks for the root documents
├── .gitignore
└── README.md
```

## Getting Started

### Prerequisites

Install [Python](https://www.python.org/downloads/) and [uv](https://docs.astral.sh/uv/getting-started/installation/).

### Backend Development

From the repository root:

```bash
cd backend
uv sync
uv run uvicorn backend.app:app --reload
```

Once the server is running:

- **API:** http://127.0.0.1:8000/
- **Interactive API documentation:** http://127.0.0.1:8000/docs
- **Alternative API documentation:** http://127.0.0.1:8000/redoc

### Running Tests

From the `backend/` directory:

```bash
uv --version
uv sync --locked
uv run pytest -v
```

- `uv --version` confirms uv is installed.
- `uv sync --locked` installs dependencies and checks that `uv.lock` matches the project configuration.
- `uv run pytest -v` runs backend tests with detailed results.

**GitHub Actions workflow validation (optional):** Install [actionlint](https://github.com/rhysd/actionlint) using a prebuilt executable or a package manager. Go is not required when using the executable. From the **repository root**, run:

```bash
actionlint .github/workflows/ci.yml
```

No output and an exit code of `0` normally mean actionlint found no errors.

## Frontend Development

### Prerequisites

Install [Node.js](https://nodejs.org/) 22 and [pnpm](https://pnpm.io/installation) 10. [gitleaks](https://github.com/gitleaks/gitleaks) is optional but recommended (the pre-commit hook scans staged changes with it when it is installed).

### Running the app

From the `frontend/` directory:

```bash
cd frontend
pnpm install
pnpm dev
```

`pnpm install` also installs the git hooks (husky). The app runs at http://localhost:3000 with these routes: `/`, `/dashboard` and `/invoices/new`.

### Checks

From the `frontend/` directory:

```bash
pnpm lint              # Biome lint and format check
pnpm format            # Biome: apply fixes and formatting
pnpm run type-check    # next typegen && tsc --noEmit
pnpm test --run        # Vitest, single run (pnpm test watches)
pnpm build             # next build
```

### Commit messages and hooks

Commits must follow `type(scope): description` (for example `feat(invoices): add vendor filter`). Allowed types are `feat`, `fix`, `docs`, `style`, `refactor`, `perf`, `test`, `build`, `ci`, `chore`, `revert` and `init`. On commit, staged frontend files are formatted and fixed by Biome and type-checked, and direct pushes to `main` are blocked. The full list of rules and their enforcers is in [`ENFORCEMENT.md`](./ENFORCEMENT.md).

## Continuous Integration

GitHub Actions configuration lives in [`.github/workflows/`](./.github/workflows/). It runs on pull requests to `main`, on pushes to `main`, and on demand. These jobs run in parallel:

- **Backend (FastAPI + uv):** install locked dependencies, run pytest, `ruff check` and `ruff format --check`.
- **Frontend (Next.js + React):** install dependencies and run the Vitest suite.
- **Frontend Type Check:** `pnpm run type-check`.
- **Frontend Lint:** `pnpm lint` (Biome).
- **Frontend Build:** `pnpm build`.
- **Enforcement Table:** `node scripts/check-enforcement.mjs`, which verifies that every rule in `ENFORCEMENT.md` names an enforcer that exists and that no dated exception has expired.

## Project Status

**In development.** The FastAPI backend has route modules and Pydantic schemas for bills, approvals, vendors, vendor accounts, payments and properties. The frontend has a dashboard and an invoice entry form. Authentication, persistence and AI-powered features are not implemented yet.
