from backend.models import Course, CourseChunk, Lesson


def test_course_model_accepts_lessons():
    lesson = Lesson(lesson_number=1, title="Introduction", lesson_link="https://example.com/lesson")
    course = Course(
        title="RAG Fundamentals",
        course_link="https://example.com/course",
        instructor="Example Instructor",
        lessons=[lesson],
    )

    assert course.title == "RAG Fundamentals"
    assert course.lessons[0].lesson_number == 1


def test_course_chunk_defaults_optional_lesson_number():
    chunk = CourseChunk(
        content="Course text",
        course_title="RAG Fundamentals",
        chunk_index=0,
    )

    assert chunk.lesson_number is None
    assert chunk.chunk_index == 0
