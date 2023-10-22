import PyPDF2

def merge_pdfs(file_list, output_name):
    """
    Merge a list of PDF files into a single PDF file.

    Args:
        file_list (list): List of file paths to the PDF files to be merged.
        output_name (str): The name of the merged PDF file to be created.

    Raises:
        Exception: If there's an issue reading a PDF file.
    
    Prints:
        Error messages for files that are not PDFs or cannot be merged.
    """
    merge = PyPDF2.PdfMerger()

    for pdf_file in file_list:
        if pdf_file.lower().endswith(".pdf"):
            try:
                merge.append(pdf_file)
            except Exception as e:
                print(f"Error: can't read the archive '{pdf_file}': {e}")
        else:
            print(f"Error: the file '{pdf_file}' isn't a PDF and can't be merged.")

    merge.write(output_name)
    merge.close()
