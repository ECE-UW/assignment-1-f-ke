import re
class Point:
    def __init__(self,x,y):
        self.x=float(x)
        self.y=float(y)

    def __str__(self):
        return "("+str(self.x)+","+str(self.y)+")"

class line:
    def __init__(self,src,dst):
        self.src=src
        self.dst=dst
    def gets(self):
        return self.src
    def getd(self):
        return self.dst




    def __str__(self):
        return str(self.src)+"->"+str(self.dst)

class intersect:
    def __init__(self,l1,l2):
        self.l1=l1
        self.l2=l2

    def __str__(self):
        x1=self.l1.src.x
        x2 =self.l1.dst.x
        x3 =self.l2.src.x
        x4 = self.l2.dst.x
        y1 = self.l1.src.y
        y2 = self.l1.dst.y
        y3 = self.l2.src.y
        y4 = self.l2.dst.y
        a1 = y2 - y1
        b1 = -1*(x2 - x1)
        c1 = -1*x1 * y2 + x2 * y1

        a2 = y4 - y3
        b2 = -1*(x4 - x3)
        c2 = -1*x3 * y4 + x4 * y3
        d = a1 * b2 - a2 * b1 #d is xden and yden
        xnum=b1*c2-b2*c1
        ynum=a2*c1-a1*c2

        if xnum==-0.0:
            xum=0.0

        if ynum==-0.0:
            ynum=0.0
        if d!=0.0:

            xoccur=xnum/d
            yoccur=ynum/d
            if xoccur >=min(x1,x2) and yoccur<=max(y1,y2)and xoccur >=min(x3,x4) and yoccur<=max(y3,y4):
                return(xoccur,yoccur)

        else:
            return None

def getvetex(x):#getvetex from input vetex
    import re

    #s=""
    # for i in x.strip():
    #     if i == "(": continue
    #     if i == ",": continue
    #     if i == ")": continue
    #     if i == " ": continue #tomorrow use re to optimize it
    #     print i "this way  not work when we input negative number
    x = x.replace(" ", "")
    x = x.replace(")(", ",")
    x = x.replace(")", "")
    x = x.replace("(", "")
    x = x.replace(",", " ")
    x = x.split(' ')
    s= [i for i in x ]
    vertexeven = s[0::2]
    vertexodd = s[1::2]
    vertex = []
    for i in range(len(vertexeven)):
        vertex.append((float(vertexeven[i]), float(vertexodd[i])))

    # print("vertex is: ", vertex)
    return vertex
dics = {} #dictionary of street and following vertex

vertex_id = []




def main():
    while True:
        command=raw_input("please put your command here:")
        if command.strip()=='g':
            Graph()
            break

        patterna = r'\s*a \"(.+?)\"(( ?\(\-?\d+,\-?\d+\))+)\s*$'
        patternc = r'\s*c\s*\"(.+?)\"(( ?\(\-?\d+,\-?\d+\))+)\s*$'
        patternr = r'\s*r\s* \"(.+?)\"'
        amatch = re.match(patterna, command)

        cmatch = re.match(patternc, command)
        rmatch = re.match(patternr, command)
        command=command.replace(") (",")(")

        command_list = command.split('"')

        if len(command_list)==3:
            vertexstr = getvetex(command_list[2])
            for i in vertexstr:
                if i not in vertex_id:
                    vertex_id.append(i)
            print "vertex_id:",vertex_id
            print "command_list:",command_list
        if amatch:
            if command_list[1].lower not in dics:
                dics[command_list[1].lower()]=vertexstr

            else:
                print("errow for street name")
        elif cmatch:
            if command_list[1] in dics:
                dics[command_list[1].lower()]=vertexstr
            else:
                print("thie street is not existed")

        elif rmatch:
            if command_list[1] in dics:
                del dics[command_list[1].lower()]
            else:
                print "this street has been removed before"




        else:print "informal input"
        # print "your dics imformation:",dics


def Graph():
    global dics
    allpoints = []  # convert dictionary to list
    for i in dics:
        allpoints.append(dics[i])
        #print Point(allpoints[0][0][0],allpoints[0][0][1])

   # print allpoints
    interline=[]
    for i in range(len(allpoints)):
        for j in range(i+1,len(allpoints)):
            for m in range(len(allpoints[i])-1):
                l1=line(Point(allpoints[i][m][0],allpoints[i][m][1]),Point(allpoints[i][m+1][0],allpoints[i][m+1][1]))
                for p in range(len(allpoints[j])-1):
                    l2 = line(Point(allpoints[j][p][0], allpoints[j][p][1]),
                          Point(allpoints[j][p + 1][0], allpoints[j][p + 1][1]))
                    print l1,l2


                    if intersect(l1,l2).__str__():
                        interpoint =intersect(l1,l2).__str__()
                        if interpoint not in vertex_id:
                            vertex_id.append(interpoint)

                        if [allpoints[i][m],interpoint,allpoints[i][m+1]] not in interline:
                            interline.append([allpoints[i][m],interpoint,allpoints[i][m+1]])
                        if [allpoints[j][p],interpoint,allpoints[j][p+1]] not in interline:
                            interline.append([allpoints[j][p],interpoint,allpoints[j][p+1]])

    V={}
    vv=[]
    for i in range(len(interline)):
        for j in interline[i]:
            if j not in vv:
                vv.append(j)
    #print "vv:",vv

    for i in vv:

        # print "vertexid.index(i):",vertex_id.index(i)
        # print i
        V[vertex_id.index(i)]=i
    #print 'vertex_id:', vertex_id

    print "V{"
    for key, value in V.items():
        print ' ' + str(key) + ': ' + str(value)
    print "}"
    for p in range(len(interline)-1):
        for q in range(p+1, len(interline)):
            if interline[p][0]==interline[q][0] and interline[p][-1]==interline[q][-1]:
                newline=[]
                for i in interline[p]:
                    newline.append(i)
                for j in interline[q]:
                    if j not in newline:
                        newline.append(j)
                newline=sorted(newline)
                del interline[q]
                del interline[p]
                interline.append(newline)
                break

        if p == len(interline) - 2:
                break

    E=[]
    print "E={"
    for i in interline:
        # print'i',i
        for j in range(len(i)-1):
            # print 'i[j]',i[j]
            print "<"+str(vertex_id.index(i[j]))+" "+str(vertex_id.index(i[j+1]))+">"
            E.append([vertex_id.index(i[j]),vertex_id.index(i[j+1])])

    print "}"



if __name__ == '__main__':
    main()













