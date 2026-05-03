# Architectural Design Principles

This file contains the foundational logic used by the `planner` agent to ensure systems are built professionally and sustainably.

## Core Mandates
1. **Separation of Concerns**: UI, logic, and data storage must be strictly isolated.
2. **Stateless Services**: Where possible, backend logic should be stateless to allow horizontal scaling.
3. **Fail-Fast Mechanics**: Validate all inputs at the boundary. Fail immediately with clear, descriptive errors.
4. **Data Integrity**: Enforce constraints at the database level, not just the application level.

## The Planning Algorithm
When breaking down a feature:
1. Identify the core domain models.
2. Draft the API/Service boundaries.
3. Detail the state management approach for the frontend.
4. List specific security risks and mitigation strategies.
