"""Student name:  Tomas Bosschieter
Student UvAnetID: 12195073
University:       University of Amsterdam
Year:             Year 2
Course:           Introduction Computational Science
Assignment:       Assigment 3
File:             transient_lengths.py

Program description: Here, we allow the user to create a png that shows the
transient lengths. We find the transient length by checking for cycles, and
then we use the fact that time=0 till the start of the first cycle is by
definition the transient length. For each lambda, we find 5 transient
lengths.

Because we're using python 3 as our programming language,
we have to run it with the following command, on Ubuntu 18.4:
python3 transient_lengths.py.

Recommended size of the frame: full-screen.
"""

import ca
import matplotlib.pyplot as plt

partition = 20
num_points_per_lambda = 5

class changed_length(ca.CASim):
    def get_transient_length(self, lambda_now):
        """ We check whether we have seen a row before or not, and that way
            we find out whether there is a cycle or not, from which we can
            deduce the transient length. """
        self.use_lambdaa = True
        self.use_rand_seed = True
        self.lambdaa = lambda_now
        self.reset()

        # We have seen the first row. We now also add the other ones, till
        # there are no more steps left.
        already_visited = [[sim.config[0].tolist()]]
        time = 0

        while not self.step():
            time += 1
            cur_row = self.config[time].tolist()

            # Check if seen before. Otherwise, add it to the list of seen rows.
            if cur_row in already_visited:
                return already_visited.index(cur_row)

            already_visited.append(cur_row)

        # If we have found no loop, it is at least as big as our time
        # variable now, which is our height, so we return that.
        return time


    def data_lambda(self, lambdaa):
        # print(lambdaa)
        return [self.get_transient_length(lambdaa) for _ in range(num_points_per_lambda)]


    def create_the_plot(self, data):
        fig = plt.figure()
        fig.suptitle("Transient Lengths")
        fig.text(0.5, 0.9, 'In this figure we see the transient lengths for' \
            ' lambda values between 0 and 1, where take a partition of this' \
            ' axis, using 20 points. We take r = 2, k = 4, width = 30 and height = 15000,' \
            ' to get meaningful results, as is done in the paper. We take 5' \
            ' data points per lambda, to get more accurate results. Since we' \
            ' plot these 5 for each lambda, we do not average results and' \
            ' thus the error bars are implicit, and not necessary since we' \
            ' show all of the data, which gives a satisfactory result, because it matches' \
            ' our expectations.'\
            ' This is because near lambda = 0.75, the maximal useful lambda, where the the critical' \
            ' slowing down is, the transient length should be longer.' \
            ' This also matches what we see: around 0.75, we transient lengths' \
            ' are high, whereas below and after the critical slowing down, ' \
            ' this is not the case, although there are outliers (these are' \
            ' special cases, which can be seen from the transparency), but there' \
            ' is a clear pattern.',
            horizontalalignment = 'center', wrap = True)


        plt.scatter([[i/partition]* num_points_per_lambda for i in range(partition+1)], data,
                    alpha=0.4)
        plt.xlabel("Lambda")
        plt.ylabel("Transient Length")

        plt.axis([0, 1, 0, 16000])
        plt.show()


if __name__ == '__main__':
    sim = changed_length()

    # You may choose these values as you wish.
    sim.r = 2
    sim.k = 4
    sim.width = 30
    sim.height = 15000

    data = [sim.data_lambda(i / partition) for i in range(partition+1)]
    sim.create_the_plot(data)
