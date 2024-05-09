import * as React from 'react';
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

export default function AlgoChild(props) {
  const [tableChilds] = useState(props.childrens);
  const [tableChildsAlgo] = useState(props.childrensAlgo);

  return (
    <Stack sx={{ display: 'flex', justifyItems: 'center', alignItems: 'center' }}>
      <TableContainer sx={{ maxHeight: '400px', maxWidth: '1000px' }} component={Paper}>
        <Table stickyHeader aria-label="collapsible table">
          <TableHead>
            <TableRow>
              <TableCell align="center" sx={{ backgroundColor: 'rgb(33, 150, 243,0.7)' }} />
              <TableCell align="center" sx={{ color: 'white', backgroundColor: 'rgb(33, 150, 243,0.7)' }}>
                Subject
              </TableCell>
              <TableCell align="center" sx={{ color: 'white', backgroundColor: 'rgb(33, 150, 243,0.7)' }}>
                Old Budget
              </TableCell>
              <TableCell align="center" sx={{ color: 'white', backgroundColor: 'rgb(33, 150, 243,0.7)' }}>
                New Budget
              </TableCell>
              <TableCell align="center" sx={{ color: 'white', backgroundColor: 'rgb(33, 150, 243,0.7)' }}>
                Difference
              </TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {Object.keys(tableChilds).map((key, index) =>
              key !== 'total' ? (
                <AlgoRow key={index} name={key} row={tableChilds[key]} rowAlgo={tableChildsAlgo[key]} />
              ) : null
            )}
          </TableBody>
        </Table>
      </TableContainer>
    </Stack>
  );
}

AlgoChild.propTypes = {
  // childrens: PropTypes.objectOf(PropTypes.object).isRequired,
  childrensAlgo: PropTypes.objectOf(PropTypes.any).isRequired,
};
