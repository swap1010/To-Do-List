from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String, Date
import datetime
days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
engine = create_engine('sqlite:///todo.db')
Base = declarative_base()


class tasks(Base):
    __tablename__ = 'task'
    id = Column(Integer, primary_key=True)
    task = Column(String, default='')
    deadline = Column(Date, default=datetime.datetime.today())


def print_tasks(day, todays):
    all_tasks = session.query(tasks).filter(tasks.deadline == todays).all()
    print(f"\n{day} {todays.day} {todays.strftime('%b')}:")
    if not all_tasks:
        print("Nothing to do!\n")
    else:
        for id1, t in enumerate(all_tasks, 1):
            print(f"{id1}. {t.task}\n")


Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()
while True:
    print("1) Today's tasks")
    print("2) Week's tasks")
    print("3) All tasks")
    print("4) Missed tasks")
    print("5) Add task")
    print("6) Delete task")
    print("0) Exit")
    choice = int(input())
    if choice == 1:
        today = datetime.datetime.today().date()
        print_tasks("Today", today)
    elif choice == 2:
        today = datetime.datetime.today()
        for i in range(7):
            dates = today + datetime.timedelta(days=i)
            print_tasks(days[dates.weekday()], dates.date())
    elif choice == 3:
        print("All tasks:")
        all_task = session.query(tasks).order_by(tasks.deadline).all()
        if not all_task:
            print("Nothing to do!")
        else:
            for id2, task in enumerate(all_task, 1):
                print(f"{id2}. {task.task}. {task.deadline.day} {task.deadline.strftime('%b')}")
    elif choice == 4:
        mis_tasks = session.query(tasks).filter(tasks.deadline < datetime.datetime.today().date()).all()
        if not mis_tasks:
            print("Nothing is missed!")
        else:
            for id3, mis_task in enumerate(mis_tasks, 1):
                print(f"{id3}. {mis_task.task}. {mis_task.deadline.day} {mis_task.deadline.strftime('%b')}")
            print()
    elif choice == 5:
        task = input("Enter task\n")
        deadline = datetime.datetime.strptime(input("Enter deadline\n"), '%Y-%m-%d')
        new_task = tasks(task=task, deadline=deadline)
        session.add(new_task)
        session.commit()
        print("The task has been added!")
    elif choice == 6:
        print("Choose the number of the task you want to delete:")
        al_tasks = session.query(tasks).order_by(tasks.deadline).all()
        if not al_tasks:
            print("Nothing to delete!")
        else:
            for id4, task in enumerate(al_tasks, 1):
                print(f"{id4}. {task.task}. {task.deadline.day} {task.deadline.strftime('%b')}")
            n = int(input())
            rows = session.query(tasks).all()
            session.delete(rows[n - 1])
            session.commit()
            print("The task has been deleted!\n")
    else:
        print("Bye!")
        exit()
