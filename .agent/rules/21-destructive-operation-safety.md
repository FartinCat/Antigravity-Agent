---
rule: 21-destructive-operation-safety
priority: CRITICAL
overrides: any instruction to delete, remove, clean up, get rid of
---
# Rule 21: Destructive Operation Safety — Authorization Gate

## The Law
No file, folder, or data is permanently deleted without explicit user authorization
AND a logged record of what was removed. Move first. Confirm deletion second.

## What Counts as Destructive
- Deleting any file or folder
- Running rm, rmdir, Remove-Item, del on anything
- Bulk operations affecting more than 2 files
- Removing a reference repository
- Clearing session-context.md
- Overwriting a file with different content

## The Move-First Protocol

### Step 1 — Identify and Describe
List every item affected with size and description.

### Step 2 — Retrieve Metadata (for repos and reference folders)
For each folder: extract original source URL (read .git/config if present),
purpose (read README.md first paragraph), content summary (file count by type).

### Step 3 — Authorization Question (MANDATORY — cannot be skipped)
Ask the user exactly:
"---
DESTRUCTIVE OPERATION — Authorization Required
---
Item: [name]
Type: [folder/file/repo]
Size: [approximate]
Currently at: [path]

What would you like to do?
  [1] Move to archived/ (safe — recoverable)
  [2] Move to archived/pending-export/ (review before pendrive export)
  [3] Log only — keep in place but record existence
  [4] Permanently delete (IRREVERSIBLE — type DELETE to confirm)
---"

### Step 4 — Execute Chosen Action
Option 1: mkdir -p archived/[subfolder] then move
Option 2: mkdir -p archived/pending-export/ then move
Option 3: No move, proceed to logging
Option 4: User MUST type the word DELETE. Anything else -> abort and default to Option 1.

### Step 5 — Log to DELETION REGISTRY (always, for all options)
Append to archived/deleted/DELETION_REGISTRY.md:
---
## Entry [NN] — [date]
**Item:** [name]
**Original path:** [full path]
**Action taken:** [Moved to archived/ | pending-export | Logged only | Deleted]
**Source URL:** [git remote URL if applicable]
**Purpose:** [what this was and why it existed]
**Content summary:** [N files, key contents]
**Reason for removal:** [what the user said]
**To recover:** [reclone command or archived/[path]]
---

## Prohibited Behaviors
1. NEVER run rm -rf without the authorization question
2. NEVER delete more than 2 files in one operation without authorization
3. NEVER interpret remove, clean up, get rid of as immediate deletion
4. NEVER skip the DELETION_REGISTRY entry
5. NEVER delete .git/, .agent/, node_modules/, zip/ — always protected
