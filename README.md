# Programming-for-mathematics
In this repository, I add my files for the final project of the Programming for mathematics course at Utrecht University. The final project is a Python program that serves as a calculator for lambda calculus. With the Python code, it is possible to evaluate lambda expressions and habndle computations regarding arithmetic operations and substitution of variables.

## Lambda calculus 
Lambda calculus, in short $\lambda$-calculus, is a method of formally creating and describing functions. Due to $\lambda$-calculus, it is possible to express computations based on the abstraction and application of functions. The mathematician, computer scientist, and philosopher Alonzo Church invented the $\lambda$-calculus around 1930. He developed the $\lambda$-calculus system to find an answer to the question: "Is there a procedure by which you can determine whether a given mathematical statement is true or not?" He provided a systematic analysis. 

## Basic principles of lambda calculus 
$\lambda$-calculus is build on three main concepts: function abstraction, function application and reduction. First, function abstraction describes the function as $$(\lambda x.M) $$ in which x is the variable and M is the body. By function apllication, the argument will be applied to the function: $$((\lambda x.M\) N)$$. Lastly, reduction is the process to simplify or transform the $\lambda$-calculus expression into another, more simple expression. This rule is defined as $$((\lambda x.M) \ N\ \to \ M[ := N])$$.

## Functionality
The user of this Python program can inut $\lambda$-terms and the program will apply the rules of $\lambda$-calculus to evaluate the term and to compute the result. The possible results of the code are integers, a reduced $\lambda$-term or an error when the input is wrongly entered. To achieve this, the code makes use of $\beta$-reduction and the rules for function abstraction and application.
The program is able to handle the basic arithmetic operations, such as addition, substraction, multiplation, division and exponentiation. 
In addition, the program can evaluate and compare two $\lambda$-terms whether they are equivalent. When the two terms are equivalent, the program will print that message.

## Usage 
### $\lambda$-terms
For $\lambda$-terms is the following syntax working:
- Variable: this can be any symbol which represents another value (e.g. x and y).
- Numiric literal: every number or integer (e.g. 2 and 9).
- Function abstraction: difined as $$(\lambda x.M) $$, in which x is the variable and M is the body of the $\lambda$-term.
- Application: two terms will be applied to each other, for example $$(\lambda x.x) y)$$.
- Arithmetic operations: the basic mathematical computations will be applied, such as $$(3+2)$$ and $$(x^2)$$.

### Code explination
The Python code consists of different classes that represent the sevaral concepts of $$\lambda$$-calculus.
- LambdaTerm: in this class the basics $\lambda$-terms are evaluated and represented.
- Abstractions: applies the rules of function abstraction.
- Application: applies the rules of function application.
- Variable: this class represents the evaluation of variables in $\lambda$-calculus.
- NumericLiteral: this class represents the numerical value of the $\lambda$-calculus.
- ArithmeticOperation: this class represents the mathematical operations.
The evaluate-function evaluates a $\lambda$-term and reduces the term to its normal form. The reduce-method applies the reductions.
