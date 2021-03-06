import xgboost as xgb
import numpy as np

arg_file = open('output/args.csv','r')
data = []
x_train =[]
y_train =[]
x_test =[]

for line in arg_file:
    ll = line.split("\t")
    del ll[0]
    aux = []
    for l in ll:
        aux.append(l.split("\n")[0])
    data.append(aux)

means=[]

for d in data:
    if len(d)!=10:
        pass
    else:
        means.append(float(d[-1]))

maxMean = max(means)
print "MaxMean: "+str(maxMean)
i = means.index(maxMean)
args = data[i][:len(data[i])-1]

#leitura de arquivo
# file = open('output/hashing_trick_train.csv','r')
file = open('data/train_file.csv','r')
file = file.read()
lines = file.replace("\r","").split("\n")
del lines[-1]

#for line in lines:
for line in lines[1:]:
    l = line.split(",")
    y_train.append(l[-1])
    del l[-1]
    x_train.append(l)

y_train = np.array(y_train, dtype='f')
x_train = np.array(x_train, dtype='f')

#leitura de arquivo
#file = open('output/hashing_trick_test.csv','r')
file = open('data/test_file.csv','r')
file = file.read()
lines = file.replace("\r","").split("\n")

#for line in lines:
for line in lines[1:]:
    l = line.split(",")
    x_test.append(l)

print "Parametros utilizados:"
print args

del x_test[-1]
x_test = np.array(x_test, dtype='f')

dtrain = xgb.DMatrix( x_train, label=y_train)
param = {
            'bst:max_depth':int(float(args[2])),
            'bst:eta':float(args[0]),
            'silent':1,
            'objective':'binary:logistic',
            'nthread':4, 
            'eval_metric':'auc',
            'gamma' : float(args[1]),
            'min_child_weight' : int(float(args[3])),
            'subsample' : float(args[4]),
            'colsample_bytree' : float(args[5]),
            'num_round' : 300, #int(float(args[6])),
            'scale_pos_weight' : float(args[7]),
            'max_delta_step' : int(float(args[8]))
        }
plst = param.items()
bst = xgb.train(plst, dtrain)

# predict is not working without this code
# bst.save_model("model")
# bst = xgb.Booster(param)
# bst.load_model("model")

dteste = xgb.DMatrix(x_test)
y_pred = bst.predict(dteste, ntree_limit=bst.best_ntree_limit)

output = open('output/output.csv','w')
for elem in y_pred:
    output.write(str(elem))
    output.write("\n")