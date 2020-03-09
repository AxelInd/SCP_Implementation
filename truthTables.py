class truthTable (object):
    def __init__(self, logicType="L"):
        switch = {"L":self.getTruthTables_L(),"P":self.getTruthTables_P()}
        self.tbl_and, self.tbl_or, self.tbl_implication, self.tbl_bijective, self.tbl_not = switch[logicType]
    def getTruthTables(self):
        return self.tbl_and, self.tbl_or, self.tbl_implication, self.tbl_bijective, self.tbl_not
    @staticmethod
    def getTruthTables_L():
        tbl_and = {'True' : {'True': True,'None': None,'False':False}, 
        'None' : {'True': None,'None': None,'False':True},
        'False' : {'True': False,'None': False,'False':False}}
        
        tbl_or = {'True' : {'True': True,'None': True,'False':True}, 
        'None' : {'True': True,'None': None,'False':None},
        'False' : {'True': True,'None': None,'False':False}}
        
        tbl_implication = {'True' : {'True': True,'None': None,'False':False}, 
        'None' : {'True': True,'None': True,'False':None},
        'False' : {'True': True,'None': True,'False':True}}
        
        tbl_bijective = {'True' : {'True': True,'None': None,'False':False}, 
        'None' : {'True': None,'None': True,'False':None},
        'False' : {'True': False,'None': None,'False':True}}
        
        tbl_not = {'True': False, 'None':None, 'False':True}    

        return tbl_and, tbl_or, tbl_implication, tbl_bijective, tbl_not    

    @staticmethod
    def getTruthTables_P():
        tbl_and = {'True' : {'True': True,'False':False}, 
        'False' : {'True': False,'False':False}}
        
        tbl_or = {'True' : {'True': True,'False':True}, 
        'False' : {'True': True,'False':False}}
        
        tbl_implication = {'True' : {'True': True, 'False':False}, 
        'False' : {'True': True, 'False':True}}
        
        tbl_bijective = {'True' : {'True': True,'False':False}, 
        'False' : {'True': False, 'False':True}}
        
        tbl_not = {'True': False,'False':True}    
    
        return tbl_and, tbl_or, tbl_implication, tbl_bijective, tbl_not 
    def __str__(self):
        s = "--AND--\n{}\n--OR--\n{}\n--IMPLICAITON--\n{}\n--BIJECTION--\n{}\n--TABLENOT--\n{}\n".format(self.tbl_and, self.tbl_or, self.tbl_implication, self.tbl_bijective, self.tbl_not)
        return s