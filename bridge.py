import sys
import json
from bomlevelcore import BOMLevelCalculator

# 简单的 API 包装
def main():
    target = sys.argv[1]
    qty = float(sys.argv[2])
    inv = json.loads(sys.argv[3]) # 从字符串接收库存 JSON

    calc = BOMLevelCalculator("bom.xlsx")
    result = calc.calculate_by_level(target, qty, inv)
    
    # 将结果转为 JSON 打印，C# 会捕获这段输出
    print(json.dumps(result, ensure_ascii=False))

if __name__ == "__main__":
    main()