import os
import re
import tkinter as tk
from tkinter import filedialog, messagebox

# Expected ranks & suits
ranks = ["2","3","4","5","6","7","8","9","10",
         "jack","queen","king","ace"]

suits = ["hearts","diamonds","clubs","spades"]

def normalize_name(filename):
    name, ext = os.path.splitext(filename.lower())

    name = name.replace(" ", "_").replace("-", "_")
    name = re.sub(r"[^a-z0-9_]", "", name)

    found_rank = None
    found_suit = None

    for r in ranks:
        if r in name:
            found_rank = r
            break

    for s in suits:
        if s in name:
            found_suit = s
            break

    if found_rank and found_suit:
        return f"{found_rank}_of_{found_suit}{ext}"
    else:
        return None

def rename_cards_gui():
    folder = filedialog.askdirectory(title="Select your Cards Folder")

    if not folder:
        return

    files = os.listdir(folder)
    renamed = 0
    failed = []

    for file in files:
        old_path = os.path.join(folder, file)

        if not os.path.isfile(old_path):
            continue

        new_name = normalize_name(file)

        if new_name:
            new_path = os.path.join(folder, new_name)
            if old_path != new_path:
                os.rename(old_path, new_path)
                renamed += 1
        else:
            failed.append(file)

    msg = f"✅ Renamed {renamed} cards successfully!\n"

    if failed:
        msg += "\n⚠️ Could not auto-detect:\n" + "\n".join(failed[:10])
        msg += "\n\n(First 10 shown)"

    messagebox.showinfo("Done", msg)

# GUI Window
root = tk.Tk()
root.title("Card Renamer")
root.geometry("350x200")

tk.Label(root, text="♠️ Auto Rename Playing Cards ♠️",
         font=("Arial", 12, "bold")).pack(pady=20)

tk.Button(root, text="Select Cards Folder & Rename",
           command=rename_cards_gui, width=30).pack(pady=20)

root.mainloop()
