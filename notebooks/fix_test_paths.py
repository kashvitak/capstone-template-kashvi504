import json
from pathlib import Path

nb_path = Path(r"c:\Users\Kashvi Tak\OneDrive\Desktop\capstone\capstone-template-kashvi504\notebooks\invention_assistant_demo.ipynb")

with open(nb_path, "r", encoding="utf-8") as f:
    nb = json.load(f)

# Fix the test execution cell
for cell in nb["cells"]:
    if cell.get("id") == "40b95180":
        cell["source"] = [
            "import subprocess, sys\n",
            "def run_test(path):\n",
            "    print('Running test:', path)\n",
            "    proc = subprocess.run([sys.executable, path], capture_output=True, text=True)\n",
            "    print(proc.stdout)\n",
            "    if proc.returncode != 0:\n",
            "        print('Test failed:', proc.stderr)\n",
            "\n",
            "run_test(str(repo_root / 'tests/test_schema.py'))\n",
            "run_test(str(repo_root / 'tests/test_integration.py'))"
        ]
        break

with open(nb_path, "w", encoding="utf-8") as f:
    json.dump(nb, f, indent=1)

print("Fixed test paths in notebook.")
