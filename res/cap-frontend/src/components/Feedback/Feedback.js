import React, { useState, useEffect } from 'react';
import "../Ranking/Ranking.css"
import Board from "../Board/Board";
import Navbar from "../Navbar/Navbar";
import { API } from "../../api/api-service";



function Feedback(props) {
   
    const [ranking_end, setRanking_end] = useState(false);
    const [course_group, setCourse_group] = useState([]);
    const [email,setEmail] = useState('')
    const [status,setStatus] = useState(true)

    useEffect(() => {
        API.getTime()
            .then(resp => {
                setRanking_end(resp['feedback'])
            })
            .catch(error => console.log(error))
        
        API.studentRankingStatus()
        .then(resp => {
            if (!resp)
                setStatus(false)
            else
                setCourse_group(resp)})
        .catch(error => console.log(error))

        API.getStudentDetails()
        .then(resp => setEmail(resp['user']['email']))
        .catch(error => console.log(error))
    }, [])


    const changeCheckbox = (is_checked,i) => {      
        const updatedCourseGroup = Array.from(course_group); 
        updatedCourseGroup[i].result = is_checked;
        setCourse_group(updatedCourseGroup);
    }

    const SaveClicked = (course_group) => async (evt) => {
            API.SaveResultsFeedback(course_group)
                .then(resp => {
                    alert("תודה על מילוי המשוב!")
                })
                .catch(error => console.log(error))
            
    }

    return (
        <div className="Rank" data-testid="Rank">
    <Navbar active='משוב' />
    <div className='text text-center '>
        <h1 className='Headline'>משוב שיבוצים</h1>
        
        <h4 className='text-center'>אנא השיבו על שני חלקי המשוב: שאלון וסימון הקורסים</h4>

        <div className=" justify-content-center">
            <ul className="nav nav-tabs justify-content-center" id="myTabs">
                <li className="nav-item" role="presentation">
                    <a className="nav-link active" id="survey-tab" data-bs-toggle="tab" href="#survey" role="tab" aria-controls="survey" aria-selected="true">שאלון</a>
                </li>
                <li className="nav-item" role="presentation">
                    <a className="nav-link" id="feedback-tab" data-bs-toggle="tab" href="#feedback" role="tab" aria-controls="feedback" aria-selected="false">סימון קורסים</a>
                </li>
            </ul>
            <div className="tab-content" id="myTabsContent">
                <div className="tab-pane fade show active" id="survey" role="tabpanel" aria-labelledby="survey-tab">
                <div className='container-rank item-center'>
                    <iframe title="survey" className="iframe" src={`https://docs.google.com/forms/d/e/1FAIpQLSfJbjvgR8bv3-iGhkOD8CBqIhGuQCU_lfu7znoa8UZbbdUI9w/viewform?usp=pp_url&entry.348055013=${email}&embedded=true`}
                        width="100%" height= "766" frameBorder="0" marginHeight="0" marginWidth="0">בטעינה…</iframe>
                </div>
                </div>
                <div className="tab-pane fade" id="feedback" role="tabpanel" aria-labelledby="feedback-tab">
                    <h2 className='text-center mt-5'><b>סמנו את הקורסים שאליהם נרשמתם</b></h2>
                    <h4 className='text-center'>(דרך המידע האישי של האוניברסיטה)</h4>

                    <div className='container-rank item-center'>
                        {ranking_end ? (
                            status?
                            <Board course_group={course_group} setCourse_group={setCourse_group} changeCheckbox={changeCheckbox} feedback={true} SaveClicked={SaveClicked} />
                            : 
                            'סימון הקורסים זמין עבור סטודנטים שדירגו את הקורסים'
                            ) : (
                            'מילוי המשוב יהיה זמין לאחר הדירוג'
                        )}
                    </div>
                </div>
            </div>
        </div>
           
    </div>
</div>
    )
}


export default Feedback;