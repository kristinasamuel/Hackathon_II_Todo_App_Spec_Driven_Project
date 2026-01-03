# Todo API Contract

## Overview
This contract defines the expected behavior for the console-based todo application based on the functional requirements in the specification.

## Functional Requirements Implementation

### FR-001: Display welcome message on startup
- **Input**: Application launch
- **Output**: Welcome message "Welcome to the Todo Console App"
- **Success criteria**: Message appears within 3 seconds of launch

### FR-002: Present numbered menu options
- **Input**: Application launch or return from operation
- **Output**: Menu with options 1-6 as specified
- **Success criteria**: All 6 options displayed with correct numbering

### FR-003: Allow menu option selection by number
- **Input**: User enters number 1-6
- **Output**: Corresponding action is executed
- **Success criteria**: Action executes without error

### FR-004: Store todos in memory with required fields
- **Input**: Todo creation with title
- **Output**: Todo stored with ID, Title, Description, Status
- **Success criteria**: All fields stored correctly, ID assigned automatically

### FR-005: Add new todo with title and optional description
- **Input**: Title (required), description (optional)
- **Output**: New todo added to in-memory list
- **Success criteria**: Todo appears in list with correct attributes

### FR-006: Display todos in structured table format
- **Input**: View Todos option selected
- **Output**: Table with ID, Status, Title, Description columns
- **Success criteria**: All todos displayed in readable format

### FR-007: Update existing todo by ID
- **Input**: Valid todo ID and new title/description
- **Output**: Todo updated in memory
- **Success criteria**: Changes reflected when viewing todos

### FR-008: Delete todo by ID
- **Input**: Valid todo ID
- **Output**: Todo removed from memory
- **Success criteria**: Todo no longer appears when viewing todos

### FR-009: Toggle todo status by ID
- **Input**: Valid todo ID
- **Output**: Todo status changed (Complete ↔ Incomplete)
- **Success criteria**: Status change reflected when viewing todos

### FR-010: Return to main menu after actions
- **Input**: Any completed action (except Exit)
- **Output**: Main menu displayed again
- **Success criteria**: User can select another option

### FR-011: Display success message after valid actions
- **Input**: Any completed action
- **Output**: Appropriate success message
- **Success criteria**: Clear feedback provided to user

### FR-012: Handle invalid menu selections
- **Input**: Number not in range 1-6
- **Output**: Error message and return to main menu
- **Success criteria**: User not crashed, returned to menu

### FR-013: Handle invalid todo IDs
- **Input**: ID that doesn't exist in todo list
- **Output**: Error message and return to main menu
- **Success criteria**: User not crashed, returned to menu

### FR-014: Allow application exit
- **Input**: Option 6 selected
- **Output**: Application terminates cleanly
- **Success criteria**: No errors on exit