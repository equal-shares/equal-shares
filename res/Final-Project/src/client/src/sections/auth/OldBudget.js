import PropTypes from 'prop-types';
import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableCell from '@mui/material/TableCell';
import TableContainer from '@mui/material/TableContainer';
import TableHead from '@mui/material/TableHead';
import TableRow from '@mui/material/TableRow';
import Paper from '@mui/material/Paper';
import Stack from '@mui/material/Stack';
import OldBudgetRow from './OldBudgetRow';
import LoadingTable from './LoadingTable';

export default function OldBudget(props) {
  const totalBudget = 596770415000;
  return (
    <Stack sx={{ justifyItems: 'end', display: 'inline-block', alignItems: 'center' }}>
      {props.tableData.length === 0 ? (
        <LoadingTable />
      ) : (
        <TableContainer
          id="table"
          sx={{
            marginLeft: '-140px',
            justifyContent: 'center',
            alignItems: 'center',
            maxHeight: 'auto',
            width: '700px',
          }}
          component={Paper}
        >
          <Table stickyHeader aria-label="collapsible table">
            <TableHead>
              <TableRow sx={{ fontWeight: 'bold' }}>
                <TableCell align="center" sx={{ backgroundColor: 'rgb(33, 150, 243,0.8)' }} />
                <TableCell
                  sx={{
                    color: 'white',
                    backgroundColor: 'rgb(33, 150, 243,0.8)',
                    fontWeight: 'bold',
                    fontSize: '18px',
                  }}
                  align="center"
                >
                  Subject
                </TableCell>
                <TableCell
                  sx={{
                    color: 'white',
                    backgroundColor: 'rgb(33, 150, 243,0.8)',
                    fontWeight: 'bold',
                    fontSize: '18px',
                  }}
                  align="center"
                >
                  Old Budget
                </TableCell>
                <TableCell
                  sx={{
                    color: 'white',
                    backgroundColor: 'rgb(33, 150, 243,0.8)',
                    fontWeight: 'bold',
                    fontSize: '18px',
                  }}
                  align="center"
                >
                  Precent
                </TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {props.tableData.map((row) => (
                <OldBudgetRow key={row.id} row={row} totalBudget={totalBudget} />
              ))}
            </TableBody>
          </Table>
        </TableContainer>
      )}
    </Stack>
  );
}

OldBudget.propTypes = {
  tableData: PropTypes.arrayOf(
    PropTypes.shape({
      id: PropTypes.number.isRequired,
      name: PropTypes.string.isRequired,
      allocated_budget_amount: PropTypes.number.isRequired,
      children: PropTypes.arrayOf(
        PropTypes.shape({
          id: PropTypes.number.isRequired,
          name: PropTypes.string.isRequired,
          allocated_budget_amount: PropTypes.number.isRequired,
        })
      ),
    })
  ).isRequired,
};
