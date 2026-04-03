import subprocess
import sys

result = subprocess.run(
    [r"c:\Users\zship\dev\python\rpgnlp\.venv\Scripts\python.exe", "-m", "unittest", "tests.test_engine"],
    capture_output=True,
    text=True,
    cwd=r"c:\Users\zship\dev\python\rpgnlp"
)
print("=== STDOUT ===")
print(result.stdout)
print("=== STDERR ===")
print(result.stderr)
print("=== RETURN CODE ===")
print(result.returncode)
