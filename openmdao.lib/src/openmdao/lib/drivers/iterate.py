"""
A simple iteration driver. Basically runs a workflow, pasing the output
to the input for the next iteration. Relative change and number of iterations
are used as termination criterea.
"""

# pylint: disable-msg=E0611,F0401
from numpy import zeros

from openmdao.lib.traits.float import Float
from openmdao.lib.traits.int import Int
from openmdao.main.api import Driver, Expression
from openmdao.main.exceptions import RunStopped

class Iterate(Driver):
    """ A simple iteration driver. Basically runs a workflow, pasing the output
    to the input for the next iteration. Relative change and number of
    iterations are used as termination criterea."""

    # pylint: disable-msg=E1101
    loop_end = Expression(iotype='in', desc='loop output to pass to input') 
    loop_start = Expression(iotype='out', 
                            desc='loop input, taken from the input')
    
    max_iteration = Int(25, iotype='in', desc='Maximum number of \
                                         iterations before termination')
    
    tolerance = Float(0.00001, iotype='in', desc='Absolute convergence \
                                            tolerance between iterations')


    def __init__(self, doc=None):
        super(Iterate, self).__init__(doc)
        
        self.history = zeros(0)
        self.current_iteration = 0
        
    def execute(self):
        """Perform the iteration."""

        # perform an initial run for self-consistency
        self.run_iteration()
        
        self.current_iteration = 0
        history = zeros(self.max_iteration)
        history[0] = self.loop_end.evaluate()
        unconverged = True

        while unconverged:

            if self._stop:
                self.raise_exception('Stop requested', RunStopped)

            # check max iteration
            if self.current_iteration >= self.max_iteration-1:
                self.history = history[:self.current_iteration+1]
                self.raise_exception('Max iterations exceeded without ' + \
                                     'convergence.', RuntimeError)
                
            # Pass output to input
            val0 = history[self.current_iteration]
            self.loop_start.set(val0)

            # run the workflow
            self.run_iteration()
            self.current_iteration += 1
        
            # check convergence
            history[self.current_iteration] = self.loop_end.evaluate()
            val1 = history[self.current_iteration]
            
            if abs(val1-val0) < self.tolerance:
                break
            # relative tolerance -- problematic around 0
            #if abs( (val1-val0)/val0 ) < self.tolerance:
            #    break
            
        self.history = history[:self.current_iteration+1]
            

# End iterate.py