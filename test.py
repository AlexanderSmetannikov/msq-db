with open("../tolst.txt", 'r') as file:
    lines = file.read()
#
parts = lines.split('.')
parts = [part.strip() for part in parts if part.strip()]
print(parts[15977])
print("------------------")
print(parts[5006])
print("------------------")
print(parts[5577])
print("------------------")
print(parts[4948])
