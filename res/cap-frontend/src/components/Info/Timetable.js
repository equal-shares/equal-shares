import React from 'react';
import './Timetable.css';


function Timetable(props)
{
    const courses = props.course_group 

    return(
        <div>
            <div className="item-center">
                {courses && courses.map( (course,i) => {
                return (
                <div  key={i} data-testid="userCourseId">
                    {course.course_id}
                </div>
                )
            })}
            </div>
            <div className='overflow-x-scroll' >
            <table className="table table-bordered" border="2">
                <thead className='table-primary table-bordered' >
                    <tr style={{height: '20px'}}>
                        <th width="auto">שעה</th>
                        <th width="auto">ראשון</th>
                        <th width="auto">שני</th>
                        <th width="auto">שלישי</th>
                        <th width="auto">רביעי</th>
                        <th width="auto">חמישי</th>
                        <th width="auto">שישי</th>
                    </tr>
                </thead>
                <tbody style={{backgroundColor:'white'}}>
                {courses && courses.map( (hour,i) => {
                    if(hour[0].length === 0 && hour[1].length ===0 && hour[2].length ===0 && hour[3].length ===0 && hour[4].length ===0 && hour[5].length ===0)
                    {
                        return (
                            <tr key={i} style={{height:'25px', verticalAlign:'top'}}>
                                <th scope="row" className="w-2">{i+8}:00</th>
                                {hour && hour.map( (day,j) => {
                                return (
                                    <td key={j} style={{ verticalAlign:'top'}}>       
                                    </td>
                                )
                                })}
                                
                            </tr>
                        )
                    } else {
                        return (
                            <tr key={i} style={{height:'25px', verticalAlign:'top'}}> 
                            <th scope="row" className="w-2">{i+8}:00</th>
                                {hour && hour.map( (day,j) => {
                                    return (
                                    <td key={j} style={{ verticalAlign:'top'}}> 
                                    <div className='d-flex cell' >
                                            { day && day.length > 0 &&day.map( (course,k) => {
                                            return (
                                                <div key={k} className='border inner-cell'> 
                                                    {course.mandatory && <h6  style={{ verticalAlign:'top', backgroundColor: 'red'}}>
                                                        {course.course_group}<br/>  המרצה: {course.lecturer} <br/> שעות: {(course.time_start).substring(0, 5)}-{(course.time_end).substring(0, 5)}
                                                    </h6> }                                   
                                                    {!course.mandatory && <h6  style={{ verticalAlign:'top'}}> {course.mandatory}
                                                    <p className='fw-bold'> {course.course_group.name} {course.class_type? '- ' +course.class_type : ''} </p> {course.lecturer} <br/>{(course.time_start).substring(0, 5)}-{(course.time_end).substring(0, 5)}
                                                    </h6> }  
                                                </div>
                                            )
                                            })}
                                            </div>   
                                        
                                        
                                    </td>
                            )})}
                            </tr>
                        )
                    }
                })}
                </tbody>

           
            </table>
            </div>
        </div>
        
        
        
    );
}

export default Timetable