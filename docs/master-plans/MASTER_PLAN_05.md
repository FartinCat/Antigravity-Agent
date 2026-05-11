# MASTER PLAN 05 — Specification-to-Implementation Drift Detection
**Feature:** Automated checker that compares written specs against actual implementation over time
**Priority:** MEDIUM-HIGH — nobody has built this for file-based agent systems
**Estimated effort:** 7–10 days (most complex plan)
**Depends on:** MASTER_PLAN_00 (typed spec format), MASTER_PLAN_03 (project flags)
**Unlocks:** Creates a closed loop between spec writing and implementation quality

---

## Problem Statement

As projects evolve, the specification written in session 1 drifts away from what is
actually built in sessions 3 through 15. Nobody currently tracks this. There is no
"spec compliance score" over time.

Rule 16 (sdd-lifecycle) and Skill 17 (spec-compliance) describe this as aspirational
requirements. Neither provides a mechanism to check compliance after the fact.
The result: developers discover the implementation has diverged from the spec only
during user testing or code review — not during development when it is cheapest to fix.

This plan builds spec_drift.py — a script that reads SPEC_*.md files, extracts
acceptance criteria using keyword matching, searches the codebase for corresponding
implementations and tests, and generates a drift report showing:
  - Which spec requirements have complete implementation
  - Which requirements are partially implemented
  - Which requirements are unimplemented
  - Which implementations exist with no corresponding spec requirement (scope creep)

---

## Architecture Overview

```
SPEC_feature_00.md exists in docs/specs/
        |
        v
spec_drift.py reads the spec and extracts requirements
        |
        v
For each requirement: search codebase for implementation evidence
  - Look for function names, class names, endpoint paths mentioned in spec
  - Look for test names that match the requirement description
  - Look for comments referencing the requirement
        |
        v
Score each requirement: IMPLEMENTED | PARTIAL | MISSING
        |
        v
Scan codebase for implementation WITHOUT spec coverage (scope creep)
        |
        v
Generate docs/audit-reports/SPEC_DRIFT_{NN}.md
        |
        v
Weekly review workflow includes drift report
        |
If drift > 20%: flag as architectural debt
```

---

## Phase 1 — Define the Spec Format Requirements

For drift detection to work, specs must have structured acceptance criteria.
Update `.agent/workflows/13-spec-discovery.md` to enforce this format:

### Step 1.1 — Acceptance Criteria Format Standard

In SPEC files, acceptance criteria must use this format:

```markdown
## Acceptance Criteria

### AC-001: User can register with email and password
- GIVEN: Registration form is submitted with valid email and unique password
- WHEN: User clicks Submit
- THEN: Account is created, verification email is sent, user is redirected to dashboard

### AC-002: Password must meet security requirements
- GIVEN: User enters a password during registration
- WHEN: Password is shorter than 8 characters or lacks special characters
- THEN: Form shows specific validation error, account is not created

### AC-003: Duplicate email registration is rejected
- GIVEN: Email address already exists in the system
- WHEN: User attempts to register with that email
- THEN: Error message shown, no duplicate account created
```

The IDs (AC-001, AC-002) are critical — they allow spec_drift.py to track
individual criteria over time.

### Step 1.2 — Update spec-discovery workflow

In `.agent/workflows/13-spec-discovery.md`, after the existing spec content requirements,
add:

```markdown
### Acceptance Criteria Requirements (MANDATORY)
Every SPEC file MUST have an Acceptance Criteria section with:
1. Each criterion numbered as AC-NNN (AC-001, AC-002, etc.)
2. GIVEN/WHEN/THEN format (or equivalent: "must", "shall", "will")
3. At least 3 acceptance criteria per feature spec
4. Criteria must be testable (observable, measurable outcome)

Without structured AC blocks, spec_drift.py cannot track compliance.
```

---

## Phase 2 — Build the Drift Detection Script

### Step 2.1 — Create .agent/scripts/spec_drift.py

```python
#!/usr/bin/env python3
"""
Antigravity Agent OS — Specification Drift Detector
====================================================
Location: .agent/scripts/spec_drift.py

Compares written specifications against actual implementation to detect drift.
Generates a drift report showing implemented, partial, and missing requirements.

Usage:
  python .agent/scripts/spec_drift.py                          # scan all specs
  python .agent/scripts/spec_drift.py --spec docs/specs/SPEC_auth_00.md
  python .agent/scripts/spec_drift.py --output docs/audit-reports/DRIFT_00.md
  python .agent/scripts/spec_drift.py --threshold 20           # fail if >20% drift
"""
import argparse
import os
import re
import sys
from datetime import datetime
from typing import Optional

BASE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SPECS_DIR = os.path.join(BASE, "docs", "specs")
REPORTS_DIR = os.path.join(BASE, "docs", "audit-reports")

EXCLUDED_DIRS = {".git", ".agent", "node_modules", "__pycache__", ".venv",
                 "archived", "docs", "dist", "build", ".next"}

SOURCE_EXTENSIONS = {
    ".py", ".ts", ".tsx", ".js", ".jsx", ".go", ".rs", ".java", ".cs",
    ".rb", ".php", ".swift", ".kt", ".cpp", ".c", ".h"
}

TEST_PATTERNS = [
    r"test_", r"_test\.", r"\.test\.", r"\.spec\.", r"it\('", r"it\(`",
    r"describe\('", r"def test", r"func Test", r"#\[test\]"
]


class AcceptanceCriterion:
    def __init__(self, criterion_id: str, title: str, body: str):
        self.criterion_id = criterion_id     # AC-001
        self.title = title                   # User can register with email
        self.body = body                     # GIVEN/WHEN/THEN text
        self.keywords = self._extract_keywords()

        # Results filled by drift analysis
        self.implementation_evidence = []   # list of (filepath, line_num, excerpt)
        self.test_evidence = []             # list of (filepath, line_num, excerpt)
        self.status = "MISSING"             # IMPLEMENTED | PARTIAL | MISSING

    def _extract_keywords(self) -> list[str]:
        """Extract searchable keywords from criterion title and body."""
        stop_words = {"the", "a", "an", "is", "are", "was", "will", "with",
                      "that", "this", "for", "and", "or", "not", "when",
                      "then", "given", "should", "must", "can", "user"}
        combined = f"{self.title} {self.body}".lower()
        # Remove punctuation
        combined = re.sub(r"[^\w\s]", " ", combined)
        words = combined.split()
        # Keep meaningful words (length >= 4, not stop words)
        return list({w for w in words if len(w) >= 4 and w not in stop_words})

    def compute_status(self):
        has_impl = len(self.implementation_evidence) > 0
        has_test = len(self.test_evidence) > 0

        if has_impl and has_test:
            self.status = "IMPLEMENTED"
        elif has_impl and not has_test:
            self.status = "PARTIAL"  # impl exists but no test
        elif not has_impl and has_test:
            self.status = "PARTIAL"  # test exists but no impl found
        else:
            self.status = "MISSING"


def extract_criteria_from_spec(spec_path: str) -> list[AcceptanceCriterion]:
    """Parse a SPEC.md file and extract all AC-NNN criteria."""
    with open(spec_path, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read()

    criteria = []

    # Pattern: ### AC-NNN: Title
    ac_pattern = re.compile(
        r"###\s+(AC-\d{3,4}):\s+(.+?)\n((?:(?!###).)*)",
        re.DOTALL
    )

    for match in ac_pattern.finditer(content):
        criterion_id = match.group(1).strip()
        title = match.group(2).strip()
        body = match.group(3).strip()
        criteria.append(AcceptanceCriterion(criterion_id, title, body))

    # Also try simpler formats: "must", "shall", numbered lists
    if not criteria:
        # Fallback: extract bullet points from Acceptance Criteria section
        ac_section_match = re.search(
            r"##\s+Acceptance Criteria\n((?:(?!##).)*)",
            content, re.DOTALL
        )
        if ac_section_match:
            ac_text = ac_section_match.group(1)
            bullet_pattern = re.compile(r"[-*]\s+(.+)")
            for i, match in enumerate(bullet_pattern.finditer(ac_text)):
                criterion_id = f"AC-{i+1:03d}"
                title = match.group(1).strip()
                criteria.append(AcceptanceCriterion(criterion_id, title, ""))

    return criteria


def scan_codebase_for_keywords(keywords: list[str], is_test: bool = False) -> list[tuple]:
    """Search source files for keyword occurrences."""
    evidence = []
    kw_set = {kw.lower() for kw in keywords}

    for root, dirs, files in os.walk(BASE):
        dirs[:] = [d for d in dirs if d not in EXCLUDED_DIRS and not d.startswith(".")]

        for fname in files:
            ext = os.path.splitext(fname)[1].lower()
            if ext not in SOURCE_EXTENSIONS:
                continue

            filepath = os.path.join(root, fname)
            rel_path = os.path.relpath(filepath, BASE).replace("\\", "/")

            # Filter for test/impl files
            is_test_file = any(re.search(p, rel_path) for p in TEST_PATTERNS)
            if is_test != is_test_file:
                continue

            try:
                with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
                    lines = f.readlines()
            except OSError:
                continue

            for line_num, line in enumerate(lines, 1):
                line_lower = line.lower()
                matches = [kw for kw in kw_set if kw in line_lower]
                if len(matches) >= 2:  # Require at least 2 keyword matches
                    evidence.append((rel_path, line_num, line.strip()[:100]))
                    if len(evidence) >= 5:  # Cap evidence per criterion
                        return evidence

    return evidence


def find_undocumented_features(all_criteria: list[AcceptanceCriterion]) -> list[dict]:
    """
    Find source code patterns that have no corresponding spec criteria.
    This detects scope creep — implementation without specification.
    """
    spec_keywords = set()
    for criterion in all_criteria:
        spec_keywords.update(criterion.keywords)

    undocumented = []
    function_pattern = re.compile(
        r"(?:def |function |func |async function |public |private )"
        r"([a-zA-Z_][a-zA-Z0-9_]{4,})\s*\(",
        re.MULTILINE
    )

    for root, dirs, files in os.walk(BASE):
        dirs[:] = [d for d in dirs if d not in EXCLUDED_DIRS and not d.startswith(".")]

        for fname in files:
            ext = os.path.splitext(fname)[1].lower()
            if ext not in SOURCE_EXTENSIONS:
                continue

            rel_path = os.path.relpath(os.path.join(root, fname), BASE).replace("\\", "/")

            # Skip test files for scope creep check
            if any(re.search(p, rel_path) for p in TEST_PATTERNS):
                continue

            try:
                with open(os.path.join(root, fname), "r", encoding="utf-8", errors="ignore") as f:
                    content = f.read()
            except OSError:
                continue

            for match in function_pattern.finditer(content):
                func_name = match.group(1).lower()
                func_words = re.findall(r"[a-z]+", func_name)  # split camelCase
                func_words = [w for w in func_words if len(w) >= 4]

                # Check if this function name has any keywords in the spec
                if func_words and not any(w in spec_keywords for w in func_words):
                    undocumented.append({
                        "file": rel_path,
                        "function": match.group(1),
                        "words": func_words
                    })

    return undocumented[:20]  # Return top 20


def analyze_spec(spec_path: str) -> dict:
    """Full drift analysis for one spec file."""
    print(f"Analyzing: {os.path.basename(spec_path)}")
    criteria = extract_criteria_from_spec(spec_path)

    if not criteria:
        return {
            "spec": spec_path,
            "error": "No acceptance criteria found. Add AC-NNN format criteria.",
            "criteria": []
        }

    print(f"  Found {len(criteria)} acceptance criteria")

    for criterion in criteria:
        print(f"  Checking {criterion.criterion_id}: {criterion.title[:40]}...")
        criterion.implementation_evidence = scan_codebase_for_keywords(
            criterion.keywords, is_test=False
        )
        criterion.test_evidence = scan_codebase_for_keywords(
            criterion.keywords, is_test=True
        )
        criterion.compute_status()

    implemented = sum(1 for c in criteria if c.status == "IMPLEMENTED")
    partial = sum(1 for c in criteria if c.status == "PARTIAL")
    missing = sum(1 for c in criteria if c.status == "MISSING")

    drift_pct = ((partial * 0.5 + missing) / len(criteria) * 100) if criteria else 0

    return {
        "spec": os.path.basename(spec_path),
        "analyzed_at": datetime.utcnow().isoformat(),
        "total_criteria": len(criteria),
        "implemented": implemented,
        "partial": partial,
        "missing": missing,
        "drift_percentage": round(drift_pct, 1),
        "health": "GREEN" if drift_pct < 10 else ("YELLOW" if drift_pct < 30 else "RED"),
        "criteria": criteria
    }


def generate_report(analyses: list[dict], undocumented: list[dict]) -> str:
    """Generate a markdown drift report."""
    lines = [
        "# Specification Drift Report",
        f"**Generated:** {datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}",
        ""
    ]

    # Summary table
    lines.append("## Spec Health Summary")
    lines.append("")
    lines.append("| Spec | Total | Implemented | Partial | Missing | Drift | Health |")
    lines.append("|---|---|---|---|---|---|---|")

    for a in analyses:
        if "error" in a:
            lines.append(f"| {a['spec']} | — | — | — | — | ERROR | ⚠️ |")
            continue
        health_emoji = {"GREEN": "🟢", "YELLOW": "🟡", "RED": "🔴"}.get(a["health"], "⚪")
        lines.append(
            f"| {a['spec']} | {a['total_criteria']} | {a['implemented']} | "
            f"{a['partial']} | {a['missing']} | {a['drift_percentage']}% | "
            f"{health_emoji} {a['health']} |"
        )

    # Detailed findings per spec
    for analysis in analyses:
        if "error" in analysis:
            lines.extend(["", f"## {analysis['spec']}", f"ERROR: {analysis['error']}"])
            continue

        lines.extend(["", f"## {analysis['spec']}", ""])

        # Missing criteria
        missing_criteria = [c for c in analysis["criteria"] if c.status == "MISSING"]
        if missing_criteria:
            lines.append("### Missing Implementation")
            for c in missing_criteria:
                lines.append(f"- **{c.criterion_id}**: {c.title}")

        # Partial criteria
        partial_criteria = [c for c in analysis["criteria"] if c.status == "PARTIAL"]
        if partial_criteria:
            lines.append("### Partially Implemented (needs tests or implementation)")
            for c in partial_criteria:
                has = "impl" if c.implementation_evidence else "tests"
                lacks = "tests" if c.implementation_evidence else "impl"
                lines.append(f"- **{c.criterion_id}**: {c.title} — has {has}, missing {lacks}")

        # Implemented criteria
        impl_criteria = [c for c in analysis["criteria"] if c.status == "IMPLEMENTED"]
        if impl_criteria:
            lines.append(f"### Implemented ({len(impl_criteria)} criteria) ✓")
            for c in impl_criteria:
                lines.append(f"- **{c.criterion_id}**: {c.title}")

    # Scope creep section
    if undocumented:
        lines.extend(["", "## Potential Scope Creep (Implementation Without Spec)", ""])
        lines.append("These functions were found in the codebase but have no corresponding")
        lines.append("acceptance criteria. Consider adding AC entries or removing them.")
        lines.append("")
        for item in undocumented[:10]:
            lines.append(f"- `{item['function']}()` in `{item['file']}`")

    # Recommendations
    all_drift = [a["drift_percentage"] for a in analyses if "error" not in a]
    avg_drift = sum(all_drift) / len(all_drift) if all_drift else 0

    lines.extend(["", "## Recommendations", ""])
    if avg_drift > 30:
        lines.append("🔴 **CRITICAL**: Average drift is >30%. Run /spec to update specifications.")
    elif avg_drift > 10:
        lines.append("🟡 **WARNING**: Average drift is >10%. Review partial implementations.")
    else:
        lines.append("🟢 **HEALTHY**: Spec compliance is good. Continue spec-first development.")

    if undocumented:
        lines.append(f"⚠️  **SCOPE CREEP**: {len(undocumented)} undocumented functions found.")

    return "\n".join(lines)


def get_next_report_number() -> str:
    os.makedirs(REPORTS_DIR, exist_ok=True)
    existing = [f for f in os.listdir(REPORTS_DIR) if f.startswith("SPEC_DRIFT_")]
    return f"{len(existing):02d}"


def main():
    parser = argparse.ArgumentParser(description="Spec Drift Detector")
    parser.add_argument("--spec", help="Path to specific spec file")
    parser.add_argument("--output", help="Output report path")
    parser.add_argument("--threshold", type=float, default=0,
                        help="Exit with error if drift exceeds this percentage")
    args = parser.parse_args()

    # Find spec files
    if args.spec:
        spec_files = [args.spec] if os.path.exists(args.spec) else []
    else:
        spec_files = []
        if os.path.exists(SPECS_DIR):
            for fname in os.listdir(SPECS_DIR):
                if fname.endswith(".md"):
                    spec_files.append(os.path.join(SPECS_DIR, fname))

    if not spec_files:
        print("No spec files found. Create specs in docs/specs/ using /spec command.")
        sys.exit(0)

    # Run analysis
    analyses = [analyze_spec(spec) for spec in spec_files]

    # Find undocumented features
    all_criteria = []
    for a in analyses:
        if "criteria" in a and isinstance(a["criteria"], list):
            all_criteria.extend(a["criteria"])

    print("Scanning for undocumented features...")
    undocumented = find_undocumented_features(all_criteria)

    # Generate report
    report = generate_report(analyses, undocumented)

    # Write output
    output_path = args.output or os.path.join(
        REPORTS_DIR, f"SPEC_DRIFT_{get_next_report_number()}.md"
    )
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(report)

    print(f"\nReport written: {output_path}")

    # Exit code for CI integration
    if args.threshold > 0:
        all_drifts = [a["drift_percentage"] for a in analyses if "error" not in a]
        max_drift = max(all_drifts) if all_drifts else 0
        if max_drift > args.threshold:
            print(f"FAIL: Max drift {max_drift}% exceeds threshold {args.threshold}%")
            sys.exit(1)


if __name__ == "__main__":
    main()
```

---

## Phase 3 — Create the /spec-drift Command

Create `.claude/commands/spec-drift.md`:

```markdown
---
description: Detect drift between written specifications and actual implementation
---

Run the specification drift detector across all specs in docs/specs/.

Execution:
  python .agent/scripts/spec_drift.py

For a single spec:
  python .agent/scripts/spec_drift.py --spec docs/specs/SPEC_{feature}_00.md

For CI/CD integration (fail if >20% drift):
  python .agent/scripts/spec_drift.py --threshold 20

After running, read the generated report in docs/audit-reports/SPEC_DRIFT_{NN}.md
and report to the user:
  - Overall health: GREEN/YELLOW/RED
  - Number of MISSING criteria
  - Number of PARTIAL criteria (has impl OR tests but not both)
  - Any scope creep detected

If MISSING criteria found:
  "ACTION: [N] requirements have no implementation. Run /impl to address them."

If drift > 30%:
  "ACTION: Specification is significantly out of sync. Run /spec to update the spec
   OR prioritize implementing the missing criteria."
```

---

## Phase 4 — Integrate Into Workflows

### Step 4.1 — Update .agent/workflows/20-weekly-review.md

Add:

```markdown
### Step N — Spec Drift Analysis
Run drift detection for all specs:

  python .agent/scripts/spec_drift.py

Include in weekly review output:
- Spec health table (GREEN/YELLOW/RED per spec)
- Count of missing requirements
- Any scope creep detected

If drift > 20% on any spec:
  "PRIORITY ACTION: [spec name] has drifted significantly from its implementation."
```

### Step 4.2 — Update .agent/workflows/11-release-project.md

Add as a pre-release gate:

```markdown
### Step N — Spec Compliance Gate (pre-release)
Before finalizing any release:

  python .agent/scripts/spec_drift.py --threshold 15

If exit code is non-zero: BLOCK the release.
"RELEASE BLOCKED: Specification drift exceeds 15%. All AC criteria must be
 implemented and tested before release."
```

---

## Verification

```bash
# 1. Create a test spec with proper AC format
cat > docs/specs/SPEC_test_drift_00.md << 'EOF'
# Test Spec

## Acceptance Criteria

### AC-001: User can login with email and password
- GIVEN: Login form with valid credentials
- WHEN: User submits form
- THEN: User is redirected to dashboard

### AC-002: Invalid password shows error
- GIVEN: Login form with wrong password
- WHEN: User submits form
- THEN: Error message displayed
EOF

# 2. Run drift detection
python .agent/scripts/spec_drift.py --spec docs/specs/SPEC_test_drift_00.md

# 3. Check report was generated
ls docs/audit-reports/SPEC_DRIFT_*.md

# 4. Test threshold enforcement
python .agent/scripts/spec_drift.py --threshold 0  # Should fail (0% allowed drift)
echo "Exit code: $?"
```

---

## Expected Outputs

| File | Status |
|---|---|
| `.agent/scripts/spec_drift.py` | NEW |
| `.claude/commands/spec-drift.md` | NEW |
| `.agent/workflows/20-weekly-review.md` | UPDATED |
| `.agent/workflows/11-release-project.md` | UPDATED |
| `.agent/workflows/13-spec-discovery.md` | UPDATED (AC-NNN format required) |

---

## Learning Resources
- Python re module (regex): https://docs.python.org/3/library/re.html
- Requirements traceability: search "requirements traceability matrix" on Wikipedia
- sentence-transformers (upgrade from keyword matching): https://sbert.net/
- spaCy NLP library: https://spacy.io/
- ICSE traceability papers: search "automated software traceability" on Google Scholar
