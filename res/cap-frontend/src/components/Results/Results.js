import React, { useState, useEffect} from 'react';
import Navbar from "../Navbar/Navbar";
import TextArea from "./TextArea"
import { API } from "../../api/api-service";
import './Results.css'

function Results(props)
{
    const [courses, setCourses] = useState([]);
    const [courses_txt, setCoursesTxt] = useState('');
    const [explanation, setExplanation] = useState('');

    useEffect(() => {
        API.getResultsInfo()
        .then(resp => {
            setCoursesTxt(resp.courses_txt)
            setExplanation(resp.explanation)
        })
    },[])

    if(courses.length === 0)
    {
        return(
            <div className="Rank">
                <Navbar active='תוצאות'/>
                <h1 className='Headline'>קורסי הבחירה שקיבלת הם:</h1>
                <div className='container-rank item-center'>
                    <div className='course_group'>
                       
                        <div className='whiteLines'>
                            <div className='item' >
                                { courses_txt?
                                    <div>
                                        
                                        <TextArea title='קורסי הבחירה שקבלת' text={courses_txt} rows='10'/>
                                        <TextArea title='הסבר תהליך האלגוריתם' text={explanation} rows='15'/>
                                    </div>
                                    : <div style={{marginLeft:'40%'}}>אין עדין תוצאות </div>
                                }
                            </div>
                        </div>
                    </div>
                </div>        
            </div>
        )
    }
    else
    {
        return(
            <div className="Rank">
                <Navbar active='תוצאות'/>
                <p className="results"> תוצאות </p>
                <div className='container-rank' >
                    <div className='course_group'>
                        <h1 style={{marginLeft:'10%'}}>הקורסים אליהם שובצת</h1>
                        <div className='whiteLines'>
                            { courses.map((course, index) => {
                            return (
                                <div key={index} className='item'>
                                    <div className='item-title'>
                                        <div className="money"> הדירוג שלך: {course.rank}</div>
                                        <div className='name'>{course.course_group}</div>
                                        <div className='index'>.{index+1}</div>
                                    </div>
                                    <div className='item-details'>
                                        <div> ביום: {course.day} בשעות: {(course.time_start).substring(0, 5)}-{(course.time_end).substring(0, 5)}</div>
                                        <div> סמסטר: {course.Semester}</div>
                                        <div> מרצה: {course.lecturer}</div>
                                    </div>
                                </div>
                                )
                            })}
                        </div>
                    </div>
                </div>        
            </div>
        )
    }
    
}

export default Results;