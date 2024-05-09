import React, { useState, useEffect } from 'react';
import BoardEditable from "../Board/BoardEditable";
import "./Ranking.css"
import Board from "../Board/Board";
import Navbar from "../Navbar/Navbar";
import { API } from "../../api/api-service";

function Ranking(props) {
    const [edit, setEdit] = useState(false);
    const [course_group, setCourse_group] = useState([]);
    const [origin_course_group, setOriginCourseGroup] = useState(null)
    const [balance, setBalance] = useState();
    const [time_message, setTime_message] = useState("");
    const [ranking_start, setRanking_start] = useState(false);

    useEffect(() => {
        API.getTime()
            .then(resp => {
                setTime_message(resp['message'])
                setRanking_start(resp['value'])
            })
            .catch(error => console.log(error))
    },  [time_message])

    useEffect(() => {
        API.getLast_ranking()
            .then(resp => {setCourse_group(resp)
                setOriginCourseGroup(JSON.parse(JSON.stringify(resp)));})
            .catch(error => console.log(error))
    }, [])

    const EditClicked = b => evt => {
        if (ranking_start) {
            setEdit(true);
            setBalance(b);
        }
        else
            alert("ההרשמה סגורה");
    }
    function timeout(delay) {
        return new Promise(res => setTimeout(res, delay));
    }
    const SaveClicked = (course_group, bal) => async (evt) => {
        if (bal === 0) {
            API.rank_courses(course_group)
                .then(resp => console.log(resp))
                .catch(error => console.log(error))
            await timeout(1000);
            setEdit(false);
        }
        else
            alert("סכום הנקודות שנותר חייב להיות בדיוק 0");

    }


    return (
        <div className="Rank" data-testid="Rank">
            <Navbar active='דירוג הקורסים' />
            <div className='text text-center '>
                <h1 className='Headline' >דירוג הקורסים</h1>
                <div className=" justify-content-center">
                    <div className="accordion mt-2 " id="accor-how">
                        <div className="accordion-item">
                            <h2 className="accordion-header" id="headingOne">
                                <button className="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#collapseOne" aria-expanded="true" aria-controls="collapseOne">
                                    איך מדרגים?
                                </button>
                            </h2>
                            <div id="collapseOne" className="accordion-collapse collapse" aria-labelledby="headingOne" data-bs-parent="#accor-how">
                                <div className="accordion-body">
                                    <ul>
                                       <li>לחצו על "עריכה" על מנת להתחיל בדירוג.</li>
                                       <li>החליטו איזה קורסים אתם מוכנים לקחת, סמנו אותם ב-V  ומחקו את הסימון מהקורסים שאתם לא מוכנים לקחת.</li>
                                       <li>גררו וסדרו את הקורסים שאתם מוכנים לקחת לפי סדר העדיפות שלכם - שימו למעלה את הקורסים שאתם הכי רוצים. </li>
                                       <li>חלקו את 1000 הנקודות שלכם בין הקורסים שאתם מוכנים לקחת - תנו יותר נקודות לקורסים שאתם רוצים יותר.</li>
                                       <li>ניתן להשתמש בחיצי המקלדת לניקוד מדויק יותר.</li>
                                       <li>לאחר שסיימתם, לחצו על "שמירת הדירוג".</li>
                                    </ul>
                                    <div className='text-right fw-bold'></div>
                                </div>
                            </div>
                        </div>
                    </div>
                    <div className="accordion" id="accor-danger">
                        <div className="accordion-item accordion-danger">
                            <h2 className="accordion-header" id="headingTwo">
                                <button className="accordion-button collapsed accordion-danger" type="button" data-bs-toggle="collapse" data-bs-target="#collapseTwo" data-bs-parent="#accor-danger" aria-expanded="true" aria-controls="collapseTwo">
                                    שימו לב
                                </button>
                            </h2>
                            <div id="collapseTwo" className="accordion-collapse collapse " aria-labelledby="headingTwo" data-bs-parent="#accor-danger">
                                <div className="accordion-body">
                                    <ul>
                                        <li>אם לא סימנתם  V  ליד "מוכן/ה לקחת", לא תקבלו את הקורס בשום מקרה - גם אם לא יישאר מקום בקורסים אחרים. </li>
                                        <li>בעת שמירת הדירוג, יתרת הדירוג חייבת לעמוד על 0 נקודות בדיוק.</li>
                                    </ul>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                <div className='container-rank item-center'>

                    {!edit ?
                        <Board course_group = {course_group} setCourse_group = {setCourse_group} EditClicked={EditClicked} time_message={time_message} />

                        :
                        <BoardEditable course_group = {course_group} setCourse_group = {setCourse_group} origin={origin_course_group} setEdit={setEdit} SaveClicked={SaveClicked} time_message={time_message} balance={balance} />
                    }

                </div>
            </div>
        </div>
    )
}


export default Ranking;