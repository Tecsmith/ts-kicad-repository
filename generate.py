import hashlib
import json
import sys
import time
from datetime import datetime as dt

VERSION = sys.argv[1]
DOWNLOAD_SHA256 = sys.argv[2]
DOWNLOAD_SIZE = sys.argv[3]
DOWNLOAD_URL = sys.argv[4]
INSTALL_SIZE = sys.argv[5]
KICAD_VERSION = sys.argv[6]
PROJECT_NAME = sys.argv[7]

# Check incoming
if PROJECT_NAME == "ts-kicad-lib":
    project_index = 0
elif PROJECT_NAME == "ts-kicad-plugins":
    project_index = 1
else:
    sys.exit(1)

with open("packages.json", "r+", encoding="utf-8") as f:
    data = json.load(f)
    info = {
        "version": VERSION,
        "status": "testing",
        "kicad_version": KICAD_VERSION,
        "download_sha256": DOWNLOAD_SHA256,
        "download_size": int(DOWNLOAD_SIZE),
        "download_url": DOWNLOAD_URL,
        "install_size": int(INSTALL_SIZE),
    }
    versions = data["packages"][project_index]["versions"]
    index = None
    for i, version in enumerate(versions):
        if version["version"] == VERSION:
            index = i
            break
    if index is not None:
        versions[index] = info
    else:
        versions.append(info)
    f.seek(0)
    json.dump(data, f, indent=4)
    f.truncate()

with open("packages.json", "rb") as f:
    packages_sha256 = hashlib.sha256(f.read()).hexdigest()

with open("repository.json", "r+", encoding="utf-8") as f:
    data = json.load(f)
    date = dt.utcnow()
    data["packages"]["sha256"] = packages_sha256
    data["packages"]["update_time_utc"] = date.strftime("%Y-%m-%d %H:%M:%S")
    data["packages"]["update_timestamp"] = int(time.mktime(date.timetuple()))
    f.seek(0)
    json.dump(data, f, indent=4)
    f.truncate()
