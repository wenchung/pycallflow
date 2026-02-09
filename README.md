# PyCallFlow - Python 函數調用流程分析器

類似 C 語言的 cflow 工具，用於靜態分析 Python 程式的函數調用關係。

## 功能特色

- **AST 靜態分析**：解析 Python 源碼的抽象語法樹，無需執行程式
- **多文件支持**：可分析單一文件或整個目錄
- **樹狀結構輸出**：清晰展示函數調用層級關係
- **遞迴檢測**：自動標記遞迴調用
- **類別方法支持**：正確處理類別中的方法調用
- **反向追蹤**：查看哪些函數調用了指定函數
- **Graphviz 導出**：生成視覺化圖表
- **行號顯示**：精確定位函數定義位置

## 安裝

無需額外安裝，只需要 Python 3.6+ 標準庫。

```bash
# 下載文件
chmod +x pycflow.py
```

## 基本用法

### 1. 分析單一文件

```bash
python pycflow.py script.py
```

輸出範例：
```
main() [script.py:25]
    fetch_data() [script.py:20]
        print() [<external>]
    process_data() [script.py:9]
        helper_function() [script.py:5]
        validate_result() [script.py:14]
```

### 2. 分析整個目錄

```bash
python pycflow.py src/
```

會遞迴掃描目錄下所有 `.py` 文件。

### 3. 指定根函數

只顯示特定函數的調用樹：

```bash
python pycflow.py script.py -f main
```

### 4. 反向追蹤

查看誰調用了某個函數：

```bash
python pycflow.py script.py -r -f process_data
```

輸出範例：
```
Functions calling process_data():

process_data() [example.py:9]
    DataProcessor.process() [example.py:52]
    main() [example.py:25]
```

### 5. 限制深度

避免過深的調用樹：

```bash
python pycflow.py script.py -d 3
```

### 6. 不顯示行號

```bash
python pycflow.py script.py --no-line-numbers
```

### 7. 導出 Graphviz 圖表

```bash
python pycflow.py script.py --dot callgraph.dot

# 生成 PNG 圖片（需要安裝 graphviz）
dot -Tpng callgraph.dot -o callgraph.png
```

## 命令列選項

```
positional arguments:
  path                  Python 文件或目錄路徑

optional arguments:
  -h, --help            顯示幫助訊息
  -f FUNCTION, --function FUNCTION
                        指定要分析的根函數
  -d DEPTH, --depth DEPTH
                        最大顯示深度（預設：10）
  -r, --reverse         反向顯示調用關係
  --no-line-numbers     不顯示行號
  --dot FILE            導出 DOT 格式到指定文件
```

## 實際範例

### 範例程式碼

```python
def helper_function(x):
    return x * 2

def process_data(data):
    result = helper_function(data)
    return validate_result(result)

def validate_result(value):
    if value > 0:
        return True
    return False

def main():
    data = [1, 2, 3]
    for item in data:
        result = process_data(item)
        print(result)

class DataProcessor:
    def load(self):
        self.data = fetch_data()
    
    def process(self):
        for item in self.data:
            process_data(item)
```

### 分析結果

```bash
$ python pycflow.py example.py
```

輸出：
```
DataProcessor.load() [example.py:18]
    fetch_data() [<external>]

DataProcessor.process() [example.py:21]
    process_data() [example.py:5]
        helper_function() [example.py:2]
        validate_result() [example.py:9]

main() [example.py:13]
    print() [<external>]
    process_data() [example.py:5]
        helper_function() [example.py:2]
        validate_result() [example.py:9]
```

## 特殊情況處理

### 遞迴函數

遞迴調用會被自動標記：

```python
def recursive_function(n):
    if n <= 0:
        return
    recursive_function(n - 1)
```

輸出：
```
recursive_function() [script.py:10]
    recursive_function() [script.py:10] <recursive>
```

### 類別方法

類別方法以 `ClassName.method` 格式顯示：

```python
class MyClass:
    def method_a(self):
        self.method_b()
    
    def method_b(self):
        pass
```

輸出：
```
MyClass.method_a() [script.py:2]
    MyClass.method_b() [script.py:5]
```

### 外部函數

內建函數或第三方庫的函數標記為 `<external>`：

```
main() [script.py:10]
    print() [<external>]
    json.dumps() [<external>]
```

## 適用場景

1. **程式碼理解**：快速掌握大型專案的函數調用關係
2. **重構前分析**：了解修改某個函數會影響哪些地方
3. **依賴分析**：查看模組間的依賴關係
4. **文檔生成**：為專案生成調用圖文檔
5. **程式碼審查**：檢查調用深度和複雜度
6. **遞迴檢測**：找出潛在的無限遞迴問題

## 限制

- **靜態分析**：無法追蹤動態調用（如 `getattr()`、`eval()`）
- **間接調用**：透過變量傳遞的函數引用可能無法完全追蹤
- **多態**：無法確定實際調用哪個子類的方法
- **裝飾器**：裝飾器本身會被記錄，但可能影響調用鏈的準確性

## 與 C 語言 cflow 的對比

| 功能 | cflow (C) | pycflow (Python) |
|------|-----------|------------------|
| 靜態分析 | ✓ | ✓ |
| 樹狀輸出 | ✓ | ✓ |
| 反向追蹤 | ✓ | ✓ |
| 遞迴檢測 | ✓ | ✓ |
| 多文件支持 | ✓ | ✓ |
| 類別/物件 | - | ✓ |
| 動態特性 | - | 有限 |

## 進階技巧

### 1. 結合 grep 過濾

```bash
python pycflow.py src/ | grep "database"
```

### 2. 只看特定深度

```bash
python pycflow.py app.py -f main -d 2 > callgraph.txt
```

### 3. 分析多個根函數

```bash
for func in main process cleanup; do
    echo "=== $func ==="
    python pycflow.py app.py -f $func
done
```

### 4. 生成視覺化圖表

```bash
# 導出 DOT 並生成多種格式
python pycflow.py app.py --dot graph.dot
dot -Tpng graph.dot -o graph.png
dot -Tsvg graph.dot -o graph.svg
dot -Tpdf graph.dot -o graph.pdf
```

## 貢獻與反饋

這是一個開源工具，歡迎提出建議和改進！

## 授權

MIT License

---

**提示**：對於大型專案，建議先用 `-f` 指定特定函數進行分析，或使用 `-d` 限制深度，以獲得更清晰的輸出。
