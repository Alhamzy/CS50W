list = [2,3,4]
print(len(list))
for el in list:
    print("index here is: ", list.index(el))
    print("next element is empty?", list.index(el)+1)