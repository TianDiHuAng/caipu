import io,re
p=r"E:\ai_project\marvis_project\caipu\temp\gen325.py"
s=io.open(p,encoding='utf-8').read()
s2,n=re.subn('"a":([0-9.]+),"(g|ml|piece)"', r'"a":\1,"u":"\2"', s)
io.open(p,'w',encoding='utf-8',newline='\n').write(s2)
print('fixed',n)
