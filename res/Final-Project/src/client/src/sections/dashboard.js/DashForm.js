import React, { useState, useEffect, useContext } from 'react';
import { Stack, Typography, Box } from '@mui/material';
import Ages from './Ages';
import Gender from './Gender';
import PreviousBudget from './PreviousBudget';
import Cards from './Cards';
import AddressContext from '../../contexts/AddressContext';

export default function DashForm() {
  const [data, setData] = useState({});
  const [voters, setVoters] = useState('0');
  const address = useContext(AddressContext);
  const url = `${address}dashboard`;

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await fetch(url, {
          method: 'GET',
          headers: { 'Content-Type': 'application/json' },
        });
        const information = await response.json();
        setData(information);
        setVoters(information.voter_count);
      } catch (error) {
        console.error(error);
      }
    };

    fetchData();
  }, []);

  useEffect(() => {
    setData(data);
  }, [data]);

  return (
    <>
      <Cards voters={voters.toString()} />
      <Box
        display="flex"
        flexDirection={{ xs: 'column', md: 'row' }}
        alignItems="center"
        justifyContent="center"
        marginTop={8}
      >
        <Stack flex="1">
          <Typography variant="h6" style={{ marginLeft: '340px' }}>
            Ages{' '}
          </Typography>
          <Ages width={400} ages={data.ages} />
        </Stack>

        <Stack>
          <Typography variant="h6" style={{ marginLeft: 'auto', marginRight: '20px' }}>
            Gender{' '}
          </Typography>
          <Gender width={400} gender={data.genders} />
        </Stack>
      </Box>

      <Stack marginTop={8}>
        <Typography variant="h6" style={{ marginLeft: 'auto' }}>
          Previous budget{' '}
        </Typography>
        <PreviousBudget />
      </Stack>
    </>
  );
}
