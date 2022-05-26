# -*- coding: utf8 -*-

from time import clock

import tkFileDialog
import tkMessageBox
from Tkinter import *

from config import *
from FctMgr import *
from PPMMgr import *


class plotterGUI:
    def __init__(self, win):
        self.win = win
        self.win.title("Plotter")
        self.range_x = 16.0
        self.range_y = 12.0
        self.center_x = 0
        self.center_y = 0
        self.functionsToPlot = []
        self.creation()

    def creation(self):
        # --- Graphic area
        self.M = plot(0, 0, 16, 12, 0.1, [])
        # creation of the basic graphic
        self.canvas = Canvas(takefocus=True)
        # canvas initialization
        self.canvas.config(width=800, height=600)
        self.picture = None
        # iamge initialization
        self.matrixToCanvas()
        # graph display
        self.canvas.bind("<Button-2>", self.areaCompute)
        self.canvas.grid(column=0, row=0)
        # --- End of graphic area

        # --- Text area functions
        functions = Frame()
        titreFonction = Label(
            functions, text="Functions of x to be plotted (one per line):"
        )
        titreFonction.pack(side=TOP)
        scrollbar = Scrollbar(functions)
        scrollbar.pack(side=RIGHT, fill=Y)
        self.functionsToPlotSaisie = Text(
            functions, yscrollcommand=scrollbar.set
        )
        self.functionsToPlotSaisie.config(width=50, height=36)
        self.functionsToPlotSaisie.pack(side=LEFT)
        scrollbar.config(command=self.functionsToPlotSaisie.yview)
        functions.grid(column=1, row=0)
        # creation of the text zone for the functions with the title and the scroll bar
        # --- End of text zone functions

        # --- Legend area
        self.functionLabelList = []
        # initialization of the list of legends
        self.legendFrame = Frame()
        legendLabel = Label(self.legendFrame, text="Legend:")
        legendLabel.pack(side=LEFT)
        self.legendFrame.grid(column=0, row=1, sticky="w")
        # --- End Legend area

        # --- Zone options
        options = Frame()
        stepLabel = Label(options, text="Step:")
        stepLabel.pack(side=LEFT)
        self.stepSaisie = Entry(options)
        self.stepSaisie.insert("0", "0.1")
        self.stepSaisie.pack(side=LEFT)
        # creation of the input field and the step label
        center_xLabel = Label(options, text="Center: X")
        center_xLabel.pack(side=LEFT)
        self.center_xSaisie = Entry(options)
        self.center_xSaisie.insert("0", "0")
        self.center_xSaisie.bind("<FocusIn>", self.bindKey)
        # when the input area has the focus, we will add a bind to it
        self.center_xSaisie.bind("<FocusOut>", self.unbindKey)
        # when the input area loses focus, we will remove the bind of this one
        self.center_xSaisie.pack(side=LEFT)
        # creation of the input field and the label center x
        center_yLabel = Label(options, text="Y")
        center_yLabel.pack(side=LEFT)
        self.center_ySaisie = Entry(options)
        self.center_ySaisie.insert("0", "0")
        self.center_ySaisie.bind("<FocusIn>", self.bindKey)
        self.center_ySaisie.bind("<FocusOut>", self.unbindKey)
        self.center_ySaisie.pack(side=LEFT)
        # creation of the input field and the label center y
        range_xLabel = Label(options, text="Range: X")
        range_xLabel.pack(side=LEFT)
        self.range_xSaisie = Entry(options)
        self.range_xSaisie.insert("0", "16")
        self.range_xSaisie.bind("<FocusIn>", self.bindKey)
        self.range_xSaisie.bind("<FocusOut>", self.unbindKey)
        self.range_xSaisie.pack(side=LEFT)
        # creation of the input field and the label range x
        range_yLabel = Label(options, text="Y")
        range_yLabel.pack(side=LEFT)
        self.range_ySaisie = Entry(options)
        self.range_ySaisie.insert("0", "12")
        self.range_ySaisie.bind("<FocusIn>", self.bindKey)
        self.range_ySaisie.bind("<FocusOut>", self.unbindKey)
        self.range_ySaisie.pack(side=LEFT)
        # creation of the input field and the label range y
        options.grid(column=0, row=2, sticky="w")
        # --- End Options area

        # --- Button area
        f = open("./static/help.txt")
        self.helpString = f.read()
        # help file reader
        bouttons = Frame()
        bouttonhelp = Button(bouttons, text="Help", command=self.helpPlotter)
        bouttonhelp.pack(side=LEFT)
        save = Button(
            bouttons, text="Save current image to file", command=self.save
        )
        save.pack(side=LEFT)
        redraw = Button(bouttons, text="Redraw plots", command=self.replot)
        redraw.pack(side=LEFT)
        bouttons.grid(column=1, row=2, sticky="e")
        # --- End Button area

        # --- Status area
        self.statutLabel = Label(
            width=203,
            bd=1,
            relief=SUNKEN,
            text="New plot area would be -8.0 <= x <= 8.0 ; -6.0 <= y <= 6.0",
        )
        self.statutLabel.grid(column=0, row=3, sticky="w", columnspan=2)
        # --- End of Status Zone

    def matrixToCanvas(self):
        """Method that creates an image according to a matrix, then displays it in a canvas"""
        self.canvas.delete(self.picture)
        # deleting the old image
        self.picture = PhotoImage(width=800, height=600)
        # initialization of the image
        image_string = ""
        for column in xrange(len(self.M[0])):
            image_string += "{"
            for line in xrange(len(self.M)):
                image_string += "#%02x%02x%02x " % tuple(self.M[line][column])
            image_string += "} "
        # conversion from matrix to image
        self.picture.put(image_string, (0, 0))
        self.canvas.create_image(0, 0, image=self.picture, anchor=NW)
        # adding the image to the canvas

    def replot(self):
        """Method that, if the values are correct, redraws the graph and updates the legend"""
        if self.verifyValues():
            # If the values entered are correct
            self.range_x = float(self.range_xSaisie.get())
            self.range_y = float(self.range_ySaisie.get())
            self.center_x = float(self.center_xSaisie.get())
            self.center_y = float(self.center_ySaisie.get())
            self.step = float(self.stepSaisie.get())
            self.functionsToPlot = self.functionsToPlotSaisie.get(
                "0.0", "end"
            ).split("\n")
            self.functionsToPlot.pop()  # allows to delete the \n at the end
            # recovery of values
            self.M = plot(
                self.center_x,
                self.center_y,
                self.range_x,
                self.range_y,
                self.step,
                self.functionsToPlot,
            )
            # creation of the new matrix
            self.matrixToCanvas()
            # graph display
            self.setLegend(self.functionsToPlot)
            # display of the new legend

    def setLegend(self, functionList):
        """Method that displays the legend"""
        self.destroyCurrentLegend()
        # destruction of the old legend
        for i in xrange(len(functionList)):
            label = Label(
                self.legendFrame,
                text=functionList[i],
                fg=self.getPaletteColor(i % COLORS_NBR),
            )
            label.pack(side=LEFT)
            # creation of each legend
            self.functionLabelList.append(label)
            # adding each caption to the list of captions

    def destroyCurrentLegend(self):
        """Méthode qui détruit la légende"""
        for label in self.functionLabelList:
            label.destroy()
            # destruction of each legend
        self.functionLabelList = []
        # resetting the legend

    def getPaletteColor(self, i):
        """Method that transforms an rgb color tuple into a hexadecimal str"""
        hexFontColor = "#%02x%02x%02x" % PLOTCOLORS[i % COLORS_NBR]
        return hexFontColor

    def setStatut(self, ev):
        """Method that updates the status bar based on the values in the option labels"""
        range_x = self.range_xSaisie.get()
        range_y = self.range_ySaisie.get()
        center_x = self.center_xSaisie.get()
        center_y = self.center_ySaisie.get()
        # recovery of values
        if (
            self.isReal(range_x)
            and self.isReal(range_y)
            and self.isReal(center_x)
            and self.isReal(center_y)
        ):
            # if the values are real
            if float(range_x) > 0 and float(range_y) > 0:
                # if the range x and y are greater than 0
                range_x = float(range_x)
                range_y = float(range_y)
                center_x = float(center_x)
                center_y = float(center_y)
                # transformation of str into float
                minX = center_x - range_x / 2
                maxX = center_x + range_x / 2
                minY = center_y - range_y / 2
                maxY = center_y + range_y / 2
                # calculation of the new area of the graph
                self.statutLabel.config(
                    text="New plot area would be "
                    + str(minX)
                    + " <= x <= "
                    + str(maxX)
                    + " ; "
                    + str(minY)
                    + " <= y <= "
                    + str(maxY)
                )
                # status display
            else:
                self.statutLabel.config(
                    text="The range must be positive numbers !"
                )
                # error display
        else:
            self.statutLabel.config(
                text="The plotting options must be real numbers !"
            )
            # error display

    def bindKey(self, ev):
        "adds to the object that has the focus the function setStatus when a key is released"
        ev.widget.bind("<KeyRelease>", self.setStatut)

    def unbindKey(self, ev):
        """removes from the object that loses focus the setStatus function when a key is released"""
        ev.widget.unbind("<KeyRelease>")

    def isReal(self, numStr):
        """check if a number given in str is a real"""
        try:
            float(numStr)
            res = True
        except ValueError:
            res = False
        return res

    def save(self):
        """save the displayed graphic to a selected file"""
        fileName = tkFileDialog.asksaveasfilename(
            defaultextension="ppm",
            filetypes=[("ppm files", ".ppm"), ("all files", ".*")],
            title="Save current image to file",
        )
        if fileName != "":
            # si l'utilisateur n'a pas annulé
            matrixToFile(self.M, fileName)

    def verifyValues(self):
        """This method checks that the values entered allow a graph to be drawn and displays a message detailing the error if there is one."""
        range_x = self.range_xSaisie.get()
        range_y = self.range_ySaisie.get()
        center_x = self.center_xSaisie.get()
        center_y = self.center_ySaisie.get()
        step = self.stepSaisie.get()
        functionsToPlot = self.functionsToPlotSaisie.get("0.0", "end").split(
            "\n"
        )
        functionsToPlot.pop()
        # recovery of values
        res = True
        # initialization of the result
        message = "There is an error in your configuration.\nDetail:"
        # initialisation du message d'erreur
        if not self.isReal(step):
            # if the self is not a real
            message += "Your step must be expressed by a number !"
            # add the message
            res = False
            # false result
        elif float(step) <= 0:
            # otherwise if the step is negative
            message += "\n- Your step must be strictly positive !"
            res = False
        if not self.isReal(range_x):
            message += "\n- Your range x must be expressed by a number !"
            res = False
        elif float(range_x) <= 0:
            message += "\n- Your range x must be strictly positive !"
            res = False
        if not self.isReal(range_y):
            message += "\n- Your range Y must be expressed by a number !"
            res = False
        elif float(range_y) <= 0:
            message += "\n- Your range Y must be strictly positive !"
            res = False
        if not self.isReal(center_x):
            message += "\n- Your center x must be expressed by a number !"
            res = False
        if not self.isReal(center_y):
            message += "\n- Your center y must be expressed by a number !"
            res = False
        for i in functionsToPlot:
            # for each function
            try:
                # test of the function
                x = 5
                eval(i)
            except NameError:
                # if there is a name or syntax error
                message += (
                    "\n- There is a syntax error in your function '"
                    + str(i)
                    + "' !"
                )
                res = False
            except SyntaxError:
                message += (
                    "\n- There is a syntax error in your function '"
                    + str(i)
                    + "' !"
                )
                res = False
            except:
                pass
        if not res:
            # if there was an error
            tkMessageBox.showerror("Erreur", message)
        return res

    def helpPlotter(self):
        """Display help"""
        tkMessageBox.showinfo("Aide", self.helpString)

    def areaCompute(self, ev):
        "This method calculates the required area according to two methods, displays the result and the execution time of each of them"
        x = ev.x
        y = ev.y
        pixels2, t2 = self.rectangle(x, y)
        pixels1, t1 = self.browseMatrix(x, y)
        ubp = self.unitByPixel()
        # recovery of the ratio of units per pixel
        aire1 = str(pixels1 * ubp)
        aire2 = str(pixels2 * ubp)
        # transformations of the two areas
        self.matrixToCanvas()
        # drawing of the surface calculated in the matrix
        tkMessageBox.showinfo(
            "Area",
            "Browse matrix : "
            + str(pixels1)
            + " pixels, i.e. "
            + aire1
            + " area units, in "
            + str(t1)
            + " secondes\nRectangle : "
            + str(pixels2)
            + " pixels, i.e. "
            + aire2
            + " area units, in "
            + str(t2)
            + " secondes",
        )
        # pop-up displaying info

    def browseMatrix(self, x, y):
        """This method calculates the number of pixels in the area according to method 1"""
        t0 = clock()
        # time initialization
        pixels = 0
        # pixel initialization
        if (
            self.M[x][y] == BG
            or self.M[x][y][0] == self.M[x][y][1] == self.M[x][y][2]
        ):
            # if the surface to be calculated is a surface
            p = [(x, y)]
            # we create the list of points with the base point inside
            while p != []:
                # until all points have been verified
                pA = p.pop()
                # we remove the last item from the list and give it to pA
                if self.M[pA[0]][pA[1]] != AREA_COLOR:
                    # if the point different from the area color
                    pixels += 1
                    # we increment the size in pixels by 1
                    self.M[pA[0]][pA[1]] = AREA_COLOR
                    # we color the pixel in the area color
                    t = (
                        (pA[0] + 1, pA[1]),
                        (pA[0] - 1, pA[1]),
                        (pA[0], pA[1] + 1),
                        (pA[0], pA[1] - 1),
                    )
                    # we create a list including the 4 points adjacent to the current point
                    for i in t:
                        # for each of these points
                        if (
                            0 <= i[0] < 799
                            and 0 <= i[1] < 600
                            and self.M[i[0]][i[1]] != AREA_COLOR
                            and (
                                self.M[i[0]][i[1]] == BG
                                or self.M[i[0]][i[1]][0]
                                == self.M[i[0]][i[1]][1]
                                == self.M[i[0]][i[1]][2]
                            )
                        ):
                            # if the point is in the image and it is not already of the area color and it is either of the background color or it is of a gray level
                            p.append(i)
                            # we add it to the list of points
        temps = clock() - t0
        # we calculate the total time of the execution by doing t1-t0
        return pixels, temps

    def rectangle(self, x0, y0):
        """This method calculates the number of pixels in the area according to method 2"""
        t0 = clock()
        # time initialization
        pixels = 0
        # pixel initialization
        if (
            self.M[x0][y0] == BG
            or self.M[x0][y0][0] == self.M[x0][y0][1] == self.M[x0][y0][2]
        ):
            # if the surface to be calculated is a surface
            xt = x0
            yt = y0
            z = True
            a = True
            b = True
            # initialization of values
            while b:
                # Step 5
                while a:
                    lyi = []
                    x = x_iTox(x0, self.center_x, self.range_x / 2)
                    # transformation of x0 into graphic coordinate
                    for i in self.functionsToPlot:
                        try:
                            lyi.append(
                                yToy_i(
                                    eval(i), self.center_y, self.range_y / 2
                                )
                            )
                        except:
                            pass
                        # calculation of the corresponding y for each function
                    ya = None
                    yb = None
                    for yi in lyi:
                        if yi < y0 and (yi > ya or ya == None):
                            # max(yi|yi < y0)
                            ya = yi
                        if yi > y0 and (yi < yb or yb == None):
                            # min(yi|yi > y0)
                            yb = yi
                    if ya == None:
                        # if no ya was found, so there is no function bordering the top
                        ya = 0
                    if yb == None:
                        # if no yb has been found, so there is no function bordering the bottom
                        yb = 597
                    if yb - ya < epsilon or x0 > 797 or x0 < 0:
                        # if the difference between yb and ya indicates that the continuation of the area is negligible or that we arrive at the end of the image
                        a = False
                        # go to step 12
                    else:
                        pixels += (yb - ya) * E
                        # we add the rectangle to the pixels
                        if z:
                            x0 += E
                        else:
                            x0 -= E
                        y0 = (yb + ya * 1.0) / 2
                        # we give the value between the two previous points to y0
                # step 12
                if z:
                    z = False
                    x0 = xt - E
                    y0 = yt
                    a = True
                    # go to step 5
                else:
                    b = False
                    # done
        temps = clock() - t0
        return pixels, temps

    def unitByPixel(self):
        """Returns the ratio of units per pixel"""
        return self.range_y / 600 * self.range_x / 800


if __name__ == "__main__":
    root = Tk()
    f = plotterGUI(root)
    root.mainloop()
