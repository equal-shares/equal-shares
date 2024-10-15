import {
  Typography,
  Card,
  CardContent,
  Grid,
  Slider,
  Input,
  Checkbox,
  Accordion,
  AccordionDetails,
  AccordionSummary,
} from '@mui/material';
import { Menu as MenuIcon, ExpandMore as ExpandMoreIcon } from '@mui/icons-material';

import { Project } from '../schemas';

export type ProjectCardProps = {
  project: Project;
  pointsStep: number;
  pointsSliderOnChange: (project: Project, value: number | number[]) => void;
  pointsBoxOnChange: (project: Project, textValue: string) => void;
  pointsBoxOnBlur: (project: Project) => void;
  markedOnChange: (project: Project) => void;
  setDragDisabled: (disabled: boolean) => void;
};

export default function ProjectCard({
  project,
  pointsStep,
  pointsSliderOnChange,
  pointsBoxOnChange,
  pointsBoxOnBlur,
  markedOnChange,
  setDragDisabled,
}: ProjectCardProps) {
  return (
    <Card className="my-[4px]" sx={{ boxShadow: 3 }}>
      <CardContent>
        <Grid container spacing={2}>
          <Grid item xs={1}>
            {!project.fixed && (
              <div className="h-full flex justify-content">
                <div className="h-fit my-auto">
                  <MenuIcon />
                </div>
              </div>
            )}
          </Grid>
          <Grid item xs={11}>
            <Typography variant="h6" component="p">
              <span className="ml-[10px]">
                {project.fixed ? (
                  <Checkbox checked disabled />
                ) : (
                  <Checkbox checked={project.marked} onChange={() => markedOnChange(project)} />
                )}
              </span>
              {project.rank}. {project.name}
            </Typography>
            <div>
              <Grid container spacing={2} alignItems="center">
                <Grid item md={8} xs={12}>
                  <div
                    className="w-[85%] pr-[15%]"
                    onMouseEnter={() => setDragDisabled(true)}
                    onMouseLeave={() => setDragDisabled(false)}>
                    <Slider
                      value={project.points}
                      min={project.min_points}
                      max={project.max_points}
                      step={pointsStep}
                      marks={[
                        {
                          value: project.min_points,
                          label: project.min_points.toString(),
                        },
                        {
                          value: project.max_points,
                          label: project.max_points.toString(),
                        },
                      ]}
                      disabled={!project.marked || project.fixed}
                      onChange={(_, value) => pointsSliderOnChange(project, value)}
                    />
                  </div>
                </Grid>
                <Grid item md={4} xs={12}>
                  <Input
                    value={project.points_text}
                    size="small"
                    sx={{ input: { textAlign: 'center' } }}
                    inputProps={{
                      step: pointsStep,
                      min: project.min_points,
                      max: project.max_points,
                      type: 'number',
                    }}
                    disabled={!project.marked || project.fixed}
                    onChange={(event) => pointsBoxOnChange(project, event.target.value)}
                    onBlur={() => pointsBoxOnBlur(project)}
                  />
                </Grid>
              </Grid>
            </div>
            <div>
              <Accordion>
                <AccordionSummary expandIcon={<ExpandMoreIcon />}>תאור</AccordionSummary>
                <AccordionDetails>{project.description_1}</AccordionDetails>
              </Accordion>
              <Accordion>
                <AccordionSummary expandIcon={<ExpandMoreIcon />}>
                  שיפור לפי התקציב
                </AccordionSummary>
                <AccordionDetails>{project.description_2}</AccordionDetails>
              </Accordion>
            </div>
          </Grid>
        </Grid>
      </CardContent>
    </Card>
  );
}
