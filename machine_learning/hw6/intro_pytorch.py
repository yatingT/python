import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from torchvision import datasets, transforms

# Feel free to import other packages, if needed.
# As long as they are supported by CSL machines.


def get_data_loader(training = True):
    transform=transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize((0.1307,), (0.3081,))
        ])
    custom_transform= transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize((0.1307,), (0.3081,))
        ])
    train_set = datasets.MNIST('./data', train=True, download=True,
                       transform=custom_transform)
    test_set = datasets.MNIST('./data', train=False,download=True,
                       transform=custom_transform)
    
    if training == True:
        return torch.utils.data.DataLoader(train_set, batch_size = 50)
    else:
        return torch.utils.data.DataLoader(test_set, batch_size = 50)

def build_model():
    model = nn.Sequential(
    nn.Flatten(),
    nn.Linear(28*28,128),
    nn.ReLU(),
    nn.Linear(128, 64),
    nn.ReLU(),
    nn.Linear(64, 10),
    )
    return model 

def train_model(model, train_loader, criterion, T):
    opt = optim.SGD(model.parameters(), lr=0.001, momentum=0.9)
    model.train()
    for epochs in range(T):
        running_loss=0
        correct = 0
        total = 0
        for images,labels in train_loader:
            opt.zero_grad()
            output=model(images)
            loss=criterion(output,labels)
            running_loss=loss.item()
            predicted=output.argmax(dim=1,keepdim=True)
            total += labels.size(0)
            correct += predicted.eq(labels.view_as(predicted)).sum().item()
            loss.backward()
            opt.step()
        print('Train Epoch:{} Accuracy:{}/{}({:.2f}%) Loss:{:.3f}'.format(epochs, correct,total,100*(correct/total),running_loss))
    
def evaluate_model(model, test_loader, criterion, show_loss = True):
    opt = optim.SGD(model.parameters(), lr=0.001, momentum=0.9)
    model.eval()
    total = 0
    correct=0
    running_loss=0
    with torch.no_grad():
        for data, labels in test_loader:
            output=model(data)
            running_loss+=criterion(output,labels).item()
            predicted=output.argmax(dim=1,keepdim=True)
            total += labels.size(0)
            correct += predicted.eq(labels.view_as(predicted)).sum().item()
    running_loss=running_loss/len(test_loader)
    if show_loss == True:
        print('Average loss:{:.4f}\nAccuracy:{:.2f}%'.format(running_loss,100*(correct/total)))
    else: 
        print('Accuracy:{:.2f}%'.format(100*(correct/total)))
    
def predict_label(model, test_images, index):
    model.eval()
    output=model(test_images)
    prob = F.softmax(output, dim=1)
    class_names = ['zero', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine']
    d={}
    for i in range(len(class_names)):
        d[class_names[i]]=float(prob[index][i])*100
    d={k: v for k, v in sorted(d.items(), key=lambda item: item[1],reverse=True)}
    for i in list(d.items())[:3]:
        print('{}:{:.2f}%'.format(i[0],i[1]))

if __name__ == '__main__':
    '''
    Feel free to write your own test code here to exaime the correctness of your functions. 
    Note that this part will not be graded.
    '''
#     train_loader = get_data_loader()
#     test_loader = get_data_loader(False)
#     print(type(train_loader))
#     print(train_loader.dataset)
#     model = build_model()
#     print(model)
#     criterion = nn.CrossEntropyLoss()
#     train_model(model, train_loader, criterion, T = 5)
#     evaluate_model(model, test_loader, criterion, show_loss = False)
#     evaluate_model(model, test_loader, criterion, show_loss = True)
#     image=[] 
#     l=[]
#     for data, labels in test_loader:
#             image.append(data)
#             l.append(labels)
#     image
#     predict_label(model, image[0], 1)
