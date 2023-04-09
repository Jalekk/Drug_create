import csv, os, re
import numpy as np
import tensorflow as tf

# cid-smiles对
def cid_smiles():
    path = 'data/data/'
    csv_files = os.listdir(path)
    cid_smiles = {}
    for file in csv_files:
        if file.endswith('.csv'):
            with open(path + file, 'r') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    smiles = row['smiles']
                    cid = row['CID']
                    cid_smiles[cid] = smiles
    np.save('data/cid_smiles.npy', cid_smiles)

# 操作：根据单双*来分割数据
def op_str(value):
    if '**' in value:
        data = []
        index = []
        s = 0
        t = ''
        result = re.findall(r'\*\*(.*?)\*\*', value)
        for i in result:
            index.append(value.index('**' + i))
        index.append(len(value))
        for j, i in enumerate(value):
            if j < index[s]:
                t = t + i
                if j == index[s] - 1 and s == len(index) - 1:
                    data.append(t)
                    t = ''
            else:
                s += 1
                data.append(t)
                t = ''
                t = t + i
        return data
    elif '* ' in value:
        # 该规则是在‘* ’的情况下，注意后面有一个空格，同时，这句话结束，后面没有句号，如果要有句号
        # 那么re.findall(r"\* (.*?)\.", value)
        # 单*前面不加*号
        data = re.findall(r"\* (.*?)", value)
        return data
    else:
        return value

# 根据cid获取smiles
def get_smiles():
    cid_smiles = np.load('data/cid_smiles.npy', allow_pickle=True).item()
    with open('data/toxicity.csv', 'r', encoding='GB18030') as f:
        reader = csv.DictReader(f)
        for row in reader:
            cid = row['CID']
            # print(cid)
            smiles = cid_smiles[cid]
            name = row['name']
            columns_name = ['toxicity_summary', 'hepatotoxicity', 'health_effects']
            for colunmu_name in columns_name:
                value = row[colunmu_name]
                if value != '':
                    value = eval(value)
                    for i in value:
                        data = op_str(i.strip().replace('\n', ' '))
                        if isinstance(data, list):
                            for j in data:
                                with open('data/toxicity.txt', 'a') as f:
                                    content = 'name: ' + name + '; ' + colunmu_name + ': ' + re.sub(r'\[.*?\]', '',re.sub(r'\(.*?\)', '',j))
                                    f.write(f'{cid}----------{smiles}----------{content}\n')
                        else:
                            with open('data/toxicity.txt', 'a') as f:
                                content = 'name: ' + name + '; ' + colunmu_name + ': ' + re.sub(r'\[.*?\]', '',re.sub(r'\(.*?\)', '',data))
                                f.write(f'{cid}----------{smiles}----------{content}\n')
                        # print(len(value))
                    # 判断value值，如果value中有带多个单*号的，就以*号为分隔符，分割成多个值，然后分别写入到txt文件中，
                    # 如果value中有带多个双*号的，就将两个**之间的内容以及第二个双**后面的内容分成一部分，然后分别写入到txt文件中，
                    # 如果没有，就直接写入到txt文件中

                # with open('data/toicity_output.txt', 'a') as f:
                #     f.write(f'{cid}----------{smiles}----------{value}\n')



if __name__ == '__main__':
    get_smiles()


    # Output: ['Symptoms of overdose include seizures', ' Bupropion induced behavioral', " \"It's a good stuent! counter-treatment known.\""]
