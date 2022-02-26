import numpy as np
from matplotlib import pyplot as plt
import csv

# Feel free to import other packages, if needed.
# As long as they are supported by CSL machines.

def get_dataset(filename):
    dataset = None
    results = []
    with open(filename) as csvfile:
        reader = csv.reader(csvfile, quoting=csv.QUOTE_NONNUMERIC)
        for row in reader: 
            results.append(row[1:])
    dataset = np.array(results[1:])
    return dataset

def print_stats(dataset, col):
    length=len(dataset)
    target= dataset[:,col]
    mean=sum(target)/len(target)
    sd=(sum((x - mean) ** 2 for x in target) / (len(target) - 1))**0.5
    print('{}\n{:.2f}\n{:.2f}'.format(length, mean,sd))
    pass

def regression(dataset, cols, betas):
    mse = None
    y=dataset[:,0]
    x=dataset[:,cols]
    x = np.hstack((np.ones((len(dataset), 1)), x))    
    mse=np.sum(np.square(x@betas-y))/len(dataset)
    return mse

def gradient_descent(dataset, cols, betas):
    grads = None
    g=[]
    y=dataset[:,0]
    x=dataset[:,cols]
    x = np.hstack((np.ones((len(dataset), 1)), x))
    for i in range(len(betas)):
        grad=((x@betas-y)@x[:,i])*2/len(y) 
        g.append(grad)
    grads=np.array(g)
    return grads

def iterate_gradient(dataset, cols, betas, T, eta):   
    for i in range(1, T + 1):
        betas=betas-(gradient_descent(dataset,cols,betas)*eta)
        mse=regression(dataset,cols,betas)
        print(i, *map(lambda x: f'{x:.2f}', [mse, *betas]))
    pass

def compute_betas(dataset, cols):
    betas = None
    mse = None
    y=dataset[:,0]
    x=dataset[:,cols]
    x = np.concatenate([np.ones((x.shape[0], 1)), x], axis=1)
    betas=(np.linalg.inv(x.T@x))@(x.T@y)
    mse=regression(dataset,cols,betas)
    return (mse, *betas)

def predict(dataset, cols, features):
    result = None
    t=compute_betas(dataset,cols)
    betas=t[1:]
    result=betas[0] 
    for i in range(len(features)):
        result+=features[i]*betas[i+1]
    return result

def synthetic_datasets(betas, alphas, X, sigma):
    z=np.random.normal(0,sigma,len(X))
    linear=np.ones((X.shape[0], 1))
    for i in range(len(X)):
        linear[i]=betas[0] + betas[1] * X[i][0] + z[i]
    linear= np.concatenate([linear, X], axis=1)
    
    quadratic=np.ones((X.shape[0], 1))
    for i in range(len(X)):
        quadratic[i]=alphas[0]+alphas[1]*(X[i][0])**2+z[i]
    quadratic= np.concatenate([quadratic, X], axis=1)
    
    return linear, quadratic

def plot_mse():
    from sys import argv
    if len(argv) == 2 and argv[1] == 'csl':
        import matplotlib
        matplotlib.use('Agg')

    X = np.random.randint(-100,101, size=(1000,1))
    alpha=np.array([0,2])
    beta=np.array([0,1])
    sigmas = np.logspace(-4, 5, num=10)
    linear_result=[]
    quadratic_result=[]
    for sigma in sigmas:
        l,q=synthetic_datasets(alpha,beta,X,sigma)
        linear=compute_betas(l,[1])
        quadratic=compute_betas(q,[1])
        linear_result.append(linear[0])
        quadratic_result.append(quadratic[0])

    fig1 = plt.plot(sigmas, linear_result, "-o", label = "Linear")
    fig2 = plt.plot(sigmas, quadratic_result, "-o", label = "Quadratic")
    plt.xscale("log")
    plt.yscale("log")
    plt.xlabel("sigmas")
    plt.ylabel("MSEs")
    plt.legend()
    plt.savefig('mse.pdf')

if __name__ == '__main__':
    ### DO NOT CHANGE THIS SECTION ###
    plot_mse()
