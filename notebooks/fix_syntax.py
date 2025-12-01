import json
from pathlib import Path

nb_path = Path(r"c:\Users\Kashvi Tak\OneDrive\Desktop\capstone\capstone-template-kashvi504\notebooks\invention_assistant_demo.ipynb")

with open(nb_path, "r", encoding="utf-8") as f:
    nb = json.load(f)

# Fix the sample inventions cell
for cell in nb["cells"]:
    if cell.get("id") == "84083c9b":
        cell["source"] = [
            "sample_inventions = [\n",
            "    {\"title\": \"Smart Water Bottle\", \"description\": \"A water bottle with integrated sensors to track hydration levels and remind users to drink water.\"},\n",
            "    {\"title\": \"Biodegradable Phone Case\", \"description\": \"A phone protective case made from 100% biodegradable materials that break down within 2 years in landfill conditions.\"},\n",
            "    {\"title\": \"AI Classroom Assistant\", \"description\": \"An AI tutor that helps students with real-time questions, note-taking, and personalized learning paths.\"},\n",
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
        break

with open(nb_path, "w", encoding="utf-8") as f:
    json.dump(nb, f, indent=1)

print("Fixed syntax errors in notebook.")
