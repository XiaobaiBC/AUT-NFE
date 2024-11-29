import pandas as pd
import json
import requests
发票号码="34"



# 文件路径
file_path = "NFe.xlsx"

# 读取 Excel 文件
data = pd.read_excel(file_path)

# 处理列数据，移除空值和格式化
data = data.fillna("")  # 将空值填充为空字符串
data['产品代码'] = data['产品代码'].astype(str).str.rstrip('.0')  # 转为字符串并移除小数点

# 构建基础的 AAD JSON 对象
AAD = {
    "tipo": 1,
    "numero": "34",  # 示例数字，可根据需要动态变化
    "dataOperacao": "2023-01-12 09:52:12",  # 示例日期，可动态生成
    "contato": {
        "nome": "Contato do Bling",
        "tipoPessoa": "J",
        "numeroDocumento": "30188025000121",
        "ie": "7364873393",
        "contribuinte": 1
    },
    "seguro": 0,  # 保险费
    "despesas": 0,  # 其他费用
    "desconto": 0,  # 折扣
    "observacoes": "",
    "itens": []  # 商品数据列表
}

# 逐行循环读取数据并将商品数据添加到 "itens" 列表中
for _, row in data.iterrows():
    item = {
        "codigo": row['产品代码'],
        "descricao": row['产品名'],
        "unidade": row['产品单位'],
        "quantidade": row['数量'],
        "valor": row['单价'],
        "tipo": "P",  # P为产品 S为服务
        "pesoBruto": row['毛重'],
        "pesoLiquido": row['净重'],
        "classificacaoFiscal": row['NCM号码'],
        "origem": 1,
        "informacoesAdicionais": row['产品备注']
    }
    # 将每个商品数据添加到 "itens" 列表
    AAD["itens"].append(item)

# 打印输出最终的 AAD JSON 对象
payload = json.dumps(AAD, indent=4, ensure_ascii=False)



url = "https://api.bling.com.br/Api/v3/nfe"
headers = {
  'Content-Type': 'application/json',
  'Accept': 'application/json',
  'Authorization': 'Bearer 287aee92d6862d2e8f2f595a290f0c4a74a1791a',
  'Cookie': 'PHPSESSID=sinqitfelqfsik62bhbbngrg1o'
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)
