import zipfile
from pypdf import PdfWriter

def updateZip(zipname, dstzipname, filename, replace, replaceto):
    with zipfile.ZipFile(zipname) as inzip, zipfile.ZipFile(dstzipname, "w") as outzip:
        # Iterate the input files
        for inzipinfo in inzip.infolist():
            # Read input file
            with inzip.open(inzipinfo) as infile:
                if inzipinfo.filename == filename:
                    content = infile.read()
                    content = str(content.decode(encoding='utf8'))
                    # Modify the content of the file by replacing a string
                    content1 = content.replace(replace, replaceto)
                    # Write content
                    outzip.writestr(inzipinfo.filename, content1)
                else:
                    content = infile.read()
                    content = str(content.decode(encoding='utf8'))
                    outzip.writestr(inzipinfo.filename, content)

updateZip('Bewerbung.odt', 'Bewerbung1.odt', 'content.xml', '${company}', 'Test GmbH')
# updateZip('Bewerbung1.odt', 'Bewerbung1.odt', 'content.xml', '${street}', 'Teststraße 1')
# updateZip('Bewerbung1.odt', 'Bewerbung1.odt', 'content.xml', '${city}', '111111 Köln')
# updateZip('Bewerbung1.odt', 'Bewerbung1.odt', 'content.xml', '${data}', '19.09.2026')
# updateZip('Bewerbung1.odt', 'Bewerbung1.odt', 'content.xml', '${salutation}', 'Sehr geehrte Damen und Herren,')

#TODO: convert Bewerbung1.odt to pdf

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