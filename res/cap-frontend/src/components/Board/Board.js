import React from 'react';
import './Board.css';
import Checkbox from '../Feedback/Checkbox'

function Board(props) {

    const {course_group}= props;
    let balance = 1000 - course_group.reduce(function (prev, current) {
        return prev + +current.score
    }, 0);



    return (

        <div className='item-center' >
            {!props.feedback? <div className="justify-items-center item-center">
                <p className="ramainingTime">{props.time_message}</p>
                <div style={{ width: 'fit-content' }} className="alert alert-secondary item-center mb-2" role="alert">יתרת ניקוד: {balance}
                </div>
                <button data-testid="editButton" className="btn btn-lg btn-primary" onClick={props.EditClicked(balance)}>עריכה</button>
            </div>: 
                  <button className="btn btn-primary ml-2" onClick={props.SaveClicked(course_group)}>שמירת המשוב</button>

}

            <div className='course_group bg-light'>
                <div data-testid="card" className='whiteLines overflow-auto  item-center'>
                    {course_group.map((course, index) => {
                    return (
                        <div key={index} className={course.is_acceptable? 'item': 'item unacceptable'}>
                            <div className='item-title'>

                                <div className="i-name">

                                    <div data-testid="groupIndex" className='index ml-1 '>
                                    {props.feedback? <Checkbox course={course} i={index} change={props.changeCheckbox}/> : `${index + 1}.`}</div>
                                    {/*course.overlap && <div style={{color: 'red'}} data-testid="groupName">{course.name}</div>*/}
                                    {!course.overlap && <div data-testid="groupName" className='name ml-2 text-right'>{course.name}</div>}
                                </div>

                                <div className="money number">{course.score} נק'</div>

                            </div>
                            <div className='item-details'>
                                <div data-testid="groupName" className='lecturer'>{course.lecturer}</div>
                            </div>
                            <div className='d-flex'>
                            <div data-testid="groupName " className="ml-2" >סמסטר {course.semester}'</div>
                            <div className="mr-auto">{course.is_acceptable? '' : 'לא מוכן/ה לקחת'}</div>                            
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
                    )
                })}
                </div> </div>
        </div>
    );
}

export default Board