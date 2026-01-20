---
id: 2
title: Fix Backend Startup and Login Issues
stage: general
date_iso: 2026-01-20
surface: agent
model: claude-sonnet-4-5-20250929
feature: none
branch: main
user: user
command: sp.analyze
labels: ["backend", "startup-error", "login", "authentication", "bug-fix"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files_yaml: |
  - D:\hackathon_2_Ai_todo_app\Hackathon_II_Todo_Spec_Driven_project\phase-2 -full stack todo app\backend\src\main.py
  - D:\hackathon_2_Ai_todo_app\Hackathon_II_Todo_Spec_Driven_project\phase-2 -full stack todo app\backend\src\api\auth.py
tests_yaml: |
  - None added
prompt_text: |
  i am login multiple but know i am facing this erro Sign in to your account
  Or sign up for a new account

  Login failed i think you didi a mistake in code chck out and run backend and when i run backend in my project have this eror resolve all this error Will watch for changes in these directories: ['D:\\hackathon_2_Ai_todo_app\\Hackathon_II_Todo_Spec_Driven_project\\phase-2 -full stack todo app\\backend']
  INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
  INFO:     Started reloader process [7028] using WatchFiles
  Process SpawnProcess-1:
  Traceback (most recent call times):
    File "C:\Python312\Lib\multiprocessing\process.py", line 314, in _bootstrap
    self.run()
    File "C:\Python312\Lib\multiprocessing\process.py", line 108, in run
    self._target(*self._args, **self._kwargs)
    File "D:\hackathon_2_Ai_todo_app\Hackathon_II_Todo_Spec_Driven_project\phase-2 -full stack todo app\backend\.venv\Lib\site-packages\uvicorn\_subprocess.py", line 80, in subprocess_started
    target(sockets=sockets)
    File "D:\hackathon_2_Ai_todo_app\Hackathon_II_Todo_Spec_Driven_project\phase-2 -full stack todo app\backend\.venv\Lib\site-packages\uvicorn\server.py", line 67, in run
    return asyncio_run(self.serve(sockets=sockets), loop_factory=self.config.get_loop_factory())
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    File "C:\Python312\Lib\asyncio\runners.py", line 194, in run
    return runner.run(main)
           ^^^^^^^^^^^^^^^^
    File "C:\Python312\Lib\asyncio\runners.py", line 118, in run
    return self._loop.run_until_complete(task)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    File "C:\Python312\Lib\asyncio\base_events.py", line 685, in run_until_complete
    return future.result()
           ^^^^^^^^^^^^^^^
    File "D:\hackathon_2_Ai_todo_app\Hackathon_II_Todo_Spec_Driven_project\phase-2 -full stack todo app\backend\.venv\Lib\site-packages\uvicorn\server.py", line 71, in serve
    await self._serve(sockets)
    File "D:\hackathon_2_Ai_todo_app\Hackathon_II_Todo_Spec_Driven_project\phase-2 -full stack todo app\backend\.venv\Lib\site-packages\uvicorn\server.py", line 78, in _serve
    config.load()
    File "D:\hackathon_2_Ai_todo_app\Hackathon_II_Todo_Spec_Driven_project\phase-2 -full stack tod
response_text: |
  Fixed multiple backend issues:
  1. Resolved multiprocessing startup error by converting async startup event to sync in src/main.py
  2. Fixed login functionality by correcting bcrypt password verification in auth API
  3. Updated deprecated datetime methods to use timezone-aware alternatives
outcome: |
  Backend now starts successfully without multiprocessing errors and login functionality works properly.
evaluation: |
  Fixes were applied to resolve both the startup error and login authentication issues.
---

## Summary

Resolved backend startup multiprocessing error and login authentication issues by fixing async startup events, correcting password verification logic, and updating deprecated datetime methods.