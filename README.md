**Tseitin** code

Define the data structure of Boolean expressions in the chosen programming language (Boolean expressions are defined as parent class Expr, atomic variables and Boolean connectors are defined as subclasses of Expr).

Implement the Tseitin encoding algorithm to convert any Boolean expression to a 3-CNF expression.

Use the following examples to test Tseitin coding:

```
((x_1→x_2)∨¬((¬x_1↔x_3)∨x_4))∧¬x_2

(x_1∨x_2∨x_3∨x_4∨x_5)∧(x_2∨x_3∨x_4∨x_5∨x_6)∧(x_3∨x_4∨x_5∨x_6∨x_7)

((x_1↔x_2)↔(x_3↔x_4))↔((x_1↔x_3)↔(x_2↔x_4))
```

Result：

```
Tseitin(((x_1→x_2)∨¬((¬x_1↔x_3)∨x_4))∧¬x_2) =
p5 & (p1 | x1) & (p3 | p4) & (p1 | ~x2) & (p3 | ~p2) & (p3 | ~x4) & (p4 | ~p1) & (p4 | ~p5) & (~p5 | ~x) & (p2 | x1 | ~x3) & (p2 | x3 | ~x1) & (p2 | x4 | ~p3) & (p5 | x | ~p4) & (x1 | x3 | ~p2) & (p1 | ~p3 | ~p4) & (x2 | ~p1 | ~x1) & (~p2 | ~x1 | ~x3)

Tseitin((x_1∨x_2∨x_3∨x_4∨x_5)∧(x_2∨x_3∨x_4∨x_5∨x_6)∧(x_3∨x_4∨x_5∨x_6∨x_7)) =
p14 & (p1 | ~x4) & (p1 | ~x5) & (p10 | ~p14) & (p10 | ~p7) & (p10 | ~x1) & (p11 | ~p13) & (p11 | ~p7) & (p11 | ~x6) & (p12 | ~p13) & (p12 | ~p3) & (p12 | ~p4) & (p13 | ~p14) & (p2 | ~x5) & (p2 | ~x6) & (p3 | ~x6) & (p3 | ~x7) & (p4 | ~p1) & (p4 | ~x3) & (p5 | ~p1) & (p5 | ~x6) & (p6 | ~p2) & (p6 | ~x7) & (p7 | ~p4) & (p7 | ~x2) & (p8 | ~p4) & (p8 | ~x6) & (p9 | ~p1) & (p9 | ~p3) & (p1 | p3 | ~p9) & (p1 | x3 | ~p4) & (p1 | x6 | ~p5) & (p2 | x7 | ~p6) & (p3 | p4 | ~p12) & (p4 | x2 | ~p7) & (p4 | x6 | ~p8) & (p7 | x1 | ~p10) & (p7 | x6 | ~p11) & (x4 | x5 | ~p1) & (x5 | x6 | ~p2) & (x6 | x7 | ~p3) & (p13 | ~p11 | ~p12) & (p14 | ~p10 | ~p13)

Tseitin(((x_1↔x_2)↔(x_3↔x_4))↔((x_1↔x_3)↔(x_2↔x_4))) =
p7 & (p1 | p2 | p5) & (p1 | x1 | x2) & (p2 | x3 | x4) & (p3 | p4 | p6) & (p3 | x1 | x3) & (p4 | x2 | x4) & (p5 | p6 | p7) & (p1 | ~p2 | ~p5) & (p1 | ~x1 | ~x2) & (p2 | ~p1 | ~p5) & (p2 | ~x3 | ~x4) & (p3 | ~p4 | ~p6) & (p3 | ~x1 | ~x3) & (p4 | ~p3 | ~p6) & (p4 | ~x2 | ~x4) & (p5 | ~p1 | ~p2) & (p5 | ~p6 | ~p7) & (p6 | ~p3 | ~p4) & (p6 | ~p5 | ~p7) & (p7 | ~p5 | ~p6) & (x1 | ~p1 | ~x2) & (x1 | ~p3 | ~x3) & (x2 | ~p1 | ~x1) & (x2 | ~p4 | ~x4) & (x3 | ~p2 | ~x4) & (x3 | ~p3 | ~x1) & (x4 | ~p2 | ~x3) & (x4 | ~p4 | ~x2)
```
