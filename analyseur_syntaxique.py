#---------- Exemples de codes fonctionnels ----------#
tokens = ["main(){", "if", "id", "<", "nombre", "id", "=", "nombre", "else", "id", "=", "nombre", "id", "=", "nombre", "}"]
#tokens = ["main(){", "int", "id", "}"]
#tokens = ["main(){", "int", "id", "float", "id", "}"]

#---------- Exemples de codes non fonctionnels ----------#
#tokens = ["main(){", "if", "id", "<", "nombre", "id", "=", "nombre", "else", "id", "=", "nombre", "id", "=", "nombre"]
#tokens = ["main(){", "if", "id", "<", "nombre", "}"]
#tokens = ["main(){", "int", "id", "<", "nombre", "}"]
#tokens = ["main(){", "int", "id", "float", "id", "=", "nombre", "}"]

position = 0  # Position dans les jetons




# Fonction pour obtenir le jeton courant
def current_token():
    if position < len(tokens):
        return tokens[position] 
    else: 
        return None

# Tableau d'analyse (LL(1)) contenant les règles de grammaire du langage C simplifié
parse_table = {
    "<Programme>" :
    {
        "main(){" : ["main(){", "<liste_declarations>", "<liste_instructions>"]
    },

    "<liste_declarations>" : 
    {
        "int" :   ["<une_declaration>", "<liste_declarations>"], 
        "float" : ["<une_declaration>", "<liste_declarations>"],
        "id" :    [],
        "if" :    [],
        "}" :     []                                             
    },

    "<une_declaration>" :
    {
        "int" : ["<type>", "id"],
        "float" : ["<type>", "id"],
    },

    "<liste_instructions>" :
    {
        "id" : ["<une_instruction>", "<liste_instructions>"],
        "if" : ["<une_instruction>", "<liste_instructions>"],
        "}" :  []
    },

    "<une_instruction>" :
    {
        "id" : ["<affectation>"],
        "if" : ["<test>"]
    },

    "<type>" :
    {
        "int" :   ["int"],
        "float" : ["float"]
    },

    "<affectation>" :
    {
        "id" : ["id", "=", "nombre"],
    },

    "<test>" :
    {
        "if" : ["if", "<condition>", "<une_instruction>", "else", "<une_instruction>"]
    },

    "<condition>" :
    {
        "id" : ["id", "<operateur>", "nombre"]
    },

    "<operateur>" : 
    {
        "<" : ["<"],
        ">" : [">"],
        "=" : ["="],
    }
}




# Analyseur LL(1) basé sur une pile
def analyse():
    global position
    stack = ["}", "<Programme>"]  # Initialisation de la pile avec le symbole de départ
    while stack:
        X = stack[len(stack) - 1]  # Symbole au sommet de la pile
        a = current_token()

        if X in parse_table: #Si c'est un non terminal
            if a in parse_table[X]: 
                stack.pop()
                for non_terminal in range(len(parse_table[X][a]) - 1, -1, -1): #Empilation des non-terminaux
                    stack.append(parse_table[X][a][non_terminal])
                print("La règle :", X, "->", parse_table[X][a])
            else:
                print("Le terminal", a, "est inattendu pour le non-terminal", X)
                return 1

        else: #Si c'est un terminal
            if X == "}": #Fin de chaîne
                if a == "}":
                    print("Y a pas de coquilles :)")
                    return 0
                else:
                    print("Le caractère de fin de chaîne n'est pas présent")
                    return 1
            else:
                if X == a:
                    stack.pop()
                    position += 1 #On passe au symbole suivant
                else:
                    print("Erreur de Syntaxe:", X, "innatendu")
                    return 1




# Exécution de l'analyseur
analyse()