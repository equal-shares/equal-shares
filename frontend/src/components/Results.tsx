import { Project } from '../schemas';
import { BarChart } from '@mui/x-charts/BarChart';

export type ResultsProps = {
  data: { [key: number]: number };
  projects: Project[];
};

export default function Results({ data, projects }: ResultsProps) {
  const withUser = projects.filter((project) => project.points > 0).length > 0;

  const charts = projects.map((project) => ({
    id: project.id,
    name: project.name,
    minPoints: project.min_points,
    maxPoints: project.max_points,
    userPoints: project.points,
    resultPoints: data[project.id],
  }));

  return (
    <>
      {charts.map((chart) => (
        <div key={chart.id} className="w-[800px] mt-[30px] flex justify-center flex-col">
          <div className="mx-auto">{chart.name}</div>
          <BarChart
            dataset={[
              withUser
                ? {
                    name: chart.name,
                    minPoints: chart.minPoints,
                    userPoints: chart.userPoints,
                    resultPoints: chart.resultPoints,
                    maxPoints: chart.maxPoints,
                  }
                : {
                    name: chart.name,
                    minPoints: chart.minPoints,
                    resultPoints: chart.resultPoints,
                    maxPoints: chart.maxPoints,
                  },
            ]}
            series={
              withUser
                ? [
                    { dataKey: 'minPoints', label: 'מינימלי' },
                    { dataKey: 'userPoints', label: 'הצעה שלך' },
                    { dataKey: 'resultPoints', label: 'הוחלט' },
                    { dataKey: 'maxPoints', label: 'מקסימלי' },
                  ]
                : [
                    { dataKey: 'minPoints', label: 'מינימלי' },
                    { dataKey: 'resultPoints', label: 'הוחלט' },
                    { dataKey: 'maxPoints', label: 'מקסימלי' },
                  ]
            }
            xAxis={[{ scaleType: 'band', dataKey: 'name' }]}
            height={500}
          />
        </div>
      ))}
    </>
  );
}
