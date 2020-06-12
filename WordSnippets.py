import os
import tempfile
from lxml import etree
import zipfile
import shutil
#zip all required files for word to get back word document
filenames=getListOfFiles('directory_name')
with zipfile.ZipFile("test.docx", "w") as docx:
    for filename in filenames:
        docx.write(filename, "\\".join(filename.split('\\')[1:]))
#extract xml for a section in word document and visualize the structure
def extract_section_xml(filename, section_id):
    extract_dir = tempfile.mkdtemp()
    zip_ref = zipfile.ZipFile(filename, "r")
    extracted = zip_ref.namelist()
    for e in extracted:
        if e == "word/document.xml":
            file = e
    zip_ref.extractall(extract_dir)
    zip_ref.close()
    document_xml = os.path.join(extract_dir, file)
    start_section_index=section_id-1
    end_section_index=start_section_index+1
    parser = etree.XMLParser(ns_clean=True)
    tree_document_xml = etree.parse(document_xml, parser)
    root_document_xml = tree_document_xml.getroot()
    for child in root_document_xml:
        body = child
 
    pstyle_list = root_document_xml.findall(
        "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}body/{http://schemas.openxmlformats.org/wordprocessingml/2006/main}p/{http://schemas.openxmlformats.org/wordprocessingml/2006/main}pPr/{http://schemas.openxmlformats.org/wordprocessingml/2006/main}pStyle"
    )
    heading_names = {}
    heading_names_index = []
    for pstyle in pstyle_list:
        attributes = pstyle.attrib
        if str(attributes)== """{'{http://schemas.openxmlformats.org/wordprocessingml/2006/main}val': 'Heading1'}""":
            parent_ptag = pstyle.getparent().getparent()
            list_ttag = parent_ptag.iterdescendants(
                tag="{http://schemas.openxmlformats.org/wordprocessingml/2006/main}t"
            )
            count = 0
            heading_string = ""
            for ttag in list_ttag:
                text_parent_ptag = ttag.text
                heading_string = heading_string + text_parent_ptag
                count = count + 1
            heading_names = {}
            heading_names[heading_string] = parent_ptag
            heading_names_index.append(heading_names)
 
    start_dict = heading_names_index[start_section_index]
    end_dict = heading_names_index[end_section_index]
 
    for value in start_dict.values():
        start_tag = value
    for value in end_dict.values():
        end_tag = value
    for sibl in start_tag.itersiblings(preceding=True):
        body.remove(sibl)
    for sibl in end_tag.itersiblings(preceding=False):
        body.remove(sibl)
 
    body.remove(end_tag)
 
    xml = etree.Element("section")
    for child in body:
        xml.append(child)
    extracted_section_xml = xml
    extracted_section_xml_str = ""
    for child in extracted_section_xml:
        extracted_section_xml_str += "".join([etree.tostring(child, encoding="unicode", pretty_print=True)])
    with open('test.xml','w') as f:
        f.write(extracted_section_xml_str)
#visualize complete xml for word document or for xml file
def word_xml_printer(file):
    extract_dir = tempfile.mkdtemp()
    zip_ref = zipfile.ZipFile(file, "r")
    extracted = zip_ref.namelist()
    for e in extracted:
        if e == "word/document.xml":
            file = e
    zip_ref.extractall(extract_dir)
    zip_ref.close()
    extracted_file = os.path.join(extract_dir, file)
    root=etree.XML((open(extracted_file).read()).encode('utf-8'))
    shutil.rmtree(extract_dir)
 
    xml_str="".join([etree.tostring(root, encoding="unicode", pretty_print=True)])
    with open('test.xml','w') as f:
        f.write(xml_str)