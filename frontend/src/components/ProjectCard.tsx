import {
  Typography,
  Card,
  CardContent,
  Grid,
  Slider,
  Input,
  Checkbox,
  FormControlLabel
} from '@mui/material';
import { Menu as MenuIcon } from '@mui/icons-material';

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
  setDragDisabled
}: ProjectCardProps) {
  return (
    <Card className="my-[4px]" sx={{ boxShadow: 3 }}>
      <CardContent>
        <Grid container spacing={2}>
          <Grid item xs={1}>
            <div className="h-full flex justify-content">
              <div className="h-fit my-auto">
                <MenuIcon />
              </div>
            </div>
          </Grid>
          <Grid item xs={6}>
            <div>
              <Typography variant="h6" component="p">
                {project.rank}. {project.name}
              </Typography>
              <Typography variant="body1" component="p">
                {project.description}
              </Typography>
            </div>
          </Grid>
          <Grid item xs={5}>
            <div>
              <Grid container spacing={4} alignItems="center">
                <Grid item xs={8}>
                  <div
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
                          label: project.min_points.toString()
                        },
                        {
                          value: project.max_points,
                          label: project.max_points.toString()
                        }
                      ]}
                      disabled={!project.marked}
                      onChange={(_, value) => pointsSliderOnChange(project, value)}
                    />
                  </div>
                </Grid>
                <Grid item xs={4}>
                  <Input
                    value={project.points_text}
                    size="small"
                    sx={{ input: { textAlign: 'center' } }}
                    inputProps={{
                      step: pointsStep,
                      min: project.min_points,
                      max: project.max_points,
                      type: 'number'
                    }}
                    disabled={!project.marked}
                    onChange={(event) => pointsBoxOnChange(project, event.target.value)}
                    onBlur={() => pointsBoxOnBlur(project)}
                  />
                </Grid>
              </Grid>
            </div>
            <div className="w-fit mr-auto ml-[40px]">
              <FormControlLabel
                control={
                  <Checkbox checked={project.marked} onChange={() => markedOnChange(project)} />
                }
                label="בחר"
              />
            </div>
          </Grid>
        </Grid>
      </CardContent>
    </Card>
  );
}
