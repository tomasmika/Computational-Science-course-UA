"""Student name:  Tomas Bosschieter
Student UvAnetID: 12195073
University:       University of Amsterdam
Year:             Year 2
Course:           Introduction Computational Science
Assignment:       Assigment 3
File:             ca.py

Program description: This piece of code allows us to simulate
cellular automata, using a rule set and the other required
elements. We allow a manipulator for setting the height and
width of a frame, the number of neighbors and the rule used.
Also, we may have an input value of lambda that will then determine
a corresponding ruletable/ruleset. Of course, this is not necessary.
We have used the random-table method, since we were allowed to choose,
and this one is more convenient to implement. However, a walkthrough table
works just as good.


To clean up the code, I put the code that allows us to graph the
cycle lengths and the transient lengths, and so forth, in other files.
To get these, you only need to run those, as is stated in their
descriptions. Running this file gives us the GIU itself.

Because we're using python 3 as our programming language,
we have to compile (and run) it with the following command, on Ubuntu 18.4:
python3 ca.py.

Recommended size of the frame: full-screen.
"""

import numpy as np
import math
import matplotlib
import random

from pyics import Model

def decimal_to_base_k(n, k):
    """Converts a given decimal (i.e. base-10 integer) to a list containing the
    base-k equivalant.

    For example, for n=34 and k=3 this function should return [1, 0, 2, 1]."""

    listCoef = []
    rem = n % k

    while n != 0:
        listCoef.append(rem)
        n //= k
        rem = n % k

    # We add the last element first, so we reverse it.
    return listCoef[::-1]


class CASim(Model):
    def __init__(self):
        Model.__init__(self)

        self.t = 0
        self.rule_set = []
        self.config = None

        self.make_param('r', 1)
        self.make_param('k', 2)
        self.make_param('width', 50)
        self.make_param('height', 50)
        self.make_param('rule', 30, setter=self.setter_rule)
        self.make_param('seed', 0, setter=self.setter_seed)
        self.make_param('use_rand_seed', False, param_type=bool)
        self.make_param('lambdaa', 0.0, setter = self.setter_lambdaa)
        self.make_param('use_lambdaa', False, param_type=bool)


    def setter_lambdaa(self, val):
        min_lambdaa = 0
        max_lambdaa = 1-1/self.k

        if min_lambdaa <= val <= max_lambdaa:
            return val

        return 0


    def setter_rule(self, val):
        """Setter for the rule parameter, clipping its value between 0 and the
        maximum possible rule number."""
        rule_set_size = self.k ** (2 * self.r + 1)
        max_rule_number = self.k ** rule_set_size

        return max(0, min(val, max_rule_number - 1))


    def setter_seed(self, val):
        """Setter for the rule parameter, clipping its value between 0 and the
        maximum possible rule number."""
        max_seed_number = self.k ** self.width

        return max(0, min(val, max_seed_number - 1))


    def setup_initial_row(self):
        """Returns an array of length `width' with the initial state for each of
        the cells in the first row. Values should be between 0 and k. Since
        concatenate only takes <= 3 arguments, this configuration/initial
        row gives the maximum number of utilized rules in the rule set."""

        if self.use_rand_seed:
            eind = [random.randint(0, self.k) for _ in range(self.width)]
        else:
            ls = decimal_to_base_k(self.seed, self.k)
            eind = [0] * (self.width - len(ls)) + ls

        return eind


    def build_rule_set(self):
        """Sets the rule set for the current rule.
        A rule set is a list with the new state for every old configuration.

        Rule set based on the value of parameter lambdaa is possible. We use
        a randomized ruletable, as opposed to a walkthrough table. We were
        allowed to implement whichever we wished for. Since lambda is used
        in lambda calculus, a part of Python, we cannot use that word.
        First, we create a list of states, and choose an index randomly,
        and the state with that index will be our quiescent state. We then
        take s_q out of our list of states, which will now be the list we
        shall take states from by random. The idea here is that of
        lambdaa = 0.7, for example, 70% has to equal s_q. Hence, if a
        random number between 0.0 and 1 gives 0.7, then we let it go to s_q,
        and otherwise we randomly select a state from the list of states
        without s_q.
        """

        if self.use_lambdaa:
            list_states = list(range(0,self.k))
            s_q = random.randint(0,self.k-1)
            del list_states[s_q]

            size = self.k ** (2*self.r + 1)
            mylist = size * [0]
            for i in range(size):
                if random.random() > self.lambdaa:
                    mylist[i] = s_q
                else:
                    mylist[i] = list_states[random.randint(0,self.k-2)]
            self.rule_set = mylist

        else:
            # We construct n in base k, which is a list here.
            n_base_k_list = decimal_to_base_k(self.rule, self.k)

            # We have to add k^N - number already in the list 0's in the list.
            length_of_zeros = self.k ** (2 * self.r + 1) - len(n_base_k_list)

            self.rule_set = length_of_zeros * [0] + n_base_k_list


    def check_rule(self, inp):
        """Returns the new state based on the input states. The input state will
        be an array of 2r+1 items between 0 and k, the neighbourhood which the
        state of the new cell depends on."""

        """We construct the value in base 10 from base k. For each number in
        our list inp (input), we multiply it by its corresponding factor.
        For example, given [1,0,1] in base 3, we zip the input with
        the given values, so [1, 0, 1] in base 3 would give
        1 * 3^0 (this is the self.k ** index), and then 0 * 3^1, since
        the item == 0 (middle one in [1,0,1] is 0). The sum of these
        products is its value in base 10 of course. Since we evaluate
        the for-loop up until the second argument (= -1), we have -1, since
        we want the 0th element.
        """

        base_10_value = 0

        for index, item in zip(range(len(inp) - 1 , -1, -1), inp):
            base_10_value += (self.k ** index) * item

        # Calculating the index of the rule.
        index_rule = len(self.rule_set) - 1 - base_10_value
        new_state = self.rule_set[int(index_rule)]

        # We return the new state of the cell according to the ruleset.
        return new_state


    def reset(self):
        """Initializes the configuration of the cells and converts the entered
        rule number to a rule set."""

        self.t = 0
        self.config = np.zeros([self.height, self.width])
        self.config[0, :] = self.setup_initial_row()
        self.build_rule_set()


    def draw(self):
        """Draws the current state of the grid."""

        import matplotlib
        import matplotlib.pyplot as plt

        plt.cla()

        if not plt.gca().yaxis_inverted():
            plt.gca().invert_yaxis()
        plt.imshow(self.config, interpolation='none', vmin=0, vmax=self.k - 1,
                cmap=matplotlib.cm.binary)
        plt.axis('image')
        plt.title('t = %d' % self.t)


    def step(self):
        """Performs a single step of the simulation by advancing time (and thus
        row) and applying the rule to determine the state of the cells."""
        self.t += 1

        if self.t >= self.height:
            return True

        for patch in range(self.width):
            # We want the items r to the left and to the right of this patch,
            # while wrapping around (e.g. index -1 is the last item on the row).
            # Since slices do not support this, we create an array with the
            # indices we want and use that to index our grid.
            indices = [i % self.width
                    for i in range(patch - self.r, patch + self.r + 1)]
            values = self.config[self.t - 1, indices]
            self.config[self.t, patch] = self.check_rule(values)


    def get_cycle_length(self):
        """ We find the cycle length by checking whether we have seen a
            state before, which then results in a cycle, so that is when
            we return the cycle length: our current index, minus the previous,
            which is automatically the first other index of the same
            configuration. """
        t_0 = 0

        while (self.height > t_0):
            if (t_0 > self.t):
                self.step()
            else:
                my_config = self.config.tolist()[0:t_0]

                already_visited = []

                for index, item in enumerate(my_config):
                    if item in already_visited:
                        return index - my_config.index(item)
                    else:
                        already_visited.append(item)

                t_0 += 1

        return t_0


import matplotlib.pyplot as plt
if __name__ == '__main__':
    sim = CASim()

    from pyics import GUI
    cx = GUI(sim)
    cx.start()
