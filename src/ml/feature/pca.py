# released under bsd licence
# see LICENSE file or http://www.opensource.org/licenses/bsd-license.php for details
# Institute of Applied Simulation (ZHAW)
# Author Thomas Niederberger

import numpy as np
from scipy import *
from scipy.sparse import *
import scipy.linalg as linalg

def pca(data, dimensions = 2):
    """calculates a PCA of the specified dataset. 
    
    Parameters
    ----------
    data : array_like
        dense data matrix which is supposed to have dataitems in the rows and features in the columns.
    dimensions : int, optional
        number of dimensions (default = 2) to consider in the PCA
        
    Returns
    -------
    loc : ndarray
        PCA matrix of shape (# of dataitems, dimensions)
    """
    covariance = np.cov(np.transpose(data))
    u_matrix, lambda_matrix, v_matrix = np.linalg.svd(covariance)
    
    # remove means from original data
    noMeansData = data - np.mean(data, 0)

    loc = np.transpose(np.dot(np.transpose(u_matrix[:, 0:dimensions]), np.transpose(noMeansData)))
    #singular_values = np.diag(lambda_matrix)
    
    return (lambda_matrix, loc, u_matrix[:, 0:dimensions])

def retained_variance(singular_values, dim):
    """Calculate how much variance (in percent) is retained when reducing the number of dimensions to dim"""
    return np.sum(singular_values[0:dim]) / np.sum(singular_values)

def mds(dist, dimensions = 2):
    n = len(dist[:,1])
    squared = dist ** 2
    
    J = np.eye(n) - np.ones(n, 'float')/n
    B = -1.0/2.0 * np.dot(np.dot(J, squared), J)
    
    #better use svd!!
    val, vec = np.linalg.eig(B)
    
    val = np.abs(val) #taking absolute values in case of negative eigenvalues occur. Not sure whether this is allowed
    eigInd = np.flipud(np.argsort(val)[(n-dimensions):n])
    loc = np.dot(vec[:, eigInd], np.sqrt(np.diag(val[eigInd])))
    return loc