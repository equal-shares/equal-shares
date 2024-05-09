import { useState } from 'react';
import Identification from './Identification';
import ForgetPass from './ForgetPass';

export default function ForgetPassForm() {
  const [isShowed, setIsShowed] = useState(true);
  const [id, setId] = useState('');


  return (
    <>
      {isShowed && <Identification setIsShowed={setIsShowed} setId={setId}/>}
      {!isShowed && <ForgetPass setIsShowed={setIsShowed} id={id} />}
    </>
  );
}
