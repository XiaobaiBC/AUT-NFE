# AUT-NFE
这段代码的目的是从一个 Excel 文件中读取发票（NFe）数据，整理成特定的 JSON 格式，并通过 HTTP 请求将其发送到一个 API 接口（例如 Bling 的 API）。以下是对代码逐行分析：

导入依赖库
python
复制代码
import pandas as pd
import json
import requests
pandas: 用于处理 Excel 文件和数据框（DataFrame）操作。
json: 用于将 Python 字典或数据结构转换为 JSON 格式。
requests: 用于发送 HTTP 请求。
设置发票号码
python
复制代码
发票号码="34"
定义一个变量 发票号码，目前硬编码为 "34"，可能用于在后续的 JSON 数据中作为发票编号。
读取 Excel 文件
python
复制代码
file_path = "NFe.xlsx"
data = pd.read_excel(file_path)
file_path 变量指定了要读取的 Excel 文件路径。
data = pd.read_excel(file_path) 读取该文件内容并加载到 pandas DataFrame 中。
数据预处理
python
复制代码
data = data.fillna("")  # 将空值填充为空字符串
data['产品代码'] = data['产品代码'].astype(str).str.rstrip('.0')  # 转为字符串并移除小数点
fillna("")：将所有空值填充为一个空字符串。
data['产品代码'] = data['产品代码'].astype(str).str.rstrip('.0')：将 "产品代码" 列的数据转换为字符串类型，并移除尾部的 .0（这通常发生在读取 Excel 中的数字列时，避免以浮动数值形式存储的产品代码被处理为浮动型数据）。
构建基础的 AAD JSON 对象
python
复制代码
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
创建了一个基础的 JSON 对象 AAD，包含了固定的字段，如发票类型、号码、操作日期以及发票联系人的信息（例如 nome，tipoPessoa 等）。
itens 是一个空列表，后续将会动态地添加商品数据。
逐行处理 Excel 数据并添加商品项到 itens 列表
python
复制代码
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
    AAD["itens"].append(item)
使用 iterrows() 方法逐行遍历 DataFrame 中的数据。
对于每一行数据，创建一个商品条目的字典 item，并填充来自 Excel 文件的数据字段：
codigo: 产品代码
descricao: 产品名称
unidade: 产品单位
quantidade: 产品数量
valor: 单价
pesoBruto: 毛重
pesoLiquido: 净重
classificacaoFiscal: NCM 编码（商品税务分类）
informacoesAdicionais: 产品备注
将构建的 item 字典添加到 AAD["itens"] 列表中。
转换为 JSON 格式并发送请求
python
复制代码
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
json.dumps(AAD, indent=4, ensure_ascii=False)：将 AAD 字典转换为格式化的 JSON 字符串。indent=4 表示缩进为 4 个空格，ensure_ascii=False 允许非 ASCII 字符（例如中文）正确输出。
url：指定 Bling API 的 URL，目标是 /Api/v3/nfe。
headers：定义了请求头，指定内容类型为 JSON，接受 JSON 响应，同时通过 Authorization 头部提供了 Bearer Token 认证（需要替换为有效的 token）和 PHP 会话 ID。
使用 requests.request 发送一个 POST 请求，将构建好的 JSON 数据作为请求体 data 发送到 Bling API。
最后打印 API 响应的文本内容 response.text。
总结：
此代码的功能是从一个 Excel 文件中读取发票相关数据，格式化后生成符合 Bling API 要求的 JSON 格式，然后通过 HTTP POST 请求将其发送到指定的 URL。AAD 是生成的 JSON 数据结构，包含发票基本信息和商品列表。在处理过程中，代码还进行了数据预处理（如填充空值和格式化产品代码），并为每个商品构建了详细的 JSON 字段。
