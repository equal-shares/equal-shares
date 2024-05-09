import { useState } from 'react';
import PropTypes from 'prop-types';
import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableCell from '@mui/material/TableCell';
import TableContainer from '@mui/material/TableContainer';
import TableHead from '@mui/material/TableHead';
import TableRow from '@mui/material/TableRow';
import Paper from '@mui/material/Paper';
import Stack from '@mui/material/Stack';
import AlgoRow from './AlgoRow';

export default function Algo(props) {
  const [tableOldBudget] = useState(props.oldBudget);
  const [tableAlgo] = useState(Object.keys(props.algo).length === 0 ? props.oldBudget : props.algo);

  return (
    <Stack sx={{ display: 'flex', justifyItems: 'center', alignItems: 'center', marginRight: 2 }}>
      <TableContainer sx={{ maxHeight: '1000px', maxWidth: '1000px' }} component={Paper}>
        <Table stickyHeader aria-label="collapsible table">
          <TableHead>
            <TableRow sx={{ fontWeight: 'bold' }}>
              <TableCell align="center" sx={{ backgroundColor: 'rgb(33, 150, 243,0.8)' }} />
              <TableCell
                sx={{ backgroundColor: 'rgb(33, 150, 243,0.8)', color: 'white', fontWeight: 'bold', fontSize: '18px' }}
                align="center"
              >
                Subject
              </TableCell>
              <TableCell
                sx={{ backgroundColor: 'rgb(33, 150, 243,0.8)', color: 'white', fontWeight: 'bold', fontSize: '18px' }}
                align="center"
              >
                Old Budget
              </TableCell>
              <TableCell
                sx={{ backgroundColor: 'rgb(33, 150, 243,0.8)', color: 'white', fontWeight: 'bold', fontSize: '18px' }}
                align="center"
              >
                New Budget
              </TableCell>
              <TableCell
                sx={{ backgroundColor: 'rgb(33, 150, 243,0.8)', color: 'white', fontWeight: 'bold', fontSize: '18px' }}
                align="center"
              >
                Difference
              </TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {Object.keys(tableOldBudget).map((key, index) =>
              key !== 'total' ? (
                <AlgoRow key={index} name={key} row={tableOldBudget[key]} rowAlgo={tableAlgo[key]} />
              ) : null
            )}
          </TableBody>
        </Table>
      </TableContainer>
    </Stack>
  );
}

Algo.propTypes = {
  oldBudget: PropTypes.object.isRequired,
  algo: PropTypes.object.isRequired,
};
