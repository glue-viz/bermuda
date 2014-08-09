"""
Basic example that adds a circle to a scatter plot,
and attaches callback functions when the shape changes.
"""
from __future__ import print_function

import matplotlib.pyplot as plt
import numpy as np
from bermuda import circle

# some data
x = np.linspace(0, 10, .1)
y = np.random.normal(np.sin(x), 0.1)

# plot
plt.plot(x, y)
axes = plt.gca()

def report(shape):
    mask = shape.contains(x, y)
    print("Contains %i points" % mask.size)

    # shape could make it easy to plot selected points
    # (automatically erasing the previous selection)
    # note: not sure how style arguments should be passed
    #       MPL defaults, or something else?
    shape.highlight_selected(x, y, 'ro')


# Note: circle could inspect its input, to automatically detect
#       that this is an MPL axes, and thus it should dispatch
#       to a MPL shape tool
c = circle(axes)

# on_drag callbacks are triggered continuously,
# as a user makes incremental changes to a shape
c.on_drag.append(report)

# on_release callbacks are triggered once
# after a shape is modified, upon mouseup
c.on_release.append(report)


plt.show()
