from flask import Flask, request, jsonify, render_template
import subprocess
import uuid
import os

app = Flask(__name__)
TEMP_DIR = "./temp"
os.makedirs(TEMP_DIR, exist_ok=True)

# ------------------------------
# HOME ROUTE
# ------------------------------
@app.route("/", methods=["GET"])
def home():
    return "Safe Code Executor API is running. Use POST /run or visit /ui"


# ------------------------------
# SIMPLE WEB UI
# ------------------------------
@app.route("/ui")
def ui():
    return render_template("index.html")


# ------------------------------
# RUN CODE ENDPOINT
# ------------------------------
@app.route("/run", methods=["POST"])
def run_code_post():
    data = request.json
    code = data.get("code")

    if not code:
        return jsonify({"error": "No code provided"}), 400

    if len(code) > 5000:
        return jsonify({"error": "Code too long. Limit is 5000 characters."}), 400

    return jsonify(run_python(code))


# ------------------------------
# PYTHON SANDBOX RUNNER
# ------------------------------
def run_python(code):
    file_name = f"{uuid.uuid4().hex}.py"
    file_path = os.path.join(TEMP_DIR, file_name)

    with open(file_path, "w") as f:
        f.write(code)

    try:
        result = subprocess.run(
            [
                "docker", "run", "--rm",

                # SECURITY FLAGS
                "--network", "none",           # Block internet
                "--memory=128m",               # Memory limit
                "--memory-swap=128m",          # No swap memory
                "--cpus=0.5",                  # CPU throttling
                "--pids-limit=50",             # Prevent fork bombs
                "--read-only",                 # Make filesystem read-only
                "--tmpfs", "/tmp:ro",          # Make /tmp read-only

                # Mount directory with user code
                "-v", f"{os.path.abspath(TEMP_DIR)}:/code",

                "python:3.11-slim",
                "python", f"/code/{file_name}",
            ],
            capture_output=True,
            text=True,
            timeout=12  # Extra safety timeout for API itself
        )

        # Detect OOM kill (memory bomb)
        if result.returncode == 137:
            return {"error": "Memory limit exceeded (container killed)", "output": ""}

        output = result.stdout or ""
        error = result.stderr or ""

    except subprocess.TimeoutExpired:
        return {"error": "Execution timed out after 10 seconds", "output": ""}

    finally:
        os.remove(file_path)

    return {"output": output, "error": error}


# ------------------------------
# MAIN APP START
# ------------------------------
if __name__ == "__main__":
    print("Starting Safe Code Executor...")
    app.run(host="0.0.0.0", port=8000)
