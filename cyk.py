non_terminals = ["S", "Greet", "Respond", "Sub", "Vrb", "Obj", "X1"]
terminals = ["Hello", "Hi", "How_are_you", "I", "You", "am", "are", "doing", "feeling", "great", "okay", "good"]

# Peraturan grammar
grammar = {
    "S": [["Greet"], ["Respond"]],
    "Greet": [["Hello"], ["Hi"], ["How_are_you"]],
    "Respond": [["Sub", "X1"]],
    "Sub": [["I"], ["You"]],
    "X1": [["Vrb", "Obj"]],
    "Vrb": [["am"], ["are"], ["doing"], ["feeling"]],
    "Obj": [["great"], ["okay"], ["good"]]
}

def cyk_parse(words):
    print(f"\nTesting sentence: {' '.join(words)}")
    print(f"Input tokens: {words}")
    print("=" * 40)

    # Validasi apakah setiap kata adalah terminal
    for word in words:
        if word not in terminals:
            print(f"Invalid word: '{word}' is not in the terminal list.")
            print("Result: False")
            return

    n = len(words)
    table = [[set() for _ in range(n)] for _ in range(n)]

    # Step 1: Isi diagonal (produksi terminal langsung)
    for j in range(n):
        for lhs, rules in grammar.items():
            for rhs in rules:
                if len(rhs) == 1 and rhs[0] == words[j]:
                    table[j][j].add(lhs)

    # Step 2: Isi bagian atas segitiga tabel (produksi non-terminal ganda)
    for l in range(2, n + 1):       # Panjang substring
        for i in range(n - l + 1):  # Start index
            j = i + l - 1           # End index
            for k in range(i, j):   # Pemisah
                for lhs, rules in grammar.items():
                    for rhs in rules:
                        if len(rhs) == 2:
                            B, C = rhs
                            if B in table[i][k] and C in table[k + 1][j]:
                                table[i][j].add(lhs)

    # Step 3: Tangani aturan unary (misal: S → Greet)
    changed = True
    while changed:
        changed = False
        for i in range(n):
            for j in range(i, n):
                current_set = table[i][j].copy()
                for lhs, rules in grammar.items():
                    for rhs in rules:
                        if len(rhs) == 1 and rhs[0] in current_set and lhs not in table[i][j]:
                            table[i][j].add(lhs)
                            changed = True

    # Step 4: Cek apakah S menghasilkan seluruh kalimat
    if "S" in table[0][n - 1]:
        print("Result: True")
    else:
        print("Result: False")

    #Cetak tabel CYK
    print("\nCYK Parse Table:")
    for i in range(n):
        row = ""
        for j in range(n):
            if j < i:
                row += "{:<20}".format("")
            else:
                row += "{:<20}".format(str(table[i][j]))
        print(row)

if __name__ == "__main__":
    sentences = [
        "Hello",
        "Hi",
        "How_are_you",
        "I am good",
        "You are okay",
        "I feeling great",
        "You doing good",
        "I am amazing",  # Invalid: "amazing" tidak ada di terminal
        "I Hello",       # Invalid struktur
        "I good"         # Invalid: tidak ada verb
    ]

    for sentence in sentences:
        cyk_parse(sentence.split())
