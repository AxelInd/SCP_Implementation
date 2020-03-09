# -*- coding: utf-8 -*-
"""
Created on Mon Feb 03 12:03:02 2020

@author: Axel
"""



class Error(Exception):
   pass
class NotBijectionError(Error):
   pass
class InvalidScpInsertion(Error):
   pass    
class InvalidScpInsertion_FirstPosition(InvalidScpInsertion):
   pass    
class InvalidScpInsertion_InvalidPosition(InvalidScpInsertion):
   pass
class invalidComplexOperation(InvalidScpInsertion):
   pass
class invalidComplexOperation_notComplexOperation(Error):
   pass     
class notImplementedError(Error):
   pass           
class notImplementedError_AbstractClass(notImplementedError):
   pass     
class notBitonicOperatorError(Error):
   pass     
class unitTestFailedError(Error):
   pass  
class invalidEpistemicStateError(Error):
    pass