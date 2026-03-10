# File Encryption and Tamper Detection System
# Overview

This project demonstrates a secure file encryption and decryption system with tamper detection using OpenSSL cryptographic tools.

The system allows a user to:

- Encrypt files securely using a password
- Decrypt files using the same password
- Detect if the encrypted file has been tampered or modified

If any changes are made to the encrypted file, the system will detect the modification and prevent successful decryption.

This project was implemented and tested in a Linux (Ubuntu) environment using OpenSSL.

# Features

- Secure AES-256 encryption
- Password-based encryption
- File integrity verification
- Tamper detection demonstration
- Command-line based implementation
- Lightweight and easy to run

# Technologies Used
- Linux (Ubuntu)
- OpenSSL
- Bash / Shell Commands
- VirtualBox
- VS Code (Remote SSH for development)

# Project Workflow

The system follows this process:

Input File
    │
    ▼
Encryption using OpenSSL
    │
    ▼
Encrypted File (.enc)
    │
    ├── Decrypt using correct password → Original File Restored
    │
    └── Tamper Encrypted File → Decryption Fails
    
# Installation

## Install OpenSSL
Most Linux systems already include OpenSSL. If not:

sudo apt update
sudo apt install openssl

## Usage
### Encrypt a File
openssl enc -aes-256-cbc -salt -in input.txt -out encrypted.enc

You will be prompted to enter a password.

### Decrypt the File
openssl enc -aes-256-cbc -d -in encrypted.enc -out decrypted.txt

Enter the same password used during encryption.

### Tampering Demonstration
To simulate file tampering:

echo "tampered data" >> encrypted.enc

Now attempt to decrypt again:

openssl enc -aes-256-cbc -d -in encrypted.enc -out decrypted.txt

The system will produce an error, indicating that the encrypted file has been modified or corrupted.

# Example
### Successful Decryption
Password entered correctly
File decrypted successfully
### Tampered File
bad decrypt
error reading input file

This shows that any modification to the encrypted file breaks decryption, proving tamper detection.

# Project Structure
file-encryption-project
│
├── input.txt
├── encrypted.enc
├── decrypted.txt
├── README.md

# Demo Scenario
1. Encrypt a file using a password
2. Decrypt the file successfully
3. Modify the encrypted file manually
4. Attempt decryption again
5. System detects tampering and fails

# Future Improvements
- Web-based UI for encryption and decryption
- File upload interface
- Hash-based integrity verification
- Digital signature verification
- Automated tamper detection alerts
