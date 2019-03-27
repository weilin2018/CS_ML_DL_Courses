#!python
import numpy as np
from numpy import linalg
import pylab as pl
np.random.seed(100)

##=======================================================================
## Kernel Functions
##=======================================================================

def linear_kernel(x1, x2):
    return np.dot(x1, x2)

def polynomial_kernel(x, y, p=2):
    return (1 + np.dot(x, y)) ** p

def gaussian_kernel(x, y, sigma=5.0):
    return np.exp(-linalg.norm(x-y)**2 / (2 * (sigma ** 2)))


##=======================================================================
## Kernel Perceptron
##=======================================================================

def fit(X, y, T,kernel):
    n_samples, n_features = X.shape
    alpha = np.zeros(n_samples, dtype=np.float64)

    # Gram matrix
    K = np.zeros((n_samples, n_samples))
    for i in range(n_samples):
        for j in range(n_samples):
            K[i,j] = kernel(X[i], X[j])

    for t in range(T):
        for i in range(n_samples):
            if np.sign(np.sum(K[:,i] * alpha * y)) != y[i]:
                alpha[i] += 1.0
    
    idx = alpha > 1e-5
    alpha = alpha[idx]
    sv = X[idx]
    sv_y = y[idx]
    
    return alpha,sv,sv_y

def project(X,kernel,alpha,sv,sv_y):
    
    y_predict = np.zeros(len(X))
    for i in range(len(X)):
        s = 0
        for a, svy, sv_ in zip(alpha, sv_y, sv):
            s += a * svy * 1
            s += a * svy * kernel(X[i], sv_)
        y_predict[i] = s
    return y_predict

def predict(X,kernel,alpha,sv,sv_y):
    X = np.atleast_2d(X)
    n_samples, n_features = X.shape
    return np.sign(project(X,kernel,alpha,sv, sv_y))

##=======================================================================
## Use kernel percetpron
##=======================================================================

def gen_lin_separable_data(num_data):
    # generate training data in the 2-d case
    mean1 = np.array([0, 2])
    mean2 = np.array([2, 0])
    cov = np.array([[0.8, 0.6], [0.6, 0.8]])
    X1 = np.random.multivariate_normal(mean1, cov, num_data)
    y1 = np.ones(len(X1))
    X2 = np.random.multivariate_normal(mean2, cov, num_data)
    y2 = np.ones(len(X2)) * -1
    return X1, y1, X2, y2

def gen_non_lin_separable_data(num_data):
    mean1 = [-1, 2]
    mean2 = [1, -1]
    mean3 = [4, -4]
    mean4 = [-4, 4]
    cov = [[1.0,0.8], [0.8, 1.0]]
    X1 = np.random.multivariate_normal(mean1, cov, num_data)
    X1 = np.vstack((X1, np.random.multivariate_normal(mean3, cov, num_data)))
    y1 = np.ones(len(X1))
    X2 = np.random.multivariate_normal(mean2, cov, num_data)
    X2 = np.vstack((X2, np.random.multivariate_normal(mean4, cov, num_data)))
    y2 = np.ones(len(X2)) * -1
    return X1, y1, X2, y2

def gen_lin_separable_overlap_data(num_data):
    # generate training data in the 2-d case
    mean1 = np.array([0, 2])
    mean2 = np.array([2, 0])
    cov = np.array([[1.5, 1.0], [1.0, 1.5]])
    X1 = np.random.multivariate_normal(mean1, cov,  num_data)
    y1 = np.ones(len(X1))
    X2 = np.random.multivariate_normal(mean2, cov,  num_data)
    y2 = np.ones(len(X2)) * -1
    return X1, y1, X2, y2

def split_train(X1, y1, X2, y2):
    X1_train = X1[:90]
    y1_train = y1[:90]
    X2_train = X2[:90]
    y2_train = y2[:90]
    X_train = np.vstack((X1_train, X2_train))
    y_train = np.hstack((y1_train, y2_train))
    return X_train, y_train

def split_test(X1, y1, X2, y2):
    X1_test = X1[90:]
    y1_test = y1[90:]
    X2_test = X2[90:]
    y2_test = y2[90:]
    X_test = np.vstack((X1_test, X2_test))
    y_test = np.hstack((y1_test, y2_test))
    return X_test, y_test


def plot_contour(X1_train, X2_train, kernel,alpha,sv,sv_y):
    pl.plot(X1_train[:,0], X1_train[:,1], "ro")
    pl.plot(X2_train[:,0], X2_train[:,1], "bo")
    pl.scatter(sv[:,0], sv[:,1], s=100, c="g")

    X1, X2 = np.meshgrid(np.linspace(-6,6,50), np.linspace(-6,6,50))
    X = np.array([[x1, x2] for x1, x2 in zip(np.ravel(X1), np.ravel(X2))])
    Z = project(X,kernel,alpha,sv,sv_y).reshape(X1.shape)
    pl.contour(X1, X2, Z, [0.0], colors='k', linewidths=1, origin='lower')

    pl.axis("tight")
    pl.show()

def test_kernel():
    X1, y1, X2, y2 = gen_lin_separable_data(100)
    X_train, y_train = split_train(X1, y1, X2, y2)
    X_test, y_test = split_test(X1, y1, X2, y2)

    # kernel = polynomial_kernel
    kernel = gaussian_kernel
    epochs = 20
    alpha,sv,sv_y = fit(X_train, y_train,epochs,kernel)
    y_predict = predict(X_test,kernel,alpha,sv,sv_y)

    # correct
    print("y_test = {}".format(y_test))
    correct = np.sum(y_predict == y_test)
    print("%d out of %d predictions correct" % (correct, len(y_predict)))

    plot_contour(X_train[y_train==1], X_train[y_train==-1], kernel,alpha,sv,sv_y)

if __name__ == "__main__":
    
    test_kernel()