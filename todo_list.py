from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date
from datetime import datetime, timedelta
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///todo.db?check_same_thread=False')
Base = declarative_base()


class Table(Base):          #Create table in the database using SQLalchemy
    __tablename__ = "task"
    id = Column(Integer, primary_key=True)
    task = Column(String, default='default_value')
    deadline = Column(Date, default=datetime.today())

    def __repr__(self):
        return self.task


Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()


def today_task(date):
    rows = session.query(Table).filter(Table.deadline == date).all()
    if len(rows) == 0:
        return 'Nothing to do!'
    list_of_tasks = []
    count = 0
    for i in rows:
        count = count + 1
        list_of_tasks.append('{}. {}'.format(count, i))
    return '\n'.join(list_of_tasks)     #Used .join method using \n to return multiline output


#weeks_tasks function calls today_task function 7 times
#day_definition function created for converting integer o/p of .weekday() to day strings
def weeks_tasks():
    today = datetime.today().date()
    week_task_list = []
    for i in range(0,7):
        day_of_week = today + timedelta (days = i)
        week_task_list.append('{} {} {}:'.format(day_definition(day_of_week.weekday()), day_of_week.day, day_of_week.strftime('%b')))
        week_task_list.append(today_task(day_of_week))
        week_task_list.append('')
    return '\n'.join(week_task_list)
    


def all_tasks():
    rows = session.query(Table).all()
    list_all_tasks = []
    list_all_tasks_combined = []
    count = 0
    # Sorted using python method. This can also be done with .order_by of SQL
    for i in rows:
        list_all_tasks.append((i.deadline, i))
    list_all_tasks.sort(key = lambda x: x[0])

    for i, j in list_all_tasks:
        count = count + 1
        list_all_tasks_combined.append(str(count) + '. ' + str(j) + '. ' + str(i.day) + ' ' + i.strftime('%b'))
    return '\n'.join(list_all_tasks_combined)


def missed_tasks():
    today_date = datetime.today().date()
    rows = session.query(Table).filter(Table.deadline < today_date).order_by(Table.deadline).all()
    if len(rows) == 0:
        return 'Nothing is missed!'
    list_missed = []
    count = 0
    for i in rows:
        count = count + 1
        list_missed.append('{}. {}. {} {}'.format(count, i, i.deadline.day, i.deadline.strftime('%b')))
    return '\n'.join(list_missed)
    

def enter_task(task_descr, deadline_date):
    new_row = Table(task=task_descr, deadline = deadline_date)
    session.add(new_row)
    session.commit()
    return 'The task has been added!'

def delete_task(num):
    task_data = all_tasks()
    all_tasks_list = task_data.split('\n')
    task_to_delete = all_tasks_list[num-1]
    task_name = task_to_delete.split('.')[1].strip()
    rows = session.query(Table).filter(Table.task == task_name).all()
    specific_row = rows[0]
    session.delete(specific_row)
    session.commit()
    return 'The task has been deleted!'

def day_definition(id):
    if id == 0:
        return 'Monday'
    elif id == 1:
        return 'Tuesday'
    elif id == 2:
        return 'Wednesday'
    elif id == 3:
        return 'Thursday'
    elif id == 4:
        return 'Friday'
    elif id == 5:
        return 'Saturday'
    else:
        return 'Sunday'


while True:
    print("1) Today's tasks")
    print("2) Week's tasks")
    print("3) All tasks")
    print("4) Missed tasks")
    print("5) Add task")
    print("6) Delete task")
    print("0) Exit")

    try:
        user_choice = int(input())
    except:
        print('Incorrect Input. Please enter an Integer between 0 and 6!')
        continue
    
    if user_choice == 1:
        today = datetime.today()
        print('\nToday {} {}'.format(today.day, today.strftime('%b')))
        today_date = today.date()
        print(today_task(today_date), '\n')

    elif user_choice == 2:
        print()
        print(weeks_tasks())

    elif user_choice == 3:
        print('\nAll tasks:')
        print(all_tasks(), '\n')

    elif user_choice == 4:
        print()
        print('Missed tasks:')
        print(missed_tasks())
        print()
        
    elif user_choice == 5:
        print('\nEnter task')
        task = input()
        while True:
            print('Enter deadline')
            deadline = input()
            try:
                deadline_date = datetime.strptime(deadline, '%Y-%m-%d')
                break
            except:
                print('Incorrect date entered!')
                continue
        print(enter_task(task, deadline_date), '\n')

    elif user_choice == 6:
        print()
        print('Chose the number of the task you want to delete:')
        print(all_tasks())
        num_task = int(input())
        print(delete_task(num_task))
        print()
    
    elif user_choice == 0:
        print('\nBye!')
        break

    else:
        print('Incorrect Input. Please enter an Integer between 0 and 6!')
