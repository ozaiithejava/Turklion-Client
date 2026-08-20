import json
import shutil
import os
import subprocess
import sys

repo_dir = r"F:\projelerim\Turklion-Client"
desktop_jar = r"C:\Users\ozaii\Desktop\Turklion.jar"
repo_jar = os.path.join(repo_dir, "turklion.jar")
version_file = os.path.join(repo_dir, "version.json")

print("=> Turklion.jar masaustunden kopyalaniyor...")
if not os.path.exists(desktop_jar):
    print("HATA: Masaustunde Turklion.jar bulunamadi!")
    sys.exit(1)

shutil.copy2(desktop_jar, repo_jar)

print("=> versiyon okunuyor...")
with open(version_file, "r", encoding="utf-8") as f:
    data = json.load(f)

current_version = data["jar_version"]
parts = current_version.split(".")
parts[-1] = str(int(parts[-1]) + 1)
new_version = ".".join(parts)
data["jar_version"] = new_version
data["jar_url"] = "https://github.com/ozaiithejava/Turklion-Client/raw/main/turklion.jar"

with open(version_file, "w", encoding="utf-8") as f:
    json.dump(data, f, separators=(', ', ': '))

print(f"=> Versiyon guncellendi: {current_version} -> {new_version}")

print("=> Github'a yukleniyor...")
os.chdir(repo_dir)

subprocess.run(["git", "add", "turklion.jar", "version.json"])
subprocess.run(["git", "commit", "-m", f"Auto-update jar to {new_version}"])
res = subprocess.run(["git", "push", "origin", "main"])

if res.returncode == 0:
    print("\n==========================================")
    print(f"BASARILI! Turklion v{new_version} basariyla yayinlandi.")
    print("==========================================")
else:
    print("\n[HATA] Push basarisiz oldu! Githup baglantini kontrol et.")
