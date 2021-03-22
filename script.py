test = "hejhfufkfgkhfllo"



test_string = "Heekforgeeks"

res = ''.join(sorted(test, key=lambda v : v.upper()))

res2 = ''.join(sorted(test_string, key=lambda v : v.upper()))


print("String after sorting : " + str(res)) 


resultat = res == res2

print(resultat)
