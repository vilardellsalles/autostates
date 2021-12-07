# Lights

In this very first example ([lights.py](./lights.py)), a user specified number
of lights have to be switched on consecutively. To run the example, simply
type:

```sh
python3 lights.py <number_of_lights>
```

The result will be different at each execution, since there are many ways to
switch a certain number of lights on. However, the program will always execute
the required actions to achieve the desired goal. If the number of lights is
smaller than 10, a [Matplotlib](https://matplotlib.org/stable/index.html) plot
with all the possible actions for each possible combination of light states
will be shown, together with the chosen solution:

```
Example on how to switch 3 lights on:

Step 1: Switching light 1 on
Step 2: Switching light 2 on
Step 3: Switching light 3 on

Once all lights are on, plot domain graph and solution

Bye
```

<p align="center"><span title="Diagram with all possible actions in a group of
three lights and the chosen solution"><a href="./lights.svg"><img
src="./lights.svg" width="50%" /></a></span></p>

In case that the number of lights is larger than 5, a
[Bokeh](https://docs.bokeh.org/en/latest/index.html) plot is used to allow the
possibility to hover over all the possible light states:

```
Example on how to switch 7 lights on:

Step 1: Switching light 1 on
Step 2: Switching light 2 on
Step 3: Switching light 3 on
Step 4: Switching light 4 on
Step 5: Switching light 7 on
Step 6: Switching light 6 on
Step 7: Switching light 5 on

Once all lights are on, plot domain graph and solution

Bye
```

<p align="center"><span title="Diagram with all possible actions in a group of
seven lights and the chosen solution"><a href="./lights_bokeh.png"><img
src="./lights_bokeh.png" width="50%" /></a></span></p>

Even you can choose any number of lights, I would recommend not to make it
larger than 15. With 15 lights, you will have almost half a milion possible
actions.  It will take some time to choose one of the possible ways to switch
all lights on.
