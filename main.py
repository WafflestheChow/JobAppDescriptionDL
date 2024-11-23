import os.path

import pdfkit
import tkinter as tk
from tkinter import simpledialog, messagebox
from datetime import datetime

def get_month_year_directory(base_dir='output'):
    current_time = datetime.now()
    folder_name = f"{current_time.strftime('%B')} {current_time.year}" # e.g. "June 2024"

    # Create a directory with the month and year
    month_year_dir = os.path.join(base_dir, folder_name)
    # Create the directory if it doesn't exist
    os.makedirs(month_year_dir, exist_ok=True)

    return month_year_dir

def convert_webpage_to_pdf(url, output_filename="jobdescription.pdf"):
    """Converts a webpage to a PDF and saves it."""
    try:
        if not output_filename.lower().endswith(".pdf"):
            output_filename += ".pdf"

        target_directory = get_month_year_directory()

        output_path = os.path.join(target_directory, output_filename)

        # Convert webpage to PDF
        pdfkit.from_url(url, output_filename)
        messagebox.showinfo("Success", f"PDF saved as {output_filename} at {output_path}")
    except OSError as e:
        messagebox.showerror(
            "Error", "wkhtmltopdf not found or not installed. Please install it."
        )
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

def main():
    # Create a simple GUI
    root = tk.Tk()
    root.withdraw()  # Hide the main tkinter window

    # Ask the user for the URL
    url = simpledialog.askstring("Input", "Enter the URL of the job description webpage:")
    if not url:
        messagebox.showerror("Error", "No URL entered. Exiting.")
        return

    # Ask for the output filename
    output_filename = simpledialog.askstring(
        "Input", "Enter the output filename (default: jobdescription.pdf):"
    )
    if not output_filename:
        output_filename = "jobdescription.pdf"

    # Convert the webpage to PDF
    convert_webpage_to_pdf(url, output_filename)

if __name__ == "__main__":
    main()
