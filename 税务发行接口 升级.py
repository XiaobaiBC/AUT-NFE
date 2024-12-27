import random
import numpy as np
from typing import List, Tuple
import math

class SmartCalculator:
    """
    智能计算器类
    功能：根据用户输入的目标金额，生成一系列乘法计算，使总和接近但略大于目标金额
    特点：
    1. 使用固定的乘数：15、13、10、3.5、10
    2. 生成20-90条计算式
    3. 使用机器学习思想动态调整计算策略
    4. 智能控制误差在较小范围内
    """
    def __init__(self):
        # 系统预设的乘数列表
        self.multipliers = [15, 13, 10, 3.5, 10]
        # 学习率：用于调整权重的步长，值越小调整越保守
        self.learning_rate = 0.01
        # 初始化每个乘数的权重，初始时所有乘数权重相等
        self.weights = np.array([1.0] * len(self.multipliers)) / len(self.multipliers)
        
    def adjust_weights(self, target: float, result: float, used_multiplier_idx: int):
        """
        动态调整乘数权重的方法
        
        工作原理：
        1. 比较目标值和实际结果的差异
        2. 根据差异调整使用过的乘数的权重
        3. 确保所有权重为正数且总和为1
        
        参数说明：
        target: 目标值
        result: 实际结果
        used_multiplier_idx: 使用的乘数在列表中的索引
        """
        try:
            # 计算误差（目标值 - 实际结果）
            error = target - result
            # 根据误差调整对应乘数的权重
            self.weights[used_multiplier_idx] += self.learning_rate * error
            # 确保权重不会太小（避免除零错误）
            self.weights = np.maximum(self.weights, 0.0001)
            weight_sum = np.sum(self.weights)
            if weight_sum > 0:
                # 归一化处理，使所有权重之和为1
                self.weights /= weight_sum
            else:
                # 如果权重出现异常，重置为均匀分布
                self.weights = np.array([1.0] * len(self.multipliers)) / len(self.multipliers)
        except Exception as e:
            # 发生任何错误时重置权重
            self.weights = np.array([1.0] * len(self.multipliers)) / len(self.multipliers)
    
    def select_multiplier(self) -> Tuple[float, int]:
        """
        智能选择乘数的方法
        
        工作原理：
        1. 根据当前权重概率选择乘数
        2. 权重越大的乘数被选中的概率越高
        
        返回值：
        - 选中的乘数和其索引位置
        """
        try:
            # 根据权重概率选择乘数
            idx = np.random.choice(len(self.multipliers), p=self.weights)
            return self.multipliers[idx], idx
        except:
            # 出现异常时随机选择
            idx = random.randint(0, len(self.multipliers) - 1)
            return self.multipliers[idx], idx
    
    def calculate_base(self, target: float, current_sum: float, multiplier: float, 
                      remaining_steps: int) -> int:
        """
        计算基数的智能方法
        
        工作原理：
        1. 根据剩余金额和步数计算理想基数
        2. 最后一步时使用更小的波动范围以提高精度
        3. 在理想基数附近随机选择一个合适的值
        
        参数说明：
        target: 目标金额
        current_sum: 当前累计金额
        multiplier: 选中的乘数
        remaining_steps: 剩余计算步数
        
        返回值：
        - 计算出的基数（整数）
        """
        try:
            remaining = target - current_sum
            if remaining_steps == 1:  # 最后一步
                ideal_base = remaining / multiplier
                variation = 0.05  # 最后一步使用5%的波动范围
            else:
                ideal_result = remaining / remaining_steps
                ideal_base = ideal_result / multiplier
                variation = 0.1  # 常规步骤使用10%的波动范围
            
            # 计算基数的合理范围
            min_base = max(1, int(ideal_base * (1 - variation)))
            max_base = max(min_base + 1, int(ideal_base * (1 + variation)))
            
            return random.randint(min_base, max_base)
        except:
            # 计算出错时返回一个安全值
            return random.randint(1, 1000)
    
    def fine_tune(self, target: float, current_sum: float) -> Tuple[int, float, float]:
        """
        精确调整最后计算结果的方法
        
        工作原理：
        1. 尝试所有可用的乘数
        2. 对每个乘数计算最接近目标的基数
        3. 选择误差最小的组合
        
        参数说明：
        target: 目标金额
        current_sum: 当前累计金额
        
        返回值：
        - (最优基数, 选中的乘数, 计算结果)的元组
        """
        best_diff = float('inf')
        best_result = None
        
        for multiplier in self.multipliers:
            # 计算理想基数
            ideal_base = (target - current_sum) / multiplier
            # 尝试向上和向下取整两种情况
            bases = [math.floor(ideal_base), math.ceil(ideal_base)]
            
            for base in bases:
                if base <= 0:
                    continue
                result = base * multiplier
                new_sum = current_sum + result
                diff = abs(new_sum - target)
                
                # 更新最优结果
                if diff < best_diff:
                    best_diff = diff
                    best_result = (base, multiplier, result)
        
        return best_result or (1, self.multipliers[0], self.multipliers[0])
    
    def generate_calculations(self, target_number: float) -> Tuple[List[Tuple], float]:
        """
        生成计算式的主方法
        
        工作流程：
        1. 生成主要计算式（达到最小数量要求）
        2. 使用精确调整方法处理最后一步
        3. 如需要，添加额外的小额计算以达到目标
        
        参数说明：
        target_number: 目标金额
        
        返回值：
        - (计算式列表, 总金额)的元组
        """
        if not isinstance(target_number, (int, float)) or target_number <= 0:
            raise ValueError("目标数字必须是大于0的数字")
            
        calculations = []
        current_sum = 0
        min_steps = 30  # 最少生成30条计算式
        max_steps = 90  # 最多生成90条计算式
        
        # 第一阶段：生成主要计算式
        target_per_step = target_number / min_steps
        while len(calculations) < min_steps - 1:
            multiplier, idx = self.select_multiplier()
            base = self.calculate_base(target_number, current_sum, multiplier, 
                                     min_steps - len(calculations))
            
            result = base * multiplier
            # 控制单步结果不要过大
            if result > target_per_step * 1.5:
                continue
                
            calculations.append((base, multiplier, result))
            current_sum += result
            
            ideal_partial_sum = (target_number / min_steps) * len(calculations)
            self.adjust_weights(ideal_partial_sum, current_sum, idx)
        
        # 第二阶段：添加精确调整的最后一步
        base, multiplier, result = self.fine_tune(target_number, current_sum)
        calculations.append((base, multiplier, result))
        current_sum += result
        
        # 第三阶段：如果需要，继续添加小额计算
        while current_sum < target_number and len(calculations) < max_steps:
            base, multiplier, result = self.fine_tune(target_number, current_sum)
            if result < 0.01:  # 避免死循环
                break
            calculations.append((base, multiplier, result))
            current_sum += result
                
        return calculations, current_sum

def main():
    """
    主程序入口
    
    功能：
    1. 接收用户输入
    2. 生成计算式
    3. 格式化输出结果
    4. 错误处理
    """
    try:
        # 获取并验证用户输入
        input_str = input("请输入一个目标数字：").strip()
        if not input_str:
            raise ValueError("输入不能为空")
            
        target = float(input_str)
        if target <= 0:
            raise ValueError("请输入大于0的数字")
            
        # 创建计算器实例并生成计算式
        calculator = SmartCalculator()
        calculations, total = calculator.generate_calculations(target)
        
        # 格式化输出结果
        print("\n生成的计算式：")
        for i, (base, multiplier, result) in enumerate(calculations, 1):
            print(f"{i}. {base:,} × {multiplier} = {result:,.2f}")
            
        print(f"\n总计算式数量：{len(calculations)}")
        print(f"计算结果总和：{total:,.2f}")
        print(f"目标数字：{target:,.2f}")
        print(f"差额：{(total - target):,.2f}")
        print(f"偏差率：{((total - target) / target * 100):.10f}%")
        
    except ValueError as e:
        print(f"错误：{str(e) or '请输入有效的数字！'}")
    except Exception as e:
        print(f"发生错误：{str(e)}")

if __name__ == "__main__":
    main() 
