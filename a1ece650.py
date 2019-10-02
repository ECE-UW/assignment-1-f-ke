"regrage"

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


def reinterline(interline):  # merge some more than one intersection group
    new_intersect_group = []
    tmp = []

    for j in range(len(interline) - 1):
        for i in range(j + 1, len(interline)):
            if interline[j][0] == interline[i][0] and interline[j][-1] == \
                    interline[i][-1]:
                for m in interline[j]:
                    tmp.append(m)
                for n in interline[i]:
                    if n not in tmp:
                        tmp.append(n)
                    else:
                        continue
                del interline[i]
                del interline[j]
                interline.append(sorted(tmp))
                tmp = []
                break
        if j == len(interline) - 2:
            break

    for i in new_intersect_group:
        interline.append(i)
    return interline


def getvetex(x):#getvetex from input vetex
    import re


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
def overlap(l1,l2):
    x1, y1 = l1.src.x, l1.src.y
    x2, y2 = l1.dst.x, l1.dst.y
    x3, y3 = l2.src.x, l2.src.y
    x4, y4 = l2.dst.x, l2.dst.y
    xden_new = (x3-x1)*(y2-y4) - (x2-x4)*(y3-y1)
    xden_new_2 = (x4-x1)*(y3-y2) - (x3-x2)*(y4-y1)
    if xden_new == 0 and xden_new_2 == 0:
        return True
    else:
        return False



dics = {} #dictionary of street and following vertex

vertex_id = []




def main():
    while True:
        command = raw_input()
        command_list=[]


        if '"' in command:
            command_list = command.split('"')
            if len(command_list)==3 and command[0]!='r':
                vertexstr = getvetex(command_list[2])
                for i in vertexstr:
                    if i not in vertex_id:
                        vertex_id.append(i)

        if command == '':
            print "Error: empty input!"
        elif command[0] == 'g':
            Graph()
        elif command[0] == 'a':
            patterna = r'a\s* \"(.+?)\" (( ?\(\-?\d+,\-?\d+\))+)\s*$'
            amatch = re.match(patterna, command)
            if amatch == None:
                print "Error: invalid input!"
            else:
                vetstre = getvetex(command_list[2])
                if command_list[1].lower() not in dics:
                    dics[command_list[1].lower()] = vetstre
                else:
                    print "Error: street name already exists!"
        elif command[0] == 'c':
            patternc = r'c\s* \"(.+?)\" (( ?\(\-?\d+,\-?\d+\))+)\s*$'
            cmatch = re.match(patternc, command)
            if cmatch == None:
                print "Error: invalid input! Please check again!"
            else:
                vetstre = getvetex(command_list[2])
                if command_list[1].lower() in dics:
                    dics[command_list[1].lower()] =vetstre
                else:
                    print "Error: 'c' specified for a street that does not exist!"
        elif command[0] == 'r':
            patternr = r'r\s* \"(.+?)\"'
            rmatch = re.match(patternr, command)
            if rmatch == None:
                print "Error: invalid input!"
            else:
                if command_list[1].lower() in dics:
                    del dics[command_list[1].lower()]
                else:
                    print "Error: 'r' specified for a street that does not exist!"
        else:
            print "Error: invalid input!"

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
                    #print l1,l2


                    if intersect(l1,l2).__str__():
                        interpoint =intersect(l1,l2).__str__()
                        if interpoint not in vertex_id:
                            vertex_id.append(interpoint)

                        if [allpoints[i][m],interpoint,allpoints[i][m+1]] not in interline:
                            interline.append([allpoints[i][m],interpoint,allpoints[i][m+1]])
                        if [allpoints[j][p],interpoint,allpoints[j][p+1]] not in interline:
                            interline.append([allpoints[j][p],interpoint,allpoints[j][p+1]])
                    elif overlap(l1, l2):
                        four_nodes = [allpoints[i][m], allpoints[i][m + 1], allpoints[j][p],allpoints[j][p + 1]]
                        four_nodes = sorted(four_nodes)
                        interline.append([four_nodes[0], four_nodes[1], four_nodes[2], four_nodes[3]])
                    else:
                        continue
    tmp = []

    while (not (tmp == interline)):
        tmp = []
        tmp = tmp + interline
        interline = reinterline(interline)





    V={}
    vv=[]
    for i in range(len(interline)):
        for j in interline[i]:
            if j not in vv:
                vv.append(j)


    for i in vv:
        V[vertex_id.index(i)]=i
    #print 'vertex_id:', vertex_id

    print "V{"
    for key, value in V.items():
        print ' ' + str(key) + ': ' + '(' + str("{0:.2f}".format(value[0])) + ',' + str(
            "{0:.2f}".format(value[1])) + ')'
    print "}"





    print "E={"
    for i in range(len(interline)):
    # print'i',i
        if i==len(interline)-1:

            for j in range(len(interline[i]) - 2):
        # print 'i[j]',i[j]
                print "<" + str(vertex_id.index(interline[i][j])) + " " + str(vertex_id.index(interline[i][j + 1])) +\
                      ">,"
            for j in range ((len(interline[i]) - 2),(len(interline[i]) - 1)):
                print "<" + str(vertex_id.index(interline[i][j])) + " " + str(vertex_id.index(interline[i][j + 1])) +\
                      ">"
        else:
            for j in range(len(interline[i]) - 1):
        # print 'i[j]',i[j]
                print "<" + str(vertex_id.index(interline[i][j])) + " " + str(vertex_id.index(interline[i][j + 1])) +\
                      ">,"




    print "}"


if __name__ == '__main__':
    main()















