import re
import json
files = ["epoch96.txt", "epoch144.txt"]

modelx = 0
for file in files:
    modelx += 1
    with open(file, 'r') as f, open(f"model_{modelx}.json", 'w', encoding='utf-8') as f2:
        L = f.readlines()
        atom = {
            "context": [],
            "responses": [],
            "target": ""
        }
        for l in L:
            l = l.strip()
            m = re.match("Batch", l)
            if m is not None:
                # json.dump(atom, f2, ensure_ascii=False, indent=4)
                json.dump(atom, f2, ensure_ascii=False)
                f2.write("\n")
                atom = {
                    "context": [],
                    "responses": []
                }

            m = re.match("Context", l)
            if m is not None:
                atom["context"].append(l)
                # break

            m = re.match("Target", l)
            if m is not None:
                m = re.findall(r"Target >> (.*)", l)
                atom["target"] = m[0]

            m = re.match("Sample", l)
            if m is not None:
                m = re.findall(r"Sample [0-9]+ >> (.*)", l)
                atom["responses"].append(m[0])
