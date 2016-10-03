import csv

import matplotlib.pyplot as plt


class StateRecorder:
    def __init__(self):
        self.clear()

    def getDataAtIteration(self,filter,iteration):
        result=[]
        for i,d in self.recording_data:
            if d[0]==filter or filter=='':
                result.append(d[iteration+1])
        return result

    def clear(self):
        self.recording_data = []
        self.cleared = True

    def recordXIterations(self,cortical_network,iterations,sub_iterations,activate_patterns):
        for it in range(iterations):
            cortical_network.new_iterations(sub_iterations,activate_patterns)
            self.record(cortical_network)

    def record(self,cortical_network):
        if self.cleared:
            self.cleared = False
            for ncount,neuron in enumerate(cortical_network.neurons):
                values, labels=neuron.getStateValues()
                for l in labels:
                    self.recording_data.append([l])
        i=0
        for neuron in cortical_network.neurons:
            values, labels = neuron.getStateValues()
            for v in values:
                self.recording_data[i].append(v)
                i+=1

    def save(self, filename):
        with open(filename, 'wb') as csvfile:
            writer = csv.writer(csvfile, delimiter=';',quotechar='|', quoting=csv.QUOTE_MINIMAL)
            for rec in self.recording_data:
                writer.writerow(rec)
                #spamwriter.writerow(['Spam', 'Lovely Spam', 'Wonderful Spam'])

    def format(self,row):
        for i,entity in enumerate(row):
            if i==0:
                row[i] = entity
            else:
                row[i] = float(entity)
        return row

    def load(self, filename):
        self.clear()
        self.cleared = False
        with open(filename, 'rb') as csvfile:
            reader = csv.reader(csvfile, delimiter=';', quotechar='|')
            for row in reader:
                print(row)
                self.recording_data.append(self.format(row))

    def plot_Neuron_Activities(self, neuronNr=[]):
        plt.ion()

        activityindexes=[]
        neuronnumber=-1
        for i in range(len(self.recording_data)):
            if self.recording_data[i][0]=='activity':
                neuronnumber+=1
                if neuronnumber in neuronNr:
                    activityindexes.append(i)


        plt.figure()
        plt.subplot(len(activityindexes), 1, 1)
        x = range(len(self.recording_data[0]) - 1)

        for i,a in enumerate(activityindexes):
            y = self.recording_data[a][1:]
            plt.subplot(len(activityindexes), 1, i+1)
            plt.plot(x, y, label=self.recording_data[a][0])
            plt.ylim((0.0, 1.0))
            plt.axhline(y=.5,color='r')
        plt.show()

    def plot_recordings(self,neuronNr=[]):
        plt.ion()

        currentNeuronnumber=-1
        x = range(len(self.recording_data[0]) - 1)

        subplotcount=0
        neuron_end_index=0
        neuron_start_index=0
        last_label='###'

        for i in range(len(self.recording_data)):
            if i==len(self.recording_data)-1 or (self.recording_data[i+1][0]=='activity'):
                currentNeuronnumber+=1
                neuron_end_index = i
                if currentNeuronnumber in neuronNr or neuronNr==[]:

                    last_label = '###'
                    plt.figure()
                    plt.subplot(subplotcount, 1, 1)
                    plt.title('Neuron{}'.format(currentNeuronnumber))
                    c=0
                    for j in range(neuron_start_index,neuron_end_index):

                        if self.recording_data[j][0][0:2]!=last_label[0:2]:
                            last_label = self.recording_data[j][0][0:2]
                            c+=1

                        y = self.recording_data[j][1:]
                        plt.subplot(subplotcount, 1, c)
                        plt.plot(x, y, label=self.recording_data[j][0])
                        plt.legend(loc='upper right',prop={'size':6})

                neuron_start_index=i+1
                subplotcount=0
                last_label = '###'
            else:
                if self.recording_data[i][0][0:2]!=last_label[0:2]:
                    last_label=self.recording_data[i][0][0:2]
                    subplotcount += 1


        plt.show()

        '''
            if neuronNr==[] or data[1] in neuronNr:
                if currentNeuronnumber!=data[1]:
                    plt.figure()
                    plt.subplot(data[2] + 1, 1, 1)
                    plt.title('Neuron{}'.format(data[1]))
                    plt.ylim((0.0, 0.1))
                    c = 1
                    currentNeuronnumber=data[1]


                y=data[1:]

                if data[0]!='synapse':
                    c+=1

                plt.subplot(data[2] + 1, 1, c)


                plt.plot(x, y, label=data[0])
                plt.legend(loc='upper right')
'''

            #if data[0]=='synapse':
            #else:
            #    plt.subplot(len(self.recording_data)+1, 1, c + 1)
            #    c+=1
            #    plt.plot(x, y, label=data[0])
            #    plt.legend(loc='upper right')


        #for i,l in enumerate(labels):
         #   if l!='synapse':
          #      plt.subplot(parametercount+1, 1, c + 1)
           #     c+=1

            #plt.plot(x,y[i], label=l)
            #plt.legend(loc='upper right')




#sr=StateRecorder()
#sr.recording_data=[['a',1,0.1],['b',2,0.2],['c',3,0.3]]
#sr.save('C:/Users/Marius/Desktop/test.csv')
#sr.load('C:/Users/Marius/Desktop/test.csv')
#sr.save('C:/Users/Marius/Desktop/test2.csv')
#sr.load('C:/Users/Marius/Desktop/test2.csv')


'''
    def plot_neuron_parameters(self,neuron):
        plt.ion()
        plt.figure()

        parametercount=4

        x=[]
        y=[[] for s in range(len(neuron.inp_synapses)+parametercount)]
        labels=[]

        for i in range(1000):
            print(i)
            self.cortical_network.new_iterations(True,1)
            x.append(i)

            values,labels=neuron.getStateValues()

            for vnum,value in enumerate(values):
                y[vnum].append(value)


        plt.subplot(parametercount + 1, 1, 1)
        plt.ylim((0.0,0.1))
        c=1
        for i,l in enumerate(labels):
            if l!='synapse':
                plt.subplot(parametercount+1, 1, c + 1)
                c+=1

            plt.plot(x,y[i], label=l)
            plt.legend(loc='upper right')

        plt.show()

    def plotresponses(self,pattern):
        plt.ion()
        plt.figure()

        x=[[] for n in self.cortical_network.neurons]
        y=[[] for n in self.cortical_network.neurons]
        for i in range(100):
            self.cortical_network.new_iteration(False)

        self.cortical_network.activatePattern(pattern)

        for i in range(100):
            self.cortical_network.new_iteration(False)
            for ni, n in enumerate(self.cortical_network.neurons):
                x[ni].append(i)
                y[ni].append(n.activity)

        for ni,n in enumerate(self.cortical_network.neurons):
            plt.subplot(len(self.cortical_network.neuronrows), len(self.cortical_network.neuronrows[0]), ni + 1)
            plt.plot(x[ni],y[ni])
            plt.ylim((0.0, 1.0))

        #plt.figure()
        plt.show()
'''