# 1. Student role: returning None and unclear error message when id / class is incorrect.
# 2. Teacher role - view students: incomplete or incorrect error message.
# 3. Admin role - check database: Very unpresentable appearance.
# 4. Admin role - Teacher management - delete teacher: print of None None, before the   error message instead of just the error message and error message is not customized.
# 5. Admin role - Teacher Management - add teacher: does not tell the teacher added it's ID. And name is not properly capitalized.
# 6. Teacher role - view students: if empty, return a message instead of an empty list.
# 7. Admin role - student management - add student: if class not properly inputted, does not let user know why the student was not added and just end operation.
# 8. Admin role - student management - add student: if every field is empty except class, empty student will be put into the system. No input validation for atleast:
##    Surname
##    Name
##    D.O.B
##    Guardian Name
##    Class
# 9. Admin role - student management - update student - change class: Student can change class to the same class student is in, which shouldn't be so.
# 10. Admin role - student manegement - update student - edit info: user should be able to see what student info can be changed and the input format of it - is acceptable.
# 11. Teacher role - view students: ugly presentation of students.
# 12. Teacher role - edit students: can continue to edit student's scores endlessly, should not be able to edit more than once.
# 13. Admin role - student management - change class: if student already has a report card, the report card is not moved with the student or not deleted when student is moved to another class. therefore causing student to access that report card even student is not in that class - issue with validating only student id and not both id and class.
# 14. Customize seperate operations of student not found based on the reason student is being looked for.
# 15. Scores can be edited once, by teacher, until before student accesses the report card for the first time, make the score no longer editable after student accesses the report card.
# 16. All name related input should return error if a number is detected, if puntuation marks are used.
# 17. What should be backup if the json file got mistakenly emptied?






# THINGS THAT MUST NEVER HAPPEN
### A student exists in two classes
### A deleted teacher is still assigned
### Scores become inconsistent
### A lookup returns the wrong student
### Data changes are not saved



++++++++++++++++++++++++++++++++++ The errror code if json file is mistakenly empty empty ++++++++++++++++++++++++++++++++++

$ python index.py
Traceback (most recent call last):
 line 530, in <module>
    main()
    ~~~~^^
 line 18, in main
    student_classes = base_file_config()
 line 152, in base_file_config
    student_classes = json.load(database_file)
  File "Python.framework/Versions/3.13/lib/python3.13/json/__init__.py", line 298, in load
    return loads(fp.read(),
        cls=cls, object_hook=object_hook,
        parse_float=parse_float, parse_int=parse_int,
        parse_constant=parse_constant, object_pairs_hook=object_pairs_hook, **kw)
  File "Python.framework/Versions/3.13/lib/python3.13/json/__init__.py", line 352, in loads
    return _default_decoder.decode(s)
           ~~~~~~~~~~~~~~~~~~~~~~~^^^
  File "Python.framework/Versions/3.13/lib/python3.13/json/decoder.py", line 345, in decode
    obj, end = self.raw_decode(s, idx=_w(s, 0).end())
               ~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^
  File "Python.framework/Versions/3.13/lib/python3.13/json/decoder.py", line 363, in raw_decode
    raise JSONDecodeError("Expecting value", s, err.value) from None
json.decoder.JSONDecodeError: Expecting value: line 1 column 1 (char 0)







