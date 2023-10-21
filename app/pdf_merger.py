import PyPDF2

def merge_pdfs(file_list, output_name):
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
