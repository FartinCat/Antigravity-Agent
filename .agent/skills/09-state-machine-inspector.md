# State Machine Inspector

**Purpose**: Detects classes/modules that manage state through multiple boolean flags instead of a unified state type (enum/union).

## Detection Criteria

Flag a class/module when:
1. It has ≥ 3 boolean fields that represent mutually exclusive states
   - Example: `is_loading`, `is_error`, `is_success`, `is_idle`
2. State transitions are managed by setting/unsetting individual booleans
   - Example: `self.is_loading = False; self.is_success = True`
3. Guard conditions check multiple booleans with AND/OR logic
   - Example: `if not is_loading and not is_error and is_initialized:`

## Recommended Refactoring

```python
# BEFORE (boolean soup)
class Request:
    is_idle: bool
    is_loading: bool
    is_success: bool
    is_error: bool
    error_message: str | None

# AFTER (unified state)
class RequestState(Enum):
    IDLE = "idle"
    LOADING = "loading"
    SUCCESS = "success"
    ERROR = "error"

class Request:
    state: RequestState
    error_message: str | None  # only valid when state == ERROR
```

## Language-Specific Patterns

| Language | Recommended Type |
|---|---|
| Python | `enum.Enum` or `typing.Literal` |
| Rust | `enum` with variants (tagged union) |
| TypeScript | Discriminated union type |
| Go | `iota` const block |
| C | `typedef enum` |

## Exemptions
- Feature flags (independent booleans that are NOT mutually exclusive)
- Configuration objects where booleans represent independent toggles
