#!/usr/bin/env python3
"""
Python Call Flow Analyzer - 類似 cflow 的 Python 靜態分析工具

功能：
- 解析 Python 源碼並建立函數調用關係圖
- 支持多文件分析
- 生成樹狀結構的調用流程圖
- 偵測遞迴調用
"""

import ast
import os
import sys
from collections import defaultdict
from pathlib import Path
from typing import Dict, Set, List, Tuple


class CallFlowAnalyzer(ast.NodeVisitor):
    """AST 訪問者,用於分析函數調用關係"""
    
    def __init__(self, filename: str):
        self.filename = filename
        self.current_function = None
        self.call_graph: Dict[str, Set[str]] = defaultdict(set)
        self.function_defs: Dict[str, int] = {}  # 函數名 -> 定義行號
        self.class_context = []  # 追蹤當前的類別上下文
        
    def visit_ClassDef(self, node: ast.ClassDef):
        """訪問類別定義"""
        self.class_context.append(node.name)
        self.generic_visit(node)
        self.class_context.pop()
    
    def visit_FunctionDef(self, node: ast.FunctionDef):
        """訪問函數定義"""
        # 構建完整的函數名稱(包含類別)
        if self.class_context:
            func_name = f"{'.'.join(self.class_context)}.{node.name}"
        else:
            func_name = node.name
        
        self.function_defs[func_name] = node.lineno
        
        # 保存外層函數並進入新函數
        outer_function = self.current_function
        self.current_function = func_name
        
        # 訪問函數體
        self.generic_visit(node)
        
        # 恢復外層函數
        self.current_function = outer_function
    
    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef):
        """訪問異步函數定義(處理方式與普通函數相同)"""
        self.visit_FunctionDef(node)
    
    def visit_Call(self, node: ast.Call):
        """訪問函數調用"""
        if self.current_function:
            called_func = self._get_call_name(node.func)
            if called_func:
                self.call_graph[self.current_function].add(called_func)
        
        self.generic_visit(node)
    
    def _get_call_name(self, node) -> str:
        """從調用節點提取函數名稱"""
        if isinstance(node, ast.Name):
            return node.id
        elif isinstance(node, ast.Attribute):
            # 處理 obj.method() 形式
            parts = []
            current = node
            while isinstance(current, ast.Attribute):
                parts.append(current.attr)
                current = current.value
            if isinstance(current, ast.Name):
                parts.append(current.id)
            return '.'.join(reversed(parts))
        elif isinstance(node, ast.Call):
            # 處理裝飾器或高階函數
            return self._get_call_name(node.func)
        return None


class PyCallFlow:
    """Python 調用流程分析主類"""
    
    def __init__(self):
        self.analyzers: List[CallFlowAnalyzer] = []
        self.all_functions: Dict[str, Tuple[str, int]] = {}  # func_name -> (filename, lineno)
        self.call_graph: Dict[str, Set[str]] = defaultdict(set)
    
    def analyze_file(self, filepath: str):
        """分析單個 Python 文件"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                source = f.read()
            
            tree = ast.parse(source, filename=filepath)
            analyzer = CallFlowAnalyzer(filepath)
            analyzer.visit(tree)
            
            self.analyzers.append(analyzer)
            
            # 合併分析結果
            for func_name, lineno in analyzer.function_defs.items():
                self.all_functions[func_name] = (filepath, lineno)
            
            for caller, callees in analyzer.call_graph.items():
                self.call_graph[caller].update(callees)
            
            return True
        except Exception as e:
            print(f"Error analyzing {filepath}: {e}", file=sys.stderr)
            return False
    
    def analyze_directory(self, dirpath: str):
        """分析目錄下所有 Python 文件"""
        path = Path(dirpath)
        py_files = list(path.rglob("*.py"))
        
        if not py_files:
            print(f"No Python files found in {dirpath}", file=sys.stderr)
            return
        
        for py_file in py_files:
            self.analyze_file(str(py_file))
    
    def print_call_tree(self, root_function: str = None, max_depth: int = 10, 
                       show_line_numbers: bool = True, reverse: bool = False):
        """
        打印調用樹
        
        Args:
            root_function: 根函數名稱,None 則顯示所有頂層函數
            max_depth: 最大顯示深度
            show_line_numbers: 是否顯示行號
            reverse: 反向顯示(誰調用了這個函數)
        """
        if reverse:
            self._print_reverse_tree(root_function, show_line_numbers)
            return
        
        if root_function:
            if root_function not in self.all_functions:
                print(f"Function '{root_function}' not found", file=sys.stderr)
                return
            self._print_tree(root_function, 0, set(), max_depth, show_line_numbers)
        else:
            # 找出所有頂層函數(沒有被其他函數調用的)
            all_called = set()
            for callees in self.call_graph.values():
                all_called.update(callees)
            
            top_level = set(self.all_functions.keys()) - all_called
            
            if not top_level:
                top_level = set(self.all_functions.keys())
            
            for func in sorted(top_level):
                self._print_tree(func, 0, set(), max_depth, show_line_numbers)
                print()
    
    def _print_tree(self, func_name: str, depth: int, visited: Set[str], 
                   max_depth: int, show_line_numbers: bool):
        """遞迴打印調用樹"""
        indent = "    " * depth
        
        # 準備顯示訊息
        if func_name in self.all_functions:
            filepath, lineno = self.all_functions[func_name]
            filename = os.path.basename(filepath)
            if show_line_numbers:
                location = f"{filename}:{lineno}"
            else:
                location = filename
        else:
            location = "<external>"
        
        # 檢測遞迴
        if func_name in visited:
            print(f"{indent}{func_name}() [{location}] <recursive>")
            return
        
        print(f"{indent}{func_name}() [{location}]")
        
        # 深度限制
        if depth >= max_depth:
            if self.call_graph.get(func_name):
                print(f"{indent}    ...")
            return
        
        # 遞迴訪問被調用的函數
        visited.add(func_name)
        callees = sorted(self.call_graph.get(func_name, []))
        for callee in callees:
            self._print_tree(callee, depth + 1, visited.copy(), max_depth, show_line_numbers)
        visited.remove(func_name)
    
    def _print_reverse_tree(self, func_name: str, show_line_numbers: bool):
        """打印反向調用樹(誰調用了這個函數)"""
        # 建立反向調用圖
        reverse_graph: Dict[str, Set[str]] = defaultdict(set)
        for caller, callees in self.call_graph.items():
            for callee in callees:
                reverse_graph[callee].add(caller)
        
        print(f"Functions calling {func_name}():\n")
        self._print_tree_helper(func_name, 0, set(), 10, show_line_numbers, reverse_graph)
    
    def _print_tree_helper(self, func_name: str, depth: int, visited: Set[str],
                          max_depth: int, show_line_numbers: bool, graph: Dict[str, Set[str]]):
        """輔助函數用於反向調用樹"""
        indent = "    " * depth
        
        if func_name in self.all_functions:
            filepath, lineno = self.all_functions[func_name]
            filename = os.path.basename(filepath)
            location = f"{filename}:{lineno}" if show_line_numbers else filename
        else:
            location = "<external>"
        
        if func_name in visited:
            print(f"{indent}{func_name}() [{location}] <recursive>")
            return
        
        print(f"{indent}{func_name}() [{location}]")
        
        if depth >= max_depth:
            return
        
        visited.add(func_name)
        callers = sorted(graph.get(func_name, []))
        for caller in callers:
            self._print_tree_helper(caller, depth + 1, visited.copy(), max_depth, 
                                   show_line_numbers, graph)
        visited.remove(func_name)
    
    def export_dot(self, output_file: str = "callgraph.dot"):
        """導出 Graphviz DOT 格式,可用 graphviz 生成圖片"""
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("digraph CallGraph {\n")
            f.write("    rankdir=LR;\n")
            f.write("    node [shape=box];\n\n")
            
            for caller, callees in self.call_graph.items():
                for callee in callees:
                    f.write(f'    "{caller}" -> "{callee}";\n')
            
            f.write("}\n")
        
        print(f"Call graph exported to {output_file}")
        print(f"Generate image with: dot -Tpng {output_file} -o callgraph.png")


def main():
    """主程式入口"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Python Call Flow Analyzer - 靜態分析 Python 函數調用關係",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s script.py                    # 分析單個文件
  %(prog)s src/                         # 分析整個目錄
  %(prog)s script.py -f main           # 只顯示 main 函數的調用樹
  %(prog)s script.py -r -f process     # 反向顯示(誰調用了 process)
  %(prog)s script.py --dot             # 導出 DOT 格式圖形
        """
    )
    
    parser.add_argument("path", help="Python 文件或目錄路徑")
    parser.add_argument("-f", "--function", help="指定要分析的根函數")
    parser.add_argument("-d", "--depth", type=int, default=10, help="最大顯示深度(預設:10)")
    parser.add_argument("-r", "--reverse", action="store_true", help="反向顯示調用關係")
    parser.add_argument("--no-line-numbers", action="store_true", help="不顯示行號")
    parser.add_argument("--dot", help="導出 DOT 格式到指定文件")
    
    args = parser.parse_args()
    
    # 創建分析器
    analyzer = PyCallFlow()
    
    # 分析文件或目錄
    path = Path(args.path)
    if path.is_file():
        if not analyzer.analyze_file(str(path)):
            sys.exit(1)
    elif path.is_dir():
        analyzer.analyze_directory(str(path))
    else:
        print(f"Error: {args.path} is not a valid file or directory", file=sys.stderr)
        sys.exit(1)
    
    # 輸出結果
    if args.dot:
        analyzer.export_dot(args.dot)
    else:
        analyzer.print_call_tree(
            root_function=args.function,
            max_depth=args.depth,
            show_line_numbers=not args.no_line_numbers,
            reverse=args.reverse
        )


if __name__ == "__main__":
    main()
