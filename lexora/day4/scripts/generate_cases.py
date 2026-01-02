import json
import random

convicted_templates = [
    "The accused fraudulently transferred money by impersonating the victim through online platforms.",
    "Digital evidence confirmed unauthorized access to the victim's financial accounts.",
    "The accused created fake profiles and cheated multiple individuals through online transactions.",
    "Cyber forensic reports established the involvement of the accused in online fraud.",
    "The accused impersonated a government official and deceived victims for financial gain."
]

acquitted_templates = [
    "The prosecution failed to establish a direct link between the accused and the alleged offense.",
    "Digital evidence presented was inconclusive and insufficient to prove guilt.",
    "Witnesses turned hostile and no corroborative evidence was produced.",
    "The accused was named in the complaint but no technical evidence supported the allegations.",
    "Procedural lapses weakened the prosecution's case beyond reasonable doubt."
]

charge_sets = [
    ["IPC 420"],
    ["IPC 420", "IT Act 66D"],
    ["IT Act 66C"],
    ["IPC 419", "IPC 420"],
    ["IT Act 43", "IPC 506"]
]

cases = []
case_id = 1

# Generate convicted cases
for _ in range(100):
    cases.append({
        "case_id": f"C{case_id:03}",
        "facts": random.choice(convicted_templates),
        "charges": random.choice(charge_sets),
        "outcome": "convicted"
    })
    case_id += 1

# Generate acquitted cases
for _ in range(100):
    cases.append({
        "case_id": f"C{case_id:03}",
        "facts": random.choice(acquitted_templates),
        "charges": random.choice(charge_sets),
        "outcome": "acquitted"
    })
    case_id += 1

# Shuffle dataset
random.shuffle(cases)

# Save to file
output_path = "../data/cases_raw/cases.json"
with open(output_path, "w") as f:
    json.dump(cases, f, indent=2)

print(f"✅ Generated {len(cases)} cases and saved to {output_path}")
