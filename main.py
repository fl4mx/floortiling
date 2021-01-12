#dependencies
import numpy
import matplotlib.pyplot as plt

#init values
rows = 26
columns = 5
piece = 122
wastage = 0
minimumgap = 25
delta = 10
leftover = 0

#init arrays
finalarray = numpy.zeros((int(rows), int(columns)))
rowlengths = (numpy.array([495, 495, 500, 500, 500, 500, 500, 500, 500, 435, 435, 435, 435, 435, 435, 435, 435, 435, 435, 435, 435, 435, 430, 430, 430, 430]))


#iterate rows
for row in range(rows):
    if (leftover < minimumgap):
        wastage = wastage + leftover
        leftover = 0
    endlength = (rowlengths[row] - leftover - (3 * piece))
    if (((endlength < minimumgap) & (endlength > 0)) | (((piece - abs(endlength)) < minimumgap))):
        difference = minimumgap - endlength
        front = leftover - difference
        endlength = minimumgap
        if (endlength == finalarray[row - 1][3]):
            print("same")
            endlength = endlength + delta
            difference = minimumgap - endlength
            #difference = endlength - minimumgap
            front = leftover - difference
        wastage = wastage + abs(difference)
        leftover = piece - minimumgap
        finalarray[row][0] = front
        finalarray[row][1] = piece
        finalarray[row][2] = piece
        finalarray[row][3] = piece
        finalarray[row][4] = endlength
    elif (endlength <= 0):
        front = leftover
        if abs(endlength) >= 20:
            leftover = abs(endlength)
        else:
            leftover = 0
            wastage = wastage + abs(endlength)
        #endlength is negative, so we add it
        endlength = piece + endlength
        if (endlength == finalarray[row - 1][3]):
            print("same")
            endlength = endlength + delta
        finalarray[row][0] = front
        finalarray[row][1] = piece
        finalarray[row][2] = piece
        finalarray[row][3] = endlength
    elif (endlength > minimumgap):
        front = leftover
        leftover = piece - endlength
        finalarray[row][0] = front
        finalarray[row][1] = piece
        finalarray[row][2] = piece
        finalarray[row][3] = piece
        finalarray[row][4] = endlength


#data structures for plotting
arrangeDict = {}
category_names = ["Board 1", "Board 2", "Board 3", "Board 4", "Board 5"]

#DEBUG: check lengths are correct
check = True
for row in range(rows):
    rowsum = sum(finalarray[row])
    if (rowsum != rowlengths[row]):
        check = False
    #finalarray[row][5] = str(rowsum)
    arrangeDict["Row{0}".format(row + 1)] = finalarray[row]

#outputs
print(finalarray)
print("wastage = " + str(wastage))

if (check == True):
    print("all lengths verified are correct")
else:
    print("incorrect lengths")

#plotter method
def plotter(arrangeDict, category_names):
    labels = list(arrangeDict.keys())
    data = numpy.array(list(arrangeDict.values()))
    data_cum = data.cumsum(axis=1)
    category_colors = plt.get_cmap("RdYlGn")(numpy.linspace(0.15, 0.85, data.shape[1]))
    fig, ax = plt.subplots(figsize=(6, 8))
    #fig, ax = plt.subplots()
    ax.invert_yaxis()
    ax.xaxis.set_visible(False)
    ax.set_xlim(0, numpy.sum(data, axis = 1).max())
    #print(data)
    y_pos = 40 * numpy.arange(len(labels))
    #print(y_pos)
    for i, (colname, color) in enumerate(zip(category_names, category_colors)):
        widths = data[:, i]
        #print("widths")
        #print(widths)
        starts = data_cum[:, i] - widths
        #print("starts")
        #print(starts)
        ax.barh(y_pos, widths, left = starts, height = 40, label = colname, color = color)
        xcenters = starts + (widths / 2)
        r, g, b, _ = color
        text_color = 'white' if r * g * b < 0.2 else 'darkgrey'
        for y, (x, c) in enumerate(zip(xcenters, widths)):
            ax.text(x, y_pos[y], str(int(c)), ha = "center", va = "center", color = text_color)
    ax.legend(ncol = len(category_names), bbox_to_anchor = (1.04, 1.02), loc = "center right", fontsize = "small")
    ax.set_yticks(y_pos)
    ax.set_yticklabels(labels)
    fig.suptitle("Floorboard Arrangement", fontsize = 20, fontweight = "bold")
    ax.text(0.98, 1.07, ("Wastage = " + str(wastage)), verticalalignment = "bottom", horizontalalignment = "center", transform = ax.transAxes, color = 'green', fontsize = 8)
    ax.text(0.98, 1.04, ("Minimum Gap = " + str(minimumgap)), verticalalignment = "bottom", horizontalalignment = "center", transform = ax.transAxes, color = 'green', fontsize = 8)
    #print(labels)
    return fig, ax

#plot
plotter(arrangeDict, category_names)
plt.show()
