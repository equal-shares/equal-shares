import {Releases} from "./Releases"
import './About.css'
import {Github, EnvelopeAtFill,} from 'react-bootstrap-icons'
import Navbar from "../Navbar/Navbar";
import Cookies from 'js-cookie';

function About() {
  
    return (
        <div className="about">
            {Cookies.get('csrftoken')? <Navbar/> : null }
            <div className="container-fluid mt-2">
            <h1>אודות האתר</h1>
            <p>
                תהליך הרישום הנוכחי לקורסי בחירה מתנהל בשיטת "כל הקודם זוכה".
                </p>
            <p>         
                בעקבות בקשות רבות של סטודנטים, הוחלט בבית-הספר למדעי המחשב לנסות שיטה חדשה,
                שמטרתה להשיג חלוקה הוגנת של קורסים.
                </p>                
            <p>
                האתר הוקם כדי להדגים ולנסות את השיטה, על-מנת שנוכל להחליט בהמשך אם היא אכן טובה יותר מהשיטה הקיימת.
            </p>
            <br/>
              
                {Releases.map((item, index) => (
                    <div key={index}>
                    <h4>גרסא <b>{item.version}</b> {item.year}</h4>
                    <p>{`תיכנות: ${item.programmers}`}</p>
                    </div>
                ))}
                <div>
                    הנחיה: ד"ר אראל סגל-הלוי.
                </div>
                <br/>
                     <ul className="list-unstyled d-flex justify-content-center ">
                 <li className="ms-3"><a href='https://github.com/ariel-research' className="link-body-emphasis"><Github/></a></li>
                 <li className="ms-3"><a href='mailto:support@csariel.xyz' className="link-body-emphasis"><EnvelopeAtFill/>ariel-research23@gmail.com</a></li>
                 </ul>

            </div>
            {!Cookies.get('csrftoken')?
            <p className="text-center text-muted mt-5 mb-0"><a href="/"
            className="fw-bold text-body pr"><u>התחברו כאן!</u></a></p> 
            : null }
        </div>
    )

}
export default About;