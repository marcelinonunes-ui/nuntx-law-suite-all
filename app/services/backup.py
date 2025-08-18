import os, datetime as dt, shutil, subprocess
def run_backup(db_uri: str, dest_dir: str = "backups"):
    os.makedirs(dest_dir, exist_ok=True)
    stamp = dt.datetime.utcnow().strftime("%Y%m%d-%H%M%S")
    target = os.path.join(dest_dir, f"backup-{stamp}.sql")
    try:
        subprocess.check_call(["pg_dump", db_uri, "-f", target])
    except Exception as e:
        with open(target, "w", encoding="utf-8") as f: f.write(f"-- backup failed: {e}\n")
    return target
