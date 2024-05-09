import React, { useState, useEffect, useCallback } from 'react';
import './Board.css';
import Slider from './slider';
import Checkbox from './Checkbox'
//import Switch from './Switch'

import { DragDropContext, Droppable, Draggable } from 'react-beautiful-dnd';
import { usolve } from "mathjs"

function BoardEditable(props) {
  const {course_group, setCourse_group}= props;
  const origin_course_group= props.origin
  const [balance, setBalance] = useState(props.balance);
  const original_balance = props.balance
  //let student_details = JSON.parse(localStorage.getItem('student_details'));
  const [num_options, setNumOptions] = useState(0);
  const [num_courses_acceptable, setNumCoursesAcceptable] = useState(0)
  const [initializationDone, setInitializationDone] = useState(false); // New state variable
  const MAX_POINTS = 1000;  

  
  const getNumAcceptableCourses = useCallback(() => { 
    return course_group.reduce((accumulator, currentValue) => {
      return  currentValue.is_acceptable? accumulator + 1 : accumulator 
     },0)
  },[course_group])




  const suggestClicked = (event) => {
    const options = Number(num_options);
    const selectedOption = event.target.value;
    const updatedCourseGroup = Array.from(course_group);
    const partition = (i, weight) => {
      weight = parseInt(weight)
      updatedCourseGroup[i].score = weight
    }
    
    if (selectedOption === 'e') { //equal partition

      let weight = MAX_POINTS / num_courses_acceptable;
      for (let i = 0; i < options; i++) {
        if (updatedCourseGroup[i].is_acceptable)
          partition(i, weight);
      }
    }
    else if (selectedOption === 'o') { //partition by list order

      let factor = (num_courses_acceptable * 0.5) * (num_courses_acceptable + 1);
      const a = [[factor]];
      const b = [MAX_POINTS];
      const x = usolve(a, b)[0][0];
      let i_partition = 0;
      for (let i=0; i<options; i++){
        if (updatedCourseGroup[i].is_acceptable){
          const weight = x * (num_courses_acceptable - i_partition)
          partition(i, weight);
          i_partition++;
        }
      }
    }
    else if (selectedOption === 'z') { //reset all scores
      for (let i = 0; i < options; i++) {
        partition(i, 0);
      }
    }
    
    const temp_balance = (MAX_POINTS - updatedCourseGroup.reduce(function (prev, current) {
      return prev + +current.score
    }, 0))
    console.log("course:",course_group)

    setCourse_group(updatedCourseGroup);
    setBalance(temp_balance)
    console.log("orignal:",origin)

  };


  const handleDragEnd = (result, disabled=true) => {
    if (!result.destination) return; // Not a valid drop target
    const { source, destination } = result;
    const updatedCourseGroup = Array.from(course_group);

    // Reorder the course cards
    const [removed] = updatedCourseGroup.splice(source.index, 1);
    updatedCourseGroup.splice(destination.index, 0, removed);
    // Update the state with the new order
    setCourse_group(updatedCourseGroup);

  };

  const changeCheckbox = (is_checked,i) => {      
    const updatedCourseGroup = Array.from(course_group); 
    
    updatedCourseGroup[i].is_acceptable = is_checked;
    if (!is_checked){   
      setBalance(balance+updatedCourseGroup[i].score)
      updatedCourseGroup[i].score = 0;
      setNumCoursesAcceptable(num_courses_acceptable-1);
    }
    else{
      setNumCoursesAcceptable(num_courses_acceptable+1);
    }
    setCourse_group(updatedCourseGroup);


  }
  const changeSlide = (v, i) => {
    course_group[i].score = Number(v)
    setBalance(MAX_POINTS - course_group.reduce(function (prev, current) {
      return prev + +current.score
    }, 0))
    
  }
  
  const handleCancel = () => {
    console.log(origin)
    setCourse_group(JSON.parse(JSON.stringify(origin_course_group)));
    setBalance(original_balance)
    props.setEdit(false)
    
  }

  useEffect(() => {
    if (course_group.length>0 && !initializationDone) { // Check if initialization is done
      setNumOptions(course_group.length);
      setNumCoursesAcceptable(getNumAcceptableCourses());
      setInitializationDone(true); // Set the flag to true after initialization
    }
  }, [course_group,initializationDone,getNumAcceptableCourses]);


  return (

    <div className='item-center' >
      <div className="justify-items-center item-center">
        <p className="ramainingTime">{props.time_message}</p>
        <div style={{ width: 'fit-content' }} className="alert alert-secondary item-center mb-2" role="alert">יתרת ניקוד: {balance}</div>
      </div>
      <button className="btn btn-primary ml-2" onClick={props.SaveClicked(course_group, balance)}>שמירת הדירוג</button>
      <button className="btn btn-secondary " onClick={() => handleCancel()}>ביטול</button>

      <div className="rowC justify-content-center container-fluid mt-3">
        <div>
          <div className="btn-group" role="group" aria-label="Basic outlined example" onClick={suggestClicked}>
            דוגמאות לניקוד: &nbsp;&nbsp;&nbsp;
            <button type="button" value="o" className="btn btn-outline-primary" >חלוקה לפי הסדר</button>
            <button type="button" value="e" className="btn btn-outline-primary" >חלוקה שווה</button>
            <button type="button" value="z" className="btn btn-outline-primary" >איפוס הכל</button>
          </div>
        </div>
      </div>
      
      <div className='course_group bg-light'>
        <DragDropContext onDragEnd={handleDragEnd}>
          <Droppable droppableId="course-group">
            {(provided) => (
              <div
                ref={provided.innerRef}
                {...provided.droppableProps}
                data-testid="card" className='whiteLines overflow-auto  item-center'
              >
                {course_group.map((course, index) => (
                  <Draggable
                    key={index}
                    draggableId={`course-${index}`}
                    index={index}
                    
                  >
                    {(provided) => (
                      <div
                        ref={provided.innerRef}
                        {...provided.draggableProps}
                        {...provided.dragHandleProps}
                        className={course.is_acceptable? 'item': 'item unacceptable'}
                      >
                        <div className="item-title">
                          <div className="i-name">

                            <div data-testid="groupIndex" className='index ml-1 '>{index + 1}.</div>
                            {/*course.overlap && <div style={{color: 'red'}} data-testid="groupName">{course.name}</div>*/}
                            {!course.overlap && <div data-testid="groupName" className='name ml-2 text-right'>{course.name}</div>}
                          </div>
                          {<Slider course={course} i={index} balance={balance} change={changeSlide}/>}
                          
                        </div>
                        <div className='item-details'>
                                <div data-testid="groupName" className='lecturer'>{course.lecturer}</div>
                            </div>
                            <div className='d-flex'>
                            <div data-testid="groupName " className="ml-2" >סמסטר {course.semester}'</div>
                            <div className="mr-auto">{<Checkbox course={course} i={index} change={changeCheckbox} />}</div>
                            </div>
                            <div className='d-flex'>
                                
                                <div data-testid="groupName " className="ml-2">יום {course.day}'</div>
                                <div data-testid="groupName">{(course.time_start).substring(0, 5)}-{(course.time_end).substring(0, 5)}</div>
                            </div>
                            
                            {course.course_time? (
                                course.course_time.map((time,i_time) => (
                                    <div className='d-flex' key={i_time}>
                                        <div data-testid="groupName " className="ml-2">יום {time.day}'</div>
                                        <div data-testid="groupName">{(time.time_start).substring(0, 5)}-{(time.time_end).substring(0, 5)}</div>
                                    </div>
                                ))): null }
                               
                        </div>
                        
                    )}
                  </Draggable>
                ))}
                {provided.placeholder}
              </div>
            )}
          </Droppable>
        </DragDropContext>

      </div>

    </div>
  );
}

export default BoardEditable