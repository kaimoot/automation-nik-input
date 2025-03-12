import subprocess

# Upgrade pip
subprocess.run(["python", "-m", "pip", "install", "--upgrade", "pip"])

# Dapatkan daftar paket yang perlu diperbarui
outdated_packages = subprocess.run(
    ["pip", "list", "--outdated", "--format=freeze"],
    capture_output=True,
    text=True
).stdout.splitlines()

# Perbarui setiap paket yang kedaluwarsa
for package in outdated_packages:
    package_name = package.split("==")[0]
    subprocess.run(["pip", "install", "--upgrade", package_name])

print("Semua paket telah diperbarui.")
