import numpy as np


class RegularSteppedTopology(object):
    
    def __init__(self, params):

        self._dim_elems = (params['nelx'], params['nely'])
        self._a0 = params['a0']
        self._b0 = params['b0']
        
        # The topology is formulated on a normalised mesh where elements are
        # 1x1 units. The aspect ratio of the elements is defined by (a,b) and
        # is only taken into account in the finite element model.
        nelx, nely = self._dim_elems
        ii, jj = np.meshgrid(np.arange(nelx), np.arange(nely))
        self._x = ii.T + 0.5
        self._y = jj.T + 0.5
        
        # Public attributes.
        self.a = self._a0
        self.b = self._b0
        self.ind_size = 4
        self.topology = None
        self.connectivity_penalty = 0.0
        self.is_connected = True
        self.xtip = 0
        self.ytip = 0
        
    def get_params(self):
        return (self.topology,
                self.a,
                self.b,
                self.xtip,
                self.ytip)
        
        
    def update_topology(self, xs):
        
        # Range of xs is [-1,1], make range [0,1].
        xss = [0.5*x + 0.5 for x in xs]
        
        scale = xss[3] if xss[3] > 0.05 else 0.05
        self.a = self._a0 * scale
        self.b = self._b0 * scale
        
        nelx, nely = self._dim_elems
        p1 = (nelx - 1)*xss[0]
        p2 = nely*xss[1]
        p3 = p1 + (nelx - 1 - p1)*xss[2]
        
        in1x = (p1 <= self._x) & (self._x <= nelx)
        in1y = (0 <= self._y) & (self._y <= p2)
        in2x = (p3 <= self._x) & (self._x <= nelx)
        in2y = (p2 <= self._y) & (self._y <= nely)
        topology = (in1x & in1y) | (in2x & in2y)

        self.topology = np.vstack((topology, np.flipud(topology)))
        self.xtip = 2 * self.a * nelx
        self.ytip = 2 * self.b * (nely - 0.05)
