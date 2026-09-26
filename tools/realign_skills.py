import os
import shutil
import time

base = r"d:\Project\DIGITAL_EVIDENCE\_skills"
only_dir = os.path.join(base, "Only")
name_dir = os.path.join(base, "Name")
consistent_dir = os.path.join(base, "Consistent")
temp_dir = os.path.join(base, "_Temp_Corroborated")

print("Starting safe rename...")
# 1. Move Only -> Consistent
if os.path.exists(only_dir):
    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir)
    shutil.copytree(only_dir, temp_dir)
    shutil.rmtree(only_dir)
    shutil.copytree(temp_dir, consistent_dir)
    shutil.rmtree(temp_dir)
    print("Moved old Only -> Consistent")

# 2. Move Name -> Only
if os.path.exists(name_dir):
    shutil.copytree(name_dir, only_dir)
    shutil.rmtree(name_dir)
    print("Moved Name -> Only")

print("Rename complete successfully!")
