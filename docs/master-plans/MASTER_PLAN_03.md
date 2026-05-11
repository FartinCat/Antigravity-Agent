# MASTER PLAN 03 — Conditional Workflow Composition Engine
**Feature:** DAG-based workflow branching that activates conditional steps based on project analysis
**Priority:** HIGH — transforms flat linear pipelines into intelligent adaptive workflows
**Estimated effort:** 6–8 days
**Depends on:** MASTER_PLAN_00 (typed scanner output feeds the flag system)
**Unlocks:** Plan 06 (caching uses flags), Plan 09 (DNA fingerprinting uses flags)

---

## Problem Statement

Every workflow in Antigravity is a fixed linear pipeline. Spec-discovery runs the same
six steps whether you are building a login page or a nuclear plant monitoring system.
The security-auditor is only invoked if you manually run /ship — not automatically when
the scanner detects authentication code. The build-website workflow has no idea whether
the project handles payments and therefore needs PCI compliance checks.

The real world requires conditional logic: IF the project has authentication code THEN
automatically activate security hardening. IF the spec mentions database migrations THEN
queue the api-design skill before implementation. IF the task is frontend-only THEN skip
backend quality gates.

LangGraph (Python) solves this with actual graph execution. This plan solves it
within Antigravity's file-based architecture using a flags system and a composition engine.

---

## Architecture Overview

```
/scanner runs
        |
        v
Scanner emits project_flags.json
(e.g. HAS_AUTH, HAS_PAYMENTS, IS_FRONTEND_ONLY, HAS_CONCURRENCY)
        |
        v
workflow_composer.py reads project_flags.json
        |
        v
For each active workflow:
  - Reads the workflow's [COMPOSITION] block
  - Checks which flags are set
  - Injects conditional steps into the workflow at runtime
        |
        v
Modified workflow runs with injected steps
        |
        v
After workflow completes: project_flags.json updated
```

---

## Phase 1 — Define the Flag System

### Step 1.1 — Create .agent/schemas/project-flags.schema.json

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "$id": "project-flags",
  "type": "object",
  "properties": {
    "generated_at": { "type": "string", "format": "date-time" },
    "project_root": { "type": "string" },
    "flags": {
      "type": "object",
      "properties": {
        "HAS_AUTH":           { "type": "boolean", "description": "Auth/session/JWT/OAuth code detected" },
        "HAS_PAYMENTS":       { "type": "boolean", "description": "Payment processing code detected" },
        "HAS_DB":             { "type": "boolean", "description": "Database migrations or schema files" },
        "HAS_DB_MIGRATIONS":  { "type": "boolean", "description": "Migration files specifically (alembic, flyway, etc)" },
        "HAS_CONCURRENCY":    { "type": "boolean", "description": "Async/parallel/threading patterns" },
        "HAS_EXTERNAL_API":   { "type": "boolean", "description": "Third-party API integrations" },
        "HAS_FILE_UPLOAD":    { "type": "boolean", "description": "File upload handling" },
        "HAS_WEBSOCKETS":     { "type": "boolean", "description": "Real-time WebSocket connections" },
        "IS_FRONTEND_ONLY":   { "type": "boolean", "description": "No backend files detected" },
        "IS_BACKEND_ONLY":    { "type": "boolean", "description": "No frontend files detected" },
        "IS_FULLSTACK":       { "type": "boolean", "description": "Both frontend and backend present" },
        "IS_CLI_TOOL":        { "type": "boolean", "description": "Command-line tool (no web server)" },
        "IS_LIBRARY":         { "type": "boolean", "description": "Library/package (no main executable)" },
        "IS_SECURITY_SENSITIVE": { "type": "boolean", "description": "Any of: HAS_AUTH, HAS_PAYMENTS, HAS_FILE_UPLOAD" },
        "REQUIRES_COMPLIANCE":   { "type": "boolean", "description": "GDPR/HIPAA/PCI indicators found" },
        "HAS_TESTS":          { "type": "boolean", "description": "Test files exist" },
        "HAS_CI":             { "type": "boolean", "description": "CI configuration found" },
        "HAS_DOCKER":         { "type": "boolean", "description": "Dockerfile or docker-compose found" },
        "IS_MONOREPO":        { "type": "boolean", "description": "Multiple package.json or pyproject.toml found" }
      }
    },
    "tech_stack": {
      "type": "object",
      "properties": {
        "languages":   { "type": "array", "items": { "type": "string" } },
        "frameworks":  { "type": "array", "items": { "type": "string" } },
        "databases":   { "type": "array", "items": { "type": "string" } },
        "runtime":     { "type": "string" }
      }
    },
    "file_counts": {
      "type": "object",
      "properties": {
        "total":      { "type": "integer" },
        "source":     { "type": "integer" },
        "test":       { "type": "integer" },
        "config":     { "type": "integer" }
      }
    }
  }
}
```

### Step 1.2 — Flag Detection Rules

Document how each flag is detected in `.agent/rules/23-workflow-composition.md`:

```markdown
## Flag Detection Keywords

HAS_AUTH: any file contains: "jwt", "oauth", "session", "bearer", "authenticate",
  "bcrypt", "passport", "auth0", "login", "signup", "token", "refresh_token"

HAS_PAYMENTS: any file contains: "stripe", "paypal", "checkout", "payment",
  "invoice", "billing", "subscription", "pci", "card_number", "amount"

HAS_DB: any file matches: **/migrations/**, schema.sql, *.prisma, models.py,
  entity/*.ts, @Entity, CREATE TABLE, alembic, flyway, db.migrate

HAS_CONCURRENCY: any file contains: "async ", "await ", "Promise", "goroutine",
  "threading", "multiprocessing", "concurrent", "asyncio", "tokio"

HAS_EXTERNAL_API: any file contains: "fetch(", "axios", "requests.get",
  "httpx", "webhook", "api_key", "base_url"

HAS_FILE_UPLOAD: any file contains: "multer", "formData", "multipart",
  "UploadFile", "s3.upload", "file.save"

IS_SECURITY_SENSITIVE: automatically TRUE if any of HAS_AUTH, HAS_PAYMENTS,
  HAS_FILE_UPLOAD are TRUE

IS_FRONTEND_ONLY: no files in: src/api/, server/, backend/, app.py, main.go,
  server.ts — AND has: index.html, App.tsx, or *.vue files

HAS_TESTS: any directory matches: tests/, test/, __tests__/, spec/, *.test.*,
  *.spec.*
```

---

## Phase 2 — Build the Flag Scanner

### Step 2.1 — Create .agent/scripts/flag_scanner.py

```python
#!/usr/bin/env python3
"""
Antigravity Agent OS — Project Flag Scanner
==========================================
Location: .agent/scripts/flag_scanner.py

Scans the project and emits a project_flags.json that drives
conditional workflow composition.

Usage:
  python .agent/scripts/flag_scanner.py
  python .agent/scripts/flag_scanner.py --output .agent/data/project_flags.json
  python .agent/scripts/flag_scanner.py --flag HAS_AUTH  # check single flag
"""
import argparse
import json
import os
import re
from datetime import datetime

BASE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUTPUT_PATH = os.path.join(BASE, ".agent", "data", "project_flags.json")

EXCLUDED_DIRS = {".git", ".agent", "node_modules", "__pycache__", ".venv",
                 "venv", "dist", "build", ".next", "target", "archived"}

# Flag detection keyword maps
FLAG_KEYWORDS = {
    "HAS_AUTH": [
        "jwt", "oauth", "bearer", "authenticate", "bcrypt", "passport",
        "auth0", "refresh_token", "login_required", "session_start", "pyjwt"
    ],
    "HAS_PAYMENTS": [
        "stripe", "paypal", "checkout", "payment_intent", "invoice",
        "billing", "pci", "card_number", "stripe.create"
    ],
    "HAS_CONCURRENCY": [
        "goroutine", "threading.Thread", "multiprocessing", "asyncio.gather",
        "Promise.all", "concurrent.futures", "tokio::spawn"
    ],
    "HAS_EXTERNAL_API": [
        "api_key", "base_url", "webhook", "requests.get", "requests.post",
        "axios.get", "fetch("
    ],
    "HAS_FILE_UPLOAD": [
        "multer", "UploadFile", "s3.upload", "multipart/form-data",
        "file.save", "shutil.move"
    ],
    "HAS_WEBSOCKETS": [
        "websocket", "socket.io", "ws://", "wss://", "on('message'",
        "emit(", "broadcast("
    ],
    "REQUIRES_COMPLIANCE": [
        "gdpr", "hipaa", "pci", "data_retention", "right_to_erasure",
        "data_subject", "phi", "pii_field"
    ],
}

FLAG_FILE_PATTERNS = {
    "HAS_DB": [
        r"migrations?/.*\.sql$", r"schema\.sql$", r"\.prisma$",
        r"alembic\.ini$", r"flyway\.conf$", r"V\d+__.*\.sql$"
    ],
    "HAS_CI": [
        r"\.github/workflows/.*\.ya?ml$", r"\.gitlab-ci\.yml$",
        r"Jenkinsfile$", r"\.circleci/config\.yml$", r"azure-pipelines\.yml$"
    ],
    "HAS_DOCKER": [
        r"Dockerfile$", r"docker-compose\.ya?ml$", r"\.dockerignore$"
    ],
}

LANGUAGE_EXTENSIONS = {
    "python":     [".py"],
    "typescript": [".ts", ".tsx"],
    "javascript": [".js", ".jsx", ".mjs"],
    "go":         [".go"],
    "rust":       [".rs"],
    "java":       [".java"],
    "csharp":     [".cs"],
    "cpp":        [".cpp", ".cc", ".cxx"],
    "ruby":       [".rb"],
    "php":        [".php"],
}

FRAMEWORK_INDICATORS = {
    "react":    ["react-dom", "jsx", "useState", "useEffect"],
    "vue":      ["vue-router", "defineComponent", "<template>"],
    "svelte":   ["SvelteKit", ".svelte"],
    "fastapi":  ["FastAPI", "from fastapi"],
    "django":   ["django.db", "from django"],
    "express":  ["express()", "app.use("],
    "nextjs":   ["next/head", "getStaticProps", "next.config"],
    "nestjs":   ["@Module", "@Controller", "@Injectable"],
    "gin":      ["gin.Default()", "gin.Context"],
    "axum":     ["axum::Router", "axum::extract"],
}


def walk_project(base: str):
    """Walk project files, excluding irrelevant directories."""
    for root, dirs, files in os.walk(base):
        dirs[:] = [d for d in dirs if d not in EXCLUDED_DIRS and not d.startswith(".")]
        for fname in files:
            yield os.path.join(root, fname)


def scan() -> dict:
    flags = {k: False for k in list(FLAG_KEYWORDS.keys()) + list(FLAG_FILE_PATTERNS.keys())}
    flags.update({
        "HAS_TESTS": False, "IS_FRONTEND_ONLY": False, "IS_BACKEND_ONLY": False,
        "IS_FULLSTACK": False, "IS_CLI_TOOL": False, "IS_LIBRARY": False,
        "IS_SECURITY_SENSITIVE": False, "IS_MONOREPO": False, "HAS_DB_MIGRATIONS": False,
    })

    lang_counts = {k: 0 for k in LANGUAGE_EXTENSIONS}
    framework_hits = {k: 0 for k in FRAMEWORK_INDICATORS}
    total_files = source_files = test_files = config_files = 0
    package_json_count = pyproject_count = 0
    has_frontend = has_backend = False

    for filepath in walk_project(BASE):
        rel = os.path.relpath(filepath, BASE).replace("\\", "/")
        ext = os.path.splitext(filepath)[1].lower()
        total_files += 1

        # Language counting
        for lang, exts in LANGUAGE_EXTENSIONS.items():
            if ext in exts:
                lang_counts[lang] += 1
                source_files += 1

        # Test detection
        if any(p in rel for p in ["/test/", "/tests/", "/__tests__/", "/spec/"]) \
           or any(rel.endswith(s) for s in [".test.ts", ".test.js", ".spec.py", "_test.go"]):
            flags["HAS_TESTS"] = True
            test_files += 1

        # Config detection
        if ext in [".json", ".yaml", ".yml", ".toml", ".ini", ".env"]:
            config_files += 1

        # Monorepo detection
        if rel.endswith("package.json") and rel.count("/") == 1:
            package_json_count += 1
        if rel.endswith("pyproject.toml"):
            pyproject_count += 1

        # File pattern flags
        for flag, patterns in FLAG_FILE_PATTERNS.items():
            if any(re.search(p, rel) for p in patterns):
                flags[flag] = True
                if flag == "HAS_DB" and "migration" in rel.lower():
                    flags["HAS_DB_MIGRATIONS"] = True

        # Frontend / backend detection
        if ext in [".tsx", ".jsx", ".vue", ".svelte"] or "components/" in rel:
            has_frontend = True
        if any(p in rel for p in ["server/", "api/", "backend/", "app.py",
                                    "main.go", "server.ts", "server.js"]):
            has_backend = True

        # Keyword scanning (skip large files and binaries)
        try:
            if os.path.getsize(filepath) > 500_000:  # skip >500KB
                continue
            with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read().lower()

            for flag, keywords in FLAG_KEYWORDS.items():
                if not flags[flag] and any(kw in content for kw in keywords):
                    flags[flag] = True

            for fw, indicators in FRAMEWORK_INDICATORS.items():
                if any(ind.lower() in content for ind in indicators):
                    framework_hits[fw] += 1

        except (OSError, PermissionError):
            continue

    # Derived flags
    flags["IS_SECURITY_SENSITIVE"] = flags["HAS_AUTH"] or flags["HAS_PAYMENTS"] or flags["HAS_FILE_UPLOAD"]
    flags["IS_FRONTEND_ONLY"] = has_frontend and not has_backend
    flags["IS_BACKEND_ONLY"] = has_backend and not has_frontend
    flags["IS_FULLSTACK"] = has_frontend and has_backend
    flags["IS_MONOREPO"] = package_json_count > 2 or pyproject_count > 1

    # Tech stack
    languages = [lang for lang, cnt in lang_counts.items() if cnt > 0]
    frameworks = [fw for fw, cnt in framework_hits.items() if cnt > 0]

    return {
        "generated_at": datetime.utcnow().isoformat(),
        "project_root": BASE,
        "flags": flags,
        "tech_stack": {
            "languages": languages,
            "frameworks": frameworks,
            "databases": [],  # populated from DB flag + content analysis
            "runtime": "node" if lang_counts["typescript"] > lang_counts["python"] else "python"
        },
        "file_counts": {
            "total": total_files,
            "source": source_files,
            "test": test_files,
            "config": config_files
        }
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default=OUTPUT_PATH)
    parser.add_argument("--flag", help="Check a single flag value")
    parser.add_argument("--quiet", action="store_true")
    args = parser.parse_args()

    result = scan()

    if args.flag:
        val = result["flags"].get(args.flag, "UNKNOWN")
        print(f"{args.flag}: {val}")
        return

    os.makedirs(os.path.dirname(args.output), exist_ok=True)
    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2)

    if not args.quiet:
        print(f"Project flags written to: {args.output}")
        print(f"Tech stack: {result['tech_stack']['languages']}")
        print(f"Frameworks: {result['tech_stack']['frameworks']}")
        print("Active flags:")
        for flag, val in result["flags"].items():
            if val:
                print(f"  [x] {flag}")


if __name__ == "__main__":
    main()
```

---

## Phase 3 — Build the Workflow Composer

### Step 3.1 — Create .agent/scripts/workflow_composer.py

```python
#!/usr/bin/env python3
"""
Antigravity Agent OS — Workflow Composer
=========================================
Location: .agent/scripts/workflow_composer.py

Reads project flags and injects conditional steps into workflows.
Prints the composed workflow to stdout for the agent to follow.

Usage:
  python .agent/scripts/workflow_composer.py --workflow 16-feature-development
  python .agent/scripts/workflow_composer.py --workflow 13-spec-discovery
"""
import argparse
import json
import os
import sys

BASE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
FLAGS_PATH = os.path.join(BASE, ".agent", "data", "project_flags.json")
WORKFLOWS_DIR = os.path.join(BASE, ".agent", "workflows")

# Conditional injections: {flag: {workflow: [steps_to_inject]}}
CONDITIONAL_STEPS = {
    "IS_SECURITY_SENSITIVE": {
        "13-spec-discovery": [
            "### [INJECTED] Security Spec Review\n"
            "Because IS_SECURITY_SENSITIVE is set:\n"
            "1. Add a Security Considerations section to SPEC.md\n"
            "2. List: authentication method, authorization model, data sensitivity level\n"
            "3. Invoke security-auditor persona to review the spec before proceeding to /plan\n"
        ],
        "16-feature-development": [
            "### [INJECTED] Security Gate\n"
            "Because IS_SECURITY_SENSITIVE is set:\n"
            "1. After /impl completes: run security-auditor on all new files\n"
            "2. If any CRITICAL/HIGH findings: fix before proceeding to /ship\n"
            "3. Add security test cases to the test plan\n"
        ],
    },
    "HAS_PAYMENTS": {
        "13-spec-discovery": [
            "### [INJECTED] Payment Compliance Check\n"
            "Because HAS_PAYMENTS is set:\n"
            "1. Spec must include: PCI DSS scope assessment\n"
            "2. Document: which card data is handled? Stored? Transmitted?\n"
            "3. Confirm: using Stripe/PayPal tokenization (never store raw card numbers)\n"
            "4. Activate commercial-quality-standard instinct for all payment code\n"
        ],
    },
    "HAS_DB_MIGRATIONS": {
        "16-feature-development": [
            "### [INJECTED] Migration Safety Protocol\n"
            "Because HAS_DB_MIGRATIONS is set:\n"
            "1. Before implementing: check for backward-incompatible schema changes\n"
            "2. Any column removal or rename must have a deprecation period\n"
            "3. All migrations must have a rollback script\n"
            "4. Test migration against a production data snapshot (anonymized)\n"
        ],
    },
    "HAS_CONCURRENCY": {
        "16-feature-development": [
            "### [INJECTED] Concurrency Hazard Check\n"
            "Because HAS_CONCURRENCY is set:\n"
            "1. After /impl: run test-engineer with race condition focus\n"
            "2. Check: are shared resources protected by locks/mutexes?\n"
            "3. Check: are goroutines/threads properly terminated?\n"
            "4. Activate INSTINCT-006 (RACE_WINDOW_TOCTOU) for all concurrent code\n"
        ],
    },
    "HAS_FILE_UPLOAD": {
        "13-spec-discovery": [
            "### [INJECTED] File Upload Security Spec\n"
            "Because HAS_FILE_UPLOAD is set:\n"
            "1. Spec must include: allowed MIME types, max file size, storage location\n"
            "2. Confirm: virus scanning or content validation strategy\n"
            "3. Confirm: files are NOT served directly from upload directory\n"
        ],
    },
    "IS_FRONTEND_ONLY": {
        "18-quality-gate": [
            "### [INJECTED] Frontend-Only Quality Gate\n"
            "Because IS_FRONTEND_ONLY is set:\n"
            "Skip: API design checks, database schema validation, backend security\n"
            "Add:  Lighthouse performance audit (LCP, FID, CLS)\n"
            "Add:  Accessibility audit (axe-core or similar)\n"
            "Add:  Bundle size check (warn >250KB, fail >500KB gzipped)\n"
        ],
    },
}


def load_flags() -> dict:
    if not os.path.exists(FLAGS_PATH):
        return {}
    with open(FLAGS_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data.get("flags", {})


def load_workflow(workflow_name: str) -> str:
    # Try exact name first
    path = os.path.join(WORKFLOWS_DIR, f"{workflow_name}.md")
    if not os.path.exists(path):
        # Try searching by partial name
        for fname in os.listdir(WORKFLOWS_DIR):
            if workflow_name in fname:
                path = os.path.join(WORKFLOWS_DIR, fname)
                break
    if not os.path.exists(path):
        print(f"ERROR: Workflow not found: {workflow_name}")
        sys.exit(1)
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def compose(workflow_name: str) -> str:
    flags = load_flags()
    base_workflow = load_workflow(workflow_name)

    injections = []
    for flag, flag_val in flags.items():
        if not flag_val:
            continue
        if flag in CONDITIONAL_STEPS:
            for wf_pattern, steps in CONDITIONAL_STEPS[flag].items():
                if wf_pattern in workflow_name:
                    injections.extend(steps)

    if not injections:
        return base_workflow

    injection_block = "\n\n---\n## Conditionally Injected Steps\n\n"
    injection_block += "\n".join(injections)

    print(f"[COMPOSER] Injected {len(injections)} conditional step(s) based on flags: "
          f"{[f for f, v in flags.items() if v]}")

    return base_workflow + injection_block


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--workflow", required=True, help="Workflow name (e.g. 16-feature-development)")
    parser.add_argument("--flags-only", action="store_true", help="Just print active flags")
    args = parser.parse_args()

    if args.flags_only:
        flags = load_flags()
        active = [f for f, v in flags.items() if v]
        print("Active project flags:", active)
        return

    composed = compose(args.workflow)
    print(composed)


if __name__ == "__main__":
    main()
```

---

## Phase 4 — Create Rule 23

Create `.agent/rules/23-workflow-composition.md`:

```markdown
---
rule: 23-workflow-composition
priority: HIGH
---
# Rule 23: Conditional Workflow Composition

## The Law
Workflows adapt to project context. Before executing any major workflow,
check project_flags.json and inject conditional steps for active flags.

## How It Works
1. /scanner runs flag_scanner.py — emits .agent/data/project_flags.json
2. Any workflow invocation checks: python .agent/scripts/workflow_composer.py --workflow [name]
3. If project flags are set, additional steps are automatically appended
4. The agent follows the composed (base + injected) workflow

## Flag Priority
IS_SECURITY_SENSITIVE → always activates security-auditor at spec AND impl stages
HAS_PAYMENTS → activates PCI compliance checks at spec stage
HAS_DB_MIGRATIONS → activates rollback protocol at implementation stage
HAS_CONCURRENCY → activates race condition checks at test stage
HAS_FILE_UPLOAD → activates upload security spec requirements
IS_FRONTEND_ONLY → replaces backend quality gates with frontend-specific checks

## Enforcement
Before running any workflow listed in CONDITIONAL_STEPS:
  python .agent/scripts/workflow_composer.py --workflow [workflow-name]
Follow the composed output, not the raw workflow file.

If project_flags.json does not exist: run /scanner first.
```

---

## Phase 5 — Update Scanner to Emit Flags

### Step 5.1 — Update .agent/workflows/01-scanner.md

After Step 6g (existing final detection step), add:

```markdown
### Step 7 — Emit Project Flags
Run the flag scanner:

  python .agent/scripts/flag_scanner.py --output .agent/data/project_flags.json

Add to the SCAN_REPORT.md output:
## Project Flags
[paste the active flags from the scanner output]

Note for user:
"Project flags have been set. Workflows will now adapt to your project automatically.
 Run: python .agent/scripts/workflow_composer.py --workflow [name] before any pipeline."
```

---

## Verification

```bash
# 1. Run the flag scanner on the current project
python .agent/scripts/flag_scanner.py

# 2. Check a specific flag
python .agent/scripts/flag_scanner.py --flag IS_FRONTEND_ONLY

# 3. Compose a workflow and see injections
python .agent/scripts/workflow_composer.py --workflow 16-feature-development

# 4. Check flags only
python .agent/scripts/workflow_composer.py --workflow 13-spec-discovery --flags-only

# 5. Validate the flags JSON against schema (needs Plan 00 validation script)
python .agent/scripts/validate_output.py --agent project-flags --input .agent/data/project_flags.json
```

---

## Expected Outputs

| File | Status |
|---|---|
| `.agent/schemas/project-flags.schema.json` | NEW |
| `.agent/scripts/flag_scanner.py` | NEW |
| `.agent/scripts/workflow_composer.py` | NEW |
| `.agent/rules/23-workflow-composition.md` | NEW |
| `.agent/data/project_flags.json` | NEW (generated, gitignored) |
| `.agent/workflows/01-scanner.md` | UPDATED |

---

## Learning Resources
- LangGraph (stateful agent workflows): https://github.com/langchain-ai/langgraph
- Directed acyclic graphs: search "DAG workflow execution Python"
- Python re module (for keyword detection): https://docs.python.org/3/library/re.html
- State machines in Python: https://github.com/pytransitions/transitions
