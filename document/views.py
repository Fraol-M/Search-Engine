from django.shortcuts import render, redirect, HttpResponse
from .forms import Uploadfile
from .models import Document, ExtractedText
from .extract import extract_text_clean

def get_file(request):
    if request.method == "POST":
        form = Uploadfile(request.POST, request.FILES)
        
        if form.is_valid():
            # Save the uploaded PDF
            uploaded_pdf = form.save() 
            pdf_path = uploaded_pdf.file.path

            # Extract the text from the PDF
            extracted = extract_text_clean(pdf_path)

            # Save the extracted text in the ExtractedText model
            ExtractedText.objects.create(pdf=uploaded_pdf, text=extracted)

            return redirect('success', document_id=uploaded_pdf.id)  # Pass the document ID to the success page
    else:
        form = Uploadfile()
    
    return render(request, "index.html", {'form': form})

def success(request, document_id):  
    # Retrieve the ExtractedText object using the document ID
    extracted_text = ExtractedText.objects.filter(pdf_id=document_id).first()  # get the first matching text
    
    if extracted_text:
        # Render the success page with the extracted text
        return HttpResponse(f"<h1>Extracted Text:</h1><pre>{extracted_text.text}</pre>")
    else:
        return HttpResponse("<h1>No extracted text found!</h1>")
