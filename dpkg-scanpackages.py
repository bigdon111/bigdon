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
            
            # Extract control file using dpkg-deb
            try:
                control_data = subprocess.check_output(
                    f"dpkg-deb -f '{deb_path}'",
                    shell=True,
                    text=True
                )
            except subprocess.CalledProcessError:
                print(f"Error extracting control data from {filename}, skipping...")
                continue
            
            # Add SileoDepiction and ModernDepiction if missing
            if "SileoDepiction: " not in control_data:
                control_data += "\nSileoDepiction: https://bigdon111.github.io/bigdon/sileo-depiction.json"
            if "ModernDepiction: " not in control_data:
                control_data += "\nModernDepiction: https://bigdon111.github.io/bigdon/sileo-depiction.json"
            if "Icon: " not in control_data:
                control_data += "\nIcon: https://bigdon111.github.io/bigdon/CydiaIcon.png"
            
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
