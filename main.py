import pdfkit
import tkinter as tk
from tkinter import simpledialog, messagebox

def convert_webpage_to_pdf(url, output_filename="jobdescription.pdf"):
    """Converts a webpage to a PDF and saves it."""
    try:
        # Convert webpage to PDF
        pdfkit.from_url(url, output_filename)
        messagebox.showinfo("Success", f"PDF saved as {output_filename}")
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
