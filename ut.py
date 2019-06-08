import unittest

import xml.etree.ElementTree as ET


import utils
import model
import paragraph_processor

xml_namespaces = 'xmlns:calcext="urn:org:documentfoundation:names:experimental:calc:xmlns:calcext:1.0" xmlns:chart="urn:oasis:names:tc:opendocument:xmlns:chart:1.0" xmlns:css3t="http://www.w3.org/TR/css3-text/" xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:dom="http://www.w3.org/2001/xml-events" xmlns:dr3d="urn:oasis:names:tc:opendocument:xmlns:dr3d:1.0" xmlns:draw="urn:oasis:names:tc:opendocument:xmlns:drawing:1.0" xmlns:drawooo="http://openoffice.org/2010/draw" xmlns:field="urn:openoffice:names:experimental:ooo-ms-interop:xmlns:field:1.0" xmlns:fo="urn:oasis:names:tc:opendocument:xmlns:xsl-fo-compatible:1.0" xmlns:form="urn:oasis:names:tc:opendocument:xmlns:form:1.0" xmlns:formx="urn:openoffice:names:experimental:ooxml-odf-interop:xmlns:form:1.0" xmlns:grddl="http://www.w3.org/2003/g/data-view#" xmlns:loext="urn:org:documentfoundation:names:experimental:office:xmlns:loext:1.0" xmlns:math="http://www.w3.org/1998/Math/MathML" xmlns:meta="urn:oasis:names:tc:opendocument:xmlns:meta:1.0" xmlns:number="urn:oasis:names:tc:opendocument:xmlns:datastyle:1.0" xmlns:of="urn:oasis:names:tc:opendocument:xmlns:of:1.2" xmlns:office="urn:oasis:names:tc:opendocument:xmlns:office:1.0" xmlns:officeooo="http://openoffice.org/2009/office" xmlns:ooo="http://openoffice.org/2004/office" xmlns:oooc="http://openoffice.org/2004/calc" xmlns:ooow="http://openoffice.org/2004/writer" xmlns:rpt="http://openoffice.org/2005/report" xmlns:script="urn:oasis:names:tc:opendocument:xmlns:script:1.0" xmlns:style="urn:oasis:names:tc:opendocument:xmlns:style:1.0" xmlns:svg="urn:oasis:names:tc:opendocument:xmlns:svg-compatible:1.0" xmlns:table="urn:oasis:names:tc:opendocument:xmlns:table:1.0" xmlns:tableooo="http://openoffice.org/2009/table" xmlns:text="urn:oasis:names:tc:opendocument:xmlns:text:1.0" xmlns:xforms="http://www.w3.org/2002/xforms" xmlns:xhtml="http://www.w3.org/1999/xhtml" xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"'

class MyTests(unittest.TestCase):

    def test_has_indented_style(self):
        elem = ET.fromstring(f'<text:p {xml_namespaces} text:style-name="P326">Nana i ba aning i ma. </text:p>')
        self.assertTrue(utils.has_indented_style(elem))


    def test_PatternIndentation_Matches(self):
        elem = ET.fromstring(f'<text:p {xml_namespaces} text:style-name="P326">Nana i ba aning i ma. </text:p>')
        bible_items = []
        self.assertTrue(paragraph_processor.PatternIndentation.Matches({}, bible_items, elem, {}))

    def test_PatternIndentation_Act(self):
        elem = ET.fromstring(f'<text:p {xml_namespaces} text:style-name="P326">Nana i ba aning i ma. </text:p>')
        bible_items = []
        paragraph_processor.PatternIndentation.Act({}, bible_items, elem)
        self.assertTrue(len(bible_items) == 1)

    def test_verse_starts_indented_True_case(self):
        elem = ET.fromstring(f"""
            <text:p text:style-name="P186" {xml_namespaces}>7
                <text:tab/>
                <text:tab/>
                Bang 'puohimo Ngming'puohibu kpali, a di niba nuori 'kuubuhi ang i 'wulibuhi bang 'wuno. 
                <text:s/>
                (Ai'zeeya G. 29:13)</text:p>
            """)
        self.assertTrue(utils.verse_starts_indented(elem))

    def test_verse_starts_indented_False_case(self):
        elem = ET.fromstring(f"""
            <text:p text:style-name="P186" {xml_namespaces}>7
                <text:tab/>
                Bang 'puohimo Ngming'puohibu kpali, a di niba nuori 'kuubuhi ang i 'wulibuhi bang 'wuno. 
                <text:s/>
                (Ai'zeeya G. 29:13)</text:p>
            """)
        self.assertFalse(utils.verse_starts_indented(elem))

if __name__ == '__main__':
    unittest.main()