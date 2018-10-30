import os
import re
import xml.etree.ElementTree
from typing import List

from doxybook.markdown import Md, MdDocument, MdCode, MdCodeBlock, MdBold, MdItalic, MdLink, MdHeader, MdList, MdParagraph, MdRenderer, MdLine, MdTable, MdTableRow, MdTableCell, Text, Br
from doxybook.node import Node
from doxybook.kind import Kind
from doxybook.cache import Cache
from doxybook.config import config
from doxybook.generators.paragraph import generate_paragraph, convert_xml_para

def generate_modules(index_path: str, output_path: str, node: Node, cache: Cache) -> dict:
    output_file = os.path.join(output_path, 'modules.md')
    print('Generating ' + output_file)
    document = MdDocument()

    # Add title
    document.append(MdHeader(1, [Text('Modules')]))

    document.append(MdParagraph([Text('Here is a list of all modules:')]))
    
    lst = MdList([])
    modules = {}
    keywords = []

    # List through all groups
    for child in node.members:
        if child.kind == Kind.GROUP:
            keywords.append(child.name)
            path = os.path.join(index_path, child.refid + '.xml')
            xml_root = xml.etree.ElementTree.parse(path).getroot()
            compounddef = xml_root.find('compounddef')
            if compounddef is not None:
                briefdescription_paras = compounddef.find('briefdescription').findall('para')
                p = MdParagraph([])

                name = compounddef.find('compoundname').text
                refid = compounddef.get('id')
                p.append(MdBold([MdLink([Text(name)], refid + '.md')]))

                modules[refid] = name

                p.append(Text(' '))
                for para in briefdescription_paras:
                    p.extend(convert_xml_para(para, cache))
                lst.append(p)

    document.append(lst)

    if not config.noindex:
        document.set_keywords(keywords)
    document.set_title('Modules')

    # Save
    with open(output_file, 'w') as f:
        document.render(MdRenderer(f))

    return modules