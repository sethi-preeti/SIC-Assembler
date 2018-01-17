from collections import OrderedDict
def a24to6(Bits):			#Function to convert 24 bit binary to hexadecimal
	res=""
	arr=['0','1','2','3','4','5','6','7','8','9','A','B','C','D','E','F']
	for i in range(6):
		s=Bits[i*4:(i*4)+4]
		x=int(s,2)
		res+=arr[x]
	return res

def a16to6(Bits):			#Function to convert 16 bit binary to hexadecimal
	res=""
	arr=['0','1','2','3','4','5','6','7','8','9','A','B','C','D','E','F']
	for i in range(4):
		s=Bits[i*4:(i*4)+4]
		x=int(s,2)
		res+=arr[x]
	return res

def hextobin(n):				#Function to convert hexadecimal to binary
	result=""
	for i in n:
		OneHexCharacter=""
		x=bin(int(i,16))
		OneHexCharacter+=x[2:]
		Zero="0"*(4-len(x[2:]))
		OneHexCharacter=Zero+OneHexCharacter
		result+=OneHexCharacter
	return result[1:]

def hexAdd(loc,x):					#Function to Add hexadecimal number
	temp=int(str(loc),16)
	temp+=int(x)
	return hex(temp)
def readFile():						#Function to read input file
	symtab=[]
	optab=[]
	operand=[]
	lines=[]
	f=open('input.txt',"r+")
	for line in f.readlines():					#Making 3 arrays, each for symbol,opcode and operand for every instruction in input file
		s=line.strip()
		if(len(s)!=0 and not s.__contains__(".")):		
			x=s.split(" ")
			print(x)
			y=[]
			for i in range(len(x)):
				x[i]=x[i].strip()
				if(len(x[i])>=1):
					y.append(x[i])
			x=y[:]
			if(len(x)==1):
`				x=[" "]+x+[" "]
				operand.append(x[0])
			elif(len(x)==2):
				x=[" "]+x
				optab.append(x[0])
				operand.append(x[1])
			else:
				symtab.append(x[0])
				optab.append(x[1])
				operand.append(x[2])
			lines.append(x)						#lines contains all the lines of input, individually
	return symtab,optab,operand,lines
symtab,optab,operand,lines=readFile()
f1=open('intermediate.txt',"w+")
tempVar=""
ProgName=""
machineCodes=[]
LOC=0
tim=lines[0]
if 'START' or 'Start' in tim:
	LOC=tim[-1]
	tempVar=tim[-1]
	ProgName=tim[0]
	s=" ".join(tim)
	f1.write("%s %s\n"%(LOC,s))			
	machineCodes.append(tempVar)
temp=0
if 'START' or 'Start' in tim:
	temp=1
if(temp==1):
	machineCodes.append(tempVar)
	s=" ".join(lines[1])
	f1.write("%s %s\n"%(LOC,s))			
else:
	machineCodes.append("0000")
for i in range(temp+1,len(lines)):
	s="".join(lines[i])
	if(lines[i][1]=='END'):
		break
	else:
		t=0
		if(lines[i][1]=='WORD'):
			LOC=hexAdd(LOC,3)
		elif(lines[i][1]=='RESW'):
			LOC=hexAdd(LOC,3)
			t=3*int(lines[i][2])-3
		elif(lines[i][1] == 'RESB'):
			LOC=hexAdd(LOC,3)
			t=int(lines[i][2])-3
		elif(lines[i][1] == 'BYTE'):
			by=0
			p=lines[i][2]
			if(p[0]=="C"):
				temp=p[2:-1]
				if(temp=="EOF"):
					by=3
				else:
					by=len(temp)
			elif(p[0]=='X'):
				temp=p[2:-1]
				by=len(temp)//2
			LOC=hexAdd(LOC,3)
			t=by-3
		else:
			LOC=hexAdd(LOC,3)
	temporary=LOC[2:]+" "+" ".join(lines[i])		
	f1.write("%s\n"%(temporary))
	machineCodes.append(LOC[2:])
	LOC=hexAdd(LOC,t)
symtab=[]
optab=[]
operands=[]
for i in lines:
	# print(i)
	if(i[0]!=' ' and len(i[0])>=1):
		symtab.append(i[0])
	if(i[1]!=' ' and len(i[1])>=1):
		optab.append(i[1])
	if(i[2]!=' ' and len(i[2])>=1):
		operands.append(i[2])
abc={}
for i in range(len(symtab)):
	for j in range(len(lines)):
		if(lines[j][0]==symtab[i]):
			abc[symtab[i]]=machineCodes[j]
opcode={}
f3=open("opfile","r+")
for line in f3.readlines():
	x=line.split(" ")
	y=[]
	for j in x:
		p=j.strip()
		if(len(p)>0):
			y.append(p)
	opcode[y[0]]=y[1]
print(opcode)
objcode=[]
for i in lines:
	s=""
	if(i[1]=="START"):
		s=""
	elif(i[1]=="WORD"):
		b=hex(int(i[-1]))[2:]
		c="0"*(6-len(b))
		s+=c+b
	elif(i[1]=="RESW" or i[1]=="RESB"):
		s=""
	elif(i[1]=="END"):
		continue
	elif(i[1]=="BYTE"):
		p=i[-1]
		if(p[0]=="C"):
			temp=p[2:-1]
			if(temp=="EOF"):
				s="454F46"
			else:
				s=""
		elif(p[0]=='X'):
			temp=p[2:-1]
			s=temp
	elif(i[1]=="RSUB"):							
		s=opcode['RSUB']+"0000"
	else:
		oc=opcode[i[1]]
		s+=oc
		t=""
		u=0
		opr=i[-1]
		if(opr.__contains__(',')):
			t+="1"
			opr=opr[:opr.index(',')]
		else:
			t+="0"
		if(abc.keys().__contains__(opr)):
			u=abc[opr]
		t+=hextobin(u)
		s+=a16to6(t)
	objcode.append(s)
for objectCode in objcode:
	print(objectCode)

def sst(startaddr):
	f2.write("T^")
	x="0"*(6-len(startaddr))
	f2.write("%s%s^"%(x,startaddr))	

def writeTof2(stradr,ObjectCodes):
	f2.write("T^")
	x="0"*(6-len(stradr))
	f2.write("%s%s^"%(x,stradr))
	temp=""
	for objco in ObjectCodes:
		temp+=objco
	size=len(temp)//2
	s=hex(size)[2:]
	y="0"*(2-len(s))
	f2.write("%s%s^"%(y,s))
	for i in ObjectCodes:
		if i!='' and i!=' ':
			f2.write("%s^"%i)
	f2.write("\n")
mapMAddrToObjCode=OrderedDict()
for i in range(len(machineCodes)):
	mapMAddrToObjCode[machineCodes[i]]=objcode[i]
print("mapMAddrToObjCode=",mapMAddrToObjCode)

f1.close()
f1=open('intermediate.txt',"r+")
f2=open('objProg.txt',"w+")
f2.write("H^")
f2.write("%s"%(	))
x=" "*(6-len(ProgName))
f2.write("%s^"%(x))
x="0"*(6-len(tempVar))
f2.write("%s%s^"%(x,tempVar))
y=hex(int(machineCodes[-1],16) - int(machineCodes[0],16) + 1)[2:]
x="0"*(6-len(y))
f2.write("%s%s\n"%(x,y))

dr=[]
co=0
flag=1
stradr=tempVar
for i in range(1,len(machineCodes)):
	print(machineCodes[i])
	print(co)
	print(dr)
	if flag==1:
		stradr=machineCodes[i]
		flag=0
	if(mapMAddrToObjCode[machineCodes[i]]==' ' or co==10):
		if(len(dr)>0):
			writeTof2(stradr,dr)
			dr=[]
			co=0
			flag=1
		if(len(mapMAddrToObjCode[machineCodes[i]])>0):			
			co+=1
			dr.append(mapMAddrToObjCode[machineCodes[i]])
	else:
		co+=1
		dr.append(mapMAddrToObjCode[machineCodes[i]])
if(len(dr)):
	writeTof2(stradr,dr)

f2.write("E^")

x=lines[-1][1]
if(x=='END'):
	LastinsAddr=""
	Lastins=lines[-1][2] 
	for i in range(len(lines)):
		if(lines[i][0]==Lastins):
			LastinsAddr=machineCodes[i]
	t="0"*(6-len(LastinsAddr))
	f2.write("%s%s"%(t,LastinsAddr))
else:
	Lastins="0"*6
	f2.write("%s"%(Lastins))
