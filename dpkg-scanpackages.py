#!/usr/bin/env python3
import os
import hashlib
import gzip
import bz2
import subprocess

# Directory containing .deb files
debs_dir = "./debs"

# Create Packages file
with open("Packages", "w") as packages_file:
    for filename in os.listdir(debs_dir):
        if filename.endswith(".deb"):
            deb_path = os.path.join(debs_dir, filename)
            
            # Get control data using ar and tar
            control_data = subprocess.check_output(
                f"ar -p '{deb_path}' control.tar.gz | tar -xzO ./control",
                shell=True,
                text=True
            )
            
            # Replace old icon path with new one
            control_data = control_data.replace("Icon: https://bigdon111.github.io/bigdon/assets/icon.png", "Icon: https://bigdon111.github.io/bigdon/CydiaIcon.png")
            
            # Add ModernDepiction if missing
            if "SileoDepiction: " in control_data and "ModernDepiction: " not in control_data:
                sileo_depiction = control_data.split("SileoDepiction: ")[1].split("\n")[0]
                control_data = control_data + "\nModernDepiction: " + sileo_depiction
            
            # Calculate MD5 and SHA checksums
            with open(deb_path, "rb") as f:
                data = f.read()
                md5 = hashlib.md5(data).hexdigest()
                sha1 = hashlib.sha1(data).hexdigest()
                sha256 = hashlib.sha256(data).hexdigest()
            
            # Get file size
            size = os.path.getsize(deb_path)
            
            # Write package information
            packages_file.write(control_data.strip() + "\n")
            packages_file.write(f"Filename: debs/{filename}\n")
            packages_file.write(f"Size: {size}\n")
            packages_file.write(f"MD5sum: {md5}\n")
            packages_file.write(f"SHA1: {sha1}\n")
            packages_file.write(f"SHA256: {sha256}\n\n")

# Create compressed versions
with open("Packages", "rb") as f:
    data = f.read()
    with gzip.open("Packages.gz", "wb") as gz:
        gz.write(data)
    with bz2.open("Packages.bz2", "wb") as bz:
        bz.write(data)

print("Generated Packages, Packages.gz, and Packages.bz2 files")
