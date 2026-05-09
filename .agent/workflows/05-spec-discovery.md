---

title: "SPEC DISCOVERY"

description: "Functional and technical spec extraction."

order: 05

---



# Workflow 05: Spec Discovery



**Objective:** Transform ambiguous user intent into a rigid, actionable, and unambiguous specification. Do not write code during this phase. This workflow is the foundation for all subsequent development.



## Philosophy

Code written without a spec is technical debt generated at the speed of thought. The Spec Discovery workflow is designed to forcefully extract constraints, surface hidden assumptions, and define exact boundaries before a single line of logic is synthesized. You are an investigative architect, not a code generator.



## 1. Assumption Surfacing Protocol

Before writing the spec, you must challenge the prompt. Identify the unspoken assumptions the user is making.



- **Scale Assumptions:** Are they assuming this handles 10 users or 10,000?

- **State Assumptions:** Is this stateless? Where does data persist?

- **Failure Assumptions:** What happens when the network drops? When the API rate limits?

- **Security Assumptions:** Who has access to this? Is the data sensitive?



*Action:* Ask the user directly about the top 3 most critical unknowns. Do not proceed until these are answered.



## 2. The 6-Pillar Spec Framework



A valid specification must cover these six areas comprehensively. 



### Pillar 1: Objective & Persona

Define exactly what the software does and who it is for.

- **Primary Goal:** (e.g., "A CLI tool to compress local images.")

- **Target User:** (e.g., "Developers integrating it into CI pipelines.")

- **Success Criteria:** How will we know it works? (e.g., "Reduces PNG sizes by >20% without visible artifacting.")



### Pillar 2: Core Workflows (The Happy Path)

Detail the step-by-step user journey.

1. User does X.

2. System validates Y.

3. System outputs Z.



### Pillar 3: Edge Cases & Error States (The Unhappy Path)

Explicitly document how the system fails gracefully.

- Invalid inputs.

- Missing dependencies.

- Network timeouts.

- File permission errors.



### Pillar 4: Technical Stack & Architecture

Lock down the foundational technologies.

- **Language/Framework:** (e.g., Next.js 14 App Router, Python 3.11)

- **State Management:** (e.g., Zustand, native Context)

- **Data Persistence:** (e.g., Postgres via Prisma)

- **Styling:** (e.g., Tailwind CSS, Vanilla CSS)



### Pillar 5: Testing Strategy

Define how the spec will be verified.

- **Unit Tests:** (What functions must be isolated?)

- **Integration Tests:** (What boundaries must be crossed?)

- **Mocking Strategy:** (What external services will be stubbed?)



### Pillar 6: Constraints & Boundaries

What is explicitly *out of scope*?

- "We will NOT support mobile browsers for v1."

- "We will NOT implement user authentication."



## 3. Phase Gating



The spec discovery process is gated. You cannot move to the next phase without user approval.



- **Gate 1: The Questionnaire.** You present the top 3 unknowns. (Waiting for User)

- **Gate 2: The Draft Spec.** You present the 6-Pillar framework. (Waiting for User)

- **Gate 3: The Final Sign-off.** User confirms the spec is the single source of truth.



## 4. Anti-Patterns to Avoid



- **The "Yes Man" Anti-Pattern:** Blindly accepting a vague request like "build a chat app" without defining the protocol, persistence, or scaling constraints.

- **The "Implementation Detail" Anti-Pattern:** Putting variable names or database schemas in the spec. The spec is for *what* and *why*, not *how*.

- **The "Feature Creep" Anti-Pattern:** Suggesting new features the user didn't ask for. Keep the scope tight.



## 5. Output Format



Once discovery is complete, generate the `SPEC.md` file in the project root using this exact template:



```markdown

# Product Specification: [Project Name]



## 1. Objective

[Clear, 2-sentence description]



## 2. Target Audience

[Who uses this]



## 3. Scope & Boundaries

- **In Scope:** [List]

- **Out of Scope:** [List]



## 4. Core Workflows

### Scenario: [Name]

1. [Step 1]

2. [Step 2]



## 5. Error Handling

- **[Error Condition]:** [System Response]



## 6. Technical Stack

- [Frontend]

- [Backend]

- [Infra]



## 7. Testing Requirements

- [Requirement 1]

```



## 6. Final Execution

After `SPEC.md` is saved, notify the user: "Spec Discovery Complete. Run `/planner` or `/tdd-guide` to begin implementation based on this specification."



## Output Organization (Rule 20)
1. Check if `docs/specs` exists, create if not.
2. Count existing files.
3. Output report to `docs/specs/SPEC_{feature}_{NN}.md` (increment NN zero-padded).
4. NEVER output to project root.

