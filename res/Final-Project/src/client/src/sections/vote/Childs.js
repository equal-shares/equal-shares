import * as React from 'react';
import { useState, useEffect } from 'react';
import PropTypes from 'prop-types';
import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableCell from '@mui/material/TableCell';
import TableContainer from '@mui/material/TableContainer';
import TableHead from '@mui/material/TableHead';
import TableRow from '@mui/material/TableRow';
import Paper from '@mui/material/Paper';
import Stack from '@mui/material/Stack';
import Row from './Row';

export default function Childs(props) {
  const [tableChilds, setTableChilds] = useState(props.childrens);
  // Calculate the sum of the budget of the children
  const totalChildBudget = tableChilds.reduce((total, item) => total + Number(item.allocated_budget_amount), 0);

  // Updates the children's table every time there is a change
  useEffect(() => {
    setTableChilds(props.childrens);
  }, [props.childrens]);

  return (
    <Stack sx={{ display: 'flex', justifyItems: 'center', alignItems: 'center' }}>
      <TableContainer sx={{ maxHeight: '400px', maxWidth: '1000px' }} component={Paper}>
        <Table stickyHeader aria-label="collapsible table">
          <TableHead>
            <TableRow sx={{ color: 'white' }}>
              <TableCell align="center" sx={{ backgroundColor: 'rgb(33, 150, 243,0.7)' }} />
              <TableCell align="center" sx={{ color: 'white', backgroundColor: 'rgb(33, 150, 243,0.7)' }}>
                Done
              </TableCell>
              <TableCell align="center" sx={{ color: 'white', backgroundColor: 'rgb(33, 150, 243,0.7)' }}>
                Subject
              </TableCell>
              <TableCell align="center" sx={{ color: 'white', backgroundColor: 'rgb(33, 150, 243,0.7)' }}>
                Budget
              </TableCell>
              <TableCell align="center" sx={{ color: 'white', backgroundColor: 'rgb(33, 150, 243,0.7)' }}>
                Vote
              </TableCell>
              <TableCell align="center" sx={{ color: 'white', backgroundColor: 'rgb(33, 150, 243,0.7)' }}>
                Precent
              </TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {tableChilds.map((childs) => (
              <Row
                key={childs.id}
                row={childs}
                parent={tableChilds}
                handleVote={props.handleVote}
                updateBudget={props.updateBudget}
                totalBudget={totalChildBudget}
                maxBudget={props.maxBudget}
                handleCheckBox={props.handleCheckBox}
              />
            ))}
          </TableBody>
        </Table>
      </TableContainer>
    </Stack>
  );
}

Childs.propTypes = {
  childrens: PropTypes.arrayOf(
    PropTypes.shape({
      id: PropTypes.number.isRequired,
      name: PropTypes.string.isRequired,
      children: PropTypes.arrayOf(
        PropTypes.shape({
          id: PropTypes.number.isRequired,
          name: PropTypes.string.isRequired,
        })
      ),
    })
  ).isRequired,
  handleVote: PropTypes.func.isRequired,
  handleCheckBox: PropTypes.func.isRequired,
  updateBudget: PropTypes.func.isRequired,
  maxBudget: PropTypes.number.isRequired,
};
