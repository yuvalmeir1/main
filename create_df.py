 #region info & todo
#   create_df.py
# path C:\Users\User\PycharmProjects\vsProject\anconda\mq5_py\create_df.py
# web sample https://stackoverflow.com/questions/20763012/creating-a-pandas-dataframe-from-a-numpy-array-how-do-i-specify-the-index-colum?rq=1
# web index https://www.geeksforgeeks.org/python-list-index/#:~:text=index()%20is%20an%20inbuilt,index%20where%20the%20element%20appears.&text=element%20%E2%80%93%20The%20element%20whose%20lowest,from%20where%20the%20search%20begins.
# web tuples https://www.programiz.com/python-programming/tuple
# web youtube lists & tubles https://www.programiz.com/python-programming/tuple

 
#endregion
import pandas
import numpy
# Different types of tuples

# Empty tuple
my_tuple = ()
print(my_tuple)

# Tuple having integers
my_tuple = (1, 2, 3)
print(my_tuple)

# tuple with mixed datatypes
my_tuple = (1, "Hello", 3.4)
print(my_tuple)

# nested tuple
my_tuple = ("mouse", [8, 4, 6], (1, 2, 3))
print(my_tuple)

my_tuple = 3, 4.6, "dog"
print(my_tuple)

# tuple unpacking is also possible
a, b, c = my_tuple

print(a)      # 3
print(b)      # 4.6
print(c)      # dog



list1 = [1, 2, 3, 4, 5, 6, 7, 8, 9]
  
# Will print the index of '4' in list1
print(list1.index(4))
  
list2 = ['cat', 'bat', 'mat', 'cat', 'pet']
  
print (list2[0]) 
print (list2[-1]) 
print (list2[0:3]) 

print (list1[0:3]) 
print (list1[5:7]) 
print (list1[:7])
print (list1[4:])  
list1[4] =9999
 
list1[5] ='uouoiuoi'

print (list1[3:])  
list1[7:8] =78,79
print (list1[6:]) 
print (78 in list1)  
print (100 in list1) 
for iter in  list1:      
    print (iter) 

list1.append(10000)

list1.remove('uouoiuoi')
list7=list1.copy()

numbers1=(21,-5,6,9)
print(numbers1)
numbers1[1]=100
# print(numbers1[3])
# Will print the index of 'cat' in list2 
print(list2.index('cat'))

dtype = [('Col1','int32'), ('Col2','float32'), ('Col3','float32')]
# print(dtype.index(1))
values = numpy.zeros(20, dtype=dtype)
index = ['Row'+str(i) for i in range(1, len(values)+1)]

df = pandas.DataFrame(values, index=index)