from django.shortcuts import render
from django.http import FileResponse
from .forms import PdfExtractForm, PdfMergeForm, PdfReplaceForm
import os
import PyPDF2
import zipfile


def pdf_single_page_extract(request):
    if request.method == 'POST':
        form = PdfExtractForm(request.POST, request.FILES)
        if form.is_valid():
            f = form.cleaned_data['file']
            pdfFileObj = PyPDF2.PdfFileReader(f)

            page_num_list = form.cleaned_data['page'].split(',')

            zf = zipfile.ZipFile(os.path.join('media', 'extracted_pages.zip'), 'w')

            for page_num in page_num_list:
                page_index = int(page_num) - 1
                pageObj = pdfFileObj.getPage(page_index)
                pdfWriter = PyPDF2.PdfFileWriter()
                pdfWriter.addPage(pageObj)

                pdf_file_path = os.path.join('media', 'extracted_page_{}.pdf'.format(page_num))
                with open(pdf_file_path, 'wb') as pdfOutputFile:
                    pdfWriter.write(pdfOutputFile)
                zf.write(pdf_file_path)
            zf.close()

            response = FileResponse(open(os.path.join('media', 'extracted_pages.zip'), 'rb'))
            response['content_type'] = "application/zip"
            response['Content-Disposition'] = 'attachment; filename="extracted_pages.zip"'
            return response

    else:
        form = PdfExtractForm()

    return render(request, 'pdf/pdf_extract.html', {'form': form})


def pdf_range_extract(request):
    if request.method == 'POST':
        form = PdfExtractForm(request.POST, request.FILES)
        if form.is_valid():
            f = form.cleaned_data['file']
            pdfFileObj = PyPDF2.PdfFileReader(f)

            page_range = form.cleaned_data['page'].split('-')
            page_start = int(page_range[0])
            page_end = int(page_range[1])

            pdf_file_path = os.path.join('media', 'extracted_page_{}-{}.pdf'.format(page_start, page_end))
            pdfOutputFile = open(pdf_file_path, 'ab+')
            pdfWriter = PyPDF2.PdfFileWriter()

            for page_num in range(page_start, page_end + 1):
                page_index = int(page_num) - 1
                pageObj = pdfFileObj.getPage(page_index) 
                pdfWriter.addPage(pageObj)

            pdfWriter.write(pdfOutputFile)
            pdfOutputFile.close()

            extractedPage = open(pdf_file_path, 'rb')
            response = FileResponse(extractedPage)
            response['content_type'] = "application/octet-stream"
            response['Content-Disposition'] = 'attachment; filename="extracted_pages.pdf"'

            return response
    else:
        form = PdfExtractForm()

    return render(request, 'pdf/pdf_range_extract.html', {'form': form})


def pdf_merge(request):
    if request.method == 'POST':
        form = PdfMergeForm(request.POST, request.FILES)
        if form.is_valid():
            f1 = form.cleaned_data['file1']
            f2 = form.cleaned_data['file2']
            f3 = form.cleaned_data['file3']
            f4 = form.cleaned_data['file4']
            f5 = form.cleaned_data['file5']

            f_list = [f1, f2, f3, f4, f5]

            pdfMerger = PyPDF2.PdfFileMerger()

            for f in f_list:
                if f:
                    pdfFileObj = PyPDF2.PdfFileReader(f)
                    pdfMerger.append(pdfFileObj)

            with open(os.path.join('media', 'merged_file.pdf'), 'wb') as pdfOutputFile:
                pdfMerger.write(pdfOutputFile)

            response = FileResponse(open(os.path.join('media', 'merged_file.pdf'), 'rb'))
            response['content_type'] = "application/octet-stream"
            response['Content-Disposition'] = 'attachment; filename="merged_file.pdf"'

            return response

        else:
            form = PdfMergeForm()

    else:
        form = PdfMergeForm()

    return render(request, 'pdf/pdf_merge.html', {'form': form})


def pdf_replace(request):
    if request.method == 'POST':
        form = PdfReplaceForm(request.POST, request.FILES)
        if form.is_valid():
            f1 = form.cleaned_data['file1']
            f2 = form.cleaned_data['file2']
            page = form.cleaned_data['page']

            pdfFileObj = PyPDF2.PdfFileReader(f2)
            total_page = pdfFileObj.getNumPages()


            page_start = 1
            page_end = page - 1

            pdfOutputFile1 = open(os.path.join('media', 'part_1.pdf'), 'wb+')
            pdfWriter = PyPDF2.PdfFileWriter()

            for page_num in range(page_start, page_end + 1):

                page_index = int(page_num) - 1


                pageObj = pdfFileObj.getPage(page_index) 

                pdfWriter.addPage(pageObj)

            pdfWriter.write(pdfOutputFile1)
            pdfOutputFile1.close()
            page_start = page + 1
            page_end = total_page

            pdfOutputFile2 = open(os.path.join('media', 'part_2.pdf'), 'wb+')
            pdfWriter = PyPDF2.PdfFileWriter()

            for page_num in range(page_start, page_end + 1):
                page_index = int(page_num) - 1

                pageObj = pdfFileObj.getPage(page_index) 

                pdfWriter.addPage(pageObj)

            pdfWriter.write(pdfOutputFile2)
            pdfOutputFile2.close()

            f2_part_1 = open(os.path.join('media', 'part_1.pdf'), 'rb+')
            f2_part_2 = open(os.path.join('media', 'part_2.pdf'), 'rb+')

            pdfMerger = PyPDF2.PdfFileMerger()
            pdfMerger.append(PyPDF2.PdfFileReader(f2_part_1))
            pdfMerger.append(PyPDF2.PdfFileReader(f1))
            pdfMerger.append(PyPDF2.PdfFileReader(f2_part_2))

            with open(os.path.join('media', 'replaced_file.pdf'), 'wb') as pdfOutputFile:
                pdfMerger.write(pdfOutputFile)

            response = FileResponse(open(os.path.join('media', 'replaced_file.pdf'), 'rb'))
            response['content_type'] = "application/octet-stream"
            response['Content-Disposition'] = 'attachment; filename="replaced_file.pdf"'

            return response

        else:
            form = PdfReplaceForm()

    else:
        form = PdfReplaceForm()

    return render(request, 'pdf/pdf_replace.html', {'form': form})



