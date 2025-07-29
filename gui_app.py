#!/usr/bin/env python3
"""
GUI application for MSG to EML converter.
A simple drag-and-drop interface for converting MSG files.
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import threading
from pathlib import Path
import sys
import os

# Add src to path so we can import our module
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

from msg_to_eml import convert_msg_to_eml, batch_convert


class MSGToEMLApp:
    def __init__(self, root):
        self.root = root
        self.root.title("MSG to EML Converter")
        self.root.geometry("600x500")
        self.root.resizable(True, True)

        # Set app icon (optional)
        try:
            # You can add an icon file later
            pass
        except:
            pass

        self.setup_ui()

    def setup_ui(self):
        # Main frame
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)

        # Title
        title_label = ttk.Label(main_frame, text="MSG to EML Converter", font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))

        # AI attribution
        ai_label = ttk.Label(main_frame, text="🤖 This app was completely created by AI", font=("Arial", 10), foreground="gray")
        ai_label.grid(row=1, column=0, columnspan=3, pady=(0, 20))

        # Single file conversion section
        single_frame = ttk.LabelFrame(main_frame, text="Convert Single File", padding="10")
        single_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        single_frame.columnconfigure(1, weight=1)

        ttk.Label(single_frame, text="MSG File:").grid(row=0, column=0, sticky=tk.W, padx=(0, 10))
        self.single_input = ttk.Entry(single_frame, width=50)
        self.single_input.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(0, 10))
        ttk.Button(single_frame, text="Browse", command=self.browse_single_input).grid(row=0, column=2)

        ttk.Label(single_frame, text="Output EML:").grid(row=1, column=0, sticky=tk.W, padx=(0, 10), pady=(10, 0))
        self.single_output = ttk.Entry(single_frame, width=50)
        self.single_output.grid(row=1, column=1, sticky=(tk.W, tk.E), padx=(0, 10), pady=(10, 0))
        ttk.Button(single_frame, text="Browse", command=self.browse_single_output).grid(row=1, column=2, pady=(10, 0))

        ttk.Button(single_frame, text="Convert File", command=self.convert_single).grid(row=2, column=1, pady=(15, 0))

        # Batch conversion section
        batch_frame = ttk.LabelFrame(main_frame, text="Convert Multiple Files (Batch)", padding="10")
        batch_frame.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(10, 0))
        batch_frame.columnconfigure(1, weight=1)

        ttk.Label(batch_frame, text="Input Folder:").grid(row=0, column=0, sticky=tk.W, padx=(0, 10))
        self.batch_input = ttk.Entry(batch_frame, width=50)
        self.batch_input.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(0, 10))
        ttk.Button(batch_frame, text="Browse", command=self.browse_batch_input).grid(row=0, column=2)

        ttk.Label(batch_frame, text="Output Folder:").grid(row=1, column=0, sticky=tk.W, padx=(0, 10), pady=(10, 0))
        self.batch_output = ttk.Entry(batch_frame, width=50)
        self.batch_output.grid(row=1, column=1, sticky=(tk.W, tk.E), padx=(0, 10), pady=(10, 0))
        self.batch_output_button = ttk.Button(batch_frame, text="Browse", command=self.browse_batch_output)
        self.batch_output_button.grid(row=1, column=2, pady=(10, 0))

        # Recursive option
        self.recursive_var = tk.BooleanVar(value=True)
        recursive_check = ttk.Checkbutton(batch_frame, text="Search subfolders recursively", variable=self.recursive_var)
        recursive_check.grid(row=2, column=0, columnspan=2, sticky=tk.W, pady=(10, 0))

        # Output location option
        self.output_next_to_original_var = tk.BooleanVar(value=False)
        output_location_check = ttk.Checkbutton(batch_frame, text="Create EML files next to original MSG files", variable=self.output_next_to_original_var, command=self.toggle_output_location)
        output_location_check.grid(row=3, column=0, columnspan=2, sticky=tk.W, pady=(5, 0))

        ttk.Button(batch_frame, text="Convert All Files", command=self.convert_batch).grid(row=4, column=1, pady=(15, 0))

        # Progress bar
        self.progress = ttk.Progressbar(main_frame, mode="indeterminate")
        self.progress.grid(row=4, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(20, 10))

        # Status text
        self.status_text = tk.Text(main_frame, height=8, width=70)
        self.status_text.grid(row=5, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))

        # Scrollbar for status text
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=self.status_text.yview)
        scrollbar.grid(row=5, column=3, sticky=(tk.N, tk.S), pady=(0, 10))
        self.status_text.configure(yscrollcommand=scrollbar.set)

        # Configure grid weights for resizing
        main_frame.rowconfigure(5, weight=1)

        # Initial status message
        self.log_message("Ready to convert MSG files to EML format!")
        self.log_message("Choose single file conversion or batch conversion for multiple files.")
        self.log_message("📁 Batch mode supports recursive directory scanning (searches subfolders).")
        self.log_message("📍 Option: Create EML files next to original MSG files or in separate folder.")

    def browse_single_input(self):
        filename = filedialog.askopenfilename(title="Select MSG file", filetypes=[("MSG files", "*.msg"), ("All files", "*.*")])
        if filename:
            self.single_input.delete(0, tk.END)
            self.single_input.insert(0, filename)
            # Auto-suggest output filename
            output_path = Path(filename).with_suffix(".eml")
            self.single_output.delete(0, tk.END)
            self.single_output.insert(0, str(output_path))

    def browse_single_output(self):
        filename = filedialog.asksaveasfilename(
            title="Save EML file as", defaultextension=".eml", filetypes=[("EML files", "*.eml"), ("All files", "*.*")]
        )
        if filename:
            self.single_output.delete(0, tk.END)
            self.single_output.insert(0, filename)

    def browse_batch_input(self):
        dirname = filedialog.askdirectory(title="Select folder containing MSG files")
        if dirname:
            self.batch_input.delete(0, tk.END)
            self.batch_input.insert(0, dirname)
            # Auto-suggest output directory
            output_dir = dirname + "_EML"
            self.batch_output.delete(0, tk.END)
            self.batch_output.insert(0, output_dir)

    def browse_batch_output(self):
        dirname = filedialog.askdirectory(title="Select output folder for EML files")
        if dirname:
            self.batch_output.delete(0, tk.END)
            self.batch_output.insert(0, dirname)

    def toggle_output_location(self):
        """Toggle the output location mode and update UI accordingly."""
        if self.output_next_to_original_var.get():
            # Disable the output folder fields when creating files next to originals
            self.batch_output.config(state="disabled")
            self.batch_output_button.config(state="disabled")
            self.log_message("📍 Mode: EML files will be created next to original MSG files")
        else:
            # Enable the output folder fields for separate output directory
            self.batch_output.config(state="normal")
            self.batch_output_button.config(state="normal")
            self.log_message("📁 Mode: EML files will be created in separate output folder")

    def log_message(self, message):
        """Add a message to the status text area."""
        self.status_text.insert(tk.END, f"{message}\n")
        self.status_text.see(tk.END)
        self.root.update_idletasks()

    def convert_single(self):
        """Convert a single MSG file."""
        input_path = self.single_input.get().strip()
        output_path = self.single_output.get().strip()

        if not input_path or not output_path:
            messagebox.showerror("Error", "Please select both input and output files.")
            return

        # Run conversion in background thread
        threading.Thread(target=self._convert_single_thread, args=(input_path, output_path), daemon=True).start()

    def _convert_single_thread(self, input_path, output_path):
        """Background thread for single file conversion."""
        try:
            self.progress.start()
            self.log_message(f"Converting: {Path(input_path).name}")

            convert_msg_to_eml(input_path, output_path)

            self.log_message(f"✅ Success: {Path(output_path).name}")
            messagebox.showinfo("Success", f"File converted successfully!\nSaved to: {output_path}")

        except Exception as e:
            error_msg = f"❌ Error: {str(e)}"
            self.log_message(error_msg)
            messagebox.showerror("Error", f"Conversion failed:\n{str(e)}")
        finally:
            self.progress.stop()

    def convert_batch(self):
        """Convert multiple MSG files."""
        input_dir = self.batch_input.get().strip()
        output_next_to_original = self.output_next_to_original_var.get()
        
        if not input_dir:
            messagebox.showerror("Error", "Please select an input folder.")
            return
            
        if not output_next_to_original:
            output_dir = self.batch_output.get().strip()
            if not output_dir:
                messagebox.showerror("Error", "Please select an output folder or check 'Create EML files next to original MSG files'.")
                return
        else:
            output_dir = None  # Will be ignored by the converter

        # Run conversion in background thread
        threading.Thread(target=self._convert_batch_thread, args=(input_dir, output_dir, output_next_to_original), daemon=True).start()

    def _convert_batch_thread(self, input_dir, output_dir, output_next_to_original):
        """Background thread for batch conversion."""
        try:
            self.progress.start()
            if output_next_to_original:
                self.log_message(f"Starting batch conversion from: {input_dir}")
                self.log_message("📍 Creating EML files next to original MSG files")
            else:
                self.log_message(f"Starting batch conversion from: {input_dir}")
                self.log_message(f"📁 Output directory: {output_dir}")

            recursive = self.recursive_var.get()
            if recursive:
                self.log_message("🔍 Searching subdirectories recursively...")

            # Use the updated batch_convert function
            stats = batch_convert(input_dir, output_dir, recursive=recursive, output_next_to_original=output_next_to_original)

            # Log detailed results
            if stats["msg_files_found"] == 0:
                self.log_message(f"❌ No MSG files found in {input_dir}")
                if stats["files_ignored"] > 0:
                    self.log_message(f"⚠️  {stats['files_ignored']} non-MSG files ignored")
                messagebox.showwarning("No MSG Files", "No MSG files found in the selected folder.")
                return

            self.log_message(f"📊 Found {stats['msg_files_found']} MSG files")
            if stats["files_ignored"] > 0:
                self.log_message(f"⚠️  {stats['files_ignored']} non-MSG files ignored")
                # Show some details about ignored files if there are only a few
                if stats["files_ignored"] <= 5 and "ignored_files" in stats:
                    for ignored_file in stats["ignored_files"]:
                        self.log_message(f"   • {Path(ignored_file).name}")
                elif stats["files_ignored"] > 5:
                    self.log_message(f"   (Too many to list - includes documents, images, etc.)")

            # Show conversion results
            if stats["files_converted"] > 0:
                self.log_message(f"✅ Successfully converted {stats['files_converted']} files")

            if stats["files_failed"] > 0:
                self.log_message(f"❌ Failed to convert {stats['files_failed']} files")
                for failed_file in stats.get("failed_files", []):
                    self.log_message(f"   • {Path(failed_file).name}")

            # Final summary
            result_msg = f"Batch conversion complete!\n{stats['files_converted']}/{stats['msg_files_found']} MSG files converted successfully."
            if stats["files_ignored"] > 0:
                result_msg += f"\n{stats['files_ignored']} non-MSG files were ignored."

            self.log_message(f"🎉 Conversion complete!")
            messagebox.showinfo("Batch Conversion Complete", result_msg)

        except Exception as e:
            error_msg = f"❌ Batch conversion error: {str(e)}"
            self.log_message(error_msg)
            messagebox.showerror("Error", f"Batch conversion failed:\n{str(e)}")
        finally:
            self.progress.stop()


def main():
    """Main function to run the GUI application."""
    root = tk.Tk()
    app = MSGToEMLApp(root)

    # Center the window on screen
    root.update_idletasks()
    x = (root.winfo_screenwidth() // 2) - (root.winfo_width() // 2)
    y = (root.winfo_screenheight() // 2) - (root.winfo_height() // 2)
    root.geometry(f"+{x}+{y}")

    root.mainloop()


if __name__ == "__main__":
    main()
