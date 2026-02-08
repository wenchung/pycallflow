"""
範例 Python 程式，用於測試 pycflow
"""

def helper_function(x):
    """輔助函數"""
    return x * 2

def process_data(data):
    """處理資料"""
    result = helper_function(data)
    return validate_result(result)

def validate_result(value):
    """驗證結果"""
    if value > 0:
        return True
    return False

def fetch_data():
    """獲取資料"""
    print("Fetching data...")
    return [1, 2, 3, 4, 5]

def main():
    """主程式"""
    data = fetch_data()
    for item in data:
        result = process_data(item)
        print(f"Result: {result}")
    
    # 遞迴調用範例
    recursive_function(5)

def recursive_function(n):
    """遞迴函數範例"""
    if n <= 0:
        return
    print(n)
    recursive_function(n - 1)

class DataProcessor:
    """資料處理類別"""
    
    def __init__(self):
        self.data = []
    
    def load(self):
        """載入資料"""
        self.data = fetch_data()
    
    def process(self):
        """處理資料"""
        results = []
        for item in self.data:
            results.append(process_data(item))
        return results

if __name__ == "__main__":
    main()
