Chaine = 'Ceci est une chaine.'

CHAINE = Chaine.upper()
print "Chaine en majuscules", CHAINE

print "nombre de mots dans Chaine", len(Chaine.split())

chaine = Chaine.replace(' ', '').replace('.', '')
chaine = chaine.lower()
print chaine

lettres = {}
for c in chaine:
    lettres[c] = lettres.get(c, 0) + 1
print "occurences de chaque lettre dans Chaine", lettres
