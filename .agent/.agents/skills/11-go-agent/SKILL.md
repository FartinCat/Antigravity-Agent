---
name: go-agent
description: Go-specific language agent. Encodes Go rules, instincts, and verification workflows for idiomatic, concurrent Go development.
origin: Custom Ensemble (Claude + DeepSeek + Gemini)
---

# Agent: Go Language Specialist

## Rules

### GO-R001: ERRORS_ALWAYS_HANDLED
Every function that returns an error must have that error checked immediately. `_ = riskyFunc()` is prohibited.

### GO-R002: GOROUTINE_LIFECYCLE
Every `go func()` must have:
- A documented owner (who waits for it?)
- A cancellation mechanism (`context.Context` or `done` channel)
- A panic recovery (`defer recover()`)

### GO-R003: CONTEXT_FIRST_PARAM
Functions that accept a `context.Context` must take it as the first parameter, named `ctx`.

### GO-R004: INTERFACES_AT_USE_SITE
Interfaces should be defined where they are consumed, not where they are implemented. Keep interfaces small (1-3 methods).

### GO-R005: ERROR_WRAPPING
Errors must be wrapped with context using `fmt.Errorf("operation failed: %w", err)`. Never return raw errors from deep call stacks.

### GO-R006: NO_GLOBAL_HTTP_CLIENT
Never use `http.DefaultClient` in production code. Always create a client with configured timeouts and transport settings.

---

## Instincts

### GO-INSTINCT-001: LOOP_VARIABLE_CAPTURE (p=0.90)
Loop variable captured in a goroutine closure — all goroutines share the same variable. Shadow it: `v := v` or use Go 1.22+ semantics.

### GO-INSTINCT-002: CHANNEL_DEADLOCK (p=0.82)
An unbuffered channel with no concurrent reader/writer — will deadlock.

### GO-INSTINCT-003: NIL_MAP_WRITE (p=0.88)
Writing to a `nil` map — runtime panic. Always initialize with `make(map[K]V)`.

### GO-INSTINCT-004: SLICE_APPEND_ALIASING (p=0.75)
Appending to a slice that shares underlying array with another slice — may silently overwrite data.

### GO-INSTINCT-005: DEFER_IN_LOOP (p=0.78)
`defer` inside a loop — deferred calls accumulate until function returns, not until loop iteration ends. May cause resource exhaustion.

---

## Verification Workflow
1. `go vet ./...` — static analysis
2. `staticcheck ./...` — advanced linting
3. `go test -race ./...` — unit tests with race detector
4. `golangci-lint run` — comprehensive linting
5. `go build ./...` — compile check

---

## Go Mastery Patterns
1. **Error Handling**: `errors.Is/As`, custom error types, sentinel errors, never panic in libs.
2. **Concurrency**: goroutine lifecycle management, context propagation, select patterns, avoiding goroutine leaks.
3. **Project Layout**: `cmd/` (binaries), `internal/` (private), `pkg/` (public), standard `go.mod` location.
4. **Testing**: table-driven tests, testify patterns, httptest for APIs, race detector (`-race` flag).
5. **Naming**: MixedCaps only, unexported functions lowercase, interfaces describe behavior not structure.
6. **Observability**: structured logging (`slog`), trace propagation, metric naming conventions.
7. **Context**: always accept `context.Context` as first arg, never store in structs, cancel/deadline patterns.
8. **Security**: no G101-G601 gosec violations, secrets from env, parameterized queries.
9. **Design Patterns**: functional options, dependency injection, interface segregation.
10. **Performance**: pprof profiling, `sync.Pool` for GC pressure, defer cost awareness.
\n## Advanced Operations Matrix\n\n- **Database Interaction**: Use appropriate client libraries (e.g., sqlite3 for SQLite, psycopg2 for PostgreSQL, mysql-connector-python for MySQL) with parameterized queries to prevent injection.\n- **Simulation & Modeling**: For scientific simulations, employ 
umpy, scipy, or pandas for data handling, and matplotlib or plotly for visualizations.\n- **Performance Profiling**: Run python -m cProfile or 	imeit to benchmark critical sections.\n- **Precise Explanation**: Include step‑by‑step rationale in markdown code comments and a short summary in plain text.\n- **Error Handling**: Wrap external calls in try/except blocks, log errors with context, and re‑raise if unrecoverable.\n
