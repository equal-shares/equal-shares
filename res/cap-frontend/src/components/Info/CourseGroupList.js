import React, { useState } from 'react';
import CourseGroupDetails from './CourseGroupDetails';
import './CoursesInfo.css';

function CourseGroupList(props) {
  const [showModal, setShowModal] = useState(false);
  const [selectedCourseGroup, setSelectedCourseGroup] = useState(null);

  const course_groupClicked = (course_group) => {
    setSelectedCourseGroup(course_group);
    setShowModal(true);
  };

  return (
    <div className='overflow-auto list-scroll item-center'>
      {props.course_group &&
        props.course_group.map((course_group) => (
          <div key={course_group.id} className="list-group course-list">
            <button
              type="button"
              data-testid="courseGroup"
              className="list-group-item list-group-item-action"
              onClick={() => course_groupClicked(course_group)}
              aria-current="true"
              data-bs-toggle="modal"
              data-bs-target="#exampleModal"
            >
              {course_group.name}
            </button>
          </div>
        ))}
      

      
        <div
          className={`modal fade ${showModal ? 'show' : ''}`}
          id="exampleModal"
          tabIndex="-1"
          aria-labelledby="exampleModalLabel"
          aria-hidden="true"
          style={{ display: showModal ? 'block' : 'none' }}
        >
          <div className="modal-dialog modal-dialog-centered modal-dialog-scrollable">
            <div className="modal-content modal-fc">
              <div className="modal-header d-flex justify-content-between">
                
                <h1 className="modal-title fs-5" id="exampleModalLabel">
                  פרטי הקורס
                </h1>
                <button
                  type="button"
                  className="btn-close mr-auto"
                  data-bs-dismiss="modal"
                  aria-label="Close"
                  onClick={() => setShowModal(false)}
                ></button>
              </div>
              <div className="modal-body">
                {selectedCourseGroup && (
                <CourseGroupDetails course_group={selectedCourseGroup} />)}
              </div>

            </div>
          </div> 
          
        </div>
     
    </div>
  );
}

export default CourseGroupList;
