import asyncio
from gino import Gino
from grpclib.utils import graceful_exit
from grpclib.server import Server
from student_pb2 import Student,ListStudentsResponse
from student_grpc import StudentServiceBase
from google.protobuf import empty_pb2
db = Gino()


class Pupil(db.Model):
    __tablename__ = 'students'

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String)
    email = db.Column(db.String)
    student_id = db.Column(db.String)


class StudentService(StudentServiceBase):

    async def CreateStudent(self, stream):
        request: Student = await stream.recv_message()
        name = request.name
        email = request.email
        student_id = request.student_id
        await stream.send_message(Student(name=name,email=email,student_id=student_id))
        new_student = await Pupil.create(name=name,email=email,student_id=student_id)
        # await db.pop_bind().close()

    async def GetStudent(self, stream):
        request: GetStudentRequest = await stream.recv_message()
        student_id = request.student_id
        get_student = await Pupil.query.where(Pupil.student_id == student_id).gino.first()
        name = get_student.name
        email = get_student.email
        await stream.send_message(Student(name=name, email=email, student_id=student_id))
        

    async def UpdateStudent(self, stream):
        request: UpdateStudentRequest = await stream.recv_message()
        student_id = request.student_id
        key = request.key 
        new_value = request.new_value
        all_students = await Pupil.query.gino.all()
        for student in all_students:
            if student.student_id==student_id:
                if key == 'name':
                    await student.update(name=new_value).apply()
                elif key == 'email':
                    await student.update(email=new_value).apply()
                elif key == 'student_id':
                    await student.update(student_id=new_value).apply()
                else:
                    print('Unknown keyword key\n')
            # else:
            #     print('Error student id\n')
        get_student = await Pupil.query.where(Pupil.student_id == student_id).gino.first()
        name = get_student.name
        email = get_student.email
        student_id = get_student.student_id
        await stream.send_message(Student(name=name, email=email, student_id=student_id))
        

    async def DeleteStudent(self, stream):
        request:DeleteStudentRequest = await stream.recv_message()
        student_id = request.student_id
        await Pupil.delete.where(Pupil.student_id == student_id).gino.status()
        await stream.send_message(empty_pb2.Empty())
        

    async def ListStudent(self, stream):
        request:ListStudentsRequest = await stream.recv_message()
        students = await Pupil.query.gino.all()
        data = []
        for i in students:
            data.append({
                'name':i.name,
                'email':i.email,
                'student_id':i.student_id


            })
        await stream.send_message(ListStudentsResponse(students=data))
       



async def main(*, host='127.0.0.1', port=50051):
    await db.set_bind('postgresql://root:123@localhost/main')
    await db.gino.create_all()
    server = Server([StudentService()])
    with graceful_exit([server]):
        await server.start(host, port)
        print(f'Serving on {host}:{port}')
        await server.wait_closed()


if __name__ == '__main__':
    asyncio.run(main())


