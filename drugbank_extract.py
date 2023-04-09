import xml.etree.ElementTree as ET
import pandas as pd
import re
import pickle
from pubchem_toxicity import op_str
def traverse_xml(node, level):
    flag = 0
    for child in node:
        if len(child) > 0:
            traverse_xml(child, level+1)
        else:
            if child.text == 'SMILES':
                flag = 1
            elif flag == 1:
                print(child.text)
                break
        # print(child.tag + ':' + str(child.text))
        # if child.tag.endswith('description') or child.tag.endswith('value'):
        #     with open("output1.txt", "a") as f:
        #         f.write("  " * level + child.tag + ':' + str(child.text) + "\n")
        # if len(child) > 0:
        #     traverse_xml(child, level+1)

def get_all_data_from_xml():
    tree = ET.ElementTree()
    t = tree.parse('D:/artical_code/other/first/data/full database.xml')
    childtag = t[0].tag
    children = t.findall(childtag)
    data = []
    all_tag = []
    indication = []
    pharmacodynamics = []
    absorption = []
    roe = []
    metabolism = []
    hl = []
    clearance = []
    smiles = []
    num = 0
    o_c = 0
    # traverse_xml(children, 0)
    for child in children:
        for subchild in child:
            all_tag.append(subchild.tag[24:])
        if 'calculated-properties' in all_tag:
            attr_data = {}
            flag = 0
            for subchild in child:
                if subchild.tag.endswith('calculated-properties') and len(subchild) > 0:  # 为了说明有smiles
                    for subsubchild in subchild:
                        for subsubsubchild in subsubchild:
                            if subsubsubchild.text == 'SMILES':
                                flag = 1
                            elif flag == 1:
                                attr_data['SMILES'] = str(subsubsubchild.text)
                                with open("output_toxicity.txt", "a") as f:
                                    f.write("--------------------------------------\n")
                                    f.write(str(subsubsubchild.text) + "\n")
                                smiles.append(str(subsubsubchild.text))
                                o_c = 1
                                flag = 0
                                num += 1
                                break
            if o_c == 1:
                o_c = 0
                content_num = 0
                for subchild in child:
                    s = ''
                    # 得到indication中的数据，表示7.1
                    if subchild.tag.endswith('indication'):
                        text = str(subchild.text)
                        if subchild.text is not None and text.strip() != '':
                            indication.append(str(subchild.text))
                            s = 'indication:' + str(subchild.text)
                            attr_data['indication'] = str(subchild.text).replace("\r\n", "")
                    # 得到id
                    elif subchild.tag.endswith('drugbank-id') and len(subchild.keys()) > 0:
                        text = str(subchild.text)
                        if subchild.text is not None and text.strip() != '':
                            s = 'drugbank-id:' + str(subchild.text)
                            attr_data['drugbank-id'] = str(subchild.text).replace("\r\n", "")
                    # 得到pharmacodynamics中的数据，表示8.1
                    elif subchild.tag.endswith('pharmacodynamics'):
                        text = str(subchild.text)
                        if subchild.text is not None and text.strip() != '':
                            pharmacodynamics.append(str(subchild.text))
                            s = 'pharmacodynamics:' + str(subchild.text)
                            attr_data['pharmacodynamics'] = str(subchild.text).replace("\r\n", "")
                    # 得到absorption中的数据，表示8.5
                    elif subchild.tag.endswith('absorption'):
                        text = str(subchild.text)
                        if subchild.text is not None and text.strip() != '':
                            absorption.append(str(subchild.text))
                            s = 'absorption:' + str(subchild.text)
                            attr_data['absorption'] = str(subchild.text).replace("\r\n", "")
                    # 得到roe中的数据，表示8.5
                    elif subchild.tag.endswith('route-of-elimination'):
                        text = str(subchild.text)
                        if subchild.text is not None and text.strip() != '':
                            roe.append(str(subchild.text))
                            s = 'route-of-elimination:' + str(subchild.text)
                            attr_data['route-of-elimination'] = str(subchild.text).replace("\r\n", "")
                    # 得到clearance中的数据，表示8.5
                    elif subchild.tag.endswith('clearance'):
                        text = str(subchild.text)
                        if subchild.text is not None and text.strip() != '':
                            clearance.append(str(subchild.text))
                            s = 'clearance:' + str(subchild.text)
                            attr_data['clearance'] = str(subchild.text).replace("\r\n", "")
                    # 得到metabolism中的数据，表示8.6
                    elif subchild.tag.endswith('metabolism'):
                        text = str(subchild.text)
                        if subchild.text is not None and text.strip() != '':
                            metabolism.append(str(subchild.text))
                            s = 'metabolism:' + str(subchild.text)
                            attr_data['metabolism'] = str(subchild.text).replace("\r\n", "")
                    # 得到hl中的数据，表示8.7
                    elif subchild.tag.endswith('half-life'):
                        text = str(subchild.text)
                        if subchild.text is not None and text.strip() != '':
                            hl.append(str(subchild.text))
                            s = 'half-life:' + str(subchild.text)
                            attr_data['half-life'] = str(subchild.text).replace("\r\n", "")
                    # 得到toxicity中的数据
                    elif subchild.tag.endswith('toxicity'):
                        text = str(subchild.text)
                        if subchild.text is not None and text.strip() != '':
                            a = subchild.text
                            data = op_str(str(subchild.text))
                            s = 'toxicity_summary:' + str(subchild.text)
                            attr_data['toxicity_summary'] = str(subchild.text).replace("\r\n", "")
                    if s != '':
                        text_without_newlines = s.replace("\r\n", "")
                        content_num += 1
                        with open("output_toxicity.txt", "a") as f:
                            f.write(text_without_newlines + "\n")
                # if content_num != 0:
                #     data.append(attr_data)
                #     df = pd.DataFrame(data)
                #     df.to_excel('output.xlsx', index=False, header=True)
                # with open("output.txt", "a") as f:
                #     f.write('num_all:' + str(content_num) + "\n")

    print(num)

def get_toxicity():
    tree = ET.ElementTree()
    t = tree.parse('D:/artical_code/other/first/data/full database.xml')
    childtag = t[0].tag
    children = t.findall(childtag)
    data = []
    all_tag = []
    indication = []
    pharmacodynamics = []
    absorption = []
    roe = []
    metabolism = []
    hl = []
    clearance = []
    smiles = []
    num = 0
    o_c = 0
    # traverse_xml(children, 0)
    for child in children:
        for subchild in child:
            all_tag.append(subchild.tag[24:])
        if 'calculated-properties' in all_tag:
            attr_data = {}
            flag = 0
            smiles = ''
            cid = ''
            name = ''
            for subchild in child:
                if subchild.tag.endswith('calculated-properties') and len(subchild) > 0:  # 为了说明有smiles
                    for subsubchild in subchild:
                        for subsubsubchild in subsubchild:
                            if subsubsubchild.text == 'SMILES':
                                flag = 1
                            elif flag == 1:
                                # with open("output_toxicity.txt", "a") as f:
                                #     f.write("--------------------------------------\n")
                                smiles = str(subsubsubchild.text)
                                o_c = 1
                                flag = 0
                                num += 1
                                break
            if o_c == 1:
                o_c = 0
                content_num = 0
                for subchild in child:
                    s = ''
                    if subchild.tag.endswith('drugbank-id') and len(subchild.keys()) > 0:
                        text = str(subchild.text)
                        if subchild.text is not None and text.strip() != '':
                            cid = str(subchild.text)
                    elif subchild.tag.endswith('name'):
                        text = str(subchild.text)
                        if subchild.text is not None and text.strip() != '':
                            name = str(subchild.text)
                    # 得到toxicity中的数据
                    elif subchild.tag.endswith('toxicity'):
                        text = str(subchild.text)
                        if subchild.text is not None and text.strip() != '':
                            data = op_str(str(subchild.text).replace("\r\n", ""))
                            if isinstance(data, list):
                                for j in data:
                                    with open('output_toxicity.txt', 'a') as f:
                                        content = 'name: ' + name + '; toxicity_summary: ' + re.sub(r'\[.*?\]', '', re.sub(r'\(.*?\)', '', j))
                                        f.write(f'{cid}----------{smiles}----------{content}\n')
                            else:
                                with open('output_toxicity.txt', 'a') as f:
                                    content = 'name: ' + name + '; toxicity_summary: ' + re.sub(r'\[.*?\]', '', re.sub(r'\(.*?\)', '', data))
                                    f.write(f'{cid}----------{smiles}----------{content}\n')

def get_properties():
    tree = ET.ElementTree()
    t = tree.parse('D:/artical_code/other/first/data/full database.xml')
    childtag = t[0].tag
    children = t.findall(childtag)
    dict_name_description = {}
    # traverse_xml(children, 0)
    for child in children:
        name = ''
        desc = ''
        for subchild in child:
            if subchild.tag.endswith('name'):
                name = str(subchild.text).replace("\r\n", "")
            elif subchild.tag.endswith('description'):
                desc = str(subchild.text).replace("\r\n", "")
            if name != '' and desc != '':
                dict_name_description[name] = desc
                break
    with open('name_desc.pkl', 'wb') as f:
        pickle.dump(dict_name_description, f)
            # print(subchild.tag)



if __name__ == '__main__':
    # get_toxicity()
    get_properties()


