import zipfile
from spire.doc import *
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
                    if content == content1:
                        print('fuck')
                    # Write content
                    outzip.writestr(inzipinfo.filename, content1)
                else:
                    content = infile.read()
                    content = str(content.decode(encoding='utf8'))
                    outzip.writestr(inzipinfo.filename, content)

updateZip('Bewerbung.odt', 'Bewerbung1.odt', 'content.xml', '11.09.2026', '18.09.2026')

# Create a new Document object to load and manipulate the ODT file
document = Document()

# Load the ODT file into the Document object
document.LoadFromFile('Bewerbung1.odt')

# Save the loaded document as a PDF file
document.SaveToFile('Bewerbung1.pdf', FileFormat.PDF)

# Close the Document object to release resources
document.Close()

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