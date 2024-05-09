import * as React from 'react';
import { useState, useEffect } from 'react';
import PropTypes from 'prop-types';
import Box from '@mui/material/Box';
import Collapse from '@mui/material/Collapse';
import IconButton from '@mui/material/IconButton';
import TableCell from '@mui/material/TableCell';
import TableRow from '@mui/material/TableRow';
import Slider from '@mui/material/Slider';
import KeyboardArrowDownIcon from '@mui/icons-material/KeyboardArrowDown';
import KeyboardArrowUpIcon from '@mui/icons-material/KeyboardArrowUp';
import TextField from '@mui/material/TextField';
import Checkbox from '@mui/material/Checkbox';
import InputAdornment from '@mui/material/InputAdornment';
import { debounce } from 'lodash';
import Childs from './Childs';

export default function Row(props) {
  const [row, setRow] = useState(props.row);
  const [open, setOpen] = useState(false);
  const [budget, setBudget] = useState(Number(row.allocated_budget_amount));
  const [childs, setChilds] = useState(row.children);
  const [checkBox, setCheckBox] = useState(row.checked);

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
    return num.toString();
  }

  useEffect(() => {
    setRow(props.row);
    setChilds(props.row.children);
  }, [props.row]);

  useEffect(() => {
    setCheckBox(row.checked);
  }, [row.checked]);

  // Updates the slider when there is a change in the budget
  const handleChangeSlider = debounce((event) => {
    const { value } = event.target;
    if (value > props.maxBudget) {
      event.target.value = props.maxBudget;
    } else if (value < 0) {
      event.target.value = 0;
    }
    if (!checkBox) {
      event.target.value = parseInt(event.target.value, 10);
      const diff = row.allocated_budget_amount - event.target.value;
      props.handleVote(props.parent, row.id, event.target.value, diff);
      setBudget(event.target.value);
    }
  }, 200);

  // Updates the voting text field when there is a change in the budget
  const handleChangeText = (event) => {
    const { value } = event.target * 1000000;
    if (value > props.maxBudget) {
      event.target.value = props.maxBudget;
    } else if (value < 0 || Number.isNaN(value)) {
      event.target.value = 0;
    }

    event.target.value = parseInt(event.target.value * 1000000, 10);
    // If delete the value without setting a new one
    if (!event.target.value) {
      event.target.value = 0;
    }
    if (!checkBox) {
      const diff = row.allocated_budget_amount - event.target.value;
      props.handleVote(props.parent, row.id, event.target.value, diff);
      setBudget(event.target.value);
    }
  };

  return (
    <>
      <TableRow key={row.id} sx={{ backgroundColor: row.checked ? '#F4F6F8' : 'white' }}>
        <TableCell align="center" >
          <IconButton
            id={`iconTree${row.id}`}
            aria-label="expand row"
            size="small"
            onClick={() => {
              setOpen(childs && childs.length > 0 ? !open : false);
            }}
          >
            {open ? <KeyboardArrowUpIcon /> : <KeyboardArrowDownIcon />}
          </IconButton>
        </TableCell>
        <TableCell align="center" component="th" scope="row" sx={{ width: '161px' }}>
          <Checkbox
            id={`checkbox${row.id}`}
            size="small"
            checked={row.checked}
            onClick={() => props.handleCheckBox(props.parent, row.id, !checkBox)}
          />
        </TableCell>
        <TableCell align="center" component="th" scope="row" >
          {row.name}
        </TableCell>
        <TableCell align="center" >
          <TextField
            id={`budgetText${row.id}`}
            type="number"
            variant="outlined"
            value={Number((Number(row.allocated_budget_amount) / 1000000).toFixed(1))}
            // defaultValue={Number(budget)}
            InputProps={{
              inputProps: { min: 0, max: 6000000 },
              endAdornment: <InputAdornment position="end">M</InputAdornment>,
            }}
            onChange={handleChangeText}
          />
        </TableCell>
        <TableCell align="center" sx={{ width: '180px' }}>
          <Slider
            id={`slider${row.id}`}
            value={Math.round(Number(row.allocated_budget_amount) * 10) / 10}
            onChange={handleChangeSlider}
            valueLabelDisplay="auto"
            aria-label="Default"
            max={props.maxBudget}
            valueLabelFormat={(value) => formatNumber(value)}
            sx={{ mt: 1.2 }}
          />
        </TableCell>
        <TableCell align="center" >
          {props.totalBudget === 0
            ? 0
            : Math.max(Math.min(((row.allocated_budget_amount / 596770415000) * 100).toFixed(1), 100), 0)}
          %
        </TableCell>
      </TableRow>
      <TableRow>
        <TableCell style={{ paddingBottom: 0, paddingTop: 0 }} colSpan={6}>
          <Collapse in={open} timeout="auto" unmountOnExit>
            <Box sx={{ margin: 1 }}>
              {childs.length > 0 && (
                <Childs
                  childrens={childs}
                  parent={row.children}
                  maxBudget={Number(row.allocated_budget_amount)}
                  updateBudget={props.updateBudget}
                  handleCheckBox={props.handleCheckBox}
                  handleVote={props.handleVote}
                />
              )}
            </Box>
          </Collapse>
        </TableCell>
      </TableRow>
    </>
  );
}

Row.propTypes = {
  row: PropTypes.shape({
    id: PropTypes.number.isRequired,
    name: PropTypes.string.isRequired,
    children: PropTypes.arrayOf(
      PropTypes.shape({
        id: PropTypes.number.isRequired,
        name: PropTypes.string.isRequired,
      })
    ),
  }).isRequired,
  // key: PropTypes.number.isRequired,
  handleVote: PropTypes.func.isRequired,
  handleCheckBox: PropTypes.func.isRequired,
  updateBudget: PropTypes.func.isRequired,
  maxBudget: PropTypes.number.isRequired,
  totalBudget: PropTypes.number.isRequired,
  parent: PropTypes.arrayOf(
    PropTypes.shape({
      id: PropTypes.number.isRequired,
      name: PropTypes.string.isRequired,
    })
  ).isRequired,
};
