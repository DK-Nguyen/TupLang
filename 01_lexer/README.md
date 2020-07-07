# Project 01: Lexical Analysis
## 1. What is lexical analysis and how is it related to other parts in compilation?  

Lexical Analysis is the process of converting a 
sequence of characters into a sequence of tokens 
(strings with an assigned type and other values 
such as line number, position...).  
In the compilation process, Lexical Analysis is 
the first step. It creates the tokens which then
will be the input of the Syntax Analyzer. 
The job of Syntax Analyzer is to convert the 
tokens into a syntax tree based on some grammar 
rules which are defined by the people who design 
the programming language.

--------------------------------------------
## 2. How is the lexical structure of the language expressed in the PLY tool? I.e., what parts are needed in the code and how are they related to lexical rules of the language?
In the PLY tool, the input is broken into pairs of 
token types and values.  
All of the token names must be provided in the
```token``` list.  
The token rules are defined by making declarations
with a special prefix ```t_``` followed by the
name of the rule, then specified by a regular expression
rule compatible with the Python's ```re``` module,
e.g. ```t_COMMA = r'\,'```.  
If there are some other actions that need to be done, 
the token rule can be declared as a function, e.g.
```
# Define a rule so we can track line numbers
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)
```
--------------------------------------------
## 3. Explain how the following are recognized and handled in your code:
* ___Keywords___: there are 5 keywords - ```define, begin, 
end, each, select```.
The keywords are put in a map with the lowercase
as keys and the corresponding uppercase as values
e.g. ```reserved = {'define': 'DEFINE'...}.```
The values are then appended to the token list 
```tokens = [...]```.
* ___Comments___: comments are ignored by just doing 
```t_ignore_COMMENT = r'\{.*}'```.
* ___Whitespace between tokens___: whitespaces are ignored
simply by declaring the token rule 
```t_ignore = ' '```.
* ___Operators and delimiters__: 
we just need to define these as special sequence 
(using the backslash in regrex) e.g. 
```t_LARROW = r'\<-'```.
* ___Integer literals___: defined by using the function
```def t_NUMBER_LITERAL(t)```.
* ___String literals___: defined by using the function 
```def t_STRING_LITERAL(t)```.
* ___Function names___: defined by the rule 
```t_funcIDENT = r'[A-Z][a-z0-9_]+'```.
* ___Tuple names___: ```t_tupleIDENT = r'[<][a-z]+[>]'```.

--------------------------------------------
## How can the lexer distinguish between the following lexical elements:
* ___Function names & constant names___: function names 
starts with an uppercase letter (A-Z) and
must be followed by at least one character in
set( 'a-z', '0-9', '_' ), which is defined by 
```[a-z0-9_]+``` in the ```t_funcIDENT``` rule, the
```+``` at the end means that there must be one or 
more occurrences of ```[a-z0-9_]```. 
On the other hand, constant names only contain 
one or more characters in 'A-Z'.
* ___Keywords & variable names___: they are distinguished
by the if statement: ```if t.value in reserved:
t.type = reserved[t.value]``` in the 
```def t_varIDENT(t)``` function that defines the rule
for variable names.
* ___Operators minus and right arrow___: they are
simply done by defining right arrow as a special 
character ```t_RARROW = r'\->'``` and minus as
```t_MINUS = r'-'```.
* ___String literals & variables names___: string literals
start with a double quotation mark, which we define
 in ```r'\"(\\.|[^"\\])*\"'```. Variables are not
 started with a quotation mark, so we do 
 ```r'[a-z]+[a-zA-Z0-9_]*'```.
* ___Comments & other code___: comments are ignored, so 
 we just need to add ```ignore``` to the rule like
 this ```t_ignore_COMMENT = r'\{.*}'```.
* ___Tuple names vs two variables compared to each 
other with less than___: a tuple variable starts with '<' 
and must be followed by at least one lowercase 
char ('a-z'). The last char must be '>'. Following 
these rules, we define ```t_tupleIDENT = r'[<][a-z]+[>]'```
which can separate the ```tupleIDENT``` (e.g. ```<abc>```) 
with comparing 2 variables (e.g. ```a<b```) because 
it only has 2 letters and a greater 
than or less than in the middle, which will not 
match the rule of ```t_tupleIDENT```.
--------------------------------------------
## Extras
Apart from the requirements, I implemented 2 more 
features which help to keep track of the development
process:  
1. After each run, the output of the lexer will be
written to a file named ```out.tupl```. 
2. The content of the ```out.tulp``` file will then
be compared to the corresponding ```*.expected```
file line by line, the results of the comparing process
will be reported to a file named ```report.log``` using
Python's logging tool.

--------------------------------------------
## What did you think of this assignment? What was difficult? What was easy? Did you learn anything useful?
In this assignment, I learned a lot about Regular Expression,
which is a very useful tool. Also, I know more about
the compilation process, and how to implement the 
main idea of it with the Lex & Yacc tool.  
The project to me was not difficult, it only felt a little
bit hard to start because before reading and actually
coding, Lex & Yacc - PLY looked like something
difficult, and the idea of building a compiler
also sounded very fancy.