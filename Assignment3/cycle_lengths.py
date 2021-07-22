"""Student name:  Tomas Bosschieter
Student UvAnetID: 12195073
University:       University of Amsterdam
Year:             Year 2
Course:           Introduction Computational Science
Assignment:       Assigment 3
File:             cycle_lengths.py

Program description: Here, we allow the user to create a png that shows the
average cycle lengths. This is one for assignment 2, however. Nonetheless,
it is a nice complement to the transient_length and shannon entropy files,
hence we include it.

Because we're using python 3 as our programming language,
we have to run it with the following command, on Ubuntu 18.4:
python3 cycle_lengths.py.

Recommended size of the frame: full-screen.
"""

import ca
import matplotlib.pyplot as plt


class changed_length(ca.CASim):
    def setup_initial_row(self):
        """ Initial row in case we wish to generate the png file submitted."""

        eind = [0] * (self.width // 2 ) + [1]*(self.width - self.width // 2)

        return eind


if __name__ == '__main__':
    sim = changed_length()

    info = []

    # For all rules, this is.
    for i in range(0,256):
        sim.rule = i
        sim.height = 500
        sim.r = 1
        sim.k = 2

        info.append([])

        # Widths between 50 and 55. These give decent results.
        # Comment last year: ""From your code I can see that you have measured
        # cycle lengths averaged over widths from one to eleven. Most of these
        # widths are very small, and do not produce useful results.
        # For this I have subtracted 0,5 points.""
        for j in range(50,55):
            sim.width = j
            sim.reset()
            info[-1].append(sim.get_cycle_length())


    # This is where we create our labels and group our rules according to
    # which class they belong to.
    populationLabels1 = [0, 8, 32, 40, 64, 96, 128, 136, 160, 168, 192, 224,
        234, 235, 238, 239, 248, 249, 250, 251, 252, 253, 254, 255]
    populationData1 = [info[l] for l in populationLabels1]
    populationLabels2 = [1, 2, 3, 4, 5, 6, 7, 9, 10, 11, 12, 13, 14, 15, 16, 17,
        19, 20, 21, 23, 24, 25, 26, 27, 28, 29, 31, 33, 34, 35, 36, 37, 38, 39,
        41, 42, 43, 44, 46, 47, 48, 49, 50, 51, 52, 53, 55, 56, 57, 58, 59, 61,
        62, 63, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 76, 77, 78, 79, 80, 81,
        82, 83, 84, 85, 87, 88, 91, 92, 93, 94, 95, 97, 98, 99, 100, 103, 104,
        107, 108, 109, 111, 112, 113, 114, 115, 116, 117, 118, 119, 121, 123,
        125, 127, 130, 131, 132, 133, 134, 138, 139, 140, 141, 142, 143, 144,
        145, 148, 152, 154, 155, 156, 157, 158, 159, 162, 163, 164, 166, 167,
        170, 171, 172, 173, 174, 175, 176, 177, 178, 179, 180, 181, 184, 185,
        186, 187, 188, 189, 190, 191, 194, 196, 197, 198, 199, 200, 201, 202,
        203, 204, 205, 206, 207, 208, 209, 210, 211, 212, 213, 214, 215, 216,
        217, 218, 219, 220, 221, 222, 223, 226, 227, 228, 229, 230, 231, 232,
        233, 236, 237, 240, 241, 242, 243, 244, 245, 246, 247]
    populationData2 = [info[n] for n in populationLabels2]
    populationLabels3 = [18, 22, 30, 45, 60, 75, 86, 89, 90, 101, 102, 105, 122,
        126, 129, 135, 146, 149, 150, 151, 153, 161, 165, 182, 183, 195]
    populationData3 = [info[k] for k in populationLabels3]
    populationLabels4 = [54, 106, 110, 120, 124, 137, 147, 169, 193, 225]
    populationData4 = [info[m] for m in populationLabels4]

    fig = plt.figure(figsize=(6, 4))
    fig.suptitle("Wolfram average cycle lengths", fontsize = 18)
    fig.canvas.set_window_title("CA2 Statistics")

    # Description of the figure(s). Last year, I got a comment about my y-axes
    # having different ranges, so that's been fixed now :-). (No, I didnt fail,
    # I couldn't attend the exam unfortunately and therefore dropped the class.)
    fig.text(0.5, 0.9, 'In Class 1, the average cycle lengths are low' \
        ' which was to be expected by its definition.' \
        ' In Class 2, some more intruiging patterns emerge and thus the ' \
        ' average cycle length lies higher.' \
        ' Class 3 (chaotic state) has some with the highest mean value. This is because' \
        ' of its chaotic cycles, which tend to have big cycle lengths.' \
        ' Therefore, this matches our expectations. Class 4 (Complex)' \
        ' systems also have a relatively high average, compared to Classes 1' \
        ' and 2, but not as much, or often, as the chaotic state by its definition,' \
        ' which we see confirmed in the figure. In return, their transient lengths tend to,' \
        ' be a lot longer. Our maximum height is 500, our width ranges from 50 to 55' \
        ' and the starting row is split in a white and black half. We accordingly take the average' \
        ' of the cycle lengths. All y-axes go from 0 to 520 for each subgraph.',
        horizontalalignment = 'center', wrap = True)

    # Plot boxplot of Class 1.
    ax1 = plt.subplot(2,2,1)
    ax1.boxplot(populationData1)
    ax1.set_xticklabels(populationLabels1)
    ax1.set_xlabel('Wolfram rules')
    ax1.set_ylabel('Cycle length')
    ax1.set_title("Class 1")
    ax1.set_ylim([0,sim.height + 20])

    # Plot boxplot of Class 2.
    ax2 = plt.subplot(2,2,2, sharey=ax1)
    ax2.boxplot(populationData2)
    ax2.set_xticklabels(populationLabels2)
    ax2.set_xlabel('Wolfram rules')
    ax2.set_ylabel('Cycle length')
    ax2.set_title("Class 2")
    ax2.set_ylim([0,sim.height + 20])

    # Plot boxplot of Class 3.
    ax3 = plt.subplot(2,2,3)
    ax3.boxplot(populationData3)
    ax3.set_xticklabels(populationLabels3)
    ax3.set_xlabel('Wolfram rules')
    ax3.set_ylabel('Cycle length')
    ax3.set_title("Class 3")
    ax3.set_ylim([0,sim.height + 20])

    # Plot boxplot of Class 4.
    ax4 = plt.subplot(2,2,4, sharey=ax3)
    ax4.boxplot(populationData4)
    ax4.set_xticklabels(populationLabels4)
    ax4.set_xlabel('Wolfram rules')
    ax4.set_ylabel('Cycle length')
    ax4.set_title("Class 4")
    ax4.set_ylim([0,sim.height + 20])

    plt.show()
