import addressbook_pb2
person = addressbook_pb2.Person()
person.id = 1234
person.name = "John Doe"
person.email = "jdoe@example.com"
p1 = person.phones.add()
p1.number = "555-5321"
p2 = person.phones.add()
p2.number = "555-5322"
p2.type = addressbook_pb2.Person.WORK

#print(person.IsInitialized())
#print(person)
print(person.SerializeToString())

#print('\n'.join(dir(person)))
