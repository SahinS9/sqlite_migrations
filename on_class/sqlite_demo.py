import sqlite3

# on ram data - so u dont need to comment out the create tables on each run BC it refreshes on each run
# conn = sqlite3.connect(':memory:') in memory db creation

conn = sqlite3.connect(':memory:')

# conn = sqlite3.connect('employee.db')
c = conn.cursor()

c.execute("""CREATE TABLE employees (
          first TEXT,
          last TEXT,
          pay INTEGER

)""")


# c.execute(
#     """
# Insert into employees Values ('Corey', 'Schafer', 50000)
# """
# )


# c.execute("select * from employees where last = 'Schafer'")

# # c.fetchone() - only one row - if no more values then:  NONE 
# # c.fetchmany(5) - same with limit  - 5 rows if no more values then :NONE 
# # c.fetchall() - as a list output 

# print(c.fetchone())


# c.execute(
#     """
# Insert into employees Values ('Mary', 'Schafer', 70000)
# """
# )

# c.execute("Select * from employees")

# print(c.fetchall())


from employee import Employee

emp_1 = Employee('John', 'Doe', 80000)

emp_2 = Employee('Jane', 'Doe', 90000)


print(emp_1.first)
print(emp_1.last)
print(emp_1.pay)

#insert python objects to the db


#DO NOT USE!
#format structure helps to insert data in string format to the db BUT it is not safe, because any kind of input that is able to modify db is dangerous for the application
# c.execute("Insert into employees Values ('{}', '{}','{}')".format(emp_1.first, emp_1.last, emp_1.pay))


#as second argument
# #SAFER WAYS 1ST ONE - db api placeholder - tuple - strange look on select - even one value should be in tuple
# c.execute("INSERT into employees Values( ? , ? , ? )", (emp_1.first, emp_1.last, emp_1.pay))

# #SAFER WAY 2nd ONE - dictionary
# c.execute("INSERT into employees Values( :first , :last , :pay )", {'first': emp_2.first,'last': emp_2.last,'pay': emp_2.pay})


# c.execute("Select * from employees where last = ?", ('Schafer',))

# print(c.fetchall())


# c.execute("Select * from employees where pay > :pay", {'pay':5})

# print(c.fetchall())



# FUNCTIONS FOR EASIER USAGE
#context manager WITH - connection objects as context manager, so no need to open and close with code on each insert, update
#it ll be automatically commited and roll backed

def insert_emp(emp):
    with conn:
        c.execute("INSERT into employees Values( :first , :last , :pay )", {'first': emp.first,'last': emp.last,'pay': emp.pay})


#select stat. does not need commit so we will not use WITH in this case
def get_emps_by_name(lastname):
    c.execute("Select * from employees where last = :last", {'last':lastname})
    return c.fetchall()

def update_pay(emp,pay):
    with conn:
        c.execute("UPDATE employees SET pay = :pay where first = :first and last = :last", {'pay': pay, 'first': emp.first, 'last': emp.last})

def remove_emp(emp):
    with conn:
        c.execute("DELETE from employees where first = :first and last = :last", {'first':emp.first, 'last':emp.last})


insert_emp(emp_1)
insert_emp(emp_2)

emps = get_emps_by_name(emp_1.last)

print(emps)

update_pay(emp_2,84000)
remove_emp(emp_1)

emps = get_emps_by_name(emp_2.last)

print(emps)

conn.commit()

conn.close()
