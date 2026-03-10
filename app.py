from flask import Flask, render_template, request
import os
import hashlib
import subprocess

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

stored_hash = ""
stored_file = ""

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/encrypt", methods=["POST"])
def encrypt():
    file = request.files["file"]
    password = request.form["password"]

    filepath = os.path.join("uploads", file.filename)
    file.save(filepath)

    encrypted_file = filepath + ".enc"

    subprocess.run([
        "openssl", "enc", "-aes-256-cbc", "-pbkdf2",
        "-salt", "-in", filepath,
        "-out", encrypted_file,
        "-pass", f"pass:{password}"
    ])

    # Generate SHA256 hash
    sha256_hash = hashlib.sha256()
    with open(encrypted_file, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)

    hash_value = sha256_hash.hexdigest()

    # Save hash to file
    hash_file = encrypted_file + ".hash"
    with open(hash_file, "w") as f:
        f.write(hash_value)

    return render_template("result.html",
                           hash_value=hash_value,
                           encrypted_file=encrypted_file)


@app.route("/decrypt", methods=["POST"])
def decrypt():
    password = request.form["password"]
    encrypted_file = request.form["encrypted_file"]

    # Read stored hash
    hash_file = encrypted_file + ".hash"

    if not os.path.exists(hash_file):
        return render_template("error.html", error_message="Hash file not found!")

    with open(hash_file, "r") as f:
        stored_hash = f.read().strip()

    # Recalculate current hash
    sha256_hash = hashlib.sha256()
    with open(encrypted_file, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)

    current_hash = sha256_hash.hexdigest()

    if current_hash != stored_hash:
        return render_template("tampered.html")

    decrypted_file = encrypted_file.replace(".enc", "_decrypted.txt")

    # Attempt to decrypt
    result = subprocess.run([
        "openssl", "enc", "-d", "-aes-256-cbc", "-pbkdf2",
        "-in", encrypted_file,
        "-out", decrypted_file,
        "-pass", f"pass:{password}"
    ], capture_output=True, text=True)

    # Check if decryption failed
    if result.returncode != 0:
        return render_template("password_error.html")

    try:
        with open(decrypted_file, "r", encoding="utf-8") as f:
            content = f.read()
    except UnicodeDecodeError:
        return render_template("password_error.html")

    return render_template("success.html", content=content)


if __name__ == "__main__":
    # bind to 0.0.0.0 so external browsers (or host machine) can connect
    # also allow overriding port via environment variable
    port = int(os.environ.get("PORT", 5000))
    host = "0.0.0.0"
    url = f"http://127.0.0.1:{port}/"

    print("\n=== Flask crypto_project starting ===")
    print(f"* accessible locally via {url}")
    print(f"* accessible from other machines on this network via http://<this-host-ip>:{port}/")

    # attempt to open the default browser on startup (may fail on headless systems)
    try:
        import webbrowser, threading, time
        def _open():
            time.sleep(1)
            webbrowser.open(url)
        threading.Thread(target=_open, daemon=True).start()
    except Exception as e:
        print("could not automatically launch browser:", e)

    app.run(host=host, port=port, debug=True)

