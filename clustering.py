'''
Created on May 25, 2013

@author: Tony
'''
import math
import sys
import time


class Vector:
    def __init__(self, data):
        self.data = data
    def getSimilarity(self, otherVector):
        terms = self.getVector() | otherVector.getVector()
        selfBagOfWord = self.getVector()
        otherBagOfWord = otherVector.getVector()
        dotprod = sum(selfBagOfWord.get(k, 0) * otherBagOfWord.get(k, 0) for k in terms)
        magA = math.sqrt(sum(selfBagOfWord.get(k, 0) ** 2 for k in terms))
        magB = math.sqrt(sum(otherBagOfWord.get(k, 0) ** 2 for k in terms))
        return dotprod / (magA * magB)
    
    
    def getDissimilarity(self, otherVector):
        return 1 - self.getSimilarity(otherVector)
    
    #TODO: decouple it
    def getVector(self):
        return self.data["bag_of_words"]


class Cluster:
    def __init__(self, listOfVectors, similarityCache = None):
        self.listOfVectors = listOfVectors
        if similarityCache is None:
            self.centroidVector = self.listOfVectors[0]
        else: 
            self.centroidVector = self._findCentroid(similarityCache)

    def _findCentroid(self, similarityCache):
        minDissimilarity = sys.maxint
        centroidVector = None
        for vector in self.listOfVectors:
            totalDissimilarity = 0
            for otherVector in self.listOfVectors:
                totalDissimilarity += (1 - similarityCache[frozenset([vector, otherVector])])
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
    start_time = time.clock()

    similarityCache = {}
    for cluster in listOfClustering:
        for otherCluster in listOfClustering:
            if not frozenset([cluster.centroidVector, otherCluster.centroidVector]) in similarityCache:
                similarityCache[frozenset([cluster.centroidVector, otherCluster.centroidVector])] = cluster.getSimilarity(otherCluster)

    print ("cache " + str(time.clock() - start_time))

    while True:
        maxSimilarity = 0.3
        targetClusterA = None
        targetClusterB = None
        for (index, cluster) in enumerate(listOfClustering):
            for otherCluster in listOfClustering[index + 1 :]:
                similarity = similarityCache[frozenset([cluster.centroidVector, otherCluster.centroidVector])]
                if similarity >= maxSimilarity:
                    maxSimilarity = similarity
                    targetClusterA = cluster
                    targetClusterB = otherCluster
        if targetClusterA == None or targetClusterB == None:
            break
        listOfClustering.append(Cluster((targetClusterA.listOfVectors + targetClusterB.listOfVectors), similarityCache))
        listOfClustering.remove(targetClusterA)
        listOfClustering.remove(targetClusterB)  
    return listOfClustering


def printData(data):
    print repr(data).decode("unicode_escape")
      
    
