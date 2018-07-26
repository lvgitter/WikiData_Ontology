file = open("../roles/hasForewordAuthor.txt", 'r')
lines = file.readlines()
out = ""
out += lines[0]
for line in lines[1:]:
    out += line.replace('Q', ';Q')[1:]
file_out = open("../roles/hasForewordAuthor_correct.txt", 'w')
file_out.write(out)
file.close()
file_out.close()