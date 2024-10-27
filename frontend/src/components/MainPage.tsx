import { ChangeEvent, useCallback, useEffect, useState } from 'react';

import {
  Button,
  ButtonGroup,
  Container,
  Typography,
  Accordion,
  AccordionSummary,
  AccordionDetails,
  Alert,
  Input,
} from '@mui/material';
import { ExpandMore as ExpandMoreIcon } from '@mui/icons-material';
import { toast } from 'react-toastify';

import { DataResponse, Project } from '../schemas';
import { postDataRequest, postVoteRequest } from '../api';
import ProjectCard from './ProjectCard';

import logoImage from '../assets/logo.png';
import Results from './Results';

const TOAST_ID_MAX_POINTS = 'max-points';

function sortedProjects(projects: Project[]): Project[] {
  return projects.sort((a, b) => a.rank - b.rank);
}

export type Props = {
  email: string;
  token: string;
};

export default function MainPage({ email, token }: Props) {
  const [voted, setVoted] = useState<boolean>(false);
  const [maxTotalPoints, setMaxTotalPoints] = useState<number>(1);
  const [pointsStep, setPointsStep] = useState<number>(1);
  const [openForVoting, setOpenForVoting] = useState<boolean>(true);
  const [note, setNote] = useState<string>('');
  const [result, setResult] = useState<{ [key: number]: number } | null>(null);
  const [projects, setProjects] = useState<Project[]>([]);

  const [sendingRequest, setSendingRequest] = useState<boolean>(false);

  const availablePoints = projects.reduce((acc, project) => acc - project.points, maxTotalPoints);

  const markedProjects = projects.filter((project) => project.marked);
  const unmarkedProjects = projects.filter((project) => !project.marked);

  const resetVote = useCallback(() => {
    setSendingRequest(true);
    postDataRequest(email, token)
      .then((data: DataResponse) => {
        setVoted(data.voted);
        setMaxTotalPoints(data.max_total_points);
        setPointsStep(data.points_step);
        setOpenForVoting(data.open_for_voting);
        setResult(data.results);
        setNote(data.note);
        setProjects(data.projects);
        setSendingRequest(false);
      })
      .catch(() => {
        toast.error('אירעה שגיאה בטעינת הדירוג');
        setSendingRequest(false);
      });
  }, [email, token]);

  useEffect(() => {
    resetVote();
  }, [resetVote]);

  const pointsSliderOnChange = (project: Project, value: number | number[]) => {
    if (project.fixed) {
      return;
    }

    if (typeof value !== 'number') {
      return;
    }

    value = Math.min(project.max_points, value);
    value = Math.max(project.min_points, value);

    if (availablePoints + project.points - value < 0) {
      value = project.points + availablePoints;
      toast('נגמר התקציב, כדי להוסיף הורד מפרוייקט אחר', {
        type: 'error',
        toastId: TOAST_ID_MAX_POINTS,
      });
    }

    project.points = Math.round(value / pointsStep) * pointsStep;
    project.points_text = project.points.toString();
    setProjects(sortedProjects([...projects]));
  };

  const pointsBoxOnChange = (project: Project, textValue: string) => {
    if (project.fixed) {
      return;
    }

    project.points_text = textValue;

    const value = parseInt(project.points_text, 10);

    if (!isNaN(value) && project.min_points <= value && value <= project.max_points) {
      if (project.points + availablePoints < value) {
        toast('נגמר התקציב, כדי להוסיף הורד מפרוייקט אחר', {
          type: 'error',
          toastId: TOAST_ID_MAX_POINTS,
        });
      }

      project.points = Math.min(value, project.points + availablePoints);
      project.points_text = project.points.toString();
    }

    setProjects(sortedProjects([...projects]));
  };

  const pointsBoxOnBlur = (project: Project) => {
    if (project.fixed) {
      return;
    }

    project.points = Math.round(project.points / pointsStep) * pointsStep;
    project.points_text = project.points.toString();
    setProjects(sortedProjects([...projects]));
  };

  const markedOnChange = (project: Project) => {
    if (project.fixed) {
      return;
    }

    if (!project.marked) {
      if (availablePoints - project.min_points < 0) {
        toast('אין מספיק יתרת תקציב להסיף את הפרוייקט הזה, הסר מפרוייקט אחר', {
          type: 'error',
          toastId: TOAST_ID_MAX_POINTS,
        });
        return;
      }
    }

    project.marked = !project.marked;
    project.points = project.marked ? project.min_points : 0;
    project.points_text = project.points.toString();

    project.points_text = project.points.toString();

    const markedProjects = projects.filter((project) => project.marked);
    const unmarkedProjects = projects.filter((project) => !project.marked);

    const newProjects = [...markedProjects, ...unmarkedProjects].map((project, index) => {
      project.rank = index + 1;
      return project;
    });

    setProjects(sortedProjects([...newProjects]));
  };

  const resetVoteOnClick = () => {
    if (sendingRequest) {
      return;
    }

    resetVote();
  };

  const saveOnClick = () => {
    if (sendingRequest) {
      return;
    }

    const toastId = toast.loading('שומר את הדירוג...', { type: 'info', position: 'top-center' });

    setSendingRequest(true);
    postVoteRequest(email, token, {
      note,
      projects: sortedProjects(projects).map((project) => ({
        id: project.id,
        rank: project.rank,
        points: project.points,
        marked: project.marked,
      })),
    }).then((data) => {
      toast.update(toastId, {
        render: 'הדירוג נשמר בהצלחה!',
        type: 'success',
        position: 'top-center',
        autoClose: 5000,
        isLoading: false,
      });
      setVoted(data.voted);
      setMaxTotalPoints(data.max_total_points);
      setPointsStep(data.points_step);
      setOpenForVoting(data.open_for_voting);
      setNote(data.note);
      setProjects(data.projects);
      setSendingRequest(false);
    });
  };

  return (
    <Container component="main" maxWidth={false}>
      <div className="justify-items-center item-center max-w-[90vw]">
        <Typography className="text-center" variant="h3" component="h1" gutterBottom>
          דירוג פרוייקטים
        </Typography>
        <div className="w-full h-[300px] flex justify-center">
          <img
            className="w-[150px] h-[150px] my-[75px]"
            src={logoImage}
            alt="Logo"
            width={150}
            height={150}
          />
        </div>
        {!openForVoting && (
          <>
            <div className="w-full mt-[10px] flex justify-center">
              <Alert className="w-fit" severity="info">
                הדירוג סגור כרגע
              </Alert>
            </div>
            {result !== null && <Results data={result} projects={projects} />}
          </>
        )}
        {openForVoting && (
          <>
            <Accordion>
              <AccordionSummary expandIcon={<ExpandMoreIcon />}>איך מדרגים?</AccordionSummary>
              <AccordionDetails>
                <ul className="list-disc px-[20px]">
                  <li>לחצו על "עריכה" על מנת להתחיל בדירוג.</li>
                  <li>
                    החליטו איזה פרויקטים אתם מוכנים לקחת, סמנו אותם ב-V ומחקו את הסימון מהפרויקטים
                    שאתם לא מעוניינים לקחת.
                  </li>
                  <li>
                    חלקו את התקציב שלכם בין הפרויקטים שאתם מוכנים לקחת - תנו יותר כסף לפרויקטים שאתם
                    רוצים יותר. ניתן להשתמש בחיצי המקלדת לניקוד מדויק יותר.
                  </li>
                  <li>לאחר שסיימתם, לחצו על "שמירת הדירוג".</li>
                </ul>
              </AccordionDetails>
            </Accordion>
            <Accordion>
              <AccordionSummary expandIcon={<ExpandMoreIcon />}>שימו לב</AccordionSummary>
              <AccordionDetails>
                <ul className="list-disc px-[20px]">
                  <li>אם לא סימנתם V, לא יחושב הפרויקט בחלוקת התקציב שלכם.</li>
                  <li>בעת שמירת הדירוג, יתרת התקציב חייבת לעמוד על 0 בדיוק.</li>
                </ul>
              </AccordionDetails>
            </Accordion>
            <div className="w-full mt-[5px] flex justify-center">
              <Alert className="w-fit" severity="info">
                יתרת תקציב: {availablePoints}
              </Alert>
            </div>
            <div className="w-full mt-[10px] flex justify-center">
              <ButtonGroup variant="outlined" dir="ltr">
                <Button onClick={resetVoteOnClick}>איפוס הכל</Button>
              </ButtonGroup>
            </div>
            <div>
              {markedProjects.map((project) => (
                <div key={project.id}>
                  <ProjectCard
                    project={project}
                    pointsStep={pointsStep}
                    pointsSliderOnChange={pointsSliderOnChange}
                    pointsBoxOnChange={pointsBoxOnChange}
                    pointsBoxOnBlur={pointsBoxOnBlur}
                    markedOnChange={markedOnChange}
                  />
                </div>
              ))}
              {unmarkedProjects.length > 0 && (
                <>
                  <div className="mt-[30px]"></div>
                  {unmarkedProjects.map((project) => (
                    <div key={project.id}>
                      <ProjectCard
                        project={project}
                        pointsStep={pointsStep}
                        pointsSliderOnChange={pointsSliderOnChange}
                        pointsBoxOnChange={pointsBoxOnChange}
                        pointsBoxOnBlur={pointsBoxOnBlur}
                        markedOnChange={markedOnChange}
                      />
                    </div>
                  ))}
                </>
              )}
            </div>
            <div className="mt-[10px] flex justify-center items-center">
              <div className="w-[500px]">
                <Input
                  fullWidth
                  multiline
                  minRows={2}
                  placeholder="הערות"
                  value={note}
                  onChange={(e: ChangeEvent<HTMLInputElement>) => setNote(e.target.value)}
                />
              </div>
            </div>
            <div className="mt-[10px] flex justify-center">
              <Button
                color="primary"
                variant="contained"
                onClick={saveOnClick}
                disabled={sendingRequest || availablePoints < 0}>
                {voted ? 'עדכון הדירוג' : 'שלח הדירוג'}
              </Button>
            </div>
          </>
        )}
      </div>
    </Container>
  );
}
