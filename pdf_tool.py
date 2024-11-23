import tkinter as tk
from tkinter import messagebox, Listbox, Scrollbar, Menu
import os
from datetime import datetime
import pdfkit
import subprocess


def get_month_year_directory(base_dir="output"):
    """Creates a directory for the current month and year if it doesn't exist."""
    current_time = datetime.now()
    folder_name = f"{current_time.strftime('%B')} {current_time.year}"  # Full month name
    month_year_dir = os.path.join(base_dir, folder_name)
    os.makedirs(month_year_dir, exist_ok=True)
    return month_year_dir


def convert_webpage_to_pdf(url, output_filename="jobdescription.pdf"):
    """Converts a webpage to a PDF and saves it in a month-year subdirectory."""
    try:
        if not output_filename.lower().endswith(".pdf"):
            output_filename += ".pdf"
        target_directory = get_month_year_directory(base_dir="output")
        output_path = os.path.join(target_directory, output_filename)
        pdfkit.from_url(url, output_path)
        return output_path
    except OSError:
        messagebox.showerror(
            "Error", "wkhtmltopdf not found or not installed. Please install it."
        )
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")
        return None


def download_pdf():
    """Handles the PDF download process."""
    url = url_entry.get().strip()  # Get the URL from the entry widget
    filename = filename_entry.get().strip()  # Get the filename from the entry widget

    if not url:
        messagebox.showerror("Error", "Please enter a valid URL.")
        return

    if not filename:
        filename = "jobdescription.pdf"  # Default filename if none provided

    output_path = convert_webpage_to_pdf(url, filename)
    if output_path:
        pdf_listbox.insert(tk.END, output_path)
        messagebox.showinfo("Success", f"PDF saved at {output_path}")


def handle_enter(event):
    """Trigger the download when the Enter key is pressed in any field."""
    download_pdf()


def open_pdf(event):
    """Open the selected PDF on double-click."""
    selected_index = pdf_listbox.curselection()
    if not selected_index:
        return

    selected_file = pdf_listbox.get(selected_index)
    if os.path.exists(selected_file):
        try:
            if os.name == "nt":  # Windows
                os.startfile(selected_file)
            elif os.name == "posix":  # macOS/Linux
                subprocess.call(("open" if sys.platform == "darwin" else "xdg-open", selected_file))
        except Exception as e:
            messagebox.showerror("Error", f"Could not open the file: {e}")
    else:
        messagebox.showerror("Error", "File does not exist.")


def show_context_menu(event):
    """Show the context menu on right-click."""
    try:
        context_menu.tk_popup(event.x_root, event.y_root)
    finally:
        context_menu.grab_release()


def view_properties():
    """View properties of the selected file."""
    selected_index = pdf_listbox.curselection()
    if not selected_index:
        messagebox.showerror("Error", "No file selected.")
        return

    selected_file = pdf_listbox.get(selected_index)
    if os.path.exists(selected_file):
        file_size = os.path.getsize(selected_file) / 1024  # File size in KB
        messagebox.showinfo(
            "File Properties",
            f"File: {selected_file}\nSize: {file_size:.2f} KB\nLocation: {os.path.abspath(selected_file)}",
        )
    else:
        messagebox.showerror("Error", "File does not exist.")


def delete_selected_file():
    """Delete the selected file from the list and the disk."""
    selected_index = pdf_listbox.curselection()
    if not selected_index:
        messagebox.showerror("Error", "No file selected to delete.")
        return

    selected_file = pdf_listbox.get(selected_index)
    confirm = messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete {selected_file}?")
    if confirm:
        try:
            if os.path.exists(selected_file):
                os.remove(selected_file)
            pdf_listbox.delete(selected_index)
            messagebox.showinfo("Success", f"File {selected_file} deleted.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while deleting the file: {e}")


# Create the main tkinter window
root = tk.Tk()
root.title("Job Description PDF Downloader")
root.geometry("800x400")

# Add a Frame for URL and filename input
input_frame = tk.Frame(root)
input_frame.pack(pady=10)

# URL Entry
url_label = tk.Label(input_frame, text="Enter URL:")
url_label.grid(row=0, column=0, padx=5)
url_entry = tk.Entry(input_frame, width=50)
url_entry.grid(row=0, column=1, padx=5)
url_entry.bind("<Return>", handle_enter)  # Bind Enter key to download_pdf

# Filename Entry
filename_label = tk.Label(input_frame, text="File Name:")
filename_label.grid(row=0, column=2, padx=5)
filename_entry = tk.Entry(input_frame, width=30)
filename_entry.grid(row=0, column=3, padx=5)
filename_entry.bind("<Return>", handle_enter)  # Bind Enter key to download_pdf

# Download Button
download_button = tk.Button(input_frame, text="Download PDF", command=download_pdf)
download_button.grid(row=0, column=4, padx=5)

# Add a Listbox to track downloaded PDFs
pdf_listbox = Listbox(root, height=15, width=80)
pdf_listbox.pack(pady=10)

# Add a Scrollbar for the Listbox
scrollbar = Scrollbar(root)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
pdf_listbox.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=pdf_listbox.yview)

# Bind double-click to open the PDF
pdf_listbox.bind("<Double-1>", open_pdf)

# Add a context menu for the Listbox
context_menu = Menu(root, tearoff=0)
context_menu.add_command(label="View Properties", command=view_properties)
context_menu.add_command(label="Delete", command=delete_selected_file)

# Bind right-click to show the context menu
pdf_listbox.bind("<Button-3>", show_context_menu)

# Add a Quit Button
quit_button = tk.Button(root, text="Quit", command=root.quit)
quit_button.pack(pady=5)

# Run the tkinter main loop
root.mainloop()
