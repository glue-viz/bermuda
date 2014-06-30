import matplotlib.pyplt as plt

from bermuda import ellipse, polygon, rectangle


plt.plot([1,2,3], [2,3,4])
ax = plg.gca()

# default choices for everything
e = ellipse(ax)

# custom position, genric interface for all shapes
e = ellipse(ax, bbox = (x, y, w, h, theta))
e = ellipse(ax, cen=(x, y), width=w, height=h, theta=theta)

# force square/circle?
e = ellipse(ax, aspect_equal=True)

# freeze properties?
e = ellipse(ax, width=1, height=2, aspect_frozen = True)
e = ellipse(ax, rotation_frozen=True)
e = ellipse(ax, center_frozen=True)
e = ellipse(ax, size_frozen=True)

# all of these kwargs should be settable properties as well
e.bbox = (x, y, w, h, theta)
e.aspect_equal = True
e.aspect_frozen = True
