import numpy as np

class FrozenError(Exception):
    pass


class AnchorPoint(object):

    def __init__(self, x=0, y=0, frozen=False, visible=True):
        self._x = x
        self._y = y
        self._frozen = frozen
        self._visible = visible
        
    def _check_frozen(self):
        if self.frozen:
            raise FrozenError("Cannot move: anchor is frozen")
        
    @property
    def x(self):
        return self._x
        
    @x.setter
    def x(self, value):
        self._check_frozen()
        self._x = value
            
    @property
    def y(self):
        return self._y
        
    @y.setter
    def y(self, value):
        self._check_frozen()
        self._y = value
        
    @property
    def visible(self):
        return self._visible
        
    @visible.setter
    def visible(self, value):
        self._visible = bool(value)
        
    @property
    def frozen(self):
        return self._frozen
        
    @frozen.setter
    def frozen(self, value):
        self._frozen = bool(value)

class Pointer(object):
    def __init__(self, label):
        self.label = label
        
    def __get__(self, instance, owner=None):
        return getattr(instance, self.label)
        
    def __set__(self, instance, value):
        setattr(instance, self.label, value)

class BBox(object):
    
    center = Pointer('_center')
    width = Pointer('_width')
    height = Pointer('_height')
    theta = Pointer('_theta')
    
    def __init__(self, center=(0, 0), width=1, height=1, theta=0):
        self._center  = center
        self._width = width
        self._height = height
        self._theta = theta
    
    @property
    def aspect(self):
        """
        The aspect ratio (width / height)
        """
        return 1.0 * self._width / self._height
        
    @aspect.setter
    def aspect(self, value):
        """
        Change the aspect ratio (width/height), preserving the width
        """
        self._height = self._width / value
        
    
    @property
    def vertices(self):
        """
        The 4 corners of the Bbox, as a list of tuples
        
        Returns the corners starting with the upper left, moving clockwise.        
        """
        x = np.array([-0.5, 0.5, 0.5, -0.5]) * self.width 
        y = np.array([0.5, 0.5, -0.5, -0.5]) * self.height

        # rotate
        t = np.radians(self.theta)
        x0 = x
        x = x * np.cos(t) - y * np.sin(t)
        y = x0 * np.sin(t) + y * np.cos(t)
        
        # translate
        x += self.center[0]
        y += self.center[1]
        
        return list(map(tuple, np.column_stack((x, y)).tolist()))
    
    def move_anchor(self, x, y, id, mode='resize'):
        """
        Update the bounding box by moving a particular anchor point.
        
        Parameters
        ----------
        x : float
            The x-location the anhchor was dragged to
        y : float
            The y-location the anchor was dragged to
        id : 0-7
            The ID of the anchor point. The anchors are numbered starting from
            0 in the top left, and going clockwise.
        mode : str, optional (default 'resize')
            How to respond to the update
            
            'resize' moves as few anchor points as possible during resizing
            'resize-center' preserves the center position
            'resize-aspect' preserves the aspect ratio
            'resize-center-aspect' preserves the center position and aspect ratio
            'resize-square' fixes the aspect ratio to 1
            'resize-center-square' fixes the aspect ratio to 1 and preserves the center
        """
        
        fix = {'theta': False, 'center': False, 'aspect': False}
        
        
        # For now, hard-code different modes, then look for common patterns
        
        if mode == 'rotate':
            # We find the angle from dx, dy. For theta=0, vertex=0 is at PA of 135
            # degrees (top left)
            self.theta = np.degrees(np.arctan2(dy, dx)) - 135 + 45 * float(id)

            
        
        # TREAT ROTATE SEPARATELY? (since orthogonal to all other cases)
        
        if mode == 'rotate':
            fix['center'] = True
            fix['aspect'] = self.aspect
        elif mode == 'resize':
            fix['theta'] = True
        elif mode == 'resize-center':
            fix['theta'] = True
            fix['center'] = True
        elif mode == 'resize-center-aspect':
            fix['theta'] = True
            fix['center'] = True
            fix['aspect'] = self.aspect
        elif mode == 'resize-square':
            fix['theta'] = True
            fix['aspect'] = 1.
        elif mode == 'resize-center-square':
            fix['theta'] = True
            fix['center'] = True
            fix['aspect'] = 1.
        else:
            raise ValueError("Unknown mode: {0} (should be one of 'resize', "
                             "'resize-center', 'resize-aspect', 'resize-center-aspect', "
                             "'resize-square-', or 'resize-center-aspect'".format(mode))
                             
        # Find id of opposite anchor
        opposite_id = (id + 4) % 8
                             
        # If fix['center'] = True, then we should work in the frame of reference
        # of center of bbox. Otherwise use opposite anchor as origin.
        if fix['center']:
            dx, dy = x - self.center[0], self.center[1]
        else:
            opposite_vertex = self.vertices[opposite_id]  # need to update vertices to return 8 values
            dx, dy = x - opposite_vertex[0], opposite_vertex[1]
        
        # If fix['theta'] is False, we are rotating the shape so now we just
        # find the angle from dx, dy. For theta=0, vertex=0 is at PA of 135
        # degrees (top left)
        if fix['theta']:
            self.theta = np.degrees(np.arctan2(dy, dx)) - 135 + 45 * float(id)
            return
        
        if fix['aspect'] is not False:
            pass  # TODO
        else:
            pass
            # Here determine width and height from dx, dy, but need to take into account rotation. Should be             

        # MAGIC HERE
        

        

        
        
    