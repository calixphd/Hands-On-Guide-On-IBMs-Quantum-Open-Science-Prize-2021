# IGNORE matplotlib warnings
import warnings
import matplotlib.cbook
warnings.filterwarnings("ignore",category=matplotlib.cbook.mplDeprecation)

from IPython.display import display, Markdown, Math
import numpy as np
import math
from fractions import Fraction
    
def prepare_for_print():
    #SKIPCELL
    from IPython.display import display, Markdown, Math
    from qiskit import QuantumCircuit
    import numpy as np
    import math
    from fractions import Fraction


    import matplotlib.pyplot as plt
    import matplotlib

    COLOR = 'white'
    matplotlib.rc('axes',edgecolor='w')
    matplotlib.rcParams['text.color'] = COLOR
    matplotlib.rcParams['axes.labelcolor'] = COLOR
    matplotlib.rcParams['xtick.color'] = COLOR
    matplotlib.rcParams['ytick.color'] = COLOR


    plt.rcParams.update({
        "figure.facecolor":  (1.0, 1.0, 1.0, 0.0),  
        "axes.facecolor":    (1.0, 1.0, 1.0, 0.0),  
        "savefig.facecolor": (1.0, 1.0, 1.0, 0.0),  
    })


def plot_bloch_vector_spherical(theta, phi):
    b = Bloch()

    b.clear()
    b.figsize = [3,2]
    b.vector_color = ['r']
    b.vector_width = 5
    vector_mutation = 30
    #b.view = [160,-20]
    b.font_color = 'white'
    b.frame_color = 'white'
    b.frame_width = 1
    b.sphere_alpha = 0.0
    b.sphere_color = 'white'

    vec = [sin(theta)*cos(phi),sin(theta)*sin(phi),cos(theta)]

    b.add_vectors(vec)

    return b.show()
    
    
########## QUTIP
from math import pi, sin, cos
import matplotlib.pyplot as plt
import matplotlib
import numpy as np
from qutip import Bloch

def prepare(ready=True):
    b = Bloch()

    b.clear()
    b.figsize = [3,2]
    #b.view = [160,-20]

    if ready:
        b.vector_color = ['r']
        b.vector_width = 5
        vector_mutation = 30
        b.font_color = 'white'
        b.frame_color = 'white'
        b.frame_width = 1
        b.sphere_alpha = 0.0
        b.sphere_color = 'white'

    return b

def add_vector(b, theta, phi):
    vec = [sin(theta)*cos(phi),sin(theta)*sin(phi),cos(theta)]
    b.add_vectors(vec)

    return b

def add_point(b, theta, phi):
    vec = [sin(theta)*cos(phi),sin(theta)*sin(phi),cos(theta)]
    b.add_points(vec)

    return b


def with_phase(phi):
    yp = [sin(th)*cos(phi) for th in np.linspace(0, pi, 20)]
    xp = [sin(th)*sin(phi) for th in np.linspace(0, pi, 20)]
    zp = [cos(th) for th in np.linspace(0, pi, 20)]
    return [xp, yp, zp]


    
    
def num_to_latex(num, precision=5):
    """Takes a complex number as input and returns a latex representation
    
        Args:
            num (numerical): The number to be converted to latex.
            precision (int): If the real or imaginary parts of num are not close
                             to an integer, the number of decimal places to round to
        
        Returns:
            str: Latex representation of num
    """
    r = np.real(num)
    i = np.imag(num)
    common_factor = None
    
    # try to factor out common terms in imaginary numbers
    if np.isclose(abs(r), abs(i)) and not np.isclose(r, 0):
        common_factor = abs(r)
        r = r/common_factor
        i = i/common_factor
    
    common_terms = {
        1/math.sqrt(2): '\\tfrac{1}{\\sqrt{2}}',
        1/math.sqrt(3): '\\tfrac{1}{\\sqrt{3}}',
        math.sqrt(2/3): '\\sqrt{\\tfrac{2}{3}}',
        math.sqrt(3/4): '\\sqrt{\\tfrac{3}{4}}',
        1/math.sqrt(8): '\\tfrac{1}{\\sqrt{8}}'
    }
    def proc_value(val):
        # See if val is close to an integer
        val_mod = np.mod(val, 1)
        if (np.isclose(val_mod, 0) or np.isclose(val_mod, 1)):
            # If so, return that integer
            return str(int(np.round(val)))
        # Otherwise, see if it matches one of the common terms
        for term, latex_str in common_terms.items():
             if np.isclose(abs(val), term):
                    if val > 0:
                        return latex_str
                    else:
                        return "-" + latex_str
        # try to factorise val nicely
        frac = Fraction(val).limit_denominator()
        num, denom = frac.numerator, frac.denominator
        if num + denom < 20:
            if val > 0:
                return ("\\tfrac{%i}{%i}" % (abs(num), abs(denom)))
            else:
                return ("-\\tfrac{%i}{%i}" % (abs(num), abs(denom)))
        else:
            # Failing everything else, return val as a decimal
            return "{:.{}f}".format(val, precision).rstrip("0")
    
    if common_factor != None:
        common_facstring = proc_value(common_factor)
    else:
        common_facstring = None
    realstring = proc_value(r)
    if i > 0:
        operation = "+"
        imagstring = proc_value(i)
    else:
        operation = "-"
        imagstring = proc_value(-i)
    if imagstring == "1":
        imagstring = ""
    if imagstring == "0":
        return realstring
    if realstring == "0":
        if operation == "-":
            return "-{}i".format(imagstring)
        else:
            return "{}i".format(imagstring)
    if common_facstring != None:
        return "{}({} {} {}i)".format(common_facstring, realstring, operation, imagstring)
    else:
        return "{} {} {}i".format(realstring, operation, imagstring)


def matrix_to_latex(matrix, precision=5, pretext=""):
    """Latex representation of a complex numpy array (with dimension 2)
    
        Args:
            matrix (ndarray): The matrix to be converted to latex, must have dimension 2.
            precision: (int) For numbers not close to integers, the number of decimal places to round to.
            pretext: (str) Latex string to be prepended to the latex, intended for labels.
        
        Returns:
            str: Latex representation of the matrix
    """
    out_string = "\\begin{equation}\n"+pretext
    out_string += "\\begin{bmatrix}\n"
    for row in matrix:
        for amplitude in row:
            num_string = num_to_latex(amplitude, precision=precision)
            out_string += num_string + " & "
        out_string = out_string[:-2] # remove trailing ampersands
        out_string += " \\\\\n"
    out_string += "\end{bmatrix}\n\\end{equation}\n"
    return out_string

def array_to_latex(array, precision=5, pretext="", display_output=True):
    """Latex representation of a complex numpy array (with dimension 1 or 2)
    
        Args:
            matrix (ndarray): The array to be converted to latex, must have dimension 1 or 2.
            precision: (int) For numbers not close to integers, the number of decimal places to round to.
            pretext: (str) Latex string to be prepended to the latex, intended for labels.
            display_output: (bool) if True, uses IPython.display to display output, otherwise returns the latex string.
        
        Returns:
            str: Latex representation of the array, wrapped in $$
        
        Raises:
            ValueError: If array can not be interpreted as a numerical numpy array
            ValueError: If the dimension of array is not 1 or 2
    """
    try:
        array = np.asarray(array)
        array+1 # Test array contains numerical data
    except:
        raise ValueError("array_to_latex can only convert numpy arrays containing numerical data, or types that can be converted to such arrays")
    if array.ndim == 1:
        output = vector_to_latex(array, precision=precision, pretext=pretext)
    elif array.ndim == 2:
        output = matrix_to_latex(array, precision=precision, pretext=pretext)
    else:
        raise ValueError("array_to_latex can only convert numpy ndarrays of dimension 1 or 2")
    #if display_output:
    #    display(Math(output))
    #else:
    return(output)