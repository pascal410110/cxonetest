import os
import requests

def upload_artifact(file_path, artifact_name):
    token = os.getenv("GITHUB_TOKEN")
    repo = os.getenv("REPO")
    run_id = os.getenv("GITHUB_RUN_ID")

    if not all([token, repo, run_id]):
        raise EnvironmentError("Missing environment variables.")

    create_url = f"https://api.github.com/repos/{repo}/actions/runs/{run_id}/artifacts"
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json"
    }

    with open(file_path, "rb") as f:
        files = {"file": (os.path.basename(file_path), f, "application/pdf")}
        response = requests.post(create_url, headers=headers, files=files)

    if response.status_code in (200, 201):
        print(f"[SUCCESS] Artifact '{artifact_name}' uploaded.")
    else:
        print(f"[ERROR] Upload failed: {response.status_code}")
        print(response.text)

if __name__ == "__main__":
    upload_artifact("report.pdf", "My_Report")
