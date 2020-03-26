import asyncio
from grpclib.client import Channel
from student_pb2 import Student,GetStudentRequest,UpdateStudentRequest,DeleteStudentRequest,ListStudentsRequest
from student_grpc import StudentServiceStub

user_choice = """
Enter:
- 'a' to add a new student 
- 'l' to list of students
- 'r' to delete a student
- 'd' to update a student
- 'i' to get detail of one student
- 'q' to quit


Your choice:"""


async def main():
	channel = Channel('127.0.0.1', 50051)
	student = StudentServiceStub(channel)
	choice = input(user_choice)
	while choice!='q':
		if choice=='a':
			name = input('Enter your name: ')
			email = input('Enter your email: ')
			student_id = input('Enter your student_id: ')
			reply: Student = await student.CreateStudent(Student(name=name,email=email,student_id=student_id))
			print('*****************')
			print('Student is created!')
			print(f'Name: {reply.name}')
			print(f'Email: {reply.email}')
			print(f'Student_id: {reply.student_id}')

		elif choice=='i':
			student_id = input('Enter your student_id: ')
			reply: Student = await student.GetStudent(GetStudentRequest(student_id=student_id))
			print('*******************')
			print(f'Name: {reply.name}')
			print(f'Email: {reply.email}')
			print(f'Student_id: {reply.student_id}')
		elif choice=='d':
			student_id = input('enter student_id: ')
			key = input('enter key value which are name, email, or student_id: ')
			new_value = input('enter new value: ')
			reply:Student = await student.UpdateStudent(UpdateStudentRequest(student_id=student_id,key=key,new_value=new_value))
			print('*******************')
			print('Student detail is updated')
			print(f'Name: {reply.name}')
			print(f'Email: {reply.email}')
			print(f'Student_id: {reply.student_id}')
		elif choice=='r':
			student_id = input('enter student_id: ')
			reply:Student = await student.DeleteStudent(DeleteStudentRequest(student_id=student_id))
			print('*******************')
			print(f'Student with {student_id} is deleted!')
		elif choice=='l':
			reply:Student = await student.ListStudent(ListStudentsRequest())
			print('***************************')
			print('List of students')
			print('')
			print(reply)
		else:
			print('Unknown choice\n')
			
		choice = input(user_choice)
	channel.close()


if __name__ == '__main__':
    asyncio.run(main())