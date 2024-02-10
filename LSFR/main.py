Dict = {'A': '00000', 'B': '00001', 'C': '00010',
        'D': '00011', 'E': '00100', 'F': '00101',
        'G': '00110', 'H': '00111', 'I': '01000',
        'J': '01001', 'K': '01010', 'L': '01011',
        'M': '01100', 'N': '01101', 'O': '01110',
        'P': '01111', 'Q': '10000', 'R': '10001',
        'S': '10010', 'T': '10011', 'U': '10100',
        'V': '10101', 'W': '10110', 'X': '10111',
        'Y': '11000', 'Z': '11001', '.': '11010',
        '?': '11100', '!': '11011', '(': '11101',
        ')': '11110', '-': '11111'}

#Κατασκευή του κλειδιού KSA με βάση το κλειδί "HOUSE"
Key  = "HOUSE"
seed = []
for i in range(len(Key)):  #Μετατροπή του κλειδιού που μας δίνετε στην εκφώνηση σε BINARY
    seed.append(Dict[Key[i]])

#Αλγόριθμος 3.3.1.
#Κατασκευή μετάθεσης S
seedlen = len(seed)
S = list(range(256)) #for i = 0 to 255 do {S[i] ← i} end
j = 0
for i in range(256):
    j = (j + S[i] + int(seed[i % seedlen])) % 256 #Η μεταβλητή Int χρησιμοποιείται καθώς ο πίνακας είναι STR και όχι INT
    S[i], S[j] = S[j], S[i]  #swap S[i] ↔ S[j]

#Αλγόριθμος 3.3.2.
#Εκτέλεση του PRGA και κρυπτογράφηση του μηνύματος
plaintext = "MISTAKESAREASSERIOUSASTHERESULTSTHEYCAUSE"
Binary    = []
for i in range(len(plaintext)):  #Μετατροπή της έκφρασης σε BINARY
    Binary.append(Dict[plaintext[i]])
plen = len(plaintext) #το μήκος του κλειδιού θα είναι ίσο με το μήκος του μηνύματος plen
i = 0
j = 0
Key = [] #Δημιουργούμε το κλειδί χρησιμοποιώντας τον RC4
#Το κλειδί Key είναι μια σειρά τυχαίων αριθμών που παράγονται από τον πίνακα S
while (plen > 0):
    i = (i + 1)    % 256
    j = (j + S[i]) % 256
    S[i], S[j] = S[j], S[i]
    Key.append(str(S[(S[i] + S[j]) % 256]))
    plen -= 1

i = 0
Key_Binary = []
for i in range(len(Key)):
    temp = int(Key[i])
    Key_Binary.append(format(temp, 'b')) #Έτοιμη συνάρτηση που μετατρέπει τον αριθμό σε Binary
    if (len(Key_Binary[i]) < 8):         #Ελένχει αν ο αριθμός είναι 8-bit.
        while len(Key_Binary[i]) < 8:    #Προσθέτει μηδενικά στο τέλος σε ένα δυαδικό αριθμό μέχρι να γίνει 8-bit.
            Key_Binary[i] = "0" + Key_Binary[i]

#Κωδικοποίηση του μηνύματος
Coded_Binary = [[] for _ in range(len(Binary))] #Δημιουργεία λίστας όσο το μέγεθος των Binary στοιχείων
i = 0
for i in range(len(Binary)):
    j = 0
    for j in range(5):
        if Binary[i][j] == Key_Binary[i][j]: #Η IF κάνει την πράξη XOR καθώς δεν μπορούμε να χρησιμοποιήσουμε την έτοιμη συνάρτηση
            Coded_Binary[i].append(0)
        else:
            Coded_Binary[i].append(1)
#print(Coded_Binary)

#Encrypted message
Coded = ''
j     = 0
for i in range(len(Coded_Binary)):
    k    = 0
    temp = ''
    for k in range(5): #Απο το 8-Bits του κλειδιού κρατάω τα πρώτα 5 καθώς στα άλλα είναι 0, που το έχω προσθέσει για να μπορέσει να γίνει η XOR
        temp += str(Coded_Binary[i][k]) #Κρατάω τα πρώτα 5 σε μια βοηθητική μεταβλητή
    for key in Dict.keys(): #Ψαχνει για τον αριθμο αν υπαρχει στο λεξικο
        if Dict[key] == temp:
            Coded += key #Αντιστοίχηση των Bit στο κατάλληλο γράμμα
print('Coded message:', Coded)

#Dencrypted message
Crypto_message_Binary = []
for i in range(len(Coded)):  #Μετατρέψαμε σε BINARY το κρυπτογραφημένο κείμενο
    Crypto_message_Binary.append(Dict[Coded[i]])

Decoded_Binary = [[] for _ in range(len(Crypto_message_Binary))]
i = 0
for i in range(len(Crypto_message_Binary)):  #XOR του κλειδιού με το κρυπτογραφημένο μήνυμα
    j = 0
    for j in range(5):
        if Crypto_message_Binary[i][j] == Key_Binary[i][j]:
            Decoded_Binary[i].append(0)
        else:
            Decoded_Binary[i].append(1)

#Αντιστοίχηση του μηνύματος του Binary αριμθού με τα γράμματα του λεξικού
Decoded = ''
j       = 0
for i in range(len(Decoded_Binary)):
    k    = 0
    temp = ''
    for k in range(5):
        temp += str(Decoded_Binary[i][k])
    for key in Dict.keys():
        if Dict[key] == temp:
            Decoded += key

print('Decoded message:', Decoded)
