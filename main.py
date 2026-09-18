import zipfile
from docx2pdf import convert
from pypdf import PdfWriter

#uv pip install docx2pdf pypdf

def updateZip(zipname, dstzipname, filename, replace):
    with zipfile.ZipFile(zipname) as inzip, zipfile.ZipFile(dstzipname, "w") as outzip:
        # Iterate the input files
        for inzipinfo in inzip.infolist():
            # Read input file
            with inzip.open(inzipinfo) as infile:
                if inzipinfo.filename == filename:
                    content = infile.read()
                    content = str(content.decode(encoding='utf8'))
                    # Modify the content of the file by replacing a string
                    for key, value in replace.items():
                        print(key)
                        print(value)
                        content = content.replace(key, value)
                    # Write content
                    outzip.writestr(inzipinfo.filename, content)
                else:
                    content = infile.read()
                    content = str(content.decode(encoding='utf8'))
                    outzip.writestr(inzipinfo.filename, content)

updateZip('Bewerbung.docx', 'Bewerbung1.docx', 'word/document.xml', {'xxcompanyxx': 'Test GmbH',
                                                                'xxstreetxx': 'Teststraße 1',
                                                                'xxcityxx': '111111 Köln',
                                                                'xxdatexx': '19.09.2026',
                                                                'xxsalutationxx': 'Sehr geehrte Damen und Herren,'
                                                                })

# Convert Bewerbung1.odt to pdf (styles and fonts are preserved by LibreOffice)
#OdtToPdfConverter().convert("Bewerbung1.odt", "Bewerbung1.pdf")
convert('Bewerbung1.docx', 'Bewerbung1.pdf')

# Create a writer object
writer = PdfWriter()

writer.append('Bewerbung1.pdf')
writer.append('LebenslaufSergeBerger.pdf')
writer.append('InfoschreibenKooperationsbetriebe.pdf')
writer.append('ZeugnisRealschule.pdf')

# Write the combined file to disk
with open('Bewerbung.pdf', 'wb') as output_file:
    writer.write(output_file)

# Close the writer
writer.close()