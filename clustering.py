'''
Created on May 25, 2013

@author: Tony
'''
import math
import sys
from numpy import array


class Vector:
    def __init__(self, data):
        self.data = data
    def getSimilarity(self, otherVector):
        terms = set(self.getVector()).union(otherVector.getVector())
        dotprod = sum(self.getVector().get(k, 0) * otherVector.getVector().get(k, 0) for k in terms)
        magA = math.sqrt(sum(self.getVector().get(k, 0) ** 2 for k in terms))
        magB = math.sqrt(sum(otherVector.getVector().get(k, 0) ** 2 for k in terms))
        return dotprod / (magA * magB)
    def getDissimilarity(self, otherVector):
        return 1 - self.getSimilarity(otherVector)
    
    #TODO: decouple it
    def getVector(self):
        return self.data["bag_of_words"]


class Cluster:
    def __init__(self, listOfVectors):
        self.listOfVectors = listOfVectors
        self.centroidVector = self._findCentroid()
  
    def _findCentroid(self):
        minDissimilarity = sys.maxint
        centroidVector = None
        for vector in self.listOfVectors:
            totalDissimilarity = 0
            for otherVector in self.listOfVectors:
                totalDissimilarity += vector.getDissimilarity(otherVector)
            if totalDissimilarity < minDissimilarity:
                centroidVector = vector
                minDissimilarity = totalDissimilarity
        return centroidVector
        
    def getSimilarity(self, otherCluster):
        return self.centroidVector.getSimilarity(otherCluster.centroidVector)
    def getDissimilarity(self, otherCluster):
        return self.centroidVector.getDissimilarity(otherCluster)


# Initially, every new forms a cluster
# In each iteration, combine two clusters that are the nearest
# After that, update centroid in each cluster
# Repeat until the distance between each cluster > certain limit

def clustering(listOfClustering):
    similarityCache = {}
    for cluster in listOfClustering:
        for otherCluster in listOfClustering:
            similarityCache[(cluster.centroidVector, otherCluster.centroidVector)] = cluster.getSimilarity(otherCluster)

    while True:
        maxSimilarity = 0.3
        targetClusterA = None
        targetClusterB = None
        for cluster in listOfClustering:
            for otherCluster in listOfClustering:
                if cluster == otherCluster:
                    continue
                similarity = similarityCache[(cluster.centroidVector, otherCluster.centroidVector)]
                if similarity >= maxSimilarity:
                    maxSimilarity = similarity
                    targetClusterA = cluster
                    targetClusterB = otherCluster
        if targetClusterA == None or targetClusterA == None:
            break
        listOfClustering.append(Cluster(targetClusterA.listOfVectors + targetClusterB.listOfVectors))
        listOfClustering.remove(targetClusterA)
        listOfClustering.remove(targetClusterB)  
    return listOfClustering


def printData(data):
    print repr(data).decode("unicode_escape")
      
    
