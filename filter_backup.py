import json

with open("data_backup.json", "r") as f:
    data = json.load(f)

# Filter out ContentType and other framework objects
filtered = [item for item in data if item["model"] not in ["contenttypes.contenttype", "admin.logentry", "sessions.session"]]

with open("data_backup_filtered.json", "w") as f:
    json.dump(filtered, f, indent=2)

print(f"Filtered {len(data)} items down to {len(filtered)}")
