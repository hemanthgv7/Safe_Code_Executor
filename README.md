Safe Code Executor
===================

A secure sandbox that executes untrusted Python code inside Docker with strict resource limits, filesystem isolation, and a simple web UI.

Features
--------
Core:
- Run Python code safely through an API
- Simple web UI for interactive testing
- Execute code inside isolated Docker containers

Security:
- Timeout protection (kills infinite loops)
- Memory limits (stops memory bombs)
- Network blocking
- Read-only container filesystem
- Read-only /tmp
- CPU limiting
- PID limiting
- Rejects code longer than 5000 characters

Web UI
------
A simple interface for running Python code from the browser.
<img width="1920" height="1080" alt="Screenshot (28)" src="https://github.com/user-attachments/assets/afc8b9de-5181-48f6-8277-861dbcc53582" />

API Usage
---------
Run Python Code:
POST /run
<img width="1920" height="1080" alt="Screenshot (21)" src="https://github.com/user-attachments/assets/61d1e6c6-b03c-46e9-a1f8-1f9a27ec1bc1" />

Example Request:
{
  "code": "for i in range(3): print(i)"
}

Example Response:
{
  "output": "0\n1\n2\n",
  "error": ""
}

How to Run the Project
----------------------
1. Install Requirements:
   pip install flask
<img width="1920" height="1080" alt="Screenshot (31)" src="https://github.com/user-attachments/assets/f7d57d3c-4797-4469-962f-e944b590a596" />

2. Start the API:
   python app.py
<img width="1915" height="320" alt="Screenshot (30)" src="https://github.com/user-attachments/assets/f3cebab8-ab7c-4c62-968c-45fbcfe388c3" />

3. Test API:
   POST http://localhost:8000/run
<img width="1920" height="1080" alt="Screenshot (30)" src="https://github.com/user-attachments/assets/8437f33b-0da4-46dd-8da7-523fbcd8e362" />

Docker Sandbox
--------------
docker run --rm --network none --memory=128m --memory-swap=128m --cpus=0.5 --pids-limit=50 --read-only --tmpfs /tmp:ro -v /host/temp:/code python:3.11-slim python script.py

<img width="1920" height="1080" alt="Screenshot (24)" src="https://github.com/user-attachments/assets/218fc226-148a-4d2b-b8e1-50f9d25a27ac" />

Security Test Results
---------------------
Infinite Loop:
Result: Execution timed out after 10 seconds

<img width="1920" height="1080" alt="Screenshot (27)" src="https://github.com/user-attachments/assets/f8530ed2-6c18-43fd-a2b0-390954769d6d" />

Memory Bomb:
Result: Memory limit exceeded

<img width="1920" height="1080" alt="Screenshot (29)" src="https://github.com/user-attachments/assets/abb6cd27-0480-427d-909a-14980702c223" />

Network Attack:
Result: Network unreachable or import error

<img width="1920" height="1080" alt="Screenshot (24)" src="https://github.com/user-attachments/assets/3e46cb16-b48b-4ebe-b0a6-81630ae1a6d3" />

Filesystem Attack:
Result: Read-only file system
<img width="1920" height="1080" alt="Screenshot (25)" src="https://github.com/user-attachments/assets/9c50fff8-f4a2-4379-b40e-bc2f92848f9b" />

What I Learned
--------------
- Running untrusted code safely
- Docker isolation and security limits
- Preventing infinite loops, memory abuse, file writes, and network misuse
- Designing a secure API + UI

Project Structure
-----------------
Safe-Code-Executor/
│
├── app.py
├── Dockerfile
├── README.md
├── templates/index.html
├── temp/


