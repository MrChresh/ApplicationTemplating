import zipfile
from docx2pdf import convert
from pypdf import PdfWriter
import json
#uv pip install docx2pdf pypdf

with open('config.json', encoding='utf-8') as json_file:
    config_data = json.load(json_file)
    print(config_data['read'])

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

updateZip(config_data['read'], 'temp/tempfile.docx', 'word/document.xml', config_data['replace'])

convert('temp/tempfile.docx', 'temp/tempfile1.pdf')

# Create a writer object
writer = PdfWriter()

writer.append('temp/tempfile1.pdf')

for value in config_data['append']:
    writer.append(value)

# Write the combined file to disk
with open(config_data['out'], 'wb') as output_file:
    writer.write(output_file)

# Close the writer
writer.close()