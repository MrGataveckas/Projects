#!/usr/bin/env python
"""\
FactorMe! Math Learning Software - This program generates practice questions
for Grade 10 and 11s to factor trinomials into two binomials and a coefficient.
"""
from tkinter import *
import random
__author__ = "Noah Gataveckas"
__copyright__ = "May 2023. All rights reserved."
__version__ = "1.0"
__email__ = "ngataveckas@torontoprepschool.com"
__status__ = "Beta"

fracs = {'.1':"\u2152", '.111':'⅑', '.125':'\u215b', '.167':"\u2159", '.2':"\u2155", '.222':'²⁄₉', '.25':'\u00bc',
         '.3':'³⁄₁₀', '.333':"\u2153", '.375':"\u215c", '.4':'\u2156', '.444':'⁴⁄₉', '.5':'\u00bd', '.556':'⁵⁄₉',
         '.6':'\u2157', '.625':'\u215d', '.667':"\u2154", '.7':'⁷⁄₁₀', '.75':'\u00be', '.778':'⁷⁄₉', '.8':'\u2158',
         '.875':'u215e', '.833':'\u215a', '.889':'⁸⁄₉', '.9':'⁹⁄₁₀'}
compfracs = {'.1':'1/10', '.111':'1/9', '.125':'1/8', '.167':'1/6', '.2':"1/5", '.222':'2/9', '.25':'1/4', '.3':'3/10',
             '.333':'1/3', '.375':'3/8', '.4':'2/5', '.444':'4/9', '.5':'1/2', '.556':'5/9', '.6':'3/5', '.625':'5/8',
             '.667':'2/3', '.7':'7/10', '.75':'3/4', '.778':'7/9', '.8':'4/5', '.833':'5/6', '.875':'7/8', '.889':'8/9', '.9':'9/10'}
supers = {'-':'-', '0':'\u2070', '1':'\u00b9', '2':'\u00b2', '3':'\u00b3', '4':'\u2074', '5':'\u2075', '6':'\u2076', '7':'\u2077', '8':'\u2078', '9':'\u2079'}
subs = {'0':'\u2080', '1':'\u2081', '2':'\u2082', '3':'\u2083', '4':'\u2084', '5':'\u2085', '6':'\u2086', '7':'\u2087', '8':'\u2088', '9':'\u2089'}

class app:
    def __init__(self):
        self.root = Tk()
        self.root.title("FactorMe! Math Learning Software")
        self.root.geometry("755x280")
        self.root.resizable(False, False)
        self.buildapp()

    def buildapp(self):
        self.opframe = LabelFrame(self.root, text = "Options", labelanchor='n') #Start by building options frame
        self.negvar = IntVar()
        self.covar = IntVar()
        self.decvar = IntVar()
        self.fracvar = IntVar()
        self.mixvar = IntVar()
        self.brackvar = IntVar()
        self.ssvar = IntVar()
        self.neg = Checkbutton(self.opframe, text = "Negative values", variable=self.negvar)
        self.co = Checkbutton(self.opframe, text = "Integer coefficients", variable=self.covar)
        self.dec = Checkbutton(self.opframe, text = "Decimal coefficients", variable=self.decvar)
        self.frac = Checkbutton(self.opframe, text = "Fractional coefficients", variable=self.fracvar)
        self.mix = Checkbutton(self.opframe, text = "No mixed numbers", variable = self.mixvar)
        self.brack = Checkbutton(self.opframe, text = "Brackets on fractions", variable = self.brackvar)
        self.ss = Checkbutton(self.opframe, text = "Super-/sub-scripts\non fractions", variable = self.ssvar)
        self.diff = Listbox(self.opframe, height=9, exportselection = False)
        self.neg.invoke()
        self.co.invoke()
        self.frac.invoke()
        self.mix.invoke()
        self.ss.invoke()
        self.diff.insert(1, "Easiest")
        self.diff.insert(2, "Easier")
        self.diff.insert(3, "Easy")
        self.diff.insert(4, "Medium-Easy")
        self.diff.insert(5, "Medium")
        self.diff.insert(6, "Medium-Hard")
        self.diff.insert(7, "Hard")
        self.diff.insert(8, "Harder")
        self.diff.insert(9, "Hardest")
        self.diff.select_set(4)
        self.diff.grid(row=0, column = 0, rowspan = 7)
        self.neg.grid(row=0, column = 1)
        self.co.grid(row=1, column = 1)
        self.dec.grid(row=2, column = 1)
        self.frac.grid(row = 3, column = 1)
        self.mix.grid(row = 4, column = 1)
        self.ss.grid(row = 5, column = 1)
        self.brack.grid(row = 6, column = 1)
        self.opframe.grid(row = 0, column = 1, columnspan=2)

        self.rframe = Frame(self.root) #Then build the main fields for questions and answers
        self.qframe = LabelFrame(self.rframe, text = "To be factored:")
        self.qentry = Entry(self.qframe, justify=CENTER, font=("Arial 20"), disabledbackground="white",disabledforeground="black")
        self.qentry.config(width = 30)
        self.qentry.pack()
        self.qframe.grid(row=0, column = 0, padx=10, pady=10)
        self.aframe = LabelFrame(self.rframe, text = "Your answer here:")
        self.aentry = Entry(self.aframe, font=("Arial 20"), width = 30)
        self.aentry.pack()
        self.aframe.grid(row=2, column = 0, padx=10, pady=10)
        self.rframe.grid(row=0, column = 0)
        self.genbutton = Button(self.root, text = "Generate new question", command = self.newq) #and accompanying buttons
        self.genbutton.grid(row=2, column = 0)
        self.subbutton = Button(self.root, text = "Submit answer", command = self.submit)
        self.subbutton.grid(row=3, column = 0)
        self.helpbutton = Button(self.root, text = "Help: How to use", command = self.help)
        self.helpbutton.grid(row = 2, column = 1)
        self.teachbutton = Button(self.root, text = "Help: How to factor", command = self.howtofactor)
        self.teachbutton.grid(row = 3, column = 1)
        self.aboutbutton = Button(self.root, text = "About", command = self.about)
        self.aboutbutton.grid(row = 2, column = 2)
        self.a, self.adj = '', ''
        self.myqs = ["None"]
        self.specialslash = '\u2215'

    def newq(self): #generate a string and correct values of a new 'question', which is actually going to take the form of the proper answer
        self.qentry.config(state = NORMAL)
        self.qentry.delete(0, END)
        self.aentry.delete(0, END)
        n3 = 1
        try:
            diff = self.diff.get(self.diff.curselection())
        except:
            return
        self.cof1, self.cof2 = '', ''
        if diff == "Easiest":
            self.decs = [1/2]
            r = 3
        elif diff == "Easier":
            self.decs = [1/10, 1/2]
            r = 6
        elif diff == "Easy":
            self.decs = [1/10, 1/2, 1/4, 1/5]
            r = 9
        elif diff == "Medium-Easy":
            self.decs = [1/10, 1/2, 1/4, 1/5, 1/3]
            r = 12
        elif diff == "Medium":
            self.decs = [1/10, 1/2, 1/4, 3/4, 1/5, 1/3]
            r = 15
        elif diff == "Medium-Hard":
            r = 19
            self.decs = [1/10, 1/2, 1/4, 3/4, 1/5, 1/3, 2/3, 1/8]
        elif diff == "Hard":
            self.decs = [1/10, 1/2, 1/4, 3/4, 1/5, 1/3, 2/3, 1/6, 1/8]
            r = 23
        elif diff == "Harder":
            self.decs = [1/10, 1/2, 1/4, 3/4, 1/5, 1/3, 2/3, 1/6, 5/6, 1/8]
            r = 27
        else:
            self.decs = [1/10, 1/2, 1/4, 3/4, 1/5, 1/3, 2/3, 1/6, 5/6, 1/8, 1/9]
            r = 30
        if self.negvar.get():
            n1 = random.randrange(-1 * r, r)
            n2 = random.randrange(-1 * r, r)
            if self.covar.get():
                n3 = random.randrange(-1 * int(r / 2), int(r / 2))
                if n3 in [0, 1]:
                    n3 = 2
            if self.covar.get() and (self.decvar.get() or self.fracvar.get()) and random.randrange(2) == 1:
                n3 = random.choice(self.decs) * random.randrange(-1, 2, 2)
            elif (self.decvar.get() or self.fracvar.get()) and not self.covar.get():
                n3 = random.choice(self.decs) * random.randrange(-1, 2, 2)
            if n1 == 0:
                n1 = 1
            if n2 == 0:
                n2 = 1
        else:
            n1 = random.randrange(1, r)
            n2 = random.randrange(1, r)
            if self.covar.get():
                n3 = random.randrange(2, int(r/2) + 1)
            if (self.decvar.get() or self.fracvar.get()) and self.covar.get() and random.randrange(2) == 1:
                n3 = random.choice(self.decs)
            elif (self.decvar.get() or self.fracvar.get()) and not self.covar.get():
                n3 = random.choice(self.decs)
        if diff == "Medium-Easy" and self.covar.get():
            self.cof1 = random.choice(['', 2])
            if self.cof1 == 2 and n1 % self.cof1 == 0:
                self.cof1 = 1
        elif diff == "Medium" and self.covar.get():
            self.cof1 = random.choice(['', 2, 3])
            if self.cof1 in [2, 3] and n1 % self.cof1 == 0:
                self.cof1 = ''
        elif diff == "Medium-Hard" and self.covar.get():
            self.cof1 = random.choice(['', 2, 3, 5])
            if self.cof1 in [2, 3, 5] and n1 % self.cof1 == 0:
                self.cof1 = ''
            self.cof2 = random.choice(['', 2])
            if self.cof2 == 2 and n1 % self.cof2 == 0:
                self.cof2 = ''
        elif diff == "Hard" and self.covar.get():
            self.cof1 = random.choice(['', 2, 3, 5])
            self.cof2 = random.choice(['', 2, 3, 5])
            if self.cof1 in [2, 3, 5] and n1 % self.cof1 == 0:
                self.cof1 = ''
            if self.cof2 in [2, 3, 5] and n2 % self.cof2 == 0:
                self.cof2 = ''
        elif diff == "Harder" and self.covar.get():
            self.cof1 = random.choice(['', 2, 3, 5, 7])
            self.cof2 = random.choice(['', 2, 3, 5, 7])
            if self.cof1 in [2, 3, 5, 7] and n1 % self.cof1 == 0:
                self.cof1 = ''
            if self.cof2 in [2, 3, 5, 7] and n2 % self.cof2 == 0:
                self.cof2 = ''
        elif diff == "Hardest" and self.covar.get():
            self.cof1 = random.choice(['', 2, 3, 5, 7, 9])
            self.cof2 = random.choice(['', 2, 3, 5, 7, 9])
            if self.cof1 in [2, 3, 5, 7, 9] and n1 % self.cof1 == 0:
                self.cof1 = ''
            if self.cof2 in [2, 3, 5, 7, 9] and n2 % self.cof2 == 0:
                self.cof2 = ''
        n1sign, n2sign = '', ''
        if n1 > 0:
            n1sign = '+'
        if n2 > 0:
            n2sign = '+'
        self.myq = '({}x{}{})({}x{}{})'.format(self.cof1, n1sign, n1, self.cof2, n2sign, n2)
        self.myq2 = '({}x{}{})({}x{}{})'.format(self.cof2, n2sign, n2, self.cof1, n1sign, n1)
        self.myq3 = '1' + self.myq
        self.myq4 = '1' + self.myq2
        self.myqs = [self.myq, self.myq2, self.myq3, self.myq4, '(1)' + self.myq, '(1)' + self.myq2, 
                     '1.0' + self.myq, '1.0' + self.myq2, '(1.0)' + self.myq, '(1.0)' + self.myq2]
        if self.cof1 == '':
            self.cof1 = 1
        if self.cof2 == '':
            self.cof2 = 1
        self.chance = random.randrange(2) #chance is used to decide between fractions and decimals if both are selected
        if n3 != 1:
            self.myq3 = str(fractioner(decimalcheck(n3), compfracs, True, self.brackvar.get(), False)) + self.myq
            self.myq4 = str(fractioner(decimalcheck(n3), compfracs, True, self.brackvar.get(), False)) + self.myq2
            self.myq = str(decimalcheck(n3)) + self.myq
            self.myq2 = str(decimalcheck(n3)) + self.myq2
            if self.fracvar.get() and (not self.decvar.get() or self.chance):
                self.myqs = [self.myq3, self.myq4, self.myq, self.myq2]
            else:
                self.myqs = [self.myq, self.myq2, self.myq3, self.myq4]
            for i in range(len(self.myqs)):
                if n3 < 0:
                    if self.myqs[i][0] != '-':
                        self.myqs[i] = '-' + self.myqs[i]
                    if self.myqs[i][1:3] == '1(':
                        self.myqs.append(self.myqs[i][0] + self.myqs[i][2:])
                    if self.brackvar.get() and (self.myqs[i].find('/') != -1 or self.myqs[i].find(self.specialslash) != -1):
                        self.myqs[i] = '(' + self.myqs[i][0] + self.myqs[i][2:]
                if self.myqs[i][:self.myqs[i].find('(')].find('.') != -1:
                    self.myqs.append('(' + self.myqs[i][:self.myqs[i].find('(')] + ')' + self.myqs[i][self.myqs[i].find('('):])
                if self.myqs.count(self.myqs[i]) == 2:
                    brackpoint = self.myqs[i].find('(')
                    self.myqs.append('(' + self.myqs[i][:brackpoint] + ')' + self.myqs[i][brackpoint:])
                    if self.myqs[i][:brackpoint].find('.') == -1 and self.myqs[i][0] != '(':
                        self.myqs[i] = self.myqs[i][:brackpoint] + '.0' + self.myqs[i][brackpoint:]
                        brackpoint = self.myqs[i].find('(')
                        self.myqs.append('(' + self.myqs[i][:brackpoint] + ')' + self.myqs[i][brackpoint:])
                if not self.brackvar.get() and (self.myqs[i].find('/') != -1 or self.myqs[i].find(self.specialslash) != -1):
                    brackpoint = self.myqs[i].find('(')
                    newq = '(' + self.myqs[i][:brackpoint] + ')' + self.myqs[i][brackpoint:]
                    self.myqs.append(newq)
                elif self.brackvar.get() and (self.myqs[i].find('/') != -1 or self.myqs[i].find(self.specialslash) != -1):
                    brackpoint = self.myqs[i].find(')')
                    newq = self.myqs[i][1:brackpoint] + self.myqs[i][brackpoint + 1:]
                    self.myqs.append(newq)
            while self.myqs[0][:self.myqs[0].find(')')].find('.') != -1 and str(n3).find('.') == -1:
                temp = self.myqs.pop(0)
                self.myqs.append(temp)
        self.a, self.adj = self.newa(n1, n2, n3)
        self.qentry.insert(END, self.a)
        self.qentry.config(state = DISABLED)
        
    def newa(self, n1, n2, n3): #generate a new 'answer', which is actually the question that will be prompted to the user
        a = n3
        if a < 0:
            leadingnegative = True
        else:
            leadingnegative = False
        b = a * (n1 * self.cof2 + n2 * self.cof1)
        c = a * (n1 * n2)
        a = a * self.cof1 * self.cof2
        if b >= 0:
            bsign = '+'
        else:
            bsign = '-'
        if c >= 0:
            csign = '+'
        else:
            csign = '-'
        a = decimalcheck(a)
        b = decimalcheck(b)
        c = decimalcheck(c)
        if float(b) != 0:
            if self.fracvar.get() and (not self.decvar.get() or self.chance):
                if self.mixvar.get():
                    myans = "x² {} {}x {} {}".format(bsign, fractioner(b, compfracs, True, self.brackvar.get(), self.ssvar.get()),
                                                    csign, fractioner(c, compfracs, True, self.brackvar.get(), self.ssvar.get()))
                    myadjans = myans.replace('²', '^')
                else:                      
                    myans = "x² {} {}x {} {}".format(bsign, fractioner(b, fracs, False, self.brackvar.get(), self.ssvar.get()),
                                             csign, fractioner(c, fracs, False, self.brackvar.get(), self.ssvar.get()))
                    myadjans = myans.replace('²', '^')
            else:
                myans = "x² {} {}x {} {}".format(bsign, b, csign, c)
                myans = "x² {} {}x {} {}".format(bsign, b, csign, c)
                myadjans = myans.replace('²', '^')
        else:
            if self.fracvar.get() and (not self.decvar.get() or self.chance):
                if self.mixvar.get():
                    myans = "x² {} {}".format(csign, fractioner(c, compfracs, self.mixvar.get(), self.brackvar.get(), self.ssvar.get()))
                    myadjans = myans.replace('²', '^')
                else:
                    myans = "x² {} {}".format(csign, fractioner(c, fracs, self.mixvar.get(), self.brackvar.get(), self.ssvar.get()))
                    myadjans = myans.replace('²', '^')
            else:
                myans = "x² {} {}".format(csign, c)
                myadjans = myans.replace('²', '^')
        if a != 1:
            if self.fracvar.get() and (not self.decvar.get() or self.chance):
                if self.mixvar.get():
                    myans = str(fractioner(a, compfracs, self.mixvar.get(), self.brackvar.get(), self.ssvar.get())) + myans
                    myadjans = str(fractioner(a, compfracs, self.mixvar.get(), self.brackvar.get(), self.ssvar.get())) + myadjans
                else:
                    myans = str(fractioner(a, fracs, self.mixvar.get(), self.brackvar.get(), self.ssvar.get())) + myans
                    myadjans = str(fractioner(a, fracs, self.mixvar.get(), self.brackvar.get(), self.ssvar.get())) + myadjans
            else:
                myans = str(a) + myans
                myadjans = str(a) + myadjans
            if leadingnegative and myans[0] != '-':
                myans = '-' + myans
                myadjans = '-' + myadjans
                if self.brackvar.get() and (myans.find('/') != -1 or myans.find(self.specialslash) != -1 or self.fracvar.get()) and myans[:myans.find('x')].find('(') != -1:
                    myans = '(' + myans[0] + myans[2:]
                    myadjans = '(' + myadjans[0] + myadjans[2:]
        elif a == 1 and leadingnegative:
            myans = '-' + myans
            myadjans = '-' + myadjans
        return (myans, myadjans)

    def submit(self): #the function that gets run when the 'submit answer' button is pressed
        attempt = self.aentry.get()
        if attempt != '' and attempt in self.myqs:
            self.aentry.delete(0, END)
            self.aentry.insert(END, attempt + " \u2713")
        else:
            self.aentry.delete(0, END)
            self.aentry.insert(END, "ANSWER: " + self.myqs[0])

    def help(self): #help pop-up
        mytext = ("\nTo use this program:\n" +
            "\n1. Select a difficulty level and any other options before generating a new problem." +
            "\n(The default is set to Medium (Grade 10 level), with negatives, improper fractions, and coefficients.)" +
            "\n\n2. Then click 'Generate new question' to get a new quadratic equation in standard form." +
            "\n\n3. Without using spaces, y=, the equal sign, or using the multiplication symbol, enter" +
            "\nyour answer into the field titled 'Your answer here', and hit the 'Submit answer' button" +
            "\n(For example: enter -2(x-3)(x+4) to answer correctly when factoring -2x²-2x+24, or" +
            "\n1/2(x+3)(2x+1) for  x²+7/2x+3/2, 0.333(x-2)(x+2) for 0.333x² + 2.667, etc.)" +
            "\n\n*Decimal values are used to approximate fractions. Don't treat them literally: rather, let" +
            "\n0.167 = 1/6, 0.333 = 1/3, 0.667 = 2/3, 0.833 = 5/6, 0.556 = 5/9, etc. Answers will be accepted" +
            "\nin both fraction and decimal form. Fractions can be with or without brackets. If using brackets" + 
            "\nwith negative fractions include negative signs inside brackets when working with leading coefficients." +
            "\nFor example, -1/2(x+1)(x-1) = (-1/2)(x+1)(x-1) = -0.5(x+1)(x-1) are all valid for -0.5x² + 0.5.*" +
            "\n\n4. If your answer is correct, you are awarded a checkmark (\u2713)." +
            "\n\n5. If your answer is not correct, you are informed of the correct answer without a check." +
            "\n\n6. Reset the options and difficulty level to try another problem.\n")
        newwindow = Tk()
        newwindow.title("Help: How to use")
        newlabel = Label(newwindow, text = mytext, justify=LEFT, padx = 5, font=("Arial 16"))
        newlabel.pack()

    def howtofactor(self): #another help pop-up
        mytext = ("\nHow to factor a trinomial: ax² + bx + c\n" +
            "\n1. Common factor out any value that is common to the three terms of the trinomial (a, b, and c)," +
            "\nwith the exception of positive 1, since this does not change the trinomial whatsoever." +
            "\nAfter this your a, b and c values should not include any fractional or decimal values." + 
            "\n\n*Decimal values are used to approximate fractions. Don't treat them literally: rather, let" +
            "\n0.167 = 1/6, 0.333 = 1/3, 0.667 = 2/3, 0.833 = 5/6, 0.556 = 5/9, etc. Answers will be accepted" +
            "\nin both fraction and decimal form. Don't include spaces in your answers. Fractions can be with or" +
            "\nwithout brackets. If using brackets with negative fractions include negative signs inside brackets" +
            "\nwhen working with leading coefficients. For example, -1/2(x+1)(x-1) = (-1/2)(x+1)(x-1) = -0.5(x+1)(x-1)" +
            "\nare all valid for -0.5x² + 0.5.*" +
            "\n\nExample:  2x² + 14x + 24  \u2192  2(x² + 7x + 12)" +
            "\n\n2. Based on the remaining values for a, b and c, construct a product-sum table to" +
            "\ndiscover what two values would multiply to a times c and at the same time add up to b." +
            "\n\nExample:  Product: 12  Sum: 7  \u2192  Thus 7 will decompose into 3 and 4 (since 3 + 4 = 7; 3 * 4 = 12)" +
            "\n\n3. Re-write the trinomial with four terms, having decomposed the middle" +
            "\nb value into the two terms that you discovered from the product-sum table." +
            "\n\nExample:  2(x² + 7x + 12)  \u2192  2(x² + 3x + 4x + 12)" +
            "\n\n4. Group factor the first two terms of the decomposed trinomial, and then group factor" +
            "\nthe last two terms. At this point you should have two binomials that have identical values in them." +
            "\n\nExample:  2(x² + 3x + 4x + 12)  \u2192  2( x(x + 3) + 4(x + 3) )" +
            "\n\n5. 'Re-make the broken binomial' by making a new binomial based on the values you group factored" +
            "\nout of the previous step. The other binomial will be the repeating binomial from the previous step." +
            "\n\nExample:  2( x(x + 3) + 4(x + 3) )  \u2192  2(x+3)(x+4)" + 
            "\n\n6. You should now have two binomials, possibly with a coefficient that was factored out in step 1." +
            "\nNow enter the factored form of the equation into the answer box, and click 'Submit answer'.\n")
        newwindow = Tk()
        newwindow.title("Help: How to factor trinomials")
        newlabel = Label(newwindow, text = mytext, justify=LEFT, padx = 5, font=("Arial 16"))
        newlabel.pack()

    def about(self):
        mytext = ("\nFactorMe! Math Learning Software, Version 1.0" +
                "\n\nThis program helps students to learn how to factor trinomials" +
                "\ninto two binomials, sometimes with a leading coefficient." +
                "\nSpecifically designed for students studying math in the Ontario" +
                "\ncurriculum, from grades 10, 11 and 12 (and beyond)." +
                "\n\nDeveloped by Noah Gataveckas, May 2023." +
                "\nAll rights reserved. If any bugs are found or inquiries," +
                "\nemail: ngataveckas@torontoprepschool.ca")
        newwindow = Tk()
        newwindow.title("About")
        newlabel = Label(newwindow, text = mytext, justify=LEFT, padx = 5, font=("Arial 16"))
        newlabel.pack()

def recursecheck(digit, num, depth): #a recursive function for detecting repdigits on the end of a string version of a number
    if num[-1] == digit or num[-1] == str(int(digit) - 1):
        return recursecheck(digit, num[:-1], depth+1)
    else:
        return depth

def decimalcheck(x): #function that produces rounded string of the number
    roundx = round(x, 10)
    if int(x) == roundx:
        return abs(int(x))
    strx = str(roundx)
    dpoint = strx.find('.')
    if dpoint == -1:
        return abs(int(x))
    while strx[-1] == '0':
        strx = strx[:-1]
    if recursecheck(strx[-1], strx, 1) > 3:
        strx = strx[:-1]
        while strx[-2] == strx[-1] and len(strx) > dpoint + 4:
            strx = strx[:-1]
        if int(strx[-1]) > 4:
            strx = strx[:-1] + str(int(strx[-1]) + 1)
    if strx[0] == '-':
        strx = strx[1:]
    return strx

def reducer(n, d):
    i = 2
    while i <= int(d):
        if n == 1:
            break
        if n % i == 0 and int(d) % i == 0:
            n = int(n/i)
            d = int(int(d) / i)
            i = 2
            continue
        else:
            i += 1
    if d == 1:
        return str(n)
    return str(n) + '/' + str(d)

def fractioner(x, dictfracs, mixvar, brackvar, ssvar): #function that builds fractional representations of rounded integer strings
    dpoint = str(x).find('.')
    if dpoint == -1:
        return x
    base = x[:dpoint]
    decimalvalue = x[dpoint:]
    if decimalvalue in dictfracs.keys():
        if not mixvar:
            x = base + dictfracs[decimalvalue]
            if x[0] == '0':
                x = x[1:]
            elif x[0] == '-' and x[1] == '0':
                x = x[0] + x[2:]
        else:
            numerator = abs(int(base) * int(dictfracs[decimalvalue][2:])) + int(dictfracs[decimalvalue][0])
            if base[0] == '-':
                numerator *= -1     
            denominator = dictfracs[decimalvalue][2:]
            #print ('e', base, dictfracs[decimalvalue], int(dictfracs[decimalvalue][2:]), numerator, denominator)
            x = reducer(numerator, denominator)
            if ssvar:
                ssx = ''
                spoint = x.find('/')
                for i in x[:spoint]:
                    ssx = ssx + supers[i]
                ssx = ssx + '\u2215'
                for i in x[spoint + 1:]:
                    ssx = ssx + subs[i]
                x = ssx
    
    if x[0] == '-':
        x = x[1:]
    if brackvar:
        x = '(' + x + ')'
    return x

myapp = app()
myapp.root.mainloop()
