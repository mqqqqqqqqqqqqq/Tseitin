import sympy as sp
from sympy import *
from sympy.abc import *

x0, x1, x2, x3, x4, x5, x6, x7 = symbols('x:8')  # 定义字符


# 将公式拆分为子公式，包含 &, |, >>, ⇔ 的都视为子式，~() 不单独视为子式
def change_to_sub(expr):
    if len(expr.args) == 0:  # 当 expr 为 atom 时，不返回任何值
        return []
    elif len(expr.args) == 1:  # 当最外层为 ~ 时
        if len(expr.args[0].args) == 0:  # 如果 ~ 后面为 atom，如：~a，不返回任何值
            return []
        elif len(expr.args[0].args) == 2:  # 如果 ~ 后面包含有子式，则再分情况讨论
            if len(expr.args[0].args[1].args) == 2:
                sum_sub = change_to_sub(expr.args[0].args[1]) + change_to_sub(expr.args[0])
                return sum_sub
            else:
                sum_sub = change_to_sub(expr.args[0])
                return sum_sub
        else:
            return "error"
    elif len(expr.args) == 2:
        sum_sub = [expr] + change_to_sub(expr.args[0]) + change_to_sub(expr.args[1])
        return sum_sub
    elif len(expr.args) > 2:  # 递归调用 change_to_sub
        # 这里的 expr.func 就是外层的 & 运算符，expr.args 是 expr 公式中的子式，expr.args[0] 即为第一个子式（其中()代表一个子式），eval 实现公式规范化
        sum_sub = [expr] + change_to_sub(expr.args[0]) + change_to_sub(eval(str(expr.func) + str(expr.args[1:])))
        return sum_sub
    else:
        return "This is not a formulas"


# ~ 只需一个字符，& 和 | ,>> 需要两个子式
# 计算公式中运算符个数
def expr_depth(expr):
    if len(expr.args) == 0:
        return 0
    elif len(expr.args) == 1:
        return 1 + expr_depth(expr.args[0])
    elif len(expr.args) > 1:
        # max([expr_depth(x) for x in expr.args] 用来计算公式子括号中的运算符个数
        return len(expr.args) - 1 + max([expr_depth(x) for x in expr.args])
    else:
        return "error"


# 重排列子公式，如有重复的子公式，删除重复的子公式
def remove_repeat(l):
    l = sorted(change_to_sub(l), key=expr_depth)
    return list(dict.fromkeys(l))


# 生成新的变量
def symbol_init(k, count=0):
    def new_symbol():
        nonlocal count  # 可以保存上一次调用的值
        count += 1
        return var(str(k) + str(count))  # 返回所生成的变量名

    return new_symbol


# 实现子公式的替换，expr_old 是 expr_new 的子公式，则用 expr_sub 替换 expr_new 中的 expr_old
def expr_Subs(expr_new, expr_old, expr_sub):
    return expr_new.subs(expr_old, expr_sub)


def Tseitin_new(expr):
    s = symbol_init("p")  # 调用 symbol_init，生成新变量 p1...pn
    if expr.func == Symbol:
        return true
    else:
        return Tseitin_equl(remove_repeat(expr), s)

    # 将新生成的变量 pn 分别与子式等价，将生成的 Equivalent 子式用 & 连接


def Tseitin_equl(L, s):
    new_var = s()
    if (L == []):
        return true
    if expr_depth(L[0]) > 0:
        if len(L[1:]) > 0:
            new_List = [expr_Subs(x, L[0], new_var) for x in L[1:]]
            return Equivalent(new_var, L[0]) & Tseitin_equl(new_List, s)
        else:
            return Equivalent(new_var, L[0]) & new_var
    else:
        print("error")

    # Tseitin_new 生成的公式中包含 Equivalent(除了第一个为 atom，其他子式均包含），将 Equivalent 用 ~，&，| 替换


def Tseitin_cnf(Expr):
    result = Expr.args[0]  # Tseitin_new 生成的公式（包括子式）的第一个子式为 atom
    for i in Expr.args[1:]:
        op = i.args[1].func  # op 的值为子式的第二个子式的 func。如：Equivalent(p1,~p)，op 的值为 ~
        r1 = i.args[0]  # r1 的值为子式的 atom。如：Equivalent(p1,~p)，r1 的值为 p1
        r2 = i.args[1].args[0]  # r2 的值为子式的第二个子式的 args。如：Equivalent(p1,~p)，r2 的值为 p
        # 判断 Equivalent 中子式的操作符，将 Equivalent 转换
        if (op == Not):  # ~ 只需一个字符   𝑥⇔(¬𝑦) ≡ (𝑥∨𝑦)∧(¬𝑥∨¬𝑦)
            result = result & (r1 | r2) & (~r1 | ~r2)
        else:
            r3 = i.args[1].args[1]
            if (op == And):  # 𝑥⇔(𝑦∧𝑧) ≡ (𝑦∨¬𝑥)∧(𝑧∨¬𝑥)∧(𝑥∨¬𝑦∨¬𝑧)
                result = result & (r2 | ~r1) & (r3 | ~r1) & (r1 | ~r2 | ~r3)
            elif (op == Or):  # 𝑥⇔(𝑦∨𝑧) ≡ (𝑥∨¬𝑦)∧(𝑥∨¬𝑧)∧(𝑦∨𝑧∨¬𝑥)
                result = result & (r1 | ~r2) & (r1 | ~r3) & (r2 | r3 | ~r1)
            elif (op == Implies):  # 𝑥⇔(𝑦⟹𝑧) ≡ (𝑥∨𝑦)∧(𝑥∨¬𝑧)∧(𝑧∨¬𝑥∨¬𝑦)
                result = result & (r1 | r2) & (r1 | ~r3) & (r3 | ~r1 | ~r2)
            elif (op == Equivalent):  # x⇔(y⇔z) ≡ (x∨y∨z)∧(x∨(¬y)∨(¬z))∧(y∨(¬x)∨(¬z))∧(z∨(¬x)∨(¬y))
                result = result & (r1 | r2 | r3) & (r1 | ~r2 | ~r3) & (r2 | ~r1 | ~r3) & (r3 | ~r1 | ~r2)
            else:
                print("Ihis is an unsupported operator")
    return result


def Tseitin(Expr):
    return Tseitin_cnf(Tseitin_new(Expr))

if __name__ == '__main__':
    # ((x_1→x_2)∨¬((¬x_1↔x_3)∨x_4))∧¬x_2
    F = ((x1 >> x2) | ~(Equivalent(~x1, x3) | x4)) & ~x

    # (x_1∨x_2∨x_3∨x_4∨x_5)∧(x_2∨x_3∨x_4∨x_5∨x_6)∧(x_3∨x_4∨x_5∨x_6∨x_7)
    P = (x1 | x2 | x3 | x4 | x5) & (x2 | x3 | x4 | x5 | x6) & (x3 | x4 | x5 | x6 | x7)

    # ((x_1↔x_2)↔(x_3↔x_4))↔((x_1↔x_3)↔(x_2↔x_4))
    Q = Equivalent(Equivalent(Equivalent(x1, x2), Equivalent(x3, x4)),
                   Equivalent(Equivalent(x1, x3), Equivalent(x2, x4)))

    print(Tseitin(F))
    print(Tseitin(P))
    print(Tseitin(Q))
