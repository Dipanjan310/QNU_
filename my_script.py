# import requests
# import numpy as np

# def fetch_data():
#     url = "https://api.github.com"
#     response = requests.get(url)
#     if response.status_code == 200:
#         print("GitHub API is reachable!")
#         print("Current Rate Limit Info:")
#         print(response.json().get("rate_limit_url", "No info"))
#     else:
#         print("Failed to reach GitHub API.")

# if __name__ == "__main__":
#     fetch_data()


import os
import subprocess
import shutil

BASE_DIR = os.getcwd()
WORKFLOW_DIR = os.path.join(BASE_DIR, "workflows")

def init_workflow(workflow_id, python_version="3.11", libraries=[]):
    wf_path = os.path.join(WORKFLOW_DIR, workflow_id)
    os.makedirs(wf_path, exist_ok=True)

    # Write Dockerfile
    dockerfile = f"""
    FROM python:{python_version}-slim
    WORKDIR /app
    COPY . /app
    RUN pip install --upgrade pip && pip install {' '.join(libraries)}
    CMD ["bash"]
    """
    with open(os.path.join(wf_path, "Dockerfile"), "w") as f:
        f.write(dockerfile)

    # Build the Docker image
    subprocess.run(["docker", "build", "-t", workflow_id, "."], cwd=wf_path)
    print(f"[✅] Workflow '{workflow_id}' initialized with Python {python_version}")

def update_libraries(workflow_id, new_libraries):
    container_id = subprocess.check_output(["docker", "create", workflow_id]).decode().strip()
    subprocess.run(["docker", "start", container_id])
    subprocess.run(["docker", "exec", container_id, "pip", "install"] + new_libraries)
    subprocess.run(["docker", "commit", container_id, workflow_id])
    subprocess.run(["docker", "rm", "-f", container_id])
    print(f"[✅] Libraries {new_libraries} added to workflow '{workflow_id}'")

def load_workflow(workflow_id, script_list):
    wf_path = os.path.join(WORKFLOW_DIR, workflow_id)
    script_dir = os.path.join(BASE_DIR, "workflow_scripts")
    for script in script_list:
        src = os.path.join(script_dir, script)
        dst = os.path.join(wf_path, script)
        shutil.copy(src, dst)
    print(f"[✅] Scripts {script_list} loaded into workflow '{workflow_id}'")

def run_workflow(workflow_id):
    wf_path = os.path.join(WORKFLOW_DIR, workflow_id)
    container_name = f"{workflow_id}_runner"
    subprocess.run(["docker", "run", "--name", container_name, "-v", f"{wf_path}:/app", workflow_id, "bash", "-c", " && ".join([f"python {f}" for f in os.listdir(wf_path) if f.endswith('.py')])])
    subprocess.run(["docker", "rm", "-f", container_name])
    print(f"[✅] Workflow '{workflow_id}' executed successfully.")

