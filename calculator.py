import math
import re

class SecureCalculator:
    def __init__(self):
        # القائمة البيضاء: الرموز المسموح بها فقط
        self.allowed_pattern = re.compile(r'^[0-9+\-*/().\s]*$')

    def calculate(self, expression):
        # 1. فحص أمني: هل يحتوي الإدخال على رموز خبيثة؟
        if not self.allowed_pattern.match(expression):
            return "Error: Security Violation (Invalid Characters)"

        try:
            # 2. فحص أمني: منع استخدام __ أو أي محاولة للوصول لخصائص النظام
            if "__" in expression:
                return "Error: Restricted access"

            # 3. الحساب باستخدام بيئة معزولة (Safe Eval Alternative)
            # نمرر قاموساً فارغاً للمتغيرات العالمية والمحلية لمنع الوصول للدالات المدمجة
            result = eval(expression, {"__builtins__": None}, {})
            
            # 4. التعامل مع الأرقام الضخمة (منع Denial of Service)
            if isinstance(result, (int, float)) and result > 1e15:
                return "Error: Result too large for safety"
                
            return result
        except ZeroDivisionError:
            return "Error: Division by zero"
        except Exception:
            return "Error: Invalid expression"

# تجربة الكود
if __name__ == "__main__":
    calc = SecureCalculator()
    user_input = input("Enter calculation (e.g., 5 + 5): ")
    print(f"Result: {calc.calculate(user_input)}")
