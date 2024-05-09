import React, { useState, useEffect, useContext } from 'react';
import { Typography, Box, Button } from '@mui/material';
import Loading from './Loading';
import Algo from './Algo';
import LoadingVote from './LoadingVote';
import AddressContext from '../../contexts/AddressContext';

export default function ResultsForm() {
  const [loading, setLoading] = useState(false);
  const [loadingPage, setLoadingPage] = useState(true);
  const [displayGraph1, setDisplayGraph1] = useState(false);
  const [displayGraph2, setDisplayGraph2] = useState(false);
  const [clicked1, setClicked1] = useState(false);
  const [clicked2, setClicked2] = useState(false);

  const [oldBudget, setOldBudget] = useState({});
  const [algo1, setAlgo1] = useState({});
  const [algo2, setAlgo2] = useState({});
  const [lastTime, setLastTime] = useState('');
  const address = useContext(AddressContext);

  const url = `${address}results`;

  const fetchData = async () => {
    try {
      const response = await fetch(url, {
        method: 'GET',
        headers: { 'Content-Type': 'application/json' },
      });
      const information = await response.json();
      setOldBudget(JSON.parse(information.current_budget));
      setAlgo1(JSON.parse(information.median_algorithm));
      setAlgo2(JSON.parse(information.generalized_median_algorithm));
      setLastTime(information.time.replace('GMT', ''));
    } catch (error) {
      console.error(error);
      alert('No results have been received. \nCheck later for updates.');
    }
  };

  useEffect(() => {
    fetchData();
  }, []);

  // Loading the page for 4 seconds
  useEffect(() => {
    const timer = setTimeout(() => {
      setLoadingPage(false);
    }, 4300);

    return () => {
      clearTimeout(timer);
    };
  }, []);

  // Ensures that only one table is displayed at a time
  const handleButtonClick = (number) => {
    if (!loading) {
      setDisplayGraph1(false);
      setDisplayGraph2(false);
      setLoading(true);
      setTimeout(() => {
        setLoading(false);
        setDisplayGraph1(number === 0);
        setDisplayGraph2(number === 1);
      }, 3000);
      setClicked1(number === 0);
      setClicked2(number === 1);
    }
  };

  return loadingPage ? (
    <LoadingVote />
  ) : (
    <div>
      <Typography
        align="center"
        style={{
          textAlign: 'center',
          fontFamily: 'Ubuntu',
          fontWeight: 'bold',
          fontSize: '35px',
          marginTop: '-35px',
          marginBottom: '20px',
          color: 'rgba(0, 0, 75, 0.95)',
        }}
      >
        Select an option:
      </Typography>

      <Box marginBottom={1} marginTop={7} gap={12} align="center">
        <div
          style={{
            display: 'flex',
            justifyContent: 'center',
          }}
        >
          <Button
            id="algo1"
            sx={{
              minWidth: '180px',
              width: '180px',
              height: '80px',
              fontSize: '17px',
              fontFamily: 'Ubuntu',
            }}
            variant={clicked1 ? 'contained' : 'outlined'}
            onClick={() => handleButtonClick(0)}
          >
            Median <br />
            Algorithm
          </Button>
          <img
            src={`${process.env.PUBLIC_URL}/img_bg/results.png`}
            alt="Logo"
            style={{ marginLeft: '40px', marginTop: '-95px', width: '300px' }}
          />
          <Button
            id="algo2"
            sx={{
              minWidth: '180px',
              width: '180px',
              height: '80px',
              fontSize: '17px',
              color: clicked2 ? 'primary' : 'default',
              fontFamily: 'Ubuntu',
            }}
            variant={clicked2 ? 'contained' : 'outlined'}
            onClick={() => handleButtonClick(1)}
          >
            generalized median algorithm
          </Button>
        </div>
      </Box>
      {(displayGraph1 || displayGraph2) && (
        <Typography variant="h6" align="center" marginBottom={3}>
          {lastTime}
        </Typography>
      )}
      {loading && <Loading />}
      {displayGraph1 && <Algo oldBudget={oldBudget} algo={algo1} />}
      {displayGraph2 && <Algo oldBudget={oldBudget} algo={algo2} />}
    </div>
  );
}
