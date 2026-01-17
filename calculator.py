import ast
import operator

class UltimateSecureCalc:
    def __init__(self):
        # تحديد العمليات المسموح بها فقط وربطها بدالات حقيقية
        self.operators = {
            ast.Add: operator.add, 
            ast.Sub: operator.sub, 
            ast.Mult: operator.mul,
            ast.Div: operator.truediv, 
            ast.Pow: operator.pow, 
            ast.USub: operator.neg
        }

    def calculate(self, expression):
        try:
            # تحويل النص إلى "شجرة عمليات" وليس تنفيذ مباشر
            node = ast.parse(expression, mode='eval').body
            return self._eval_node(node)
        except Exception as e:
            return f"Security/Logic Error: {str(e)}"

    def _eval_node(self, node):
        # إذا كان المدخل رقماً بسيطاً
        if isinstance(node, ast.Num):
            return node.n
        
        # إذا كانت عملية حسابية (ثنائية مثل 5 + 5)
        elif isinstance(node, ast.BinOp):
            if type(node.op) in self.operators:
                left = self._eval_node(node.left)
                right = self._eval_node(node.right)
                
                # حماية من العمليات الانتحارية (مثل الأسس العملاقة)
                if isinstance(node.op, ast.Pow) and right > 100:
                    raise ValueError("Exponent too dangerous!")
                
                return self.operators[type(node.op)](left, right)
        
        # إذا كان الرقم سالباً (مثل -5)
        elif isinstance(node, ast.UnaryOp):
            if type(node.op) in self.operators:
                return self.operators[type(node.op)](self._eval_node(node.operand))
        
        # إذا حاول المستخدم إدخال أي شيء آخر (مثل استدعاء دالات)
        raise TypeError(f"Unsupported operation: {node}")

# --- جزء التشغيل والطباعة للتأكد من العمل ---
if __name__ == "__main__":
    calc = UltimateSecureCalc()
    
    # قائمة اختبارات للتأكد من الأمان
    test_cases = [
        "10 + 5 * 2",      # عملية عادية
        "2 ** 10",         # أسس آمنة
        "(50 / 2) + 5",    # أقواس
        "__import__('os')" # محاولة اختراق (ستفشل فوراً)
    ]

    print("--- نتائج فحص الأمان والتشغيل ---")
    for tc in test_cases:
        result = calc.calculate(tc)
        print(f"Input: {tc}  =>  Result: {result}")
