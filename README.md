# Tiny Compiler

This is a "tiny" compiler project made by following along Austin Henleys [teeny tiny compiler series](https://austinhenley.com/blog/teenytinycompiler1.html).


I wanted to get a basic understanding of how compilers actually worked and this turned out to be a decent small project to study and work on. Tiny lang is a BASIC-like language. The grammar for the language is present in `grammer.txt`.

## Running the Compiler

There is an example.tiny - it calculates the avg of a list of numbers - file in the repo. It can be compiled and executed by running the bash script. It uses clang as the C compiler. You can adjust it to gcc if needed.

```
bash build.sh example.tiny
```

Or you can run it yourself via

```
 python3 tinycompiler.py example.tiny
 clang out.c
 ./a.out 
 ```


## Basic Understanding

The compiler in this repo uses a three-step approach to compile programs. Below is a diagram to understand the overrall flow of this compiler.

<img width="2280" height="856" alt="image" src="https://github.com/user-attachments/assets/1d0c844a-27c3-4181-8cbb-d886784b407e" />

