# Project 02: Syntax Analysis
## 1. What is syntax analysis and how is it related to other parts in compilation?
Syntax analysis, or parsing, is the process of analysing a set of symbols 
according to the grammar rules, which is the second stage of a compilation process.
In this project, we build the syntax analyser for a toy programing language called ```Tuplang```.   
After the Lexical Analyser produces the sequence of tokens that we need (in the file ```tokenizer.py```)
, the Syntax Analyser (in ```main.py```) will takes a set of grammar rules and use that 
to convert the tokens into a syntax tree.  
In ```Tuplang```, all the grammars are (will be explained more in the following sections):
```
program ::= {function_or_variable_definition} return_value DOT

function_or_variable_definition ::= 
    variable_definition | function_definition

function_definition ::= DEFINE funcIDENT LSQUARE [formals] RSQUARE
                        BEGIN 
                        {variable_definitions} 
                        return_value DOT 
                        END DOT

formals ::= varIDENT {COMMA varIDENT}

return_value ::= EQ simple_expression | NOTEQ pipe_expression

variable_definitions ::= varIDENT LARROW simple_expression DOT
                       | constIDENT LARROW constant_expression DOT
                       | tupleIDENT LARROW tuple_expression DOT
                       | pipe_expression RARROW tupleIDENT DOT

constant_expression ::= constIDENT
                      | NUMBER_LITERAL

pipe_expression ::= tuple_expression {PIPE pipe_operation}

pipe_operation ::= funcIDENT
                 | MULT
                 | PLUS
                 | each_statement

each_statement ::= EACH COLON funcIDENT


tuple_expression ::= tuple_atom {tuple_operation tuple_atom}

tuple_operation ::= DOUBLEPLUS

tuple_atom ::= tupleIDENT
     | function_call
     | LSQUARE constant_expression DOUBLEMULT constant_expression RSQUARE
     | LSQUARE constant_expression DOUBLEDOT  constant_expression RSQUARE
     | LSQUARE arguments RSQUARE


function_call ::= funcIDENT LSQUARE [arguments] RSQUARE

arguments ::= simple_expression {COMMA simple_expression}



atom ::= function_call | NUMBER_LITERAL | STRING_LITERAL | varIDENT |
         constIDENT | LPAREN simple_expression RPAREN |
         SELECT COLON constant_expression LSQUARE tuple_expression RSQUARE

factor ::= [MINUS] atom

term ::= factor {(MULT | DIV) factor}

simple_expression ::= term {(PLUS | MINUS) term}
```
You can run the syntax analyser with the command
```python main.py -f {the file that contains your code in tuplang}```.  e.g. 
```
python main.py -f in_and_out/01_const.tupl
```
You can find the input and expected output in the folder ```in_and_out```.  

**Note: I changed the order of the questions a little to make it easier to follow.**

--------------------------------------------
## 2. Explain in English what the syntax of the following elements mean (i.e. how would you describe the syntax in textual form): 
The following syntax is defined under EBNF (Extended Backus-Naur form).
<sup>[1](https://en.wikipedia.org/wiki/Extended_Backus%E2%80%93Naur_form)</sup>.
#### Variable definitions
```
variable_definitions ::= varIDENT LARROW simple_expression DOT
                       | constIDENT LARROW constant_expression DOT
                       | tupleIDENT LARROW tuple_expression DOT
                       | pipe_expression RARROW tupleIDENT DOT
```
Take the first row as an example: ```variable_definitions``` is defined as a ```varIDENT```, followed by a ```LARROW```, 
then a ```simple_expression``` and finally a ```DOT```. The order must be correct.  
```varIDENT```, ```LARROW``` and ```DOT``` are tokens
that can be found in the file ```tokenizer.py```. ```simple_expression``` is a simpler grammar rule, which
is declared also in the file ```main.py```, which is our ```yacc```.  
The same logic applied for 3 other cases in the following rows, note that ```|``` is an ```or``` operator, 
so there are 4 cases ```variable_definitions```. 
#### Function call
```
function_call ::= funcIDENT LSQUARE [arguments] RSQUARE
```
A function call is defined as a sequence of ```funcIDENT```, followed by a ```LSQUARE``` (a left square), 
an optional ```arguments```, and then a ```RSQUARE``` (a right square).
#### Tuple expressions
```
tuple_expression ::= tuple_atom {tuple_operation tuple_atom}
```
```tuple_expression``` is defined as a ```tuple_atom```, followed by zero or more times of a sequence 
```tuple_operation tuple_atom```.  
For example,  
```tuple_expression = tuple_atom``` or   
```tuple_expression = tuple_atom tuple_operation tuple_atom``` or   
```tuple_expression = tuple_atom tuple_operation tuple_atom tuple_operation tuple_atom```

--------------------------------------------
## 3. How is the syntactic structure of the language expressed in the PLY tool? I.e., what parts are needed in the code and how are they related to syntactic rules of the language?
In the ply tool, we used the ```ply.yacc``` module to define the grammars for our Tuplang program, 
each grammar rule is defined in the docstring of a function that starts with ```p_```, e.g. 
```python
def p_program(p):
    '''program : zero_or_more_func_or_var_def return_value DOT'''
``` 
The argument of the function is ```p```, which is a sequence containing the values of each grammar
symbol in the rule we want to define. In the above code, the values of ```p[i]``` is as followed:
```p[0] = program```, ```p[1] = zero_or_more_func_or_var_def```, ```p[2] = return_value```, and ```p[3] = DOT```.

--------------------------------------------
## 4. Answer the following based on the syntax definition:
#### Is it possible to define a "nested" function, i.e. to define a new function inside another function? Why?  
It is not possible to define a nested function, because we have not defined any grammar rule for it. 
For example, the program would give syntax error if you do something like this:
```
define Function[]
begin
    define Function[]
    begin
    aa <- 0.
    = "return expr".
end.
  aa <- 0.
  = "return expr".
end.
i9_abc <- 0.  a9 <- 9.
```

#### Is it syntactically possible to perform arithmetic with strings ("Hello"+"world")? Why?  
It is possible to do ```"Hello"+"world"``` because it is a ```simple_expression``` of ```term + term```. 
```term``` is ```factor```, which is an ```atom```, which can be a ```STRING_LITERAL```.
For example, it is perfectly fine to pass in syntax like this:
```
N <- 7.
PI <- 3.
ROUND <- 9.
var<- "hello" + "world".
= "this is an expression so it can be the last item in program".
```

#### Is it possible to initialize a variable from a constant (N<-1. var<-N.)? Why?  
It is possible to define ```N<-1. var<-N.``` because ```var``` can be a variable name (it is not in 
the reserved list), and also it obeys to the rule ```variable_definitions ::= varIDENT LARROW simple_expression DOT```:
```simple_expression``` can be a ```term```, which is an ```atom```, and an ```atom``` can be a ```constIDENT```.   
For example, it is fine to do this:
```
N <- 7.
PI <- 3.
ROUND <- 9.
var<- "hello" + "world".
N<-1. var<-N.
= "this is an expression so it can be the last item in program".
```

#### Is it possible to initialize a constant from a variable (var<-1. N<-var.)? Why?  
It is not possible to intitialize ```var <- 1. N <- var.``` because in the rule 
```variable_definitions : constIDENT LARROW constant_expression DOT```, we can see that a ```constIDENT```
can only be a ```constant_expression```, which is 
```
constant_expression ::= constIDENT
                      | NUMBER_LITERAL
```
Therefore, we cannot do ```N <- var```. However, we can do ```N <- VAR``` instead and the syntax would be OK.
In another words, doing the following is fine:
```
N <- 7.
PI <- 3.
ROUND <- 9.
var<- "hello" + "world".
N<-1. var<-N.
VAR<-1. N<-VAR.
= "this is an expression so it can be the last item in program".

```
#### Are the following allowed by the syntax: xx--yy and --xx? Why?  
Doing ```xx--yy``` is OK, because it follows this rule: ```atom MINUS MINUS atom```. However, doing 
```--xx``` is not good because we do not have a rule that allows two ```MINUS``` to be before an ```atom```. 

#### How is it ensured that addition/subtraction are done after multiplication/division?  
We do that by defining the precedence <sup>[2](http://www.dabeaz.com/ply/ply.html)</sup>:
 ```
precedence = (
     ('left', 'PLUS', 'MINUS'),
     ('left', 'TIMES', 'DIVIDE'),
 )
```
However I could not find the place to put the ```precedence``` in the ```main.py```, 
so it is not ensured in my program.

--------------------------------------------
# 5.What did you think of this assignment? What was difficult? What was easy? Did you learn anything useful?
In this assignment, I learned a lot about how to build a syntax analyser with Yacc from a set of tokens 
found by regular expression with Lex.  
I understand more about the process of how the computer gets in a bunch of code, for example, all of the
text in ```my_code.c```, then produces the output that I need. First, it runs the Lexical Analyser to find
if there are any typos (strange symbols ect...), then it runs the Syntax Analyser to parse the tokens 
according to the grammar rules that we defined (Yacc uses the shift-reduce parsing 
technique<sup>[2](http://www.dabeaz.com/ply/ply.html)</sup>).  
I found the assignment very useful, however, there are still holes in my understanding about what ```ply``` does
behind the scene, how they map these things onto the hardware, which does the arithmetic calculations of 0 and 1. 
I think these will become clearer in the 3rd and 4th assignment, and also the hardware part is not one of 
the topics that this course cover. 