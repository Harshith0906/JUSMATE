import fitz  # PyMuPDF
import re
import json
from collections import defaultdict

# ----------------------------
# Regex patterns (tuned for Indian Acts)
# ----------------------------
PART_PATTERN = re.compile(r"^PART\s+[IVXLC]+", re.IGNORECASE)
SECTION_PATTERN = re.compile(r"^Section\s+\d+[A-Z]?\.", re.IGNORECASE)
SUBSECTION_PATTERN = re.compile(r"^\(\d+[A-Z]?\)")
CLAUSE_PATTERN = re.compile(r"^\([a-z]\)")
ROMAN_CLAUSE_PATTERN = re.compile(r"^\([ivx]+\)", re.IGNORECASE)

# ----------------------------
# Utility functions
# ----------------------------
def clean(text):
    return re.sub(r"\s+", " ", text).strip()

def extract_lines(pdf_path):
    doc = fitz.open(pdf_path)
    lines = []
    for page in doc:
        for line in page.get_text().split("\n"):
            if line.strip():
                lines.append(clean(line))
    return lines

# ----------------------------
# Main extractor
# ----------------------------
def extract_act(pdf_path):
    lines = extract_lines(pdf_path)

    act = {
        "Act Title": "",
        "Act ID": "",
        "Enactment Date": "",
        "Act Definition": {},
        "Parts": {}
    }

    current_part = None
    current_section = None
    para_counter = 0
    part_counter = -1

    for line in lines:

        # ---- Act Title ----
        if not act["Act Title"] and "ACT" in line.upper():
            act["Act Title"] = line
            continue

        # ---- Act ID ----
        if not act["Act ID"] and "ACT NO." in line.upper():
            act["Act ID"] = line
            continue

        # ---- Enactment Date ----
        if not act["Enactment Date"] and re.search(r"\[\d{1,2}.*?\d{4}\]", line):
            act["Enactment Date"] = line
            continue

        # ---- PART ----
        if PART_PATTERN.match(line):
            part_counter += 1
            current_part = str(part_counter)

            act["Parts"][current_part] = {
                "ID": line,
                "Name": "",
                "Sections": {}
            }
            current_section = None
            continue

        # ---- PART NAME ----
        if current_part is not None and act["Parts"][current_part]["Name"] == "":
            if line.isupper() and len(line) < 80:
                act["Parts"][current_part]["Name"] = line
                continue

        # ---- SECTION ----
        if SECTION_PATTERN.match(line):
            current_section = line
            para_counter = 0

            act["Parts"][current_part]["Sections"][current_section] = {
                "heading": "",
                "paragraphs": {}
            }
            continue

        # ---- SECTION HEADING ----
        if current_section and act["Parts"][current_part]["Sections"][current_section]["heading"] == "":
            if not SUBSECTION_PATTERN.match(line):
                act["Parts"][current_part]["Sections"][current_section]["heading"] = line
                continue

        # ---- SUBSECTIONS & PARAGRAPHS ----
        if current_section:
            section = act["Parts"][current_part]["Sections"][current_section]

            # (1), (2A) style
            if SUBSECTION_PATTERN.match(line):
                section["paragraphs"][str(para_counter)] = {
                    "text": line,
                    "contains": {}
                }
                para_counter += 1
                continue

            # (a), (b) clauses
            if CLAUSE_PATTERN.match(line) or ROMAN_CLAUSE_PATTERN.match(line):
                last_para = section["paragraphs"].get(str(para_counter - 1))
                if isinstance(last_para, dict):
                    idx = str(len(last_para["contains"]))
                    last_para["contains"][idx] = line
                continue

            # Normal continuation text
            if para_counter > 0:
                last_para = section["paragraphs"].get(str(para_counter - 1))
                if isinstance(last_para, dict):
                    last_para["text"] += " " + line
                else:
                    section["paragraphs"][str(para_counter - 1)] += " " + line

    return act

# ----------------------------
# Run & Save
# ----------------------------
if __name__ == "__main__":
    pdf_path = "A2017_23.pdf"
    act_json = extract_act(pdf_path)

    with open("insurance_act.json", "w", encoding="utf-8") as f:
        json.dump(act_json, f, indent=2, ensure_ascii=False)

    print("✅ Legal Act extracted and structured successfully.")
