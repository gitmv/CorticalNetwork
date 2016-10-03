import csv
import datetime
import os
import random

from Analytics.TestSetting import *


class BruteForceParameterFinder:

    def __init__(self,NeuronType):
        self.NeuronType=NeuronType
        self.testsettings=[TestSetting1()]
        self.iterations=100000
        self.currentiteration=0
        for ts in self.testsettings:
            ts.createTestPatterns(self.iterations)
        self.running=False

    def getStartParameter(self):
        neuron=self.NeuronType([0,0])
        self.start_parameter_set=[]
        self.parameter_min_max=[]
        i=0
        while neuron.set_get_Parameter(i,None)!=None:
            param,min,max=neuron.set_get_Parameter(i, None)
            self.start_parameter_set.append(param)
            self.parameter_min_max.append([min,max])
            i+=1

    def getRandomParameter(self):
        result_param_set=[]
        for i,p in self.start_parameter_set:
            new_param=random.uniform(self.parameter_min_max[i][0], self.parameter_min_max[i][1])
            result_param_set.append(new_param )
        return result_param_set

    def create_directory(self,path):
        try:
            os.makedirs(path)
        except OSError:
            if not os.path.isdir(path):
                raise
        return path

    def displayFindings(self):
        print("not implemented")

    def saveparameters(self,filename,parameters):
        with open(filename, 'wb') as csvfile:
            writer = csv.writer(csvfile, delimiter=';', quotechar='|', quoting=csv.QUOTE_MINIMAL)
            writer.writerow(parameters)

    def startParameterSearch(self,search_iterations):
        self.getStartParameter()
        self.running=True
        rootfolder=datetime.datetime.now().time()
        i=0
        while self.running and i<search_iterations:
            iterationfolder = self.create_directory(rootfolder + '/{}'.format(i) + '/')
            params=self.getRandomParameter()
            self.saveparameters(iterationfolder+'params.csv',params)
            for ts in self.testsettings:
                ts.setNetworkParameters(params)
                ts.runTestSession()
                tsdir=self.create_directory(iterationfolder+ts.name+'/')
                ts.saveState(tsdir+'results.csv')
            score=self.getScore()
            i+=1


    def stopParameterSearch(self):
        self.running=False

    def getScore(self):
        score = 0.0
        for ts in self.testsettings:
            score+=ts.getTestScore()
        return score
