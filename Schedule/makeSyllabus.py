import datetime

daysstr = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
#Last day of class 12/4
#Reading day 12/7
#Final Examples 12/9-14
FIRSTDAY = datetime.date(2019, 8, 26)
Ds = [datetime.timedelta(1), datetime.timedelta(1), datetime.timedelta(1), datetime.timedelta(4)] #Monday To Tuesday, Tuesday To Wednesday, Wednesday To Thursday, Thursday To Monday
Holidays = {datetime.date(2019, 10, 14):"Fall Break", datetime.date(2019, 10, 15):"Fall Break", datetime.date(2019, 11, 27):"Thanksgiving",  datetime.date(2019, 11, 28):"Thanksgiving"}

#Put in syllabus header
fin = open("syllabus_begin.html", "r")
fout = open("index.html", "w")
for line in fin.readlines():
    fout.write(line)
fin.close()

#Load in assignments first, which will be peppered throughout the syllabus
fin = open("syllabus_content_assignments.txt", "r")
lines = fin.readlines()
fin.close()
assignments = []
for i in range(int(len(lines)/3)):
    datefields = [int(s) for s in str.split(lines[i*3+2], '-')]
    date = datetime.date(datefields[0], datefields[1], datefields[2])
    assignments.append([date, lines[i*3], lines[i*3+1]])

#Parse syllabus info and order by date
fin = open("syllabus_content_lectures.txt", "r")
lines = fin.readlines()
date = FIRSTDAY
addidx = 0
assignment_color = "#f4e6e7"
lecnum = 1

for i in range(int(len(lines)/4)):
    L = [l.rstrip() for l in lines[i*4:(i+1)*4]]
    if L[0] == "SECTION":
        fout.write("<tr><td colspan = \"5\"><h2><b>%s</b></h2><p>%s</p></td></tr>\n"%(L[1], L[2]))
    elif L[0] == "LECTURE":
        day = daysstr[date.weekday()]
        #Handle holidays
        while date in Holidays:
            fout.write("<tr><td>--</td><td>%s %i/%i/%i</td><td>%s</td><td></td><td>Enjoy!</td></tr>\n"%(day, date.month, date.day, date.year, Holidays[date]))
            date = date + Ds[addidx]
            addidx = (addidx + 1)%len(Ds)
            day = daysstr[date.weekday()]
        #Ordinary lectures
        assignmentsDueToday = []
        for a in assignments:
            if a[0] == date:
                assignmentsDueToday.append(a)
        fout.write("<tr>")
        fout.write("<td>%i</td>"%lecnum)
        fout.write("<td>%s %i/%i/%i</td>"%(day, date.month, date.day, date.year))
        if len(L[2]) > 0:
            fout.write("<td><a href = \"../Lectures/%s\">%s</a></td>"%(L[2], L[1]))
        else:
            fout.write("<td>%s</td>"%L[1])
        fout.write("<td>%s</td>"%L[3])
        if len(assignmentsDueToday) > 0:
            fout.write("<td bgcolor=%s>"%assignment_color)
        else:
            fout.write("<td>")
        for a in assignmentsDueToday:
            if len(a[2].strip()) > 0:   
                fout.write("<a href = \"%s\">%s</a>"%(a[2], a[1]))
            else:
                fout.write("%s"%a[1])
        fout.write("</td></tr>\n")
        nextdate = date + Ds[addidx]
        addidx = (addidx + 1)%len(Ds)
        #Check to see if any assignments are in between this date and the next date
        assignmentsDueInBetween = []
        for a in assignments:
            if (a[0] - date).days > 0 and (nextdate - a[0]).days > 0:
                assignmentsDueInBetween.append(a)
        if len(assignmentsDueInBetween) > 0:
            for a in assignmentsDueInBetween:
                fout.write("<tr>")
                fout.write("<td></td><td>%s %i/%i/%i</td><td></td><td></td><td bgcolor=%s>"%(daysstr[a[0].weekday()], a[0].month, a[0].day, a[0].year, assignment_color))
                if len(a[2].strip()) > 0:
                    fout.write("<a href = \"%s\">%s</a>"%(a[2], a[1]))
                else:
                    fout.write("%s"%a[1])
                fout.write("</td></tr>")
        date = nextdate
        lecnum += 1
fin.close()

#Put in syllabus footer
fin = open("syllabus_end.html", "r")
for line in fin.readlines():
    fout.write(line)
fin.close()
fout.close()
