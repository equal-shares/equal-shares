// The API schemas

export type Project = {
  id: number;
  name: string;
  description_1: string;
  description_2: string;
  fixed: boolean;
  min_points: number;
  max_points: number;
  rank: number;
  points: number;
  points_text: string;
  marked: boolean;
};

export type VotedProject = {
  id: number;
  rank: number;
  points: number;
  marked: boolean;
};

export type DataResponse = {
  voted: boolean;
  max_total_points: number;
  points_step: number;
  projects: Project[];
};

export type VoteRequestBody = {
  projects: VotedProject[];
};
