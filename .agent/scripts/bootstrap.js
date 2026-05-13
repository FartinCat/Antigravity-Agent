#!/usr/bin/env node

/**
 * bootstrap.js — Dynamic root detection for Aether Agent
 * =============================================================================
 * Rules:
 *   - Never uses __dirname-relative paths or hardcoded absolute paths to resolve the root
 *   - Never persists the root to disk (session-local variable only)
 *   - Works in VS Code, Cursor, Windsurf, Claude Code, Gemini, plain terminal, CI
 *   - Respects AETHER_ROOT env var for explicit overrides
 *   - Walks UP from cwd, not down — safe even inside massive monorepos
 */

const fs = require('fs');
const path = require('path');
const readline = require('readline');

// Markers that identify an agent root. Listed in priority order.
const ROOT_MARKERS = [
    ".agent-root",       // Explicit pin file — highest priority
    ".aether-root",      // Explicit pin file alternative
    "AETHER.md",         // Unified Aether state file — strongest content signal
    ".agents",           // Agent infrastructure directory
    ".agent",            // Agent infrastructure directory (legacy/alternative)
    ".claude",           // Claude-specific commands directory
    ".git",              // Git repo root — reliable fallback
    "package.json",      // Node.js project root
    "pyproject.toml",    // Python project root
    "Cargo.toml",        // Rust project root
    "go.mod",            // Go project root
    "CLAUDE.md",         // IDE stub — weaker than AETHER.md
];

const MAX_WALK_DEPTH = 6;
let sessionRoot = null;

/**
 * Walk up from start looking for ROOT_MARKERS.
 */
function walkUp(startDir) {
    let current = path.resolve(startDir);
    for (let depth = 0; depth <= MAX_WALK_DEPTH; depth++) {
        for (const marker of ROOT_MARKERS) {
            const candidate = path.join(current, marker);
            if (fs.existsSync(candidate)) {
                return { foundRoot: current, marker, depth };
            }
        }
        const parent = path.dirname(current);
        if (parent === current) {
            break; // Hit filesystem root
        }
        current = parent;
    }
    return { foundRoot: null, marker: null, depth: -1 };
}

/**
 * Ask user interactively for the root directory path.
 */
async function askUser(startDir) {
    console.error(`\n⚠️  Could not detect agent root from: ${startDir}`);
    console.error(`   Searched for: ${ROOT_MARKERS.join(', ')}`);
    console.error(`   Tip: create a .agent-root file in your project root to pin it.\n`);

    const rl = readline.createInterface({
        input: process.stdin,
        output: process.stderr
    });

    return new Promise((resolve) => {
        rl.question("Where is the agent root? [Enter = cwd]: ", (answer) => {
            rl.close();
            const candidate = path.resolve(answer.trim() || process.cwd());
            
            if (!fs.existsSync(candidate)) {
                console.error(`\n❌ Directory does not exist: ${candidate}`);
                process.exit(1);
            }
            if (!fs.statSync(candidate).isDirectory()) {
                console.error(`\n❌ Not a directory: ${candidate}`);
                process.exit(1);
            }
            resolve(candidate);
        });
    });
}

function isInteractive() {
    const ciVars = ["CI", "CONTINUOUS_INTEGRATION", "GITHUB_ACTIONS", "GITLAB_CI", "TRAVIS", "CIRCLECI", "JENKINS_URL", "CODEBUILD_BUILD_ID"];
    if (ciVars.some(v => process.env[v])) return false;
    return process.stdin.isTTY;
}

/**
 * Detect and cache the agent root directory for this session.
 */
async function detectRoot(startDir = process.cwd(), interactive = true) {
    if (sessionRoot !== null) {
        return sessionRoot;
    }

    // 2. Environment variable override
    const envVars = ["AETHER_ROOT", "AGENT_ROOT", "AOS_ROOT"];
    for (const envKey of envVars) {
        const envVal = process.env[envKey];
        if (envVal) {
            const candidate = path.resolve(envVal);
            if (fs.existsSync(candidate) && fs.statSync(candidate).isDirectory()) {
                sessionRoot = candidate;
                console.error(`📍 Agent root (from $${envKey}): ${sessionRoot}`);
                return sessionRoot;
            } else {
                console.error(`⚠️  $${envKey} set to '${envVal}' but path does not exist — ignoring`);
            }
        }
    }

    // 3. Walk up from start directory
    const resolvedStart = path.resolve(startDir);
    const { foundRoot, marker, depth } = walkUp(resolvedStart);

    if (foundRoot) {
        sessionRoot = foundRoot;
        const depthNote = depth === 0 ? "" : ` (walked ${depth} level${depth > 1 ? 's' : ''} up)`;
        console.error(`📍 Agent root${depthNote}: ${sessionRoot}  [via ${marker}]`);
        return sessionRoot;
    }

    // 4. Ask user interactively
    if (interactive && isInteractive()) {
        sessionRoot = await askUser(resolvedStart);
        return sessionRoot;
    }

    // 5. Fail
    console.error(
        `\n❌ Cannot detect agent root from: ${resolvedStart}\n` +
        `   Searched up ${MAX_WALK_DEPTH} directory levels for: ${ROOT_MARKERS.join(', ')}\n\n` +
        `   Fix options:\n` +
        `   A) Create a .agent-root file in your project root:  touch /your/project/.agent-root\n` +
        `   B) Set an environment variable:                     export AETHER_ROOT=/your/project\n` +
        `   C) Run from inside the project directory:           cd /your/project && ./agentic-os start\n`
    );
    process.exit(1);
}

function getRoot() {
    if (sessionRoot === null) {
        throw new Error("Agent root not initialized. Call detectRoot() before getRoot().");
    }
    return sessionRoot;
}

function rootRelative(...parts) {
    return path.join(getRoot(), ...parts);
}

module.exports = {
    detectRoot,
    getRoot,
    rootRelative
};

// Standalone execution
if (require.main === module) {
    (async () => {
        try {
            const root = await detectRoot();
            console.log(root);
        } catch (err) {
            console.error(err.message);
            process.exit(1);
        }
    })();
}
