
f = open('updates.txt', 'r')
x = f.readlines()

output = '{'
#print(x)

print(type(x))
print(x)


for item in x:
	output = output + '"line": "'+item+ '",'

f.close()

#remove the last trailing comma
output = output[:-1]
output = output + '}'