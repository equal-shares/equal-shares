import { Helmet } from 'react-helmet-async';
import ResultsForm from '../sections/results/ResultsForm';

export default function ResultsPage() {
  return (
    <>
      <Helmet>
        <title> Results </title>
      </Helmet>
      <ResultsForm />
    </>
  );
}
