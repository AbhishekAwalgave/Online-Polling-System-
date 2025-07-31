# Final update: Implemented GUI-based Online Polling System with vote recording and result visualization

import tkinter as tk
from tkinter import messagebox
import pandas as pd
import matplotlib.pyplot as plt
import os

# Candidate list
CANDIDATES = ["Ajay", "Yash", "Om", "Abhi"]
VOTE_FILE = "votes.csv"

# Global list to store button references
vote_buttons = []

# Initialize vote file
def initialize_vote_file():
    df = pd.DataFrame(columns=["Candidate"])
    df.to_csv(VOTE_FILE, index=False)

# Create poll (enable voting)
def create_poll():
    if os.path.exists(VOTE_FILE):
        os.remove(VOTE_FILE)
    initialize_vote_file()
    for btn in vote_buttons:
        btn.config(state="normal")
    messagebox.showinfo("🗳️ Poll Created", "Poll has been created. Voting is now enabled!")

# Record vote
def record_vote(candidate):
    if not os.path.exists(VOTE_FILE):
        messagebox.showwarning("⚠️ Poll Not Created", "Please create the poll before voting.")
        return
    df = pd.read_csv(VOTE_FILE)
    df = pd.concat([df, pd.DataFrame([{"Candidate": candidate}])], ignore_index=True)
    df.to_csv(VOTE_FILE, index=False)
    messagebox.showinfo("✅ Vote Recorded", "Your vote has been successfully recorded!")

# Show results with histogram
def show_results():
    if not os.path.exists(VOTE_FILE):
        messagebox.showinfo("📊 Result", "Poll not created yet.")
        return
    df = pd.read_csv(VOTE_FILE)
    if df.empty:
        messagebox.showinfo("📊 Result", "No votes yet.")
        return

    vote_counts = df["Candidate"].value_counts()
    result_df = vote_counts.reset_index()
    result_df.columns = ["Candidate", "Votes"]
    result_df.to_csv("votes.csv", index=False)

    plt.figure(figsize=(6, 5))
    bars = plt.bar(result_df["Candidate"], result_df["Votes"], color="skyblue", edgecolor="black")
    plt.title("Vote Distribution", fontsize=14)
    plt.xlabel("Candidates", fontsize=12)
    plt.ylabel("Number of Votes", fontsize=12)
    plt.grid(False)

    max_votes = result_df["Votes"].max()
    step = 1
    if max_votes > 10:
        step = 5
    elif max_votes > 5:
        step = 2
    plt.yticks(range(0, max_votes + step + 1, step))

    plt.tight_layout()
    plt.show()

# Reset votes manually
def reset_votes():
    try:
        if os.path.exists(VOTE_FILE):
            os.remove(VOTE_FILE)
        initialize_vote_file()
        for btn in vote_buttons:
            btn.config(state="disabled")
        messagebox.showinfo("🔁 Reset", "All votes have been reset successfully.")
    except Exception as e:
        messagebox.showerror("❌ Error", f"Could not reset votes:\n{str(e)}")

# Exit app
def exit_app():
    root.destroy()

# Tkinter UI
root = tk.Tk()
root.title("🗳️ Online Polling System")
root.geometry("400x550")

tk.Label(root, text="Vote for Your Candidate", font=("Arial", 14)).pack(pady=10)

# Create Poll Button
tk.Button(root, text="🆕 Create Poll", command=create_poll,
          bg="green", fg="white", font=("Arial", 11)).pack(pady=10)

# Candidate vote buttons (initially disabled)
for candidate in CANDIDATES:
    btn = tk.Button(root, text=candidate, width=25, height=2,
                    command=lambda c=candidate: record_vote(c),
                    state="disabled")
    btn.pack(pady=5)
    vote_buttons.append(btn)

tk.Button(root, text="📊 Show Result", command=show_results,
          bg="lightblue", font=("Arial", 11)).pack(pady=10)

tk.Button(root, text="🔁 Reset Votes", command=reset_votes,
          bg="orange", font=("Arial", 11)).pack(pady=10)

tk.Button(root, text="🚪 Exit", command=exit_app,
          bg="red", fg="white", font=("Arial", 11)).pack(pady=10)

root.mainloop()





















