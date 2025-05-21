# tests/test_cli.py
import subprocess

def run_cli(command):
    process = subprocess.Popen(
        ["python", "cli.py", command],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    stdout, stderr = process.communicate()
    print(f"\n=== CLI ({command}) STDOUT ===\n{stdout}")
    print(f"=== CLI ({command}) STDERR ===\n{stderr}")
    return stdout.strip()

def test_cli_random():
    out = run_cli("random")
    assert "http" in out or "Cats" in out or "🐱" in out

def test_cli_vote():
    out = run_cli("vote")
    assert "Success" in out or "Error" in out

def test_cli_top():
    out = run_cli("top")
    assert "http" in out or "❤️" in out

def test_cli_log():
    out = run_cli("log")
    assert "http" in out or "🐈" in out or "timestamp" in out
