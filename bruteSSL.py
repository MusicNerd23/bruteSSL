#!/usr/bin/env python3
import argparse
import subprocess
import sys
import os

# Set up argparse for command-line flags
parser = argparse.ArgumentParser(description="Brute-force an OpenSSL-encrypted file.")
parser.add_argument("-e", "--encrypted", required=True, help="Path to the encrypted file")
parser.add_argument("-w", "--wordlist", required=True, help="Path to the password list file")
parser.add_argument("-o", "--output", default="decrypted.txt", help="Name of the decrypted output file")
parser.add_argument("-i", "--iterations", default="100000", help="PBKDF2 iterations (default: 100000)")
parser.add_argument("-v", "--verbose", action="store_true", help="Enable verbose mode")

args = parser.parse_args()

# Define output directory
output_dir = "bruteforce-output"
output_path = os.path.join(output_dir, args.output)

# Create output directory if it doesn't exist
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Read the wordlist
try:
    with open(args.wordlist, "r") as f:
        passwords = f.read().splitlines()
except FileNotFoundError:
    print(f"[❌] Wordlist file '{args.wordlist}' not found!")
    exit(1)

print(f"[🔄] Brute-forcing {args.encrypted} with {len(passwords)} passwords...\n")

# Attempt decryption with each password
for index, password in enumerate(passwords, start=1):
    # Live update for each attempt
    sys.stdout.write(f"\r[🔄] Trying password {index}/{len(passwords)}... ")
    sys.stdout.flush()

    if args.verbose:
        print(f"({password})", end="")

    # Run OpenSSL decryption attempt
    result = subprocess.run(
        ["openssl", "enc", "-aes-256-cbc", "-d", "-salt", "-iter", args.iterations,
         "-pbkdf2", "-in", args.encrypted, "-out", output_path, "-pass", f"pass:{password}"],
        stderr=subprocess.PIPE, stdout=subprocess.PIPE
    )

    # Check if decryption was successful
    if result.returncode == 0:
        sys.stdout.write("\n")
        print(f"\n[✅] SUCCESS! Password found: {password}")
        print(f"[📂] Decrypted file saved in: {output_path}")
        exit(0)

# If no password worked
sys.stdout.write("\n")
print("[❌] No valid password found.")