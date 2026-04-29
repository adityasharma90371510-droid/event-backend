import os
import openpyxl
import re

# -----------------------------
# FILE PATH
# -----------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
EXCEL_FILE = os.path.join(BASE_DIR, "registrations.xlsx")


# -----------------------------
# SAVE TO EXCEL (NAME ONLY)
# -----------------------------
def save_to_excel(data):
    
    try:
        if not os.path.exists(EXCEL_FILE):
            wb = openpyxl.Workbook()
            ws = wb.active
            ws.title = "Registrations"

            ws.append(["ID", "Name"])
            wb.save(EXCEL_FILE)

        wb = openpyxl.load_workbook(EXCEL_FILE)
        ws = wb.active

        ws.append([
            data.get("id"),
            data.get("name")
        ])

        wb.save(EXCEL_FILE)

        print("✅ Excel saved at:", EXCEL_FILE)

    except Exception as e:
        print("❌ Excel Error:", e)


# -----------------------------
# NORMALIZE TEXT (ANTI-BYPASS)
# -----------------------------
def normalize_text(text):
    text = text.lower()

    replacements = {
        "0": "o",
        "1": "i",
        "3": "e",
        "4": "a",
        "5": "s",
        "7": "t",
        "@": "a",
        "$": "s"
    }

    for k, v in replacements.items():
        text = text.replace(k, v)

    # remove all non-alphanumeric
    text = re.sub(r'[^a-z0-9]', '', text)

    return text


# -----------------------------
# BANNED WORDS LIST (FIXED)
# -----------------------------
def load_banned_words():
    return [
        # English
        "fuck", "shit", "bitch", "asshole", "bastard",
        "dick", "pussy", "slut", "whore", "mf", "motherfucker",
        "ass", "nigga", "nigger",

        # Hindi
        "bc", "bhenchod", "behenchod",
        "mc", "madarchod",
        "chutiya", "chut", "gandu",
        "randi", "kutti", "kamine", "harami",
        "bhomsadike", "bhosadike", "raand",
        "randikabachcha", "chutmarika",

        # Variations
        "bsdk", "bkl", "lodu", "lawda"
    ]


# -----------------------------
# GUEST LIST (MIN 100 LOGIC)
# -----------------------------
def load_guest_names():
    return [
        "Aarav", "Vivaan", "Aditya", "Krishna",
        "Ananya", "Riya", "Isha", "Diya",
        "Kabir", "Arjun", "Rahul", "Neha",
        "Saanvi", "Meera", "Aryan", "Kunal",
        "Sneha", "Tanya", "Rohan", "Priya"
    ]