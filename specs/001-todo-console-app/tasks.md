---
description: "Task list for Todo In-Memory Python Console Application"
---

# Tasks: Todo In-Memory Python Console Application

**Input**: Design documents from `/specs/001-todo-console-app/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: The examples below include test tasks. Tests are OPTIONAL - only include them if explicitly requested in the feature specification.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Single project**: `src/`, `tests/` at repository root
- **Web app**: `backend/src/`, `frontend/src/`
- **Mobile**: `api/src/`, `ios/src/` or `android/src/`
- Paths shown below assume single project - adjust based on plan.md structure

<!--
  ============================================================================
  IMPORTANT: The tasks below are SAMPLE TASKS for illustration purposes only.

  The /sp.tasks command MUST replace these with actual tasks based on:
  - User stories from spec.md (with their priorities P1, P2, P3...)
  - Feature requirements from plan.md
  - Entities from data-model.md
  - Endpoints from contracts/

  Tasks MUST be organized by user story so each story can be:
  - Implemented independently
  - Tested independently
  - Delivered as an MVP increment

  DO NOT keep these sample tasks in the generated tasks.md file.
  ============================================================================
-->

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [ ] T001 Create project structure per implementation plan in src/
- [ ] T002 Initialize Python project with requirements.txt and setup files
- [ ] T003 [P] Configure linting and formatting tools (flake8, black)

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [ ] T004 Create Todo model in src/models/todo.py with id, title, description, status attributes
- [ ] T005 [P] Create TodoService in src/services/todo_service.py with in-memory storage (list of dictionaries)
- [ ] T006 [P] Create UI module in src/cli/ui.py with menu display and input handling functions
- [ ] T007 Create main application loop in src/main.py with welcome message and menu structure
- [ ] T008 Configure error handling and logging infrastructure in src/utils/

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Add Todo (Priority: P1) 🎯 MVP

**Goal**: Enable users to add new todo items to their list with title and optional description

**Independent Test**: Can be fully tested by starting the application, selecting option 1, entering a title and description, and verifying that the todo is added to the list and can be viewed.

### Tests for User Story 1 (OPTIONAL - only if tests requested) ⚠️

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [ ] T009 [P] [US1] Unit test for Todo creation in tests/unit/test_todo.py
- [ ] T010 [P] [US1] Integration test for Add Todo functionality in tests/integration/test_cli_flow.py

### Implementation for User Story 1

- [ ] T011 [P] [US1] Implement add_todo method in src/services/todo_service.py with ID generation and validation
- [ ] T012 [US1] Implement add_todo_ui function in src/cli/ui.py for user input collection
- [ ] T013 [US1] Add option 1 handling in main application loop in src/main.py
- [ ] T014 [US1] Add success message display after todo creation in src/cli/ui.py
- [ ] T015 [US1] Add validation for title (non-empty) in src/models/todo.py

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - View Todos (Priority: P2)

**Goal**: Enable users to see all their todo items in a structured table format

**Independent Test**: Can be fully tested by adding a few todos and then selecting option 2 to view them in the structured table format.

### Tests for User Story 2 (OPTIONAL - only if tests requested) ⚠️

- [ ] T016 [P] [US2] Contract test for View Todos functionality in tests/contract/test_api_contract.py
- [ ] T017 [P] [US2] Integration test for View Todos in tests/integration/test_cli_flow.py

### Implementation for User Story 2

- [ ] T018 [P] [US2] Implement get_all_todos method in src/services/todo_service.py
- [ ] T019 [US2] Implement display_todos_table function in src/cli/ui.py with proper formatting
- [ ] T020 [US2] Add option 2 handling in main application loop in src/main.py
- [ ] T021 [US2] Add proper table formatting with ID, Status, Title, Description columns in src/cli/ui.py
- [ ] T022 [US2] Handle case when no todos exist in src/cli/ui.py

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - Mark Todo Complete/Incomplete (Priority: P3)

**Goal**: Enable users to update the status of a todo item by toggling between Complete and Incomplete

**Independent Test**: Can be fully tested by adding a todo, marking it as complete, and verifying the status change is reflected when viewing todos.

### Tests for User Story 3 (OPTIONAL - only if tests requested) ⚠️

- [ ] T023 [P] [US3] Unit test for status toggle functionality in tests/unit/test_todo_service.py
- [ ] T024 [P] [US3] Integration test for Mark Todo Complete/Incomplete in tests/integration/test_cli_flow.py

### Implementation for User Story 3

- [ ] T025 [P] [US3] Implement toggle_todo_status method in src/services/todo_service.py
- [ ] T026 [US3] Implement mark_todo_ui function in src/cli/ui.py for ID input and status toggle
- [ ] T027 [US3] Add option 5 handling in main application loop in src/main.py
- [ ] T028 [US3] Add validation for valid todo ID in src/services/todo_service.py
- [ ] T029 [US3] Add success message display after status change in src/cli/ui.py

**Checkpoint**: At this point, User Stories 1, 2 AND 3 should all work independently

---

## Phase 6: User Story 4 - Update Todo (Priority: P4)

**Goal**: Enable users to modify an existing todo item by providing its ID and new title and/or description

**Independent Test**: Can be fully tested by adding a todo, updating its details, and verifying the changes are reflected when viewing todos.

### Tests for User Story 4 (OPTIONAL - only if tests requested) ⚠️

- [ ] T030 [P] [US4] Unit test for update functionality in tests/unit/test_todo_service.py
- [ ] T031 [P] [US4] Integration test for Update Todo in tests/integration/test_cli_flow.py

### Implementation for User Story 4

- [ ] T032 [P] [US4] Implement update_todo method in src/services/todo_service.py
- [ ] T033 [US4] Implement update_todo_ui function in src/cli/ui.py for ID input and new details
- [ ] T034 [US4] Add option 3 handling in main application loop in src/main.py
- [ ] T035 [US4] Add validation for valid todo ID and required title in src/services/todo_service.py
- [ ] T036 [US4] Add success message display after update in src/cli/ui.py

**Checkpoint**: At this point, User Stories 1, 2, 3 AND 4 should all work independently

---

## Phase 7: User Story 5 - Delete Todo (Priority: P5)

**Goal**: Enable users to remove a todo item from their list by providing its ID

**Independent Test**: Can be fully tested by adding a todo, deleting it, and verifying it no longer appears when viewing todos.

### Tests for User Story 5 (OPTIONAL - only if tests requested) ⚠️

- [ ] T037 [P] [US5] Unit test for delete functionality in tests/unit/test_todo_service.py
- [ ] T038 [P] [US5] Integration test for Delete Todo in tests/integration/test_cli_flow.py

### Implementation for User Story 5

- [ ] T039 [P] [US5] Implement delete_todo method in src/services/todo_service.py
- [ ] T040 [US5] Implement delete_todo_ui function in src/cli/ui.py for ID input and confirmation
- [ ] T041 [US5] Add option 4 handling in main application loop in src/main.py
- [ ] T042 [US5] Add validation for valid todo ID in src/services/todo_service.py
- [ ] T043 [US5] Add success message display after deletion in src/cli/ui.py

**Checkpoint**: At this point, all user stories should be independently functional

---

## Phase 8: User Story 6 - Exit Application & Menu Navigation (Priority: P1)

**Goal**: Implement complete menu navigation with proper exit functionality and error handling

**Independent Test**: Can be tested by navigating through all menu options and verifying proper flow and clean exit.

### Tests for User Story 6 (OPTIONAL - only if tests requested) ⚠️

- [ ] T044 [P] [US6] Integration test for complete menu flow in tests/integration/test_cli_flow.py
- [ ] T045 [P] [US6] Contract test for Exit functionality in tests/contract/test_api_contract.py

### Implementation for User Story 6

- [ ] T046 [P] [US6] Implement proper menu loop with error handling in src/main.py
- [ ] T047 [US6] Add option 6 handling to exit application cleanly in src/main.py
- [ ] T048 [US6] Implement invalid menu option handling in src/main.py
- [ ] T049 [US6] Add validation for numeric input in src/cli/ui.py
- [ ] T050 [US6] Add error message display for invalid inputs in src/cli/ui.py

**Checkpoint**: Complete application with all functionality working

---

[Add more user story phases as needed, following the same pattern]

---

## Phase N: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [ ] T051 [P] Documentation updates in docs/
- [ ] T052 Code cleanup and refactoring
- [ ] T053 Performance optimization across all stories
- [ ] T054 [P] Additional unit tests (if requested) in tests/unit/
- [ ] T055 Security hardening
- [ ] T056 Run quickstart.md validation

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3+)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2 → P3)
- **Polish (Final Phase)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) - May integrate with US1 but should be independently testable
- **User Story 3 (P3)**: Can start after Foundational (Phase 2) - May integrate with US1/US2 but should be independently testable
- **User Story 4 (P4)**: Can start after Foundational (Phase 2) - May integrate with US1/US2 but should be independently testable
- **User Story 5 (P5)**: Can start after Foundational (Phase 2) - May integrate with US1/US2 but should be independently testable
- **User Story 6 (P1)**: Can start after Foundational (Phase 2) - Integrates with all other stories

### Within Each User Story

- Tests (if included) MUST be written and FAIL before implementation
- Models before services
- Services before endpoints
- Core implementation before integration
- Story complete before moving to next priority

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel
- All Foundational tasks marked [P] can run in parallel (within Phase 2)
- Once Foundational phase completes, all user stories can start in parallel (if team capacity allows)
- All tests for a user story marked [P] can run in parallel
- Models within a story marked [P] can run in parallel
- Different user stories can be worked on in parallel by different team members

---

## Parallel Example: User Story 1

```bash
# Launch all tests for User Story 1 together (if tests requested):
Task: "Unit test for Todo creation in tests/unit/test_todo.py"
Task: "Integration test for Add Todo functionality in tests/integration/test_cli_flow.py"

# Launch all implementation tasks for User Story 1 together:
Task: "Implement add_todo method in src/services/todo_service.py with ID generation and validation"
Task: "Implement add_todo_ui function in src/cli/ui.py for user input collection"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1
4. **STOP and VALIDATE**: Test User Story 1 independently
5. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Deploy/Demo (MVP!)
3. Add User Story 2 → Test independently → Deploy/Demo
4. Add User Story 3 → Test independently → Deploy/Demo
5. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1
   - Developer B: User Story 2
   - Developer C: User Story 3
   - Developer D: User Story 4
   - Developer E: User Story 5
3. Stories complete and integrate independently

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Verify tests fail before implementing
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence