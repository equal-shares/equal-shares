import React from 'react'

function CourseGroupDetails(props) {
    return (
        <div>
            {props.course_group ? (
                <div>{props.course_group.courses.map((course, i) => {
                    return (
                        <ol className="list-group" data-testid="courseDetails" key={course.course_id}>
                            <li className="list-group-item d-flex justify-content-between align-items-start course-option" >
                                <div className=" align-text-right courses">
                                    <div className="fw-bold">{props.course_group.name}</div>
                                    <div className="fw-bold" data-testid={`courseOption${i}`}>קבוצה {i + 1}</div>
                                    <div data-testid={`teacherName${i}`}> המרצה: {course.lecturer}</div>
                                    <div data-testid={`courseSemester${i}`}>סמסטר: {course.Semester}</div>
                                    <div>שעות: {course.time_start}-{course.time_end}</div>
                                </div>
                                <span className="badge bg-primary rounded-pill">{course.capacity}</span>
                            </li>
                        </ol>

                    )
                })}</div>
            ) : null}
        </div>
    )
}

export default CourseGroupDetails