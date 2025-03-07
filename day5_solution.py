import re
import json

class Person:
    moods = {
        'h': "Happy",
        't': "Tired",
        'l': "Lazy"
    }


    def __init__(self, name, money, healthRate):
        self.name = name
        self.money = money
        self.healthRate = healthRate
        self.currentMood = Person.moods['h']
    def sleep(self, hours):
        if hours > 7:
            self.currentMood = Person.moods['l']
        elif hours < 7:
            self.currentMood = Person.moods['t']
        else :
            self.currentMood = Person.moods['h']
    def eat(self, nMeals):
        if nMeals == 3:
            self.healthRate = 100
        elif nMeals == 2:
            self.healthRate = 75
        else:
            self.healthRate = 50

    def buy(self, nItems):
        self.money -= nItems * 10


class Employee(Person):
    def __init__(self, name, money, healthRate, id, car, email, salary, distanceToWork, targetHour = 9):
        self._validateHealthRate(healthRate)
        self._validateSalary(salary)
        self._validateMail(email)
        super().__init__(name, money, healthRate)
        self.id = id
        self.car = car
        self.email = email
        self.salary = salary
        self.distanceToWork = distanceToWork
        # extra attribute to use in check late for clean & dynamic coding
        self.targetHour = targetHour

    def _validateSalary(self, s):
        if s < 1000:
            raise  ValueError("Salary must be more then 1000")

    def _validateMail(self, m):
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not (re.match(pattern, m)) :
            raise ValueError("follow email structure")

    def _validateHealthRate(self, hr):
        if (hr < 0) or (hr > 100) :
            raise ValueError("must be between 0 and 100")

    def work(self, hours):
        if hours > 8:
            Person.currentMood = Person.moods['t']
        elif hours < 8:
            Person.currentMood = Person.moods['l']
        else :
            Person.currentMood = Person.moods['h']
    # maybe I have to pass self.distanceToWork parameter
    # why aren't we passing some speed arg so we can pass it to car.run() ???
    # as run takes velocity so, the wraper method emp.drive() got to pass velocity
    # one problem arise if we don't pass speed is that the speed will remain 0 forever
    # once the car stop.
    def drive(self,  distance = None, velocity = 100,):
        """
        please specify distance param followed by velocity in km
        float :param distance: distance in km
        float :param velocity: speed in km/h
        :return: void
        """
        if not distance:
            distance = self.distanceToWork
        self.car.run(distance, velocity)
        return "driving..........."

    def refuel(self, gasAmount = 100):
        self.car.fuelRate += gasAmount
    def send_mail(self, to, subject, message, receiver, name):
        pass

class Office():
    employeesNum = 0
    @classmethod
    def chang_emps_num(cls, num):
        cls.employeesNum = num

    def __init__(self, name, employees):
        self.name = name
        self.employees = employees
        Office.employeesNum = len(employees)

    def get_all_employees(self):
        return self.employees
    def get_employee(self, empID):
        for emp in self.employees:
            if emp.id == empID:
                return emp

    def hire(self, emp):
        self.employees.append(emp)
        Office.employeesNum += 1
    def fire(self, empID):
        for emp in self.employees:
            if emp.id == empID:
                self.employees.pop(self.employees.index(emp))
                Office.employeesNum -= 1

    @staticmethod
    def calculate_lateness (targetHour , moveHour, distance, velocity):
        feasibleTime = targetHour - moveHour
        requiredTime = distance / velocity
        if feasibleTime < requiredTime:
            return 1 # late
        else :
            return 0 # not late

    def deduct(self,empID, deduction):
        for emp in self.employees:
            if emp.id == empID:
                emp.money -= deduction
    def reward(self, empID, reward ):
        for emp in self.employees:
            if emp.id == empID:
                emp.money += reward

    def check_lateness(self, empID, moveHour):
        moveHour = eval(moveHour)
        if moveHour > 9 :
            return 1 #late

        if isinstance(moveHour, float) :
            # converting 8.30 to 8.50 to measure time in decimal state
            intPart = int(moveHour)
            moveHour = intPart + (moveHour-intPart) * 100  / 60

        for emp in self.employees:
            if emp.id == empID:
                feasibleTime = emp.targetHour - moveHour
                requiredTime = emp.distanceToWork / emp.car.velocity
                if feasibleTime < requiredTime:
                    return 1  # late
                else:
                    return 0  # not late


class Car():
    def __init__(self, name, fuelRate, velocity):
        self.name = name
        self._validateVelocity(velocity)
        self._validateFuelRate(fuelRate)
        self.fuelRate = fuelRate
        self.velocity = velocity

    def _validateVelocity(self, v):
        if (v < 0) or (v > 200) :
            raise ValueError("velocity must be between 0 and 200")

    def _validateFuelRate(self, fr):
        if (fr < 0) or (fr > 100) :
            raise ValueError("fuel rate must be between 0 and 100")

    def run(self, distance, velocity = None):
        if not velocity :
            velocity = self.velocity
        self.velocity = velocity
        if self.velocity > 0 :
            # FuelRate decrease by10% every 10km distance.
            # then 1% loss of fuel per 1km of distance at any speed > 0
            fuelLoss = (distance * self.fuelRate) / 100
            if fuelLoss > self.fuelRate:
                # remaining distance is the distance of the difference in fuel which represents a percentage
                remDistance = (fuelLoss - self.fuelRate) * distance
                self.fuelRate = 0
                self.stop(remDistance)
                return
            else:
                self.fuelRate -= fuelLoss
                self.stop(0)
        else :
            self.stop(distance)
        # time = distance / velocity
        # return time


    def stop(self, remDistance):
        self.velocity = 0
        if remDistance > 0:
            print(f"you ran out of fuel or speed is zero, remaining distance is {remDistance} kilometers")

        else :
            print(f"you have reached your distination , remaining fuel is {self.fuelRate}")


#  chatgpt gererated testing code....
#  prmompt : generate validation and testing objects to this code , ! DO not rewrite the code :

# ----------------------
# Testing and Validation
# ----------------------

# 1. Test Person class:
print("---- Testing Person ----")
p1 = Person("Alice", 1000, 80)
print(f"Person: {p1.name}, Money: {p1.money}, HealthRate: {p1.healthRate}, Mood: {p1.currentMood}")

p1.sleep(6)  # < 7 hours → mood becomes "Tired"
print(f"After sleeping 6 hours, Mood: {p1.currentMood}")

p1.eat(2)  # 2 meals → healthRate should be 75
print(f"After eating 2 meals, HealthRate: {p1.healthRate}")

p1.buy(3)  # buying 3 items → decrease money by 30
print(f"After buying 3 items, Money: {p1.money}")

print("\n---- Testing Car ----")
# 2. Create a Car object:
car1 = Car("Fiat 128", fuelRate=100, velocity=100)
print(f"Car: {car1.name}, FuelRate: {car1.fuelRate}, Velocity: {car1.velocity}")

# Test run method: attempt to drive 20 km at 60 km/h.
print("Running car for 20 km at 60 km/h:")
car1.run(20, 60)
# Check console output from stop() method for feedback on fuel and destination status.

# 3. Test Employee validations and methods:
print("\n---- Testing Employee ----")
# Test invalid email
try:
    emp_invalid_email = Employee("Bob", 1500, 90, 2, car1, "invalidemail", 1500, 15)
except ValueError as e:
    print("Invalid email test passed:", e)

# Test invalid salary
try:
    emp_invalid_salary = Employee("Charlie", 1500, 90, 3, car1, "charlie@example.com", 900, 15)
except ValueError as e:
    print("Invalid salary test passed:", e)

# Create a valid Employee (Samy) with car1:
samy = Employee("Samy", 5000, 80, 1, car1, "samy@example.com", 2000, 20, targetHour=9)
print(f"Employee: {samy.name}, Email: {samy.email}, Salary: {samy.salary}, DistanceToWork: {samy.distanceToWork}")

# Test work method:
samy.work(9)  # > 8 hours → mood becomes "Tired"
print(f"After working 9 hours, Samy's mood (via Person.currentMood): {samy.currentMood}")

# Test drive method:
print("Samy driving to work:")
result = samy.drive(distance=20, velocity=80)
print(result)  # Expected to invoke car.run() and then print a message from stop()

# Test refuel method:
print("Refueling car by 50 units...")
samy.refuel(50)
print(f"Car fuel rate after refuel: {samy.car.fuelRate}")

# 4. Test Office class:
print("\n---- Testing Office ----")
# Create an Office with Samy as the initial employee.
office = Office("ITI Smart Village Office", [samy])
print(f"Office: {office.name}, Number of employees: {Office.employeesNum}")

# Create a second Car and Employee:
car2 = Car("Toyota", fuelRate=90, velocity=80)
dana = Employee("Dana", 6000, 85, 4, car2, "dana@example.com", 2500, 15)
office.hire(dana)
print("After hiring Dana:")
print("Employees in office:", [emp.name for emp in office.get_all_employees()])
print("Total employees:", Office.employeesNum)

# Test firing an employee:
office.fire(1)  # Fire Samy (id=1)
print("After firing Samy:")
print("Employees in office:", [emp.name for emp in office.get_all_employees()])
print("Total employees:", Office.employeesNum)

# Test lateness calculation using the static method:
lateness_status = Office.calculate_lateness(targetHour=9, moveHour=8.30, distance=20, velocity=80)
print(f"Calculated lateness (static method): {lateness_status}")

# Test check_lateness method:
# Here, we pass moveHour as a string "8.30" to simulate the input format.
lateness_check = office.check_lateness(empID=4, moveHour="8.30")
print(f"Check lateness for Dana (id=4) with moveHour '8.30': {lateness_check}")

# ----------------------------
# Additional Implementation Code
# ----------------------------

# 1. Implement a working send_mail method for Employee.
def employee_send_mail(self, to, subject, message, receiver, name):
    """
    Compose an email file using the given parameters.
    The file is named using the sender's name and receiver's name.
    """
    filename = f"email_from_{self.name}_to_{receiver}.txt"
    email_content = (
        f"From: {self.email}\n"
        f"To: {to}\n"
        f"Subject: {subject}\n\n"
        f"Hi, {name}\n\n"
        f"{message}\n\n"
        "Thanks,\n"
        f"{self.name}\n"
    )
    with open(filename, "w") as file:
        file.write(email_content)
    print(f"Email composed and saved to {filename}")

# Monkey-patch the send_mail method into Employee.
Employee.send_mail = employee_send_mail

# 2. Implement a salary property for Employee.
def get_salary(self):
    return self._salary

def set_salary(self, value):
    if value < 1000:
        raise ValueError("Salary must be more than 1000")
    self._salary = value

# In the Employee __init__, change assignment to use the internal variable.
# (Make sure to assign to self._salary instead of self.salary.)
Employee.salary = property(get_salary, set_salary)

# 3. Implement a healthRate property for Person.
def get_healthRate(self):
    return self._healthRate

def set_healthRate(self, value):
    if value < 0 or value > 100:
        raise ValueError("Health rate must be between 0 and 100")
    self._healthRate = value

# In the Person __init__, assign to self._healthRate instead of self.healthRate.
Person.healthRate = property(get_healthRate, set_healthRate)

# 4. (Optional) Implement a velocity property for Car with validation.
def get_velocity(self):
    return self._velocity

def set_velocity(self, value):
    if value < 0 or value > 200:
        raise ValueError("Velocity must be between 0 and 200")
    self._velocity = value

# In the Car __init__, assign to self._velocity instead of self.velocity.
Car.velocity = property(get_velocity, set_velocity)

################################################# loading OFFice() into json file
person1 = Person("ahmed", 1200, 85)
car1 = Car("ford", fuelRate=100, velocity=180)
car2 = Car("Toyota", fuelRate=90, velocity=120)

emp1 = Employee(
    name="amr",
    money=98999,
    healthRate=100,
    id=1,
    car=car1,
    email="amr.hussain@gmail.com",
    salary=2000,
    distanceToWork=30,
    targetHour=6
)

emp2 = Employee(
    name="Dana",
    money=6000,
    healthRate=85,
    id=2,
    car=car2,
    email="dana@gmail.com",
    salary=2500,
    distanceToWork=20,
    targetHour=9
)

# Create an Office and add the two employees.
office = Office("ITI Smart Village Office", [emp1, emp2])
with open("office_class.json", "w") as f:
    json.dump(office, f, default=lambda object: object.__dict__, indent=4)

print("Office data has been saved to office_data.json")