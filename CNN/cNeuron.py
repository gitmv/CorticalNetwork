import random

import numpy as np
from CNN.basicNeuron import basicNeuron

#self.activity_average_target=0.1
#self.average_activity_lag_param=10000;
#self.average_activity = activity_average_target

iteration_start = 0
activity_decrease = 1
collect_input = 2
STDP = 3
SH = 4
inhibit = 5
iteration_end = 6

class STDP_Mechanism_Set:
    def __init__(self,weight,weight_multiplyer,strength,normalize):
        self.weight = weight
        self.weight_multiplyer=weight_multiplyer
        self.strength=strength
        self.normalize=normalize

    def on_new_iteration(self,STDP_strength):
        self.weight+=STDP_strength*self.strength
        self.weight*=self.weight_multiplyer
        return self.weight


class SH_Mechanism_Set:
    def __init__(self, range_start,range_end, min, max, inc, dec):
        self.range_start = range_start
        self.range_end = range_end
        self.min=min
        self.max=max
        self.inc=inc
        self.dec=dec

        self.activity_avg=0.0
        self.range=(range_end-range_start)
        self.mul=self.range/2.0
        self.diff=self.mul+1

    def get_size_change(self,activity):
        self.activity_avg=(self.activity_avg*self.mul+activity)/self.diff
        if self.activity_avg*self.range > self.max*2.0:
            return -self.dec
        if self.activity_avg*self.range < self.min*2.0:
            return self.inc
        return 0.0


class cNeuron(basicNeuron):

    iterationsteps = [iteration_start, activity_decrease, collect_input, STDP, SH, inhibit, iteration_end]

    def __init__(self,position):
        super(self.__class__, self).__init__(position)

        #
        self.activity_multiplyer = 0.0                                  #is multiplyed to activity every iteration to decrease its value
        self.inhibition_multiplyer = 0.5
        self.firetreshold = 0.5

        #random Activity
        #self.random_activity=0.0
        self.random_history_range=200
        self.max_fire_possibility=0.0001#0.0001

        #STDP
        self.stdp_factor = 0.1                                        #ammount stdp of weight change
        self.own_activity_factor_exp=8
        self.synapse_mechanisms=[]

        # SH
        self.SH_Mechanisms=[]                                           #average counter,average factor,treshold,strength
        self.SH_Mechanisms.append(SH_Mechanism_Set(range_start=0, range_end=100, min=2, max=4, inc=0.0001, dec=0.001))
        self.SH_Mechanisms.append(SH_Mechanism_Set(range_start=0, range_end=10, min=0, max=5, inc=0.0, dec=0.01))
        self.SH_Mechanisms.append(SH_Mechanism_Set(range_start=0, range_end=5, min=0, max=3, inc=0.0, dec=0.01))


        self.synapse_weight_vector_length = random.uniform(0.5, 0.01)    #total length of all synapses

        self.min_weight_vector_length = 0.0001                          #
        self.max_weight_vector_length = 10                              #

        # history
        r=10
        r = np.maximum(self.random_history_range, r)
        for m in self.SH_Mechanisms:
            r=np.maximum(m.range_end,r)
        self.activity_history = [0.0 for i in range(r)]



    def addDendriteNeuron(self, neuron):
        synapse=super(self.__class__, self).addDendriteNeuron(neuron)
        self.synapse_mechanisms.append([
            STDP_Mechanism_Set(weight=synapse.weight, weight_multiplyer=1.0, strength=1.0,normalize=True) # long term weight
            #,STDP_Mechanism_Set(weight=0.0, weight_multiplyer=0.99, strength=1.0,normalize=False)   # short term weight
        ])


#########################################################################################################
####################################################################################################Logic
#########################################################################################################



    def refresh_activation_history(self):
        self.activity_history.insert(0,self.iteration_start_activity)
        self.activity_history.pop()
        #for i in range(self.activity_history_length):
        #    self.activity_history[self.activity_history_length-i-1]=self.activity_history[self.activity_history_length-i-2]
        #self.activity_history[0]=self.iteration_start_activity

    def get_STDP_Value(self,synapse):
        delay=2
        result=0.0

        #learn boost when both fire (dendrite spike)

        if synapse.inp.activity_history[delay+1]>synapse.inp.firetreshold: #and synapse.outp.activity_history[i+1]>synapse.outp.firetreshold:
            result+=(np.power(synapse.outp.activity_history[delay],self.own_activity_factor_exp)   *(self.synapse_weight_vector_length*self.stdp_factor))#*np.power(synapse.weight,0.1)#/(1.0+self.inhibition)

        return result

    def getActivityHistory(self,start,end):
        return self.activity_history[start:end]

    def convert_history_to_fire_binary(self,start,end):
        return list((map(lambda x: [0.0, 1.0][x > self.firetreshold], self.getActivityHistory(start,end))))

    def get_average_activity(self):
        return np.average(self.activity_history,0)

    def isFireing(self):
        return self.iteration_start_activity>self.firetreshold

    def normalize_synapse_values(self):
        # |weight vector| <= synapse_weight_vector_length
        count = 0
        for synapse, mechanisms in zip(self.inp_synapses, self.synapse_mechanisms):
            count += mechanisms[0].weight
        count *= (1 / self.synapse_weight_vector_length)
        for synapse, mechanisms in zip(self.inp_synapses, self.synapse_mechanisms):
            mechanisms[0].weight /= count

    def applySHMechanisms(self):
        for m in self.SH_Mechanisms:
            #self.synapse_weight_vector_length += m.get_size_change(self.get_activity())

            firecount = np.sum(self.convert_history_to_fire_binary(m.range_start,m.range_end))
            if firecount > m.max:  # schaetzen wie oft muster maximal auftritt
                self.synapse_weight_vector_length -= m.dec #not linear better?
            if firecount < m.min:  # schaetzen wie oft muster minimal auftritt
                self.synapse_weight_vector_length += m.inc

    def applySTDPMechanisms(self):
        for synapse,mechanisms in zip(self.inp_synapses,self.synapse_mechanisms):
            stdp_val=self.get_STDP_Value(synapse)
            synapse.weight = 0.0
            for mechanism in mechanisms:
                synapse.weight += mechanism.on_new_iteration(stdp_val)

    def apply_random_activity(self):
        activity_count = np.sum(self.convert_history_to_fire_binary(0, self.random_history_range))
        possibility=self.max_fire_possibility-self.max_fire_possibility/self.random_history_range*activity_count
        if random.uniform(0.0, 1.0) < possibility:
            self.activity=1.0

    def on_reward(self):
        for synapse_mechanisms in self.synapse_mechanisms:
            for mechanism in synapse_mechanisms[1:len(synapse_mechanisms)]:
                synapse_mechanisms[0].weight+=mechanism.weight
                mechanism.weight=0

    def new_iteration(self,step):

        ###########################
        if step == iteration_start:
            self.iteration_start_activity=self.activity
            self.refresh_activation_history()
            #self.refreshSHCounter()


        ###########################
        if step == activity_decrease:
            self.activity *= self.activity_multiplyer


        ###########################
        if step == collect_input:
            for synapse in self.inp_synapses:
                if synapse.inp.isFireing():
                    self.activity+=synapse.weight
            self.activity += self.outside_activation
            self.outside_activation=0.0

            #self.apply_random_activity()

            self.activity = np.clip(self.activity, 0.0, 1.0)


        ###########################
        if step == STDP:
            self.applySTDPMechanisms()


        ###########################
        if step == SH:
            self.applySHMechanisms()
            self.synapse_weight_vector_length = np.clip(self.synapse_weight_vector_length,self.min_weight_vector_length,self.max_weight_vector_length)


        ###########################
        if step == inhibit:
            for s in self.inhibition_targets:
                if self.isFireing():
                    s.outp.inhibition+=self.iteration_start_activity


        ############################
        if step == iteration_end:
            self.inhibition *= self.inhibition_multiplyer
            self.normalize_synapse_values()



#########################################################################################################
###################################################################################################Layout
#########################################################################################################


    def set_get_Parameter(self,i,value):
        ct=0
        if i==ct:
            if value!=None:self.activity_history_length=value
            return self.activity_history_length,1,10000
        ct+=1

        if i==ct:
            if value!=None:self.stdp_factor=value
            return self.stdp_factor,0.0001,1.0
        ct += 1

        #if i==2:
        #    if value!=None:self.minpatternactivity=value
        #    return self.minpatternactivity,0,self.activity_history_length

        #if i==3:
        #    if value!=None:self.maxpatternactivity=value
        #    return self.maxpatternactivity,self.minpatternactivity,self.activity_history_length

        #if i==4:
        #    if value!=None:self.activity_gravity=value
        #    return self.activity_gravity,0.0,1.0

        return None


    def getStateValues(self):
        values=[]
        labels=[]

        values.append(self.activity)
        labels.append('activity')

        for i,m in enumerate(self.SH_Mechanisms):
            values.append(np.sum(self.convert_history_to_fire_binary(m.range_start,m.range_end), 0))
            labels.append('SH_M_ct')
            values.append(m.min)
            labels.append('SH_M_min')
            values.append(m.max)
            labels.append('SH_M_max')


        values.append(self.synapse_weight_vector_length)
        labels.append('total synapse weight')
        #values.append(np.sum(self.convert_history_to_fire_binary(),0))
        #labels.append('firecount')

        for i,s in enumerate(self.inp_synapses):
            values.append(s.weight)
            labels.append('synapse')

        values.append(1)#TOTD: remove
        labels.append('test')

        return values,labels