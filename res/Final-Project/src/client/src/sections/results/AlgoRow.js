import * as React from 'react';
import { useState } from 'react';
import PropTypes from 'prop-types';
import Box from '@mui/material/Box';
import Collapse from '@mui/material/Collapse';
import IconButton from '@mui/material/IconButton';
import TableCell from '@mui/material/TableCell';
import TableRow from '@mui/material/TableRow';
import KeyboardArrowDownIcon from '@mui/icons-material/KeyboardArrowDown';
import KeyboardArrowUpIcon from '@mui/icons-material/KeyboardArrowUp';
import Tooltip, { tooltipClasses } from '@mui/material/Tooltip';
import { styled } from '@mui/material/styles';
import AlgoChild from './AlgoChild';

const LightTooltip = styled(({ className, ...props }) => <Tooltip {...props} classes={{ popper: className }} />)(
  ({ theme }) => ({
    [`& .${tooltipClasses.tooltip}`]: {
      backgroundColor: theme.palette.common.white,
      color: 'rgba(0, 0, 0, 0.87)',
      boxShadow: theme.shadows[1],
      fontSize: 11,
    },
  })
);

export default function AlgoRow(props) {
  const [row] = useState(props.row);
  const [open, setOpen] = useState(false);
  const [childs] = useState(typeof row === 'number' ? null : row);
  const [budget] = useState(typeof row === 'number' ? row : row.total);

  const [rowAlgo] = useState(props.rowAlgo);
  const [childsAlgo] = useState(typeof rowAlgo === 'number' ? null : rowAlgo);
  const [newBudget] = useState(typeof rowAlgo === 'number' ? rowAlgo : rowAlgo.total);
  const diff = budget - newBudget;

  function percent(num) {
    return Math.max(Math.min(((num / 596770415000) * 100).toFixed(1), 100), 0);
  }

  function formatNumber(num) {
    if (num >= 1000000000) {
      return `${(num / 1000000000).toFixed(1)} B`;
    }
    if (num >= 1000000) {
      return `${(num / 1000000).toFixed(1)} M`;
    }
    if (num >= 1000) {
      return `${(num / 1000).toFixed(1)} K`;
    }
    if (num < 1000) {
      return `${num.toFixed(1)}`;
    }
    return num.toString();
  }
  return (
    <React.Fragment>
      <TableRow key={props.name}>
        <TableCell align="center">
          <IconButton
            id={props.name}
            aria-label="expand row"
            size="small"
            onClick={() => {
              setOpen(childs ? !open : false);
            }}
          >
            {open ? <KeyboardArrowUpIcon /> : <KeyboardArrowDownIcon />}
          </IconButton>
        </TableCell>
        <TableCell align="center" component="th" scope="row">
          {props.name}
        </TableCell>
        <LightTooltip title={`${percent(budget)} %`} followCursor>
          <TableCell align="center">{formatNumber(budget)}</TableCell>
        </LightTooltip>
        <LightTooltip title={`${percent(newBudget)} %`} placement="left" followCursor>
          <TableCell align="center">{formatNumber(newBudget)}</TableCell>
        </LightTooltip>
        <LightTooltip title={`${percent(Math.abs(diff))} %`} placement="left" followCursor>
          <TableCell align="center" sx={{ color: diff > 0 ? 'red' : 'green' }}>
            {`${diff > 0 ? '-' : '+'}${formatNumber(Math.abs(diff))}`}
          </TableCell>
        </LightTooltip>
      </TableRow>
      <TableRow>
        <TableCell style={{ paddingBottom: 0, paddingTop: 0 }} colSpan={6}>
          <Collapse in={open} timeout="auto" unmountOnExit>
            <Box sx={{ margin: 1 }}>{childs && <AlgoChild childrens={childs} childrensAlgo={childsAlgo} />}</Box>
          </Collapse>
        </TableCell>
      </TableRow>
    </React.Fragment>
  );
}

AlgoRow.propTypes = {
  row: PropTypes.oneOfType([PropTypes.number, PropTypes.object]).isRequired,
  rowAlgo: PropTypes.oneOfType([PropTypes.number, PropTypes.object]).isRequired,
  name: PropTypes.string.isRequired,
  // keys: PropTypes.string.isRequired,
};
