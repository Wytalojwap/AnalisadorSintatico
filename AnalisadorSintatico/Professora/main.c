#include <stdio.h>
#include <stdlib.h>
#include <ctype.h>

/*Declaracoes globais*/
/*Variaveis*/
int charClass;
char lexeme[100];
char nextChar;
int lexLen, token, nextToken;
FILE *in_fp, *fopen();

/*Prototipo de funcoes*/
void addChar();
void getChar();
void getNonBlank();
int lex();

/*Funcoes do analisador sintatico*/
void expr();
void term();
void factor();
void error();

/* Classes de caracteres */
#define LETTER 0
#define DIGIT 1
#define UNKNOWN 99

/* Codigo de tokens*/
#define INT_LIT 10
#define IDENT 11
#define ASSIGN_OP 20
#define ADD_OP 21
#define SUB_OP 22
#define MULT_OP 23
#define DIV_OP 24
#define LEFT_PAREN 25
#define RIGHT_PAREN 26



int main(){
    /*Abrir o arquivo de dados de entrada e processar seu conteudo*/

    if((in_fp = fopen("front.in", "r")) == NULL){
        printf("ERRO - nao foi possivel abrir o arquivo.\n");
    }else{
        getChar();
        do{
            lex();
            expr();
        }while(nextToken != EOF);
    }
    return 0;
}

/******************************************************************************/
/* lookup - uma funcao para processar operadores e parenteses
 e retornar o token */
int lookup(char ch){
    switch(ch){
        case '(':
            addChar();
            nextToken = LEFT_PAREN;
            break;
        case ')':
            addChar();
            nextToken = RIGHT_PAREN;
            break;
        case '+':
            addChar();
            nextToken = ADD_OP;
            break;
        case '-':
            addChar();
            nextToken = SUB_OP;
            break;
        case '*':
            addChar();
            nextToken = MULT_OP;
            break;
        case '/':
            addChar();
            nextToken = DIV_OP;
            break;
        default:
            addChar();
            nextToken = EOF;
            break;
    }
    return nextToken;
}

/*******************************************************************/
/* addChar - uma funcao para adicionar nextChar ao vetor lexeme */
void addChar(){
    if(lexLen <= 98){
        lexeme[lexLen++] = nextChar;
        lexeme[lexLen] = 0;
    }else{
        printf("ERRO - lexeme is too long. \n");
    }
}

/*******************************************************************/
/* getChar - uma funcao para obter o proximo caractere da entrada
            e determinar sua classe de caracteres */
void getChar(){
    if((nextChar = getc(in_fp)) != EOF){
        if(isalpha(nextChar)){
            charClass = LETTER;
        }else if(isdigit(nextChar)){
            charClass = DIGIT;
        }else{
            charClass = UNKNOWN;
        }
    }else{
        charClass = EOF;
    }
}

/*******************************************************************/
/* getNonBlank - uma funcao para chamar getChar ate que ela retorne
                um caractere diferente de espaco em branco */
void getNonBlank(){
    while(isspace(nextChar)){
        getChar();
    }
}

/******************************************************************************/
/* lex - um analisador léxico simples para expressoes aritmeticas */
int lex(){
    lexLen = 0;
    getNonBlank();
    switch(charClass){
        /* Reconhecer identificadores */
        case LETTER:
            addChar();
            getChar();
            while(charClass == LETTER || charClass == DIGIT){
                addChar();
                getChar();
            }
            nextToken = IDENT;
            break;
        /* Reconhecer literais inteiros */
        case DIGIT:
            addChar();
            getChar();
            while(charClass == DIGIT){
                addChar();
                getChar();
            }
            nextToken = INT_LIT;
            break;
        /* Parenteses e operadores */
        case UNKNOWN:
            lookup(nextChar);
            getChar();
            break;
        /* Fim do arquivo */
        case EOF:
            nextToken = EOF;
            lexeme[0] = 'E';
            lexeme[1] = 'O';
            lexeme[2] = 'F';
            lexeme[3] = 0;
            break;
    }
    printf("Next token is: %d, Next lexeme is %s\n", nextToken, lexeme);
    return nextToken;
}

/******************************************************************************/
/* expr - Analisa sintaticamente cadeias na linguagem gerada pela regra:
   <expr> -> <term> {(+|-) <term>} */
void expr(){
    printf("Enter <expr>\n");
    /*Analisa sintaticamente o primeiro termo*/
    term();
    /*Desde que o proximo token seja + ou -, obtenha o proximo token e
    analise sintaticamente o proximo termo*/
    while(nextToken == ADD_OP || nextToken == SUB_OP){
        lex();
        term();
    }
    printf("Exit <expr>\n");
}

/******************************************************************************/
/* term - Analisa sintaticamente cadeias na linguagem gerada pela regra:
   <term> -> <factor> {(*|/) <factor>} */
void term(){
    printf("Enter <term>\n");
    /*Analisa sintaticamente o primeiro factor*/
    factor();
    /*Desde que o proximo token seja * ou /, obtenha o proximo token e
    analise sintaticamente o proximo factor*/
    while(nextToken == MULT_OP || nextToken == DIV_OP){
        lex();
        factor();
    }
    printf("Exit <term>\n");
}

/******************************************************************************/
/* factor - Analisa sintaticamente cadeias na linguagem gerada pela regra:
   <factor> -> id | int_constant | (<expr>) */
void factor(){
    printf("Enter <factor>\n");
    /* Determina qual lado direito */
    if(nextToken == IDENT || nextToken == INT_LIT){
        /* Obtem o proximo token */
        lex();
    }else{
        /* se o lado direito e (<expr>), chame lex para passar o parentese
        esquerdo, chame expr e verifique pelo parentese direito */
        if(nextToken == LEFT_PAREN){
            lex();
            expr();
            if(nextToken == RIGHT_PAREN){
                lex();
            }else{
                error();
            }
        }else{
            /*Nao era um identificador, um literal inteiro ou um
            parentese esquerdo */
            error();
        }
    }
    printf("Exit <factor>\n");
}

void error(){
    printf("Um erro foi detectado\n");
    exit(0);
}
