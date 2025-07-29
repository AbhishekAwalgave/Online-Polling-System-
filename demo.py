import tkinter as tk
from tkinter import messagebox
import pandas as pd
import matplotlib.pyplot as plt
import os
import sys

# Candidate list
CANDIDATES = ["Ajay", "Yash", "Om", "Abhi"]
VOTE_FILE = "votes.csv"

# Initialize vote file if not exists
def initialize_vote_file():
    if not os.path.exists(VOTE_FILE):
        df = pd.DataFrame(columns=["Candidate"])
        df.to_csv(VOTE_FILE, index=False)

initialize_vote_file()

# Record vote
def record_vote(candidate):
    df = pd.read_csv(VOTE_FILE)
    df = pd.concat([df, pd.DataFrame([{"Candidate": candidate}])], ignore_index=True)
    df.to_csv(VOTE_FILE, index=False)
    messagebox.showinfo("✅ Vote Recorded", "✅ Your response has been successfully recorded!")

# Show results with histogram
def show_results():
    df = pd.read_csv(VOTE_FILE)
    if df.empty:
        messagebox.showinfo("📊 Result", "No votes yet.")
        return

    vote_counts = df["Candidate"].value_counts()
    result_df = vote_counts.reset_index()
    result_df.columns = ["Candidate", "Votes"]
    result_df.to_csv("votes.csv", index=False)  # Overwrite with summary

    # Plot histogram
    plt.figure(figsize=(6, 5))
    bars = plt.bar(result_df["Candidate"], result_df["Votes"], color="skyblue", edgecolor="black")

    plt.title("Vote Distribution", fontsize=14)
    plt.xlabel("Candidates", fontsize=12)
    plt.ylabel("Number of Votes", fontsize=12)
    plt.grid(False)

    # Whole number y-axis
    max_votes = result_df["Votes"].max()
    step = 1
    if max_votes > 10:
        step = 5
    elif max_votes > 5:
        step = 2
    plt.yticks(range(0, max_votes + step + 1, step))

    plt.tight_layout()
    plt.show()

# Reset vote file
def reset_votes():
    try:
        if os.path.exists(VOTE_FILE):
            os.remove(VOTE_FILE)
        initialize_vote_file()
        messagebox.showinfo("🔁 Reset", "All votes have been reset successfully.")
    except Exception as e:
        messagebox.showerror("❌ Error", f"Could not reset votes:\n{str(e)}")

# Exit app
def exit_app():
    root.destroy()

# Tkinter UI
root = tk.Tk()
root.title("🗳️ Online Polling System")
root.geometry("400x500")

tk.Label(root, text="Vote for Your Candidate", font=("Arial", 14)).pack(pady=10)

for candidate in CANDIDATES:
    tk.Button(root, text=candidate, width=25, height=2,
              command=lambda c=candidate: record_vote(c)).pack(pady=5)

tk.Button(root, text="Show Result", command=show_results,
          bg="lightblue", font=("Arial", 11)).pack(pady=10)

tk.Button(root, text="🔁 Reset Votes", command=reset_votes,
          bg="orange", font=("Arial", 11)).pack(pady=10)

tk.Button(root, text="🚪 Exit", command=exit_app,
          bg="red", fg="white", font=("Arial", 11)).pack(pady=10)

root.mainloop()



















