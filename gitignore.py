# Append to .gitignore to avoid overwriting existing content
with open('.gitignore', 'a') as file:
    file.write('venv/\n')
    file.write('# Ignore virtual environment files\n')

# Read and print the contents of .gitignore
with open('.gitignore', 'r') as file:
    file_contents = file.readlines()

print(file_contents)
