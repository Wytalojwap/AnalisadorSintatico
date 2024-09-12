import re

# Classes de caracteres
LETTER = 0
DIGIT = 1
UNKNOWN = 99

# Códigos de tokens
INT_LIT = 10
IDENT = 11
ASSIGN_OP = 20
ADD_OP = 21
SUB_OP = 22
MULT_OP = 23
DIV_OP = 24
LEFT_PAREN = 25
RIGHT_PAREN = 26
EOF = -1

class Lexer:
    def __init__(self, input_string):
        self.input_string = input_string
        self.pos = 0
        self.current_char = self.input_string[self.pos]
        self.lexeme = ""
        self.char_class = UNKNOWN
        self.next_token = None
        self.lex_len = 0

    def advance(self):
        self.pos += 1
        if self.pos < len(self.input_string):
            self.current_char = self.input_string[self.pos]
        else:
            self.current_char = None  # End of input

    def get_char(self):
        if self.current_char is not None:
            if self.current_char.isalpha():
                self.char_class = LETTER
            elif self.current_char.isdigit():
                self.char_class = DIGIT
            else:
                self.char_class = UNKNOWN
        else:
            self.char_class = EOF

    def get_non_blank(self):
        while self.current_char is not None and self.current_char.isspace():
            self.advance()
        self.get_char()

    def add_char(self):
        if self.lex_len < 99:
            self.lexeme += self.current_char
            self.lex_len += 1
        else:
            raise ValueError("Lexeme is too long")

    def lookup(self):
        if self.current_char == '(':
            self.add_char()
            self.next_token = LEFT_PAREN
        elif self.current_char == ')':
            self.add_char()
            self.next_token = RIGHT_PAREN
        elif self.current_char == '+':
            self.add_char()
            self.next_token = ADD_OP
        elif self.current_char == '-':
            self.add_char()
            self.next_token = SUB_OP
        elif self.current_char == '*':
            self.add_char()
            self.next_token = MULT_OP
        elif self.current_char == '/':
            self.add_char()
            self.next_token = DIV_OP
        else:
            self.add_char()
            self.next_token = EOF

    def lex(self):
        self.lexeme = ""
        self.lex_len = 0
        self.get_non_blank()
        if self.char_class == LETTER:
            self.add_char()
            self.advance()
            self.get_char()
            while self.char_class in (LETTER, DIGIT):
                self.add_char()
                self.advance()
                self.get_char()
            self.next_token = IDENT
        elif self.char_class == DIGIT:
            self.add_char()
            self.advance()
            self.get_char()
            while self.char_class == DIGIT:
                self.add_char()
                self.advance()
                self.get_char()
            self.next_token = INT_LIT
        elif self.char_class == UNKNOWN:
            self.lookup()
            self.advance()
        elif self.char_class == EOF:
            self.next_token = EOF
            self.lexeme = "EOF"
        print(f"Next token is: {self.next_token}, Next lexeme is {self.lexeme}")
        return self.next_token

class Parser:
    def __init__(self, lexer):
        self.lexer = lexer
        self.next_token = self.lexer.lex()

    def error(self):
        raise SyntaxError("Syntax error")

    def eat(self, token_type):
        if self.next_token == token_type:
            self.next_token = self.lexer.lex()
        else:
            self.error()

    def factor(self):
        print("Enter <factor>")
        if self.next_token in (IDENT, INT_LIT):
            self.eat(self.next_token)
        elif self.next_token == LEFT_PAREN:
            self.eat(LEFT_PAREN)
            self.expr()
            self.eat(RIGHT_PAREN)
        else:
            self.error()
        print("Exit <factor>")

    def term(self):
        print("Enter <term>")
        self.factor()
        while self.next_token in (MULT_OP, DIV_OP):
            self.eat(self.next_token)
            self.factor()
        print("Exit <term>")

    def expr(self):
        print("Enter <expr>")
        self.term()
        while self.next_token in (ADD_OP, SUB_OP):
            self.eat(self.next_token)
            self.term()
        print("Exit <expr>")

def main():
    input_filename = "front.in"  # Nome do arquivo de entrada
    try:
        with open(input_filename, 'r') as file:
            input_string = file.read().strip()
            print(f"Input string: {input_string}")

            lexer = Lexer(input_string)
            parser = Parser(lexer)
            parser.expr()
            print("Parsing completed successfully")
    except FileNotFoundError:
        print(f"Error - Unable to open file: {input_filename}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()

