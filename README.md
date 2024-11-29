# AUT-NFE

# NFe JSON 生成器

这个项目旨在从 Excel 文件（.xlsx 格式）中读取发票数据（NFe），并将其转换为符合 Bling API 要求的 JSON 格式。最终生成的 JSON 数据可以通过 HTTP POST 请求发送到 Bling 的 API 接口，实现电子发票的自动化处理。

## 目录结构

```
NFe_JSON_Generator/
│
├── NFe.xlsx               # 发票数据的 Excel 文件 (示例文件)
├── NFe_JSON_Generator.py   # Python 脚本，执行数据转换并发送请求
├── README.md              # 项目说明文件
└── requirements.txt       # Python 依赖包列表
```

## 依赖项

这个项目需要以下 Python 库：

- `pandas`：用于读取和处理 Excel 文件。
- `requests`：用于发送 HTTP 请求。
- `json`：用于生成 JSON 数据。

在开始使用之前，请确保已经安装了这些依赖项。你可以通过以下命令安装：

```bash
pip install -r requirements.txt
```

`requirements.txt` 文件内容：

```
pandas==1.5.3
requests==2.28.1
```

## 使用说明

### 1. 配置 Excel 文件

确保你的 Excel 文件（`NFe.xlsx`）具有以下列：

- `产品代码`：产品的唯一标识符。
- `产品名`：产品名称。
- `产品单位`：产品的单位（例如，个、箱等）。
- `数量`：产品数量。
- `单价`：每个产品的单价。
- `毛重`：产品的毛重（例如，千克）。
- `净重`：产品的净重（例如，千克）。
- `NCM号码`：商品的税务分类代码（NCM）。
- `产品备注`：对产品的附加描述或备注。

### 2. 配置脚本

在 Python 脚本中，`发票号码` 和 API 请求中的一些静态数据（如日期）是硬编码的。如果你希望动态生成这些数据，可以根据需要调整脚本。

```python
发票号码 = "34"  # 发票号码，可以根据需要动态设置
```

### 3. 运行脚本

运行 Python 脚本 `NFe_JSON_Generator.py`，它会读取 Excel 文件并将数据转化为 JSON 格式，最终通过 POST 请求发送到 Bling API。

```bash
python NFe_JSON_Generator.py
```

### 4. 查看响应

执行脚本后，Bling API 的响应将会打印在控制台中。你可以根据响应信息检查是否成功创建了发票，或者是否有任何错误信息。

## 注意事项

- **API 密钥**：在请求头中，你需要使用自己的 Bearer Token 来进行认证。在代码中的 `Authorization` 字段替换为你自己的有效 token。
  
  ```python
  headers = {
      'Authorization': 'Bearer YOUR_API_TOKEN',
  }
  ```

- **Excel 文件格式**：确保 Excel 文件中列的名称与代码中使用的字段一致，否则代码无法正确解析数据。

## 示例 JSON 结构

当脚本成功运行时，生成的 JSON 数据大致如下：

```json
{
    "tipo": 1,
    "numero": "34",
    "dataOperacao": "2023-01-12 09:52:12",
    "contato": {
        "nome": "Contato do Bling",
        "tipoPessoa": "J",
        "numeroDocumento": "30188025000121",
        "ie": "7364873393",
        "contribuinte": 1
    },
    "seguro": 0,
    "despesas": 0,
    "desconto": 0,
    "observacoes": "",
    "itens": [
        {
            "codigo": "001",
            "descricao": "Produto A",
            "unidade": "un",
            "quantidade": 10,
            "valor": 50.0,
            "tipo": "P",
            "pesoBruto": 2.5,
            "pesoLiquido": 2.0,
            "classificacaoFiscal": "12345678",
            "origem": 1,
            "informacoesAdicionais": "Produto de exemplo"
        },
        {
            "codigo": "002",
            "descricao": "Produto B",
            "unidade": "un",
            "quantidade": 5,
            "valor": 100.0,
            "tipo": "P",
            "pesoBruto": 3.0,
            "pesoLiquido": 2.8,
            "classificacaoFiscal": "87654321",
            "origem": 1,
            "informacoesAdicionais": "Outro produto de exemplo"
        }
    ]
}
```

## 许可协议

此项目使用 [MIT 许可证](LICENSE) 开源。

## 联系方式

如果你在使用过程中遇到问题，或者有任何疑问，请通过以下方式联系：

- 邮箱：[youremail@example.com](mailto:youremail@example.com)
- GitHub Issues：直接在 [GitHub 仓库 Issues](https://github.com/yourusername/NFe_JSON_Generator/issues) 中提交问题。
