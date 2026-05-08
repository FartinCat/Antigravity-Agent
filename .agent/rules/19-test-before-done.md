---
rule: 19-test-before-done
priority: CRITICAL
---
# Rule 19: Test Before Done

## The Law
A task is not DONE until its tests pass — no exceptions.

## Why This Exists
Prevents "Works on my machine" bugs, silent regressions in existing functionality, and shipping broken code with false confidence.

## Mandatory Behaviors
1. For every `/impl` task: write or update tests.
2. Run the test suite after each task — not just at the very end of the session.
3. If a test fails: invoke `/antibug` before declaring the task done.
4. For bug fixes: write a regression test FIRST (to prove the bug exists), then fix the bug, then ensure the test passes.
5. Test coverage must not decrease after any change.

## Prohibited Behaviors
1. Saying "I'll write tests later."
2. Marking a task done when tests are currently failing.
3. Skipping tests because it is a "simple" or "trivial" change.
4. Commenting out failing tests to make the suite green.

## Enforcement
- System rejects `DONE` status on any implementation sub-task if a test run output showing a `PASS` state has not been provided or verified.
