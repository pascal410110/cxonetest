import os
import requests

def create_release_and_upload(file_path, tag_name="auto-release"):
    token = os.getenv("GITHUB_TOKEN")
    repo = os.getenv("REPO")

    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json"
    }

    # Step 1️⃣ 檢查 Release 是否已存在
    release_url = f"https://api.github.com/repos/{repo}/releases/tags/{tag_name}"
    res = requests.get(release_url, headers=headers)

    if res.status_code == 200:
        release = res.json()
        release_id = release["id"]
        upload_url = release["upload_url"].split("{")[0]
        print(f"[INFO] Existing release found (id={release_id})")
    else:
        # Step 2️⃣ 若不存在，建立新的 Release
        print("[INFO] Creating new release...")
        create_url = f"https://api.github.com/repos/{repo}/releases"
        payload = {
            "tag_name": tag_name,
            "name": f"Automated Release - {tag_name}",
            "body": "This release was created automatically by GitHub Actions.",
            "draft": False,
            "prerelease": False
        }
        res = requests.post(create_url, headers=headers, json=payload)
        if res.status_code not in (200, 201):
            print(f"[ERROR] Failed to create release: {res.status_code}")
            print(res.text)
            return
        release = res.json()
        upload_url = release["upload_url"].split("{")[0]
        print(f"[SUCCESS] Created new release: {release['html_url']}")

    # Step 3️⃣ 上傳 PDF 檔案作為 Release Asset
    print(f"[INFO] Uploading {file_path} to release...")
    file_name = os.path.basename(file_path)
    with open(file_path, "rb") as f:
        upload_headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/pdf"
        }
        upload_res = requests.post(
            f"{upload_url}?name={file_name}",
            headers=upload_headers,
            data=f
        )

    if upload_res.status_code in (200, 201):
        asset = upload_res.json()
        print(f"[SUCCESS] Uploaded asset: {asset['browser_download_url']}")
    else:
        print(f"[ERROR] Upload failed: {upload_res.status_code}")
        print(upload_res.text)

if __name__ == "__main__":
    create_release_and_upload("report.pdf", tag_name="v1.0.0")
