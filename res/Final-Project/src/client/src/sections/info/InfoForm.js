import React, { useState, useEffect, useContext } from 'react';
import { Grid } from '@mui/material';
import InfoCards from './InfoCards';
import AddressContext from '../../contexts/AddressContext';

// The design of the information cards
const styleCards = {
  boxShadow: 20,
  textAlign: 'center',
  marginLeft: 14,
  marginRight: 4,
  marginTop: 14,
  fontSize: '15px',
  borderRadius: '50%',
  backgroundColor: '#007bff',
  color: 'black',
  minWidth: '120px',
  width: '120px',
  height: '120px',
  fontFamily: ' system-ui',
};

export default function InfoForm() {
  const [table, setTable] = useState({});
  const address = useContext(AddressContext);

  const url = `${address}information`;
  // const url = 'https://peoples-budget.onrender.com/peoples_budget/information';

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await fetch(url, {
          method: 'GET',
          headers: { 'Content-Type': 'application/json' },
        });
        const information = JSON.parse(await response.json());
        setTable(information);
      } catch (error) {
        console.error(error);
      }
    };

    fetchData();
  }, []);

  return (
    <Grid container spacing={3}>
      {Object.keys(table).map((key, index) => (
        <Grid item xs={6} sm={6} md={3} key={index}>
          <InfoCards keys={key} value={table[key]} index={index} styleCards={styleCards} scrollTargetId="myScrollTarget" />
        </Grid>
      ))}
    </Grid>
  );
}
