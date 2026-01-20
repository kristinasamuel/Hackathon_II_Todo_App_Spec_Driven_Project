---
id: 1
title: Fix Checkbox Controlled Component Error
stage: general
date_iso: 2026-01-20
surface: agent
model: claude-sonnet-4-5-20250929
feature: none
branch: main
user: user
command: sp.analyze
labels: ["react", "checkbox", "controlled-component", "bug-fix"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files_yaml: |
  - D:\hackathon_2_Ai_todo_app\Hackathon_II_Todo_Spec_Driven_project\phase-2 -full stack todo app\frontend_new\src\app\dashboard\page.tsx
tests_yaml: |
  - None added
prompt_text: |
  website complete hai but ek error hai click nhi hora hai task complete or incomlete   message show hora hai kase resolve kary Console Error

  You provided a `checked` prop to a form field without an `onChange` handler. This will render a read-only field. If the field should be mutable use `defaultChecked`. Otherwise, set either `onChange` or `readOnly`.
  ../../phase-2 -full stack todo app/frontend_new/src/app/dashboard/page.tsx (295:27) @ eval

    293 |                       <div className="flex items-center justify-between">
    294 |                         <div className="flex items-center">
    > 295 |                           <input
        |                           ^
    296 |                             type="checkbox"
    297 |                             checked={task.completed}
    298 |                             onClick={() => {
  Call Stack
  19

  Show 15 ignore-listed frame(s)
  input
  <anonymous>
response_text: |
  Fixed the React controlled component error by changing onClick to onChange on the checkbox input in the dashboard page. This resolves the warning and allows the checkbox to properly handle state changes when clicked.
outcome: |
  The checkbox component now properly functions as a controlled component in React, eliminating the console error and allowing users to click the checkbox to toggle task completion status.
evaluation: |
  The fix was tested by reviewing the code and confirming that the toggleTaskCompletion function in the useTasks hook properly handles the state update.
---

## Summary

Fixed a React controlled component error in the dashboard page where the checkbox had a `checked` prop but was using `onClick` instead of `onChange`. Changed the event handler to `onChange` to properly handle the controlled component pattern, resolving the console error and restoring functionality.