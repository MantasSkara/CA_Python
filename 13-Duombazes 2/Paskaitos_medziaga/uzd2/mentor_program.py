from typing import Sequence

from db_init import init_session, close_session
from mentor import Mentor
from worker import Worker


def add_worker(name, surname, position):
    session = init_session()
    session.add(Worker(name, last_name=surname, position=position))
    session.commit()
    close_session()


def set_mentor(mentor_id: int, student_id: int):
    session = init_session()
    session.add(Mentor(mentor_id, student_id))
    session.commit()
    close_session()


def get_mentor_info(mentor_name, mentor_surname) -> Sequence[dict]:
    session = init_session()
    mentor = session.query(Worker).filter(Worker.name == mentor_name).filter(
        Worker.last_name == mentor_surname).all()[0]
    mentor_id = mentor.id
    mentorships = session.query(Mentor).filter(Mentor.mentor_id == mentor_id).all()

    student_list = [get_student_by_id(session, mentorship.student_id) for mentorship in mentorships]
    results = [_form_results_from_student_and_mentor(student, mentor) for student in student_list]

    close_session()

    return results


def get_student_by_id(session, id):
    return session.query(Worker).filter(Worker.id == id).first()


def _form_results_from_student_and_mentor(student, mentor):
    return {
        'mentor_name': mentor.name,
        'mentor_surname': mentor.last_name,
        'student_name': student.name,
        'student_surname': student.last_name,
        'student_position': student.position
    }
