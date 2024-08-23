import tkinter as tk
from tkinter import scrolledtext, messagebox
from tkinter.filedialog import asksaveasfilename
from storage_analyzer import get_disk_usage, analyze_directory, find_large_files, save_to_excel
from cleaner import remove_temp_files, clean_apt_cache, remove_old_kernels, clean_snap_cache, clean_journal_logs

class StorageCleanerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Ubuntu Storage Cleaner")
        self.root.geometry("700x600")

        self.create_widgets()

    def create_widgets(self):
        # Disk Usage Button
        self.disk_usage_button = tk.Button(self.root, text="Disk Usage Analysis", command=self.show_disk_usage)
        self.disk_usage_button.pack(pady=10)

        # Directory Analysis Button
        self.dir_analysis_button = tk.Button(self.root, text="Analyze and Categorize Files", command=self.show_directory_analysis)
        self.dir_analysis_button.pack(pady=10)

        # Largest Files Button
        self.large_files_button = tk.Button(self.root, text="Show Largest Files", command=self.show_large_files)
        self.large_files_button.pack(pady=10)

        # Save to Excel Button
        self.save_button = tk.Button(self.root, text="Save Analysis to Excel", command=self.save_to_excel)
        self.save_button.pack(pady=10)

        # Cleanup Button
        self.cleanup_button = tk.Button(self.root, text="Clean Up System", command=self.cleanup_system)
        self.cleanup_button.pack(pady=10)

        # Output Display
        self.output_display = scrolledtext.ScrolledText(self.root, wrap=tk.WORD, width=80, height=20)
        self.output_display.pack(pady=10)

    def show_disk_usage(self):
        usage = get_disk_usage()
        self.output_display.delete(1.0, tk.END)
        self.output_display.insert(tk.INSERT, f"Disk Usage Analysis:\nTotal: {usage['total']} GB, Used: {usage['used']} GB, Free: {usage['free']} GB, Percent Used: {usage['percent']}%\n")

    def show_directory_analysis(self):
        categorized_files = analyze_directory('/')
        self.output_display.delete(1.0, tk.END)
        for category, files in categorized_files.items():
            if files:  # Check if there are files in the category
                self.output_display.insert(tk.INSERT, f"{category} Files:\n")
                for file, size in sorted(files, key=lambda x: x[1], reverse=True):
                    self.output_display.insert(tk.INSERT, f"{file} - {round(size / (2**20), 2)} MB\n")
                self.output_display.insert(tk.INSERT, "\n")

    def show_large_files(self):
        large_files = find_large_files('/')
        self.output_display.delete(1.0, tk.END)
        self.output_display.insert(tk.INSERT, f"Top 20 Largest Files:\n{large_files}\n")

    def save_to_excel(self):
        file_path = asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel files", "*.xlsx")])
        if file_path:
            categorized_files = analyze_directory('/')
            disk_usage = get_disk_usage()
            save_to_excel(categorized_files, disk_usage, file_path)
            messagebox.showinfo("Saved", f"Analysis saved to {file_path}")

    def cleanup_system(self):
        self.output_display.delete(1.0, tk.END)
        self.output_display.insert(tk.INSERT, "Cleaning up the system...\n")
        remove_temp_files()
        clean_apt_cache()
        remove_old_kernels()
        clean_snap_cache()
        clean_journal_logs()
        self.output_display.insert(tk.INSERT, "Cleanup completed.\n")
        messagebox.showinfo("Cleanup", "System cleanup completed!")

if __name__ == "__main__":
    root = tk.Tk()
    app = StorageCleanerApp(root)
    root.mainloop()
