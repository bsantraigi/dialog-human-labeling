import regex
import csv
import random
import os

os.system(f"rm gcp-dataset/samples/*")

files = ["epoch96.txt", "epoch144.txt"]

modelx = 0

root_gs_path = "gs://dialogue-resp-selection/gcp-dataset"

csvfile = open(f"gcp-dataset/catalog.csv", 'w') 
goldfile = open(f"gcp-dataset/gold.txt", "w")
for file in files:
    modelx += 1
    ID = 0
    with open(file, 'r') as f:
        L = f.readlines()
        atom = {
            "context": [],
            "responses": [],
            "target": ""
        }
        for l in L:
            l = l.strip()
            m = regex.match("Batch", l)
            if m is not None:
                # json.dump(atom, csvfile, ensure_ascii=False, indent=4)
                # json.dump(atom, csvfile, ensure_ascii=False)
                # csvfile.write("\n")
                if len(atom["context"]) > 1:
                    ID += 1
                    sample_name = f"M{modelx}-{ID}.txt"
                    csvfile.write(f"{root_gs_path}/samples/{sample_name}\n")
                    goldfile.write(f"{root_gs_path}/samples/{sample_name}\n")
                    
                    target = atom['target']
                    all_resp = atom["responses"]
                    z = random.randint(0,len(all_resp))
                    all_resp = all_resp[:z] + [target] + all_resp[z:]
                    

                    with open(f"gcp-dataset/samples/{sample_name}", "w") as sample_file:
                        sample_file.write("Context:\n\n")
                        sample_file.write('\n'.join(atom["context"]))
                        sample_file.write("\n\nResponse samples:\n\n")
                        # sample_file.write(f"\nResponse 0: {}\n")
                        options = random.sample(range(len(all_resp)), 3)
                        if z not in options:
                            options.append(z)

                        for ix, x in enumerate(sorted(options)):
                            r = all_resp[x]
                            sample_file.write(f"\nResponse {ix+1}: {r}\n")
                            if z == x:
                                goldfile.write(f"Gold @ {ix}\n")

                atom = {
                    "context": [],
                    "responses": [],
                    "target": ""
                }
                if ID >= 100:
                    break

            m = regex.match("Context", l)
            if m is not None:
                # print(l)
                # m = regex.findall(r"Context \d+-\d+: \('(.*)<\/s>', \d+\)", l)
                m = regex.findall(r"Context \d+-\d+: \(.(.*)<\/s>.*\)", l)
                # print(l)
                atom["context"].append(m[0])
                # break

            m = regex.match("Target", l)
            if m is not None:
                m = regex.findall(r"Target >> (.*)", l)
                atom["target"] = m[0]

            m = regex.match("Sample", l)
            if m is not None:
                m = regex.findall(r"Sample [0-9]+ >> (.*)", l)
                atom["responses"].append(m[0])

csvfile.close()
goldfile.close()
print(open("gcp-dataset/gold.txt").read())