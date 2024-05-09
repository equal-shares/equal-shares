import { Helmet } from 'react-helmet-async';
import VotingForm from '../sections/vote/VotingForm';

export default function VotingPage() {
  return (
    <>
      <Helmet>
        <title> Voting </title>
      </Helmet>
      <VotingForm />
    </>
  );
}

