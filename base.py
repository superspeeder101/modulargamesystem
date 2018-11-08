import pygame
from pygame.locals import *

class ModuleConnectionReference:
  def __init__(self, module):
    self.module = module
    self.pendingConnections_IN = []
    self.pendingConnections_OUT = []
  
  @property
  def requiresUpdate(self):
    return self.pendingConnections_IN or self.pendingConnections_OUT
  
  def getPendingIN(self):
    return self.pendingConnections_IN
  
  def getPendingOUT(self):
    return self.pendingConnections_OUT
  
  def resetPending(self):
    self.pendingConnections_IN = []
    self.pendingConnections_OUT = []
    
  registerModuleConnectedToSelf
  registerSelfConnectedToModule

class Module:
  def __init__(self, inboundConnections):
    self.inboundConnections = inboundConnections
    self.outboundConnections = []
    self.mcr = ModuleConnectionReference(self)
  
  def __repr__(self):
    return "<{name} with {n1} inbound connections and {n2} outbound connections>".format(name=self.__class__.__name__, n1=len(self.inboundConnections), n2=len(self.outboundConnections))
  
  def connectTo(self, module):
    mcr = module.getConnectionReference()
    self.mcr.registerSelfConnectedToModule(module)
    mcr.registerModuleConnectedToSelf(self)
    self.runMCRUpdates()
  
  def __bulkConnectIN(self, connections):
    for c in connections:
      self.inboundConnections.append(c)
  
  def __bulkConnectOUT(self, connections):
    for c in connections:
      self.outboundConnections.append(c)
  
  def getConnectionReference(self):
    return self.mcr
  
  def runMCRUpdates(self):
    if self.mcr.requiresUpdate:
      self.__bulkConnectIN(self.mcr.getPendingIN())
      self.__bulkConnectOUT(self.mcr.getPendingOUT())
      self.mcr.resetPending()
