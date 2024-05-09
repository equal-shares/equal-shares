import { Helmet } from 'react-helmet-async';
import DashForm from '../sections/dashboard.js/DashForm';

export default function DashboardPage() {
  return (
    <>
      <Helmet>
        <title> Dashboard </title>
      </Helmet>
      <DashForm/>
    </>
  );
}
