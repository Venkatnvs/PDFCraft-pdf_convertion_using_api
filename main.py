from app import PdfApis

def main():
    pdf_api = PdfApis()
    print("Tasks: \nMerge Pdfs- 1\nSplit Pdf- 2\nRemove Password - 3\nExtract Text - 4\nImage To Pdf - 5\n")
    a = int(input("Enter the Task: "))
    req = None
    if a == 1:
        print("Merge Pdfs")
        file_urls = [
            'https://www.africau.edu/images/default/sample.pdf',
            'https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf'
        ]
        output_filename = "merged.pdf"
        req = pdf_api.merge_pdfs(file_urls, output_filename)
    elif a == 2:
        print("Split Pdf")
        pdf_url = "https://www.africau.edu/images/default/sample.pdf"
        output_filename = "output_split.zip"
        req = pdf_api.split_pdfs(pdf_url, output_filename)
    elif a == 3:
        print("Remove Password")
        pdf_url = "https://www.grapecity.com/documents-api-pdfviewer/demos/product-bundles/assets/pdf/password-protected-user.pdf"
        password = "user"
        output_filename = "output_unlock.pdf"
        req = pdf_api.remove_password(pdf_url,password,output_filename)
    elif a == 4:
        print("Extract Text")
        pdf_url = "https://www.africau.edu/images/default/sample.pdf"
        output_filename = "output_data.txt"
        req = pdf_api.extract_text(pdf_url,output_filename)
    elif a == 5:
        print("Image To Pdf")
        image_url = "https://st.depositphotos.com/2274151/4841/i/450/depositphotos_48410113-stock-photo-sample-red-square-grungy-stamp.jpg"
        output_filename = "images.pdf"
        req = pdf_api.convert_images_to_pdf(image_url, output_filename)
    else:
        print("Invalied Input")
    print(req)

if __name__ == "__main__":
    main()