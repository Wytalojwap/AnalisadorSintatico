import re

# Classes de caracteres
LETRA = 0
DÍGITO = 1
DESCONHECIDO = 99

# Códigos de tokens
INTEIRO = 10
REAL = 11
IDENTIFICADOR = 12
OP_ATRIBUICAO = 20
VÍRGULA = 21
PONTO_E_VÍRGULA = 22
ABRE_COLCHETE = 23
FECHA_COLCHETE = 24
ABRE_CHAVE = 25
FECHA_CHAVE = 26
LIT_INTEIRO = 27
LIT_REAL = 28
EOF = -1

class AnalisadorLexico:
    def __init__(self, input_string):
        self.input_string = input_string
        self.pos = 0
        self.caractere_atual = self.input_string[self.pos]
        self.lexema = ""
        self.classe_caractere = DESCONHECIDO
        self.proximo_token = None
        self.tamanho_lexema = 0

    def avançar(self):
        self.pos += 1
        if self.pos < len(self.input_string):
            self.caractere_atual = self.input_string[self.pos]
        else:
            self.caractere_atual = None  # Fim da entrada

    def obter_caractere(self):
        if self.caractere_atual is not None:
            if self.caractere_atual.isalpha():
                self.classe_caractere = LETRA
            elif self.caractere_atual.isdigit():
                self.classe_caractere = DÍGITO
            else:
                self.classe_caractere = DESCONHECIDO
        else:
            self.classe_caractere = EOF

    def obter_nao_branco(self):
        while self.caractere_atual is not None and self.caractere_atual.isspace():
            self.avançar()
        self.obter_caractere()

    def adicionar_caractere(self):
        if self.tamanho_lexema < 99:
            self.lexema += self.caractere_atual
            self.tamanho_lexema += 1
        else:
            raise ValueError("Lexema é muito longo")

    def procurar(self):
        if self.caractere_atual == '[':
            self.adicionar_caractere()
            self.proximo_token = ABRE_COLCHETE
        elif self.caractere_atual == ']':
            self.adicionar_caractere()
            self.proximo_token = FECHA_COLCHETE
        elif self.caractere_atual == '{':
            self.adicionar_caractere()
            self.proximo_token = ABRE_CHAVE
        elif self.caractere_atual == '}':
            self.adicionar_caractere()
            self.proximo_token = FECHA_CHAVE
        elif self.caractere_atual == '=':
            self.adicionar_caractere()
            self.proximo_token = OP_ATRIBUICAO
        elif self.caractere_atual == ',':
            self.adicionar_caractere()
            self.proximo_token = VÍRGULA
        elif self.caractere_atual == ';':
            self.adicionar_caractere()
            self.proximo_token = PONTO_E_VÍRGULA
        else:
            # Reconhecer palavras reservadas como 'int' e 'float'
            if self.lexema == "int":
                self.proximo_token = INTEIRO
            elif self.lexema == "float":
                self.proximo_token = REAL
            else:
                self.adicionar_caractere()
                self.proximo_token = EOF

    def analisar(self):
        self.lexema = ""
        self.tamanho_lexema = 0
        self.obter_nao_branco()
        if self.classe_caractere == LETRA:
            self.adicionar_caractere()
            self.avançar()
            self.obter_caractere()
            while self.classe_caractere in (LETRA, DÍGITO):
                self.adicionar_caractere()
                self.avançar()
                self.obter_caractere()
            # Verificar palavras-chave após a formação completa
            if self.lexema == "int":
                self.proximo_token = INTEIRO
            elif self.lexema == "float":
                self.proximo_token = REAL
            else:
                self.proximo_token = IDENTIFICADOR
        elif self.classe_caractere == DÍGITO:
            self.adicionar_caractere()
            self.avançar()
            self.obter_caractere()
            while self.classe_caractere == DÍGITO:
                self.adicionar_caractere()
                self.avançar()
                self.obter_caractere()
            if self.caractere_atual == '.':
                self.adicionar_caractere()
                self.avançar()
                self.obter_caractere()
                while self.classe_caractere == DÍGITO:
                    self.adicionar_caractere()
                    self.avançar()
                    self.obter_caractere()
                self.proximo_token = LIT_REAL
            else:
                self.proximo_token = LIT_INTEIRO
        elif self.classe_caractere == DESCONHECIDO:
            self.procurar()
            self.avançar()
        elif self.classe_caractere == EOF:
            self.proximo_token = EOF
            self.lexema = "EOF"
        print(f"Próximo token é: {self.proximo_token}, Próximo lexema é {self.lexema}")
        return self.proximo_token

class AnalisadorSintatico:
    def __init__(self, analisador_lexico):
        self.analisador_lexico = analisador_lexico
        self.proximo_token = self.analisador_lexico.analisar()

    def erro(self):
        raise SyntaxError("Erro de sintaxe")

    def consumir(self, tipo_token):
        if self.proximo_token == tipo_token:
            self.proximo_token = self.analisador_lexico.analisar()
        else:
            self.erro()

    def var(self):
        print("Entrando em <var>")
        self.consumir(IDENTIFICADOR)
        if self.proximo_token == ABRE_COLCHETE:
            self.consumir(ABRE_COLCHETE)
            self.consumir(LIT_INTEIRO)
            self.consumir(FECHA_COLCHETE)
            if self.proximo_token == OP_ATRIBUICAO:
                self.consumir(OP_ATRIBUICAO)
                self.consumir(ABRE_CHAVE)
                if self.proximo_token == LIT_INTEIRO:
                    self.consumir(LIT_INTEIRO)
                    while self.proximo_token == VÍRGULA:
                        self.consumir(VÍRGULA)
                        self.consumir(LIT_INTEIRO)
                elif self.proximo_token == LIT_REAL:
                    self.consumir(LIT_REAL)
                    while self.proximo_token == VÍRGULA:
                        self.consumir(VÍRGULA)
                        self.consumir(LIT_REAL)
                self.consumir(FECHA_CHAVE)
        elif self.proximo_token == OP_ATRIBUICAO:
            self.consumir(OP_ATRIBUICAO)
            if self.proximo_token in (LIT_INTEIRO, LIT_REAL):
                self.consumir(self.proximo_token)
        print("Saindo de <var>")

    def lista(self):
        print("Entrando em <lista>")
        self.var()
        while self.proximo_token == VÍRGULA:
            self.consumir(VÍRGULA)
            self.var()
        print("Saindo de <lista>")

    def tipo(self):
        print("Entrando em <tipo>")
        if self.proximo_token in (INTEIRO, REAL):
            self.consumir(self.proximo_token)
        else:
            self.erro()
        print("Saindo de <tipo>")

    def declaracao(self):
        print("Entrando em <declaracao>")
        self.tipo()
        self.lista()
        self.consumir(PONTO_E_VÍRGULA)
        print("Saindo de <declaracao>")

def principal():
    nome_arquivo_entrada = "front.in"  # Nome do arquivo de entrada
    try:
        with open(nome_arquivo_entrada, 'r') as arquivo:
            string_entrada = arquivo.read().strip()
            print(f"String de entrada: {string_entrada}")

            analisador_lexico = AnalisadorLexico(string_entrada)
            analisador_sintatico = AnalisadorSintatico(analisador_lexico)
            analisador_sintatico.declaracao()
            print("Análise concluída com sucesso")
    except FileNotFoundError:
        print(f"Erro - Não foi possível abrir o arquivo: {nome_arquivo_entrada}")
    except Exception as e:
        print(f"Ocorreu um erro: {e}")

if __name__ == "__main__":
    principal()

