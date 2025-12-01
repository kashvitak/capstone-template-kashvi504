import json
import sys
from pathlib import Path

# Path to the notebook
notebook_path = Path(__file__).parent / "invention_assistant_demo.ipynb"

# Read the notebook
with open(notebook_path, 'r', encoding='utf-8') as f:
    notebook = json.load(f)

# New sample inventions
new_sample_inventions = [
    '    {"title": "Solar-Powered Backpack", "description": "A backpack with integrated solar panels that charges devices while you walk, perfect for hikers and students."},\n',
    '    {"title": "Smart Composting Bin", "description": "An IoT-enabled composting bin that monitors temperature, moisture, and decomposition progress, providing app notifications when compost is ready."},\n',
    '    {"title": "Voice-Activated Study Lamp", "description": "A desk lamp with voice control, adjustable color temperature, and built-in timer to help students maintain healthy study habits."},\n'
]

# Find and update the cell with sample_inventions
for cell in notebook['cells']:
    if cell['cell_type'] == 'code' and 'source' in cell:
        source_text = ''.join(cell['source'])
        if 'sample_inventions = [' in source_text:
            # Reconstruct the cell with new inventions
            new_source = [
                "sample_inventions = [\n",
                *new_sample_inventions,
                "]\n",
                "\n",
                "# Run experiments\n",
                "setup_logging(False)\n",
                "results = []\n",
                "for inv in sample_inventions:\n",
                "    print('\\nRunning:', inv['title'])\n",
                "    res = run_experiment(inv)\n",
                "    results.append((inv, res))\n",
                "    paths = save_outputs(inv.get('title', 'invention'), res)\n",
                "    print('Saved:', paths['json_path'], paths['markdown_path'])\n",
                "\n",
                "# Display brief summaries\n",
                "import json\n",
                "for inv, res in results:\n",
                "    print('\\n== Summary for:', inv['title'], '==')\n",
                "    overall = res.get('scorecard', {}).get('overall', {})\n",
                "    print('Decision:', overall.get('decision'))\n",
                "    print('Rationale:', overall.get('rationale'))"
            ]
            cell['source'] = new_source
            print("[OK] Updated sample_inventions successfully!")
            break

# Write the updated notebook back
with open(notebook_path, 'w', encoding='utf-8') as f:
    json.dump(notebook, f, indent=1)

print(f"[OK] Notebook updated: {notebook_path}")
print("\nNew sample inventions:")
print("1. Solar-Powered Backpack")
print("2. Smart Composting Bin")
print("3. Voice-Activated Study Lamp")
