import numpy as np
import matplotlib.pyplot as plt
%matplotlib inline

def f(X):
    return 1/(1 + np.exp(-X))

#generate a random set of data for our training and testing
n = 50
np.random.seed(12345)
trainX = np.random.random(n) * 10 - 5
trainY = f(trainX) + np.random.randn(n) * 0.125
testX = np.random.random(n) * 10 - 5
testY = f(testX) + np.random.randn(n) * 0.125
plt.plot(trainX, trainY, 'b.', testX, testY, 'gx')
plt.show()

def phi(X):
    '''
    Return a design matrix (a NumPy ndarray) whose columns are functions of the input vector, X.
    
    Produce a set of between 5 and 8 features for a given X input, one of which is an intercept term (all 1's)
    
    X (numpy.ndarray) input vector returns numpy.ndarray feature vector
    '''
    #Create a np array X
    X= np.asarray(X)
    #create an array to store features
    features = []
    #make a column of 1's for intercept term
    features.append(np.ones(X.shape[0]))
    #add original features
    features.append(X)
    
    '''
    
    Add polynomial or non-polynomial features with features.append(np.'feature equation here'(X))
    
    For the range(2,poly) equates to (# features) = (poly value); so at poly = 4 we have 4 features, we need to add
    a minimum of 2 non-polys... for a total of 6 features. We can add up to 4 non-poly features
    
    Use at least two non-polynomial functions of 𝑥. You can use any functions you want; consider trigonometric functions, 
    logarithmic and exponential functions,  radial basis function (Gaussians), etc. The only functions you are forbidden 
    to use are functions generating a sigmoid such as the one generating the synthetic data for this problem 
    (this includes the arctangent function)!
    
    '''
    # Add polynomial features, I interpreted the instructions as we COULD used polynomials, just had to use 2 non as well
    
    #used this to play around with how high the polynomial can go without producing NA's
    poly = 4
    
    for i in range(2, poly):
        features.append(X ** i)
    
    # Add non-polynomial features NO SIGMOIDs, played with different ones to see how it changed the fit
    
#     features.append(np.abs(X)) #abs value
#     features.append(np.sqrt(np.abs(X))) #sqr rt of abs value

#     features.append(np.exp(X))

    features.append(np.sin(X))
    features.append(np.cos(X))
    

    
    # Stack the features to create the feature matrix
    feature_matrix = np.column_stack(features)
    
    return feature_matrix


#calls your newly created phi function above for testing
Phi_train = phi(trainX)
Phi_test = phi(testX)

# Print the shape of the Train and Test matrices... verifying what I did above worked
# shape should be (n, # of features)
print("Train Design Matrix Shape:", Phi_train.shape)
print("Test Design Matrix Shape:", Phi_test.shape)

Phi_train #view phi(trainX) to make sure no NaNs or infs

def lr(Phi, y):
    '''
    Computes a linear regression result w minimizing ||Phi w - y||^2 via gradient descent.
    Repeat steps until counter is greateer than 100,000 or norm is less than 1e-6
    
    #1 Start with w as the zero vector.
    #2 Initialize norm, delta, and step counter.
    #3 Calculate delta (The amount w is going to change calculated as:  𝛼Φ𝑇(𝐲−Φ𝐰))
    #4 Update w and step counter
    #5 Calculate norm (the norm of a vector is the square root of the dot product of the vector with itself)
    #6 Repeat steps 3-5 until counter is greateer than 100,000 or norm is less than 1e-6.
    
    '''    
    w = np.array([0] * Phi.shape[1]) #zero vector, #1
    norm = float('inf') # start at infinity, #2
    alpha = 0.00001 #step size
    delta = alpha #initial delat is alpha*(term =1) so just alpha, #2
    counter = 0 #start counter at zero, #2
    
    # YOUR CODE HERE - FINISH THIS
    # Hint: calcuate the delta (starts at alpha in the equation), then add to w (e.g., w = w + delta)
    
    count_max=100000
    norm_min=1e-6
    
    while norm > norm_min and counter <= count_max: #per #6
        #calculate the delta, #3
        delta = alpha * np.dot(Phi.T, (trainY - np.dot(Phi, w))) #𝛼Φ𝑇(𝐲−Φ𝐰)
        
        #updated w with delta
        w = w+delta
        
        #calc norm, square root of the dot product of the vector with itself
        norm = np.sqrt(np.dot(delta, delta))
        
        #update counter
        counter += 1
        
    #why does this have to go here? I tried putting it with the other results, but {counter} could not be found...
    print(f"Gradient Descent took {counter} iterations.")
    return w

#call lr function and test

w_results = lr(Phi_train,trainY)

#print results

print("Weight Vector:")
print(w_results) #should have a value for each feature

#RMSE code

#calc predicted values dot of features matrix with weight vector
pred_train = np.dot(Phi_train, w_results) #dot product of phi(trainX) and w vector
pred_test = np.dot(Phi_test, w_results) #dot of phi(testX) and w vector

#calculate MSE: average of results minus predicted squared
mse_train = np.mean((trainY - pred_train) ** 2)
mse_test = np.mean((testY - pred_test) ** 2)

#calculate RMSE: square root of MSE
rmse_train = np.sqrt(mse_train)
rmse_test = np.sqrt(mse_test)

print("RMSE of Training Data:", rmse_train)
print("RMSE of Test Data:", rmse_test)


#Plotting codes...

#calc yhat for x∈(−5,5) at increments of 0.1
x_plt = np.arange(-5,5,0.1)
Phi_plt = phi(x_plt)
y_hat = np.dot(Phi_plt,w_results)

# Create the first plot
plt.scatter(trainX, trainY, c='b', label='Training Data', marker='o')
plt.scatter(testX, testY, c='g', label='Testing Data', marker='x')
plt.plot(x_plt, y_hat, c='r', label='Learned Function')
plt.xlabel('X')
plt.ylabel('Y')
plt.title('Linear Regression')
plt.legend()
plt.grid(True) #I like grid lines
plt.show()


#Create the second plot, scatter of residuals

resd_train = trainY-pred_train #calc residuals

#plot
plt.scatter(trainX, resd_train, c='m', marker='o')
plt.xlabel('Training X Values')
plt.ylabel('Residuals')
plt.title('Residuals on Training Data')
plt.grid(True) 
plt.show()

# Create third plot a histogram of residuals

plt.hist(resd_train, bins=5, color='c', edgecolor= "k")
plt.xlabel('Residuals')
plt.ylabel('Frequency')
plt.title('Histogram of Residuals on Training Data')
plt.show()

