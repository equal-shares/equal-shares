import { Helmet } from 'react-helmet-async';
import InfoForm from '../sections/info/InfoForm';

export default function InfoPage() {
  return (
    <>
      <Helmet>
        <title> Information </title>
      </Helmet>
      <InfoForm />
    </>
  );
}
