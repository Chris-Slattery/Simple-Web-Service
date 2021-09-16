import ZODB, ZODB.FileStorage
import persistent
import transaction



class Student(persistent.Persistent):
    studentName = ''
    lastName = ''
    studentNumber = ''

    def setStudentName(self, sName):
        self.studentName = sName
    def getStudentName(self):
        return self.studentName
    def setLastName(self, sLastName):
    	self.lastName = sLastName
    def getLastName(self):
        return self.lastName
    def setStudentNumber(self, sNumber):
        self.studentNumber = sNumber
    def getStudentNumber(self):
        return self.studentNumber
        
	        


storage = ZODB.FileStorage.FileStorage('mydata.fs')
db = ZODB.DB(storage)
connection = db.open()
root = connection.root

        
# saving the data


root.s1 = Student()

# set the data into the node
root.s1.setStudentName("Chris")
root.s1.setLastName("Slattery")
root.s1.setStudentNumber("B00092939")


# save the changes!
transaction.commit()






