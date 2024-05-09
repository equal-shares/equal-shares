import Cookies from 'js-cookie';

import dotenv from 'dotenv';
dotenv.config();

const BASE_URL= process.env.REACT_APP_BASE_URL;

export class API {
    static getUserStatus(username)
    {
        return fetch(BASE_URL+"api/register/get_user_status/?username="+username,
        {
            method: 'GET',
            headers: 
            {
                'Content-Type': 'application/json',
            }
        })
        .then(resp => resp.json())
    }

    static studentOrOffice()
    {
        return fetch(BASE_URL+"api/student/student_or_office/",
        {
            method: 'GET',
            credentials: 'include',
            headers: 
            {
                'Content-Type': 'application/json',
            }
        })
        .then(resp => resp.json())
    }
    
    static getUserDetails()
    {
        return fetch(BASE_URL+"api/users/get_user_details/",
        {
            method: 'GET',
            credentials: 'include',
            headers: 
            {
                'Content-Type': 'application/json',
            }
        })
        .then(resp => resp.json())
    }

    static getStudentDetails(token)
    {
        return fetch(BASE_URL+"api/student/get_student_details/",
        {
            method: 'GET',
            credentials: 'include',
            headers: 
            {
                'Content-Type': 'application/json',
            }
        })
        .then(resp => resp.json())
    }

    static updateStudentDetails(body)
    {
        return fetch(BASE_URL+"api/student/update_student_details/",
        {
            method: 'POST',
            credentials: 'include',
            headers: 
            {
                'Content-Type': 'application/json',
                'X-CSRFToken': Cookies.get('csrftoken'),
            },
            body: JSON.stringify(body)
        })
        .then(resp => resp.json())
    }
    static getCourse_group()
    {
        return fetch(BASE_URL+"api/course_group/get_course_group/",
        {
            method: 'GET',
            credentials: 'include',
            headers: 
            {
                'Content-Type': 'application/json',
            }
        })
        .then(resp => resp.json())
    }

    static getCoursesA()
    {
        return fetch(BASE_URL+"api/courses/get_semester_a/",
        {
            method: 'GET',
            credentials: 'include',
            headers: 
            {
                'Content-Type': 'application/json',
            }
        })
        .then(resp => resp.json())
    }

    static getCoursesB()
    {
        return fetch(BASE_URL+"api/courses/get_semester_b/",
        {
            method: 'GET',
            credentials: 'include',
            headers: 
            {
                'Content-Type': 'application/json',
            }
        })
        .then(resp => resp.json())
    }

    static getLast_ranking()
    {
        return fetch(BASE_URL+"api/course_group/get_last_rating/",
        {
            method: 'GET',
            credentials: 'include',
            headers: 
            {
                'Content-Type': 'application/json',
            }
        })
        .then(resp => resp.json())
    }

    static studentRankingStatus()
    {
        return fetch(BASE_URL+"api/course_group/student_ranking_status/",
        {
            method: 'GET',
            credentials: 'include',
            headers: 
            {
                'Content-Type': 'application/json',
            }
        })
        .then(resp => resp.json())
    }

    static getTime()
    {
        return fetch(BASE_URL+"api/office/get_time/",
        {
            method: 'GET',
            credentials: 'include',
            headers: 
            {
                'Content-Type': 'application/json',
            }
        })
        .then(resp => resp.json())
    }
    static isClose()
    {
        return fetch(BASE_URL+"api/office/close_ranking/",
        {
            method: 'GET',
            credentials: 'include',
            headers: 
            {
                'Content-Type': 'application/json',
            }
        })
        .then(resp => resp.json())
    }
    static getDates()
    {
        return fetch(BASE_URL+"api/office/get_dates/",
        {
            method: 'GET',
            credentials: 'include',
            headers: 
            {
                'Content-Type': 'application/json',
            }
        })
        .then(resp => resp.json())
    }
    static MyStudents()
    {
        return fetch(BASE_URL+"api/office/my_students/",
        {
            method: 'GET',
            credentials: 'include',
            headers: 
            {
                'Content-Type': 'application/json',
            }
        })
        .then(resp => resp.json())
    }
    static MyCourses()
    {
        return fetch(BASE_URL+"api/office/my_courses/",
        {
            method: 'GET',
            credentials: 'include',
            headers: 
            {
                'Content-Type': 'application/json',
            }
        })
        .then(resp => resp.json())
    }
    
    static getResults()
    {
        return fetch(BASE_URL+"api/result/get_results/",
        {
            method: 'GET',
            credentials: 'include',
            headers: 
            {
                'Content-Type': 'application/json',
            }
        })
        .then(resp => resp.json())
    }

    static getResultsInfo()
    {
        return fetch(BASE_URL+"api/result/get_results_info/",
        {
            method: 'GET',
            credentials: 'include',
            headers: 
            {
                'Content-Type': 'application/json',
            }
        })
        .then(resp => resp.json())
    }

    static getAllocation()
    {
        return fetch(BASE_URL+"api/student/get_allocation/",
        {
            method: 'GET',
            credentials: 'include',
            headers: 
            {
                'Content-Type': 'application/json',
            }
        })
        .then(resp => resp.json())
    }

    static rank_courses(course_group)
    {
        return fetch(BASE_URL+"api/ranking/rank_courses/",
        {
            method: 'POST',
            credentials: 'include',
            headers: 
            {
                'Content-Type': 'application/json',
                'X-CSRFToken': Cookies.get('csrftoken'),
            },
            body: JSON.stringify( {ranks: course_group} )
        })
        .then(resp => resp.json())
    }

    static getQuestions()
    {
        return fetch(BASE_URL+"api/question/get_questions/",
        {
            method: 'GET',
            credentials: 'include',
            headers: 
            {
                'Content-Type': 'application/json',
            }
        })
        .then(resp => resp.json())
    }

    static getQ_A()
    {
        return fetch(BASE_URL+"api/question/get_questions_answers/",
        {
            method: 'GET',
            credentials: 'include',
            headers: 
            {
                'Content-Type': 'application/json',
            }
        })
        .then(resp => resp.json())
    }

    static SaveResultsFeedback(course_group)
    {
        return fetch(BASE_URL+"api/ranking/save_results_feedback/",
        {
            method: 'POST',
            credentials: 'include',
            headers: 
            {
                'Content-Type': 'application/json',
                'X-CSRFToken': Cookies.get('csrftoken'),
            },
            body: JSON.stringify( {ranks: course_group} )
        })
        .then(resp => resp.json())
    }
    
    static saveAnswers(course_group)
    {
        return fetch(BASE_URL+"api/question/save_answers/",
        {
            method: 'POST',
            credentials: 'include',
            headers: 
            {
                'Content-Type': 'application/json',
                'X-CSRFToken': Cookies.get('csrftoken'),

            },
            body: JSON.stringify( {ranks: course_group} )
        })
        .then(resp => resp.json())
    }

    static createStudents(jsonData)
    {
        return fetch(BASE_URL+"api/student/create_objects/",
        {
            method: 'POST',
            credentials: 'include',
            headers: 
            {
                'Content-Type': 'application/json',
                'X-CSRFToken': Cookies.get('csrftoken'),
            },
            body: JSON.stringify( {students: jsonData} )
        })
        .then(resp => resp.json())
    }
    static createCourses(jsonData)
    {
        return fetch(BASE_URL+"api/courses/create_objects/",
        {
            method: 'POST',
            credentials: 'include',
            headers: 
            {
                'Content-Type': 'application/json',
                'X-CSRFToken': Cookies.get('csrftoken'),
            },
            body: JSON.stringify( {courses: jsonData} )
        })
        .then(resp => resp.json())
    }
    
    static createDate(StartDate, EndDate, StartTime, EndTime)
    {
        return fetch(BASE_URL+"api/office/set_date/",
        {
            method: 'POST',
            credentials: 'include',
            headers: 
            {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify( {StartDate, EndDate, StartTime, EndTime} )
        })
        .then(resp => resp.json())
    }
    static doAlgo()
    {
        return fetch(BASE_URL+"api/office/algo/",
        {
            method: 'GET',
            credentials: 'include',
            headers: 
            {
                'Content-Type': 'application/json',
            }
        })
        .then(resp => resp.json())
    }
}