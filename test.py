with open("../tolst.txt", 'r') as file:
    lines = file.read()

parts = lines.split('.')
parts = [part.strip() for part in parts if part.strip()]
print(parts[25577])
print("------------------")
print(parts[25886])
print("------------------")
print(parts[26303])
print("------------------")
print(parts[26311])