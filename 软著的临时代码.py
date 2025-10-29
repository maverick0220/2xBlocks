old = open("code.txt", "r", encoding="utf-8")
new = open("code_new.txt", "w", encoding="utf-8")

for line in old:
     if "/**" in line:
         flag = True
         continue
     if flag and "*" in line:
         continue
     else:
         flag = False
     new.write(line)
old.close()
new.close()