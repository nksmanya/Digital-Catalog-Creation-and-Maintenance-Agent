import tkinter as tk
from tkinter import ttk

# Create main window
root = tk.Tk()
root.title("Catalog Whisperer")
root.geometry("800x600")
root.configure(bg="white")

# App Bar
app_bar = tk.Frame(root, bg="green", height=60)
app_bar.pack(fill=tk.X)

icon = tk.Label(app_bar, text="★", fg="white", bg="green", font=("Arial", 16))
icon.pack(side=tk.LEFT, padx=10, pady=10)

title_frame = tk.Frame(app_bar, bg="green")
title_frame.pack(side=tk.LEFT)

title = tk.Label(title_frame, text="Catalog Whisperer", fg="white", bg="green", font=("Times New Roman", 16, "bold"))
subtitle = tk.Label(title_frame, text="कैटलॉग व्हिस्परर", fg="white", bg="green", font=("Times New Roman", 10))
title.pack(anchor="w")
subtitle.pack(anchor="w")

language_var = tk.StringVar(value="English")
language_dropdown = ttk.Combobox(app_bar, textvariable=language_var, values=["English", "Hindi"], width=10)
language_dropdown.pack(side=tk.RIGHT, padx=10, pady=10)

rural_button = tk.Button(app_bar, text="👥 Rural Friendly", bg="lightgray")
rural_button.pack(side=tk.RIGHT, padx=10, pady=10)

# Body
body = tk.Frame(root, bg="white")
body.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

# Headings
heading = tk.Label(body, text="अपने उत्पादों को आवाज़ से जोड़ें", font=("Times New Roman", 20, "bold"), bg="white")
heading.pack(pady=(10, 5))

subheading = tk.Label(body, text="Create Professional Product Catalogs with Voice", font=("Arial", 12), fg="gray", bg="white")
subheading.pack(pady=5)

# Feature Chips
features = tk.Frame(body, bg="white")
features.pack(pady=10)

for feat in ["🔊 Voice Enabled", "🌐 Multi-language", "✨ AI Powered"]:
    chip = tk.Label(features, text=feat, relief="solid", padx=10, pady=5, bg="#F0F0F0", font=("Arial", 10))
    chip.pack(side=tk.LEFT, padx=5)

# Toggle Buttons (simulated)
toggle_frame = tk.Frame(body, bg="white")
toggle_frame.pack(pady=20)

def toggle_action(label):
    print(f"{label} selected")

for label in ["🎙 Voice", "✍ Manual", "📊 Catalog"]:
    btn = tk.Button(toggle_frame, text=label, command=lambda l=label: toggle_action(l), padx=20, pady=10)
    btn.pack(side=tk.LEFT, padx=10)

# Mic Section
mic_frame = tk.Frame(body, bg="#E8F5E9", bd=2, relief="ridge")
mic_frame.pack(pady=30, padx=50, fill=tk.X)

mic_icon = tk.Label(mic_frame, text="🎤", font=("Arial", 40), fg="green", bg="#E8F5E9")
mic_icon.pack(pady=10)

mic_text = tk.Label(mic_frame, text="बोलना शुरू करने के लिए माइक दबाएं\nTap mic to start speaking", font=("Arial", 12), bg="#E8F5E9")
mic_text.pack()

lang_chip = tk.Label(mic_frame, text="English", relief="solid", padx=10, pady=5, bg="white")
lang_chip.pack(pady=10)

# Start the GUI loop
root.mainloop()
