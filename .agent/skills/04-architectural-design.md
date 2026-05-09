---
name: architectural-design
description: Skill for architectural-design
---

# Architectural Design Principles (Advanced)

This foundational skill dictates how the `03-planner` and `04-synthesizer` agents structure complex systems. It enforces professional engineering standards to prevent technical debt.

## 1. Structural Mandates: Hexagonal Architecture (Ports & Adapters)
All project architectures must enforce a strict separation between the **Domain Core** and **Infrastructure Adapters**.

- **Domain Core**: Contains pure business logic. It must have ZERO dependencies on external frameworks, databases, or UI libraries.
- **Ports (Interfaces)**: The Domain Core defines what it needs (e.g., `UserRepository`) but not how it's implemented.
- **Adapters (Implementation)**: External layers (Database, REST API, CLI) implement the Ports. 
- **The Rule of Dependency**: Dependencies must always point **inwards** toward the Domain Core.

## 2. The SOLID Enforcement Matrix
- **Single Responsibility (SRP)**: Each class/module must solve exactly one problem. If a file exceeds 300 lines, it is a candidate for decomposition.
- **Open/Closed**: Software entities should be open for extension but closed for modification. Use composition over inheritance.
- **Liskov Substitution**: Derived classes must be substitutable for their base classes without breaking logic.
- **Interface Segregation**: Clients should not be forced to depend on methods they do not use. Keep interfaces lean.
- **Dependency Inversion**: High-level modules should not depend on low-level modules. Both should depend on abstractions.

## 3. The "Boundary Guard" Protocol (Fail-Fast)
- **Input Sanitization**: Validate all data at the entry point (API, CLI, Form) using schemas (Zod, Pydantic, etc.).
- **Total Error Handling**: Differentiate between **Transient Errors** (Retryable - e.g., network timeout) and **Permanent Errors** (Non-retryable - e.g., validation failure).
- **Graceful Degradation**: If a non-critical sub-service fails, the main application must remain functional.

## 4. Security-by-Design
- **Principle of Least Privilege**: Each component must have the minimum permissions required to function.
- **Zero-Trust Communication**: Never assume data from internal services is safe. Re-validate at every internal boundary.
- **Sensitive Data Isolation**: PII (Personally Identifiable Information) and secrets must never be logged or stored in plain text.

## 5. Scalability & Latency
- **State Management**: Prefer stateless logic to allow for horizontal scaling.
- **Asynchronous Processing**: Offload heavy computations or I/O to background workers/queues.
- **Caching Layer**: Identify read-heavy operations and implement TTL-based caching strategies.
